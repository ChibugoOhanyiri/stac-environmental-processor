"""M3: are the places named in flood reports on 'land got louder' areas?

For each place in evidence/places_osm_2026-11-07.csv that falls inside the 5 km square, report the share
of never-water land within RADIUS_M that is labelled 'land got louder', on the flood day and the two
control days, next to the share across its whole area (practice or test). Point evidence only: a named
road or district is not a flood boundary (DATA_AND_VALIDATION.md), so no accuracy is computed.
Place positions: OpenStreetMap (ODbL, © OpenStreetMap contributors); district points are approximate.
Usage: .venv/bin/python scripts/point_checks.py
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
import persistence_check as pc  # noqa: E402  (labels_for: same rules as the rest of M3)
import preprocess  # noqa: E402
import water  # noqa: E402

RADIUS_M = 250
CARD = pc.CARD
RUNS = {"30 Jun flood": CARD["case_id"], "10 Sep wet": "lagos-lekki-5km-control-wet-2026-09-10",
        "22 Sep dry": "lagos-lekki-5km-control-dry-2026-09-22"}


def main():
    jrc = ROOT / "outputs/aligned" / f"{CARD['case_id']}_jrc_water_occurrence.tif"
    with rasterio.open(jrc) as f:
        occ, transform, crs = f.read(1), f.transform, f.crs.to_string()
    px = transform.a
    areas = water.split_areas(occ.shape, int(round(CARD["split"]["gap_m"] / px)), CARD["split"]["practice_side"])
    land = occ == 0
    labels = {k: pc.labels_for(v, occ) for k, v in RUNS.items()}
    rows_out = []
    yy, xx = np.mgrid[0:occ.shape[0], 0:occ.shape[1]]
    for place in csv.DictReader(open(ROOT / "evidence/places_osm_2026-11-07.csv", encoding="utf-8")):
        e, n = preprocess.lonlat_to_crs(float(place["lon"]), float(place["lat"]), crs)
        col, row = (e - transform.c) / px, (transform.f - n) / px
        if not (0 <= col < occ.shape[1] and 0 <= row < occ.shape[0]):
            print(f"outside square: {place['name']}")
            continue
        disc = ((xx - col) ** 2 + (yy - row) ** 2) <= (RADIUS_M / px) ** 2
        side = {water.PRACTICE: "practice", water.TEST: "test", water.GAP: "gap"}[int(areas[int(row), int(col)])]
        side_mask = areas == areas[int(row), int(col)]
        out = {"place": place["name"], "side": side, "land_px_in_circle": int((disc & land).sum())}
        for k, lab in labels.items():
            red = lab == water.LAND_LOUDER
            out[f"{k}: circle %"] = round(100 * red[disc & land].mean(), 1)
            out[f"{k}: whole side %"] = round(100 * red[side_mask & land].mean(), 1)
        rows_out.append(out)
        print(f"{place['name'][:42]:42s} {side:8s} flood {out['30 Jun flood: circle %']:5.1f}% "
              f"(side {out['30 Jun flood: whole side %']}%) | wet {out['10 Sep wet: circle %']}% | dry {out['22 Sep dry: circle %']}%")
    path = ROOT / "evidence/m3_point_checks_5km.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0]))
        w.writeheader()
        w.writerows(rows_out)
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
