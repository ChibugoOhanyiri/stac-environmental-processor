"""M5: describe our derived outputs as a STAC catalogue (library catalogue cards for maps).

Analogy: a library card does not hold the book; it says what it is, when and where it is from, how it
was made and which shelf it sits on, in a format every library understands. STAC (SpatioTemporal Asset
Catalog) is that format for maps and satellite data.

What this writes (catalog/, committed):
  catalog/collection.json                       one Collection: Lekki 5 km, 30 Jun 2026 flood case + controls
  catalog/<item-id>/<item-id>.json              one Item per comparison date (flood, controls, 12 Jul)
  catalog/<item-id>/labels.tif                  the M3 label map as a Cloud-Optimised GeoTIFF (small, uint8)
Item assets also point to the receipt (evidence/runs/, committed) and to the float backscatter COGs in
outputs/cog/ (git-ignored, LOCAL ONLY: rebuild with src/preprocess.py + this script; the receipt has the
image IDs and SHA-256 of the GeoTIFFs they were made from).
Usage: .venv/bin/python src/catalog.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pystac
import rasterio
from pystac.extensions.classification import Classification, ClassificationExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sar import FrequencyBand, Polarization, SarExtension
from pystac.extensions.sat import OrbitState, SatExtension
from rasterio.warp import transform_bounds

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
import persistence_check as pc  # noqa: E402  (same labelling rules as M3)
import water  # noqa: E402

CARD = pc.CARD
ALIGNED, COG_DIR, CAT_DIR = ROOT / "outputs/aligned", ROOT / "outputs/cog", ROOT / "catalog"
COLLECTION_ID = "lekki-5km-flood-change-2026"
RUNS = {  # item id -> (case id, role, plain description)
    "lekki-5km-2026-06-30-flood": (CARD["case_id"], "flood day",
                                   "Flood morning (reported Lagos flood, 30 Jun 2026) vs August 2026 median."),
    "lekki-5km-2026-07-12-after": ("lagos-lekki-5km-after-2026-07-12", "next heavy rain",
                                   "Next pass after the flood (12 Jul 2026, very wet) vs August 2026 median."),
    "lekki-5km-2026-09-10-control-wet": ("lagos-lekki-5km-control-wet-2026-09-10", "control (wet)",
                                         "Control: equally rainy day with no reported flood vs August median."),
    "lekki-5km-2026-09-22-control-dry": ("lagos-lekki-5km-control-dry-2026-09-22", "control (dry)",
                                         "Control: dry day vs August median (radar grain level)."),
}
CLAIM = ("Measured surface change consistent with the reported flood (PRD level 2). "
         "Not a validated flood-extent map; see evaluation/ASSESSMENT.md.")
CLASS_COLOURS = {water.NO_CHANGE: "ebebeb", water.PERSISTENT_WATER: "285ac8", water.NEW_DARK_WATER: "00c8dc",
                 water.LAND_LOUDER: "dc2828", water.CANT_TELL: "fabe00", water.NOT_OBSERVED: "000000"}


def latest_receipt(case_id: str) -> Path:
    """Newest committed receipt for a case that actually downloaded files (not a dry run)."""
    found = sorted(p for p in (ROOT / "evidence/runs").glob(f"run-manifest_*_{case_id}.json")
                   if not json.loads(p.read_text(encoding="utf-8")).get("dry_run"))
    if not found:
        raise FileNotFoundError(f"No committed receipt for {case_id} in evidence/runs/.")
    return found[-1]


def acquisition_time(image_id: str) -> datetime:
    """S1D_IW_GRDH_1SDV_20260630T052917_... -> 2026-06-30 05:29:17 UTC (start of the scene)."""
    return datetime.strptime(image_id.split("_")[4], "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)


def write_cog(path: Path, data: np.ndarray, profile: dict, descriptions: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    prof = {k: profile[k] for k in ("crs", "transform", "width", "height", "nodata")}
    prof.update(driver="COG", count=data.shape[0], dtype=str(data.dtype), compress="deflate")
    with rasterio.open(path, "w", **prof) as dst:
        dst.write(data)
        for i, d in enumerate(descriptions, start=1):
            dst.set_band_description(i, d)


def rel(path: Path, start: Path) -> str:
    return Path(*([".."] * len(start.relative_to(ROOT).parts)), path.relative_to(ROOT)).as_posix()


def build() -> pystac.Collection:
    with rasterio.open(ALIGNED / f"{CARD['case_id']}_jrc_water_occurrence.tif") as f:
        occ = f.read(1)
    items = []
    for item_id, (case, role, description) in RUNS.items():
        receipt_path = latest_receipt(case)
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        event_ids = receipt["inputs"]["event"]["gee_image_ids"]
        ref_ids = receipt["inputs"]["reference"]["gee_image_ids"]
        with rasterio.open(ALIGNED / f"{case}_event.tif") as e, rasterio.open(ALIGNED / f"{case}_reference.tif") as r:
            event, reference, profile = e.read(), r.read(), e.profile
            crs, transform, bounds = e.crs, e.transform, e.bounds
        west, south, east, north = transform_bounds(crs, "EPSG:4326", *bounds)
        geometry = {"type": "Polygon", "coordinates": [[[west, south], [east, south], [east, north],
                                                         [west, north], [west, south]]]}
        labels = pc.labels_for(case, occ)
        item_dir = CAT_DIR / item_id
        write_cog(item_dir / "labels.tif", labels[np.newaxis], {**profile, "nodata": water.NOT_OBSERVED},
                  ["M3 labels: " + ", ".join(f"{k}={v}" for k, v in water.LABEL_NAMES.items())])
        write_cog(COG_DIR / f"{case}_event.tif", event, profile, ["VV_dB", "VH_dB"])
        write_cog(COG_DIR / f"{case}_reference.tif", reference, profile, ["VV_dB", "VH_dB"])
        counts = {water.LABEL_NAMES[k]: int((labels == k).sum()) for k in water.LABEL_NAMES}
        item = pystac.Item(
            id=item_id, geometry=geometry, bbox=[west, south, east, north],
            datetime=acquisition_time(event_ids[0]),
            properties={
                "title": f"Lekki 5 km: {role}, {acquisition_time(event_ids[0]):%d %b %Y}",
                "description": description,
                "platform": "sentinel-1" + receipt["settings_card"]["satellite"]["platform_number"].lower(),
                "constellation": "sentinel-1", "instruments": ["c-sar"],
                "lekki:role": role, "lekki:claim": CLAIM,
                "lekki:reference_window": receipt["inputs"]["reference"]["window"],
                "lekki:input_image_ids": {"event": event_ids, "reference": ref_ids},
                "lekki:rules": CARD["labels"], "lekki:label_pixel_counts": counts,
                "lekki:pixel_area_m2": abs(transform.a * transform.e),
                "lekki:run_id": receipt["run_id"], "lekki:code_commit": receipt["versions"]["git_commit"],
            })
        sar = SarExtension.ext(item, add_if_missing=True)
        sar.apply(instrument_mode="IW", frequency_band=FrequencyBand.C, product_type="GRD",
                  polarizations=[Polarization.VV, Polarization.VH])
        sat = SatExtension.ext(item, add_if_missing=True)
        sat.apply(orbit_state=OrbitState.DESCENDING, relative_orbit=receipt["settings_card"]["satellite"]["relative_orbit"])
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        proj.code = crs.to_string()
        proj.shape = [profile["height"], profile["width"]]
        proj.transform = list(transform)[:6]
        item.add_asset("labels", pystac.Asset(
            href="./labels.tif", media_type=pystac.MediaType.COG, title="M3 pixel labels",
            description="uint8 classes (255 = not observed). Rules in lekki:rules.", roles=["data"]))
        ClassificationExtension.ext(item.assets["labels"], add_if_missing=True).classes = [
            Classification.create(value=k, name=v.replace(" ", "_").replace("'", ""), description=v,
                                  color_hint=CLASS_COLOURS[k], nodata=(k == water.NOT_OBSERVED))
            for k, v in water.LABEL_NAMES.items()]
        for key, path, title in (("event_backscatter", COG_DIR / f"{case}_event.tif", "Event backscatter VV/VH (dB)"),
                                 ("reference_backscatter", COG_DIR / f"{case}_reference.tif",
                                  "Reference backscatter VV/VH (dB), median")):
            item.add_asset(key, pystac.Asset(
                href=rel(path, item_dir), media_type=pystac.MediaType.COG, title=title,
                description="LOCAL ONLY (git-ignored). Rebuild: src/preprocess.py then src/catalog.py.",
                roles=["data", "local-only"]))
        item.add_asset("receipt", pystac.Asset(
            href=rel(receipt_path, item_dir), media_type=pystac.MediaType.JSON, title="Run receipt",
            description="Image IDs, settings, versions, SHA-256, Earth Engine process graph.", roles=["metadata"]))
        items.append(item)

    collection = pystac.Collection(
        id=COLLECTION_ID,
        title="Lekki 5 km radar change, Lagos flood of 30 June 2026",
        description=("Derived Sentinel-1 change labels for a 5 km square of central Lekki: the reported flood morning, "
                     "the next heavy rain, and wet and dry control days, each against an August 2026 median. "
                     + CLAIM),
        extent=pystac.Extent(
            pystac.SpatialExtent([items[0].bbox]),
            pystac.TemporalExtent([[min(i.datetime for i in items), max(i.datetime for i in items)]])),
        license="other",
        providers=[pystac.Provider("ESA / Copernicus", roles=[pystac.ProviderRole.PRODUCER, pystac.ProviderRole.LICENSOR]),
                   pystac.Provider("Google Earth Engine", roles=[pystac.ProviderRole.HOST]),
                   pystac.Provider("Chibugo Ohanyiri (with AI assistance)", roles=[pystac.ProviderRole.PROCESSOR])],
        extra_fields={"lekki:attribution": "Contains modified Copernicus Sentinel data (2026), processed in Google Earth "
                                           "Engine; JRC Global Surface Water (EC JRC/Google)."})
    for item in items:
        collection.add_item(item)
    collection.normalize_hrefs(str(CAT_DIR))
    for item in items:   # normalize_hrefs rewrites asset hrefs only for relative items; keep ours as built
        item.set_self_href(str(CAT_DIR / item.id / f"{item.id}.json"))
    return collection


def main() -> None:
    collection = build()
    collection.validate_all()          # checks every Item and the Collection against the STAC JSON schemas
    collection.save(pystac.CatalogType.SELF_CONTAINED)
    print(f"Saved {len(list(collection.get_items()))} items + collection to {CAT_DIR.relative_to(ROOT)}/ (validated)")


if __name__ == "__main__":
    main()
