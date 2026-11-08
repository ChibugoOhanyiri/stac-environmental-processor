"""The recipe (M2): read the settings card, fetch Sentinel-1 pictures from Earth Engine,
put them on one exact grid, save them as GeoTIFFs and write a receipt.

Kitchen and order slip: this file is the kitchen (HOW). configs/case.json is the order slip
(WHAT: where, when, which satellite). Nothing about Lagos is written here.

Usage (from the project folder):
    .venv/bin/python src/preprocess.py --config configs/case.json --dry-run   # find only
    .venv/bin/python src/preprocess.py --config configs/case.json             # find + download
(Windows: .venv\\Scripts\\python instead of .venv/bin/python.)

Values are Sentinel-1 backscatter in dB, already calibrated and ortho-corrected by GEE
(COPERNICUS/S1_GRD). The reference uses a median; a median gives the same answer in dB or
linear units, so no unit conversion is needed for it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EmptySearchError(RuntimeError):
    """Raised when a search finds no pictures (the 'magenta May' lesson: fail loudly)."""


# ---------------------------------------------------------------------------
# PART 1 — Read the order slip
# ---------------------------------------------------------------------------
REQUIRED = {
    "case_id": str, "gee_collection": str, "area": dict, "satellite": dict,
    "dates": dict, "output": dict,
}


def load_card(path: Path) -> dict:
    """Read configs/case.json and check the important fields exist."""
    card = json.loads(Path(path).read_text(encoding="utf-8"))
    for key, kind in REQUIRED.items():
        if not isinstance(card.get(key), kind):
            raise ValueError(f"Settings card is missing '{key}' (expected {kind.__name__}).")
    for role in ("event", "reference"):
        window = card["dates"].get(role, {})
        if not (window.get("start") and window.get("end") and window["start"] < window["end"]):
            raise ValueError(f"dates.{role} needs a start before its end.")
        for key in ("start", "end"):          # catch impossible dates like 2026-06-31 before going online
            try:
                date.fromisoformat(window[key])
            except ValueError:
                raise ValueError(f"dates.{role}.{key} = '{window[key]}' is not a real calendar date (YYYY-MM-DD).") from None
    if card["output"]["pixel_size_m"] <= 0 or card["area"]["half_size_m"] <= 0:
        raise ValueError("pixel_size_m and half_size_m must be positive.")
    return card


# ---------------------------------------------------------------------------
# PART 2 — Work out the exact pixel grid (pure maths; no internet needed)
# ---------------------------------------------------------------------------
def snap_grid(centre_e: float, centre_n: float, half_size_m: float, pixel_m: float) -> dict:
    """Make a square grid around a centre point, with corners on whole pixels.

    Like ruling a sheet of graph paper so every square starts on a 10 m mark. Two pictures
    saved on the same grid line up pixel for pixel."""
    x0 = math.floor((centre_e - half_size_m) / pixel_m) * pixel_m   # west edge
    y0 = math.ceil((centre_n + half_size_m) / pixel_m) * pixel_m    # north edge
    size = int(round(2 * half_size_m / pixel_m))
    return {"x0": x0, "y0": y0, "width": size, "height": size, "pixel_m": pixel_m}


def lonlat_to_crs(lon: float, lat: float, crs: str) -> tuple[float, float]:
    """Convert a longitude/latitude to the map grid's metres (e.g. UTM 31N)."""
    from rasterio.warp import transform
    xs, ys = transform("EPSG:4326", crs, [lon], [lat])
    return xs[0], ys[0]


# ---------------------------------------------------------------------------
# PART 3 — Connect to Earth Engine and find the pictures
# ---------------------------------------------------------------------------
def gee_project() -> str:
    """Read the Cloud project ID from the environment or the git-ignored .env file."""
    if os.environ.get("GEE_PROJECT"):
        return os.environ["GEE_PROJECT"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("GEE_PROJECT="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("No GEE_PROJECT found. Copy .env.example to .env and fill it in.")


def find_images(ee, card: dict, region, window: dict):
    """Search the catalogue for pictures that match the order slip. Stop if none.
    A date window may name its own platform_number (e.g. a twin satellite for a dry-season reference);
    otherwise the card's satellite is used. Mixing twins is decision S12: use only in designs where the
    difference cancels (compare flood day and a control against the same twin reference)."""
    sat = card["satellite"]
    found = (ee.ImageCollection(card["gee_collection"])
             .filterBounds(region)
             .filterDate(window["start"], window["end"])
             .filter(ee.Filter.eq("platform_number", window.get("platform_number", sat["platform_number"])))
             .filter(ee.Filter.eq("instrumentMode", sat["instrument_mode"]))
             .filter(ee.Filter.eq("orbitProperties_pass", sat["orbit_pass"]))
             .filter(ee.Filter.eq("relativeOrbitNumber_start", sat["relative_orbit"])))
    for band in sat["bands"]:
        found = found.filter(ee.Filter.listContains("transmitterReceiverPolarisation", band))
    ids = found.aggregate_array("system:index").getInfo()
    if not ids:
        raise EmptySearchError(
            f"No pictures found for '{window.get('label', window)}' "
            f"({window['start']} to {window['end']}), satellite {window.get('platform_number', sat['platform_number'])}, "
            f"lane {sat['relative_orbit']} {sat['orbit_pass']}. Check the dates and satellite on the card.")
    return found, ids


# ---------------------------------------------------------------------------
# PART 4 — Fetch the pixels on our exact grid and save a GeoTIFF
# ---------------------------------------------------------------------------
def build_expression(image, bands: list[str], nodata: float):
    """The exact recipe sent to Earth Engine: keep our bands, use decimals, unseen pixels -> nodata.
    Built in ONE place so the receipt's recipe card is always the recipe that actually ran."""
    return image.select(bands).toFloat().unmask(nodata)


def process_graph(expression) -> dict:
    """Earth Engine's own step-by-step recipe card (its 'process graph') for an expression.
    It lists the collection, filters, combine step and band choices, not the pixels."""
    return json.loads(expression.serialize())


def fetch_pixels(ee, expression, bands: list[str], grid: dict, crs: str):
    """Ask Earth Engine for exactly our grid, using the recipe from build_expression."""
    import numpy as np
    request = {
        "expression": expression,
        "fileFormat": "NUMPY_NDARRAY",
        "grid": {
            "dimensions": {"width": grid["width"], "height": grid["height"]},
            "affineTransform": {"scaleX": grid["pixel_m"], "shearX": 0, "translateX": grid["x0"],
                                "shearY": 0, "scaleY": -grid["pixel_m"], "translateY": grid["y0"]},
            "crsCode": crs,
        },
    }
    table = ee.data.computePixels(request)            # one field per band
    return np.stack([table[b].astype("float32") for b in bands])


def save_geotiff(path: Path, data, names: list[str], grid: dict, crs: str, nodata: float) -> None:
    import rasterio
    from rasterio.transform import from_origin
    path.parent.mkdir(parents=True, exist_ok=True)
    profile = {"driver": "GTiff", "dtype": "float32", "count": data.shape[0],
               "width": grid["width"], "height": grid["height"], "crs": crs,
               "transform": from_origin(grid["x0"], grid["y0"], grid["pixel_m"], grid["pixel_m"]),
               "nodata": nodata, "compress": "deflate"}
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(data)
        for i, name in enumerate(names, start=1):
            dst.set_band_description(i, name)


def summarise(path: Path, data, nodata: float) -> dict:
    import numpy as np
    valid = data[0] != nodata
    vals = data[0][valid]
    return {"file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "valid_pixels": int(valid.sum()), "nodata_pixels": int((~valid).sum()),
            "first_band_median_db": round(float(np.median(vals)), 3) if vals.size else None}


# ---------------------------------------------------------------------------
# PART 5 — The receipt
# ---------------------------------------------------------------------------
def versions() -> dict:
    import ee
    import numpy
    import rasterio
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                capture_output=True, text=True, check=True).stdout.strip()
        # "dirty" = the code has unsaved (uncommitted) changes, so the commit above is not
        # exactly the code that ran. Commit first for a fully honest receipt.
        dirty = bool(subprocess.run(["git", "status", "--porcelain", "src", "configs"], cwd=ROOT,
                                    capture_output=True, text=True, check=True).stdout.strip())
    except (OSError, subprocess.CalledProcessError):
        commit, dirty = "unknown", None
    return {"python": platform.python_version(), "earthengine_api": ee.__version__,
            "rasterio": rasterio.__version__, "gdal": rasterio.__gdal_version__,
            "numpy": numpy.__version__, "git_commit": commit, "git_uncommitted_changes": dirty}


# ---------------------------------------------------------------------------
# PART 6 — Put it all together
# ---------------------------------------------------------------------------
def run(card_path: Path, dry_run: bool = False) -> dict:
    import ee
    card = load_card(card_path)
    out = card["output"]
    started = datetime.now(timezone.utc)
    run_id = started.strftime("%Y%m%dT%H%M%SZ") + "_" + card["case_id"]

    centre_e, centre_n = lonlat_to_crs(card["area"]["centre_lon"], card["area"]["centre_lat"], out["crs"])
    grid = snap_grid(centre_e, centre_n, card["area"]["half_size_m"], out["pixel_size_m"])
    print(f"Run {run_id}\nGrid: {grid['width']} x {grid['height']} pixels of {grid['pixel_m']} m, "
          f"top-left corner ({grid['x0']}, {grid['y0']}) in {out['crs']}")

    ee.Initialize(project=gee_project())
    proj = ee.Projection(out["crs"])
    region = ee.Geometry.Rectangle(
        [grid["x0"], grid["y0"] - grid["height"] * grid["pixel_m"],
         grid["x0"] + grid["width"] * grid["pixel_m"], grid["y0"]], proj, False)

    manifest = {"run_id": run_id, "started_utc": started.isoformat(), "dry_run": dry_run,
                "settings_card": card, "grid": {**grid, "crs": out["crs"]},
                "versions": versions(), "inputs": {}, "outputs": []}

    bands = card["satellite"]["bands"]
    for role in ("event", "reference"):
        window = card["dates"][role]
        found, ids = find_images(ee, card, region, window)
        manifest["inputs"][role] = {"window": window, "gee_image_ids": ids}
        print(f"{role}: {len(ids)} picture(s): " + ", ".join(i[17:32] for i in ids))
        if dry_run:
            continue
        # event: stitch that day's frames together; reference: middle value of all passes
        image = found.median() if window.get("combine") == "median" else found.mosaic()
        expression = build_expression(image, bands, out["nodata"])
        manifest["inputs"][role]["process_graph"] = process_graph(expression)
        data = fetch_pixels(ee, expression, bands, grid, out["crs"])
        names = [f"{b}_{role}" for b in bands]
        path = ROOT / out["folder"] / f"{card['case_id']}_{role}.tif"
        save_geotiff(path, data, names, grid, out["crs"], out["nodata"])
        info = summarise(path, data, out["nodata"])
        manifest["outputs"].append({"role": role, "bands": names, **info})
        print(f"  saved {info['file']}: {info['valid_pixels']} valid, {info['nodata_pixels']} nodata, "
              f"median {bands[0]} {info['first_band_median_db']} dB")

    # Context layers (optional): outside maps on the same grid, e.g. JRC "always water".
    # fill_masked: what a masked pixel MEANS in that product (JRC masks "never water" -> 0),
    # so it is not confused with "not observed" (our nodata).
    for layer in card.get("context", []) if not dry_run else []:
        image = ee.Image(layer["gee_image"]).select(layer["band"])
        if "fill_masked" in layer:
            image = image.unmask(layer["fill_masked"])
        expression = build_expression(image, [layer["band"]], out["nodata"])
        data = fetch_pixels(ee, expression, [layer["band"]], grid, out["crs"])
        path = ROOT / out["folder"] / f"{card['case_id']}_{layer['name']}.tif"
        save_geotiff(path, data, [layer["name"]], grid, out["crs"], out["nodata"])
        info = summarise(path, data, out["nodata"])
        info.pop("first_band_median_db")
        manifest["inputs"].setdefault("context", {})[layer["name"]] = {
            **layer, "process_graph": process_graph(expression)}
        manifest["outputs"].append({"role": f"context:{layer['name']}", "bands": [layer["name"]], **info})
        print(f"  saved {info['file']} (context layer {layer['name']})")

    manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
    receipt = ROOT / out["folder"] / f"run-manifest_{run_id}.json"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Receipt: {receipt.relative_to(ROOT)}")
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Fetch and align Sentinel-1 pictures for one case.")
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "case.json")
    parser.add_argument("--dry-run", action="store_true", help="Only search; download nothing")
    args = parser.parse_args(argv)
    try:
        run(args.config, args.dry_run)
        return 0
    except EmptySearchError as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"STOPPED: {type(exc).__name__}: {exc}", file=sys.stderr)
    except Exception as exc:                  # Earth Engine refusals: say so plainly, no long traceback
        if type(exc).__name__ != "EEException":
            raise
        print(f"STOPPED: Earth Engine refused the request: {exc}. Check the settings card; if it says quota "
              f"or time limit, wait and retry or shrink the area (half_size_m).", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
