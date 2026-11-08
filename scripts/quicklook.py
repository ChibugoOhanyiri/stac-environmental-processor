"""Make a quick-look PNG of the recipe's two output files, so a person can SEE what came out.

Panels, left to right: flood day (VV) | dry reference (VV) | difference (flood day minus reference).
Grey panels: black = quiet echo (−25 dB or less), white = loud echo (0 dB or more).
Difference panel: red = louder on the flood day, blue = quieter, white = about the same (±6 dB scale).
Uses only rasterio + numpy (already installed). Display only: no thresholds or classes.
Usage: .venv/bin/python scripts/quicklook.py   (1 km case, fig10)
       .venv/bin/python scripts/quicklook.py --case lagos-lekki-5km-2026-06-30 --zoom 1 --out docs/figures/fig11_m3_5km_quicklook.png
"""
import argparse
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "outputs" / "aligned"
CASE = "lagos-lekki-orchid-2026-06-30"
OUT = ROOT / "docs" / "figures" / "fig10_m2_outputs_quicklook.png"
ZOOM, GAP = 3, 12  # each 10 m pixel drawn as 3 x 3 screen pixels; white gap between panels


def grey(db, nodata):
    scaled = np.clip((db + 25) / 25, 0, 1) * 255
    g = scaled.astype("uint8")
    g[db == nodata] = 0
    return np.stack([g, g, g])


def diverging(diff, limit=6.0):
    t = np.clip(diff / limit, -1, 1)
    r = np.where(t > 0, 255, 255 * (1 + t))
    b = np.where(t < 0, 255, 255 * (1 - t))
    g = 255 * (1 - np.abs(t))
    return np.stack([r, g, b]).astype("uint8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default=CASE)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--zoom", type=int, default=ZOOM)
    args = ap.parse_args()
    out, zoom = ROOT / args.out, args.zoom
    with rasterio.open(FOLDER / f"{args.case}_event.tif") as e, rasterio.open(FOLDER / f"{args.case}_reference.tif") as r:
        assert e.transform == r.transform and e.crs == r.crs, "Files are not on the same grid"
        ev, ref, nodata = e.read(1), r.read(1), e.nodata
    panels = [grey(ev, nodata), grey(ref, nodata), diverging(np.where(ev == nodata, 0, ev - ref))]
    panels = [p.repeat(zoom, axis=1).repeat(zoom, axis=2) for p in panels]
    gap = np.full((3, panels[0].shape[1], GAP), 255, dtype="uint8")
    image = np.concatenate([panels[0], gap, panels[1], gap, panels[2]], axis=2)
    out.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(out, "w", driver="PNG", width=image.shape[2], height=image.shape[1],
                       count=3, dtype="uint8") as dst:
        dst.write(image)
    print(f"Saved {out.relative_to(ROOT)} ({image.shape[2]} x {image.shape[1]} px)")


if __name__ == "__main__":
    main()
