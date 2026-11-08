"""M3: how does smoothing change the flood-day vs control contrast? (land that is never water only)

For each window size, smooth flood-day/control and reference pictures (src/water.py, linear power),
then count land pixels louder or quieter by more than 3 dB. Land = JRC occurrence 0 (never water).
Usage: .venv/bin/python scripts/smoothing_check.py
"""
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import water  # noqa: E402

A = ROOT / "outputs" / "aligned"
CASES = {"30 Jun flood": "lagos-lekki-5km-2026-06-30",
         "10 Sep wet": "lagos-lekki-5km-control-wet-2026-09-10",
         "22 Sep dry": "lagos-lekki-5km-control-dry-2026-09-22"}
JRC = A / "lagos-lekki-5km-2026-06-30_jrc_water_occurrence.tif"


def read(path):
    with rasterio.open(path) as f:
        return f.read(1), f.nodata


def main():
    occ, _ = read(JRC)
    land = occ == 0
    print("window   " + "   ".join(f"{k:>24s}" for k in CASES))
    for size in (1, 3, 5, 7, 9):
        cells = []
        for case in CASES.values():
            ev, nd = read(A / f"{case}_event.tif")
            rf, _ = read(A / f"{case}_reference.tif")
            e, r = water.smooth_db(ev, size, nd), water.smooth_db(rf, size, nd)
            ok = land & (e != nd) & (r != nd)
            d = (e - r)[ok]
            cells.append(f"louder {np.mean(d > 3) * 100:5.1f}% quieter {np.mean(d < -3) * 100:4.1f}%")
        print(f"{size}x{size} ({size * 10:>2d} m) " + "   ".join(f"{c:>24s}" for c in cells))


if __name__ == "__main__":
    main()
