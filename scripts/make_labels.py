"""M3: label every pixel of the 5 km square for the flood day and both control days.

Reads the aligned GeoTIFFs + JRC layer, smooths (src/water.py), labels with the rules in
configs/case_lekki5km.json "labels", and writes:
  outputs/change/<case>_labels.tif   (uint8, 255 = not observed; git-ignored)
  evidence/m3_label_counts_5km.csv   (pixel counts and km² per label, per area: practice/test/gap)
  docs/figures/fig15_m3_labels.png   (flood day | wet control | dry control)
Usage: .venv/bin/python scripts/make_labels.py
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import water  # noqa: E402

CARD = json.loads((ROOT / "configs/case_lekki5km.json").read_text(encoding="utf-8"))
A = ROOT / "outputs/aligned"
RUNS = {"30 Jun flood": CARD["case_id"],
        "10 Sep wet control": "lagos-lekki-5km-control-wet-2026-09-10",
        "22 Sep dry control": "lagos-lekki-5km-control-dry-2026-09-22"}
COLOURS = {water.NO_CHANGE: (235, 235, 235), water.PERSISTENT_WATER: (40, 90, 200),
           water.NEW_DARK_WATER: (0, 200, 220), water.LAND_LOUDER: (220, 40, 40),
           water.CANT_TELL: (250, 190, 0), water.NOT_OBSERVED: (0, 0, 0)}


def read(path):
    with rasterio.open(path) as f:
        return f.read(1), f.profile


def main():
    rules, nd = CARD["labels"], CARD["output"]["nodata"]
    occ, _ = read(A / f"{CARD['case_id']}_jrc_water_occurrence.tif")
    px_m = CARD["output"]["pixel_size_m"]
    areas = water.split_areas(occ.shape, int(round(CARD["split"]["gap_m"] / px_m)), CARD["split"]["practice_side"])
    area_names = {water.PRACTICE: "practice (west)", water.TEST: "test (east)", water.GAP: "gap"}
    rows, pictures = [], []
    for run_name, case in RUNS.items():
        ev, profile = read(A / f"{case}_event.tif")
        rf, _ = read(A / f"{case}_reference.tif")
        labels = water.classify(water.smooth_db(ev, rules["smooth_px"], nd),
                                water.smooth_db(rf, rules["smooth_px"], nd), occ, nd,
                                rules["change_db"], rules["water_db"], rules["persistent_pct"])
        out = ROOT / "outputs/change" / f"{case}_labels.tif"
        out.parent.mkdir(parents=True, exist_ok=True)
        profile.update(dtype="uint8", count=1, nodata=water.NOT_OBSERVED)
        with rasterio.open(out, "w", **profile) as dst:
            dst.write(labels, 1)
            dst.set_band_description(1, "M3 labels: " + ", ".join(f"{k}={v}" for k, v in water.LABEL_NAMES.items()))
        for a_code, a_name in area_names.items():
            in_area = areas == a_code
            for code, name in water.LABEL_NAMES.items():
                n = int(((labels == code) & in_area).sum())
                rows.append({"date": run_name, "area": a_name, "label": name, "pixels": n,
                             "km2": round(n * px_m * px_m / 1e6, 3),
                             "pct_of_area": round(100 * n / in_area.sum(), 2)})
        rgb = np.zeros((3, *labels.shape), dtype="uint8")
        for code, colour in COLOURS.items():
            for i in range(3):
                rgb[i][labels == code] = colour[i]
        rgb[:, areas == water.GAP] = (rgb[:, areas == water.GAP] * 0.6).astype("uint8")   # dim the gap
        pictures.append(rgb)
        print(f"wrote {out.relative_to(ROOT)}")
    csv_path = ROOT / "evidence/m3_label_counts_5km.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    gap = np.full((3, pictures[0].shape[1], 12), 255, dtype="uint8")
    image = np.concatenate([pictures[0], gap, pictures[1], gap, pictures[2]], axis=2)
    fig = ROOT / "docs/figures/fig15_m3_labels.png"
    with rasterio.open(fig, "w", driver="PNG", width=image.shape[2], height=image.shape[1], count=3, dtype="uint8") as dst:
        dst.write(image)
    print(f"wrote {csv_path.relative_to(ROOT)} and {fig.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
