"""M4: do the M3 conclusions survive other reasonable rule choices? (sensitivity test)

Re-labels flood day and both controls on the TEST side for every combination of smoothing window
(3, 5, 7 px) and change threshold (3.0, 3.5, 4.0 dB); other rules as in configs/case_lekki5km.json.
Writes evidence/m4_sensitivity_5km.csv. Usage: .venv/bin/python scripts/sensitivity.py
"""
import csv
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
import persistence_check as pc  # noqa: E402
import water  # noqa: E402

CARD = pc.CARD
A = ROOT / "outputs/aligned"
RUNS = {"flood": CARD["case_id"], "wet": "lagos-lekki-5km-control-wet-2026-09-10",
        "dry": "lagos-lekki-5km-control-dry-2026-09-22"}


def main():
    with rasterio.open(A / f"{CARD['case_id']}_jrc_water_occurrence.tif") as f:
        occ = f.read(1)
    nd, r = CARD["output"]["nodata"], CARD["labels"]
    areas = water.split_areas(occ.shape, int(round(CARD["split"]["gap_m"] / CARD["output"]["pixel_size_m"])),
                              CARD["split"]["practice_side"])
    test_land = (areas == water.TEST) & (occ == 0)
    pics = {}
    for k, case in RUNS.items():
        with rasterio.open(A / f"{case}_event.tif") as e, rasterio.open(A / f"{case}_reference.tif") as g:
            pics[k] = (e.read(1), g.read(1))
    rows = []
    for size in (3, 5, 7):
        smooth = {k: (water.smooth_db(ev, size, nd), water.smooth_db(rf, size, nd)) for k, (ev, rf) in pics.items()}
        for change in (3.0, 3.5, 4.0):
            row = {"window_px": size, "change_db": change}
            for k, (ev, rf) in smooth.items():
                lab = water.classify(ev, rf, occ, nd, change, r["water_db"], r["persistent_pct"])
                row[f"{k}_louder_pct"] = round(100 * float(np.mean(lab[test_land] == water.LAND_LOUDER)), 2)
            row["ratio_vs_worst_control"] = round(row["flood_louder_pct"] / max(row["wet_louder_pct"], row["dry_louder_pct"]), 1)
            rows.append(row)
            print(row)
    out = ROOT / "evidence/m4_sensitivity_5km.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
