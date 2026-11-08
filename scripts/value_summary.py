"""M3 first look: how many pixels are 'dark' (possible open water) or changed, before any method is chosen.

Reads the two M2 GeoTIFFs (flood day and August reference) and prints, per band:
percentiles, counts below example water thresholds on each date, and counts that got louder/quieter.
The thresholds here are EXAMPLES for looking, not the M3 method. Nodata (-9999) is excluded.
Usage: .venv/bin/python scripts/value_summary.py [case_id]   (default: the 1 km Orchid case)
"""
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "outputs" / "aligned"
CASE = "lagos-lekki-orchid-2026-06-30"
EXAMPLE_THRESHOLDS_DB = {"VV": [-15, -18, -20], "VH": [-22, -25]}
CHANGE_DB = 3


def main() -> None:
    case = sys.argv[1] if len(sys.argv) > 1 else CASE
    with rasterio.open(FOLDER / f"{case}_event.tif") as e, rasterio.open(FOLDER / f"{case}_reference.tif") as r:
        if (e.crs, e.transform, e.shape) != (r.crs, r.transform, r.shape):
            raise SystemExit("STOPPED: the two pictures are not on the same grid.")
        event, ref, nodata = e.read(), r.read(), e.nodata
    for i, band in enumerate(["VV", "VH"]):
        ev, rf = event[i], ref[i]
        valid = (ev != nodata) & (rf != nodata)
        ev, rf = ev[valid], rf[valid]
        diff = ev - rf
        print(f"{band}: {valid.sum()} valid pixels")
        print(f"  flood day percentiles 1/5/50/95: {np.round(np.percentile(ev, [1, 5, 50, 95]), 1)}")
        print(f"  August    percentiles 1/5/50/95: {np.round(np.percentile(rf, [1, 5, 50, 95]), 1)}")
        for t in EXAMPLE_THRESHOLDS_DB[band]:
            print(f"  below {t} dB: flood day {(ev < t).sum()}, August {(rf < t).sum()}, both {((ev < t) & (rf < t)).sum()}")
        print(f"  louder by >{CHANGE_DB} dB: {(diff > CHANGE_DB).sum()}; quieter by >{CHANGE_DB} dB: "
              f"{(diff < -CHANGE_DB).sum()}; median change {np.median(diff):+.2f} dB")


if __name__ == "__main__":
    main()
