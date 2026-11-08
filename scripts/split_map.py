"""Picture of the practice/test split on the 5 km square (fig14).

Background: August reference VV (grey). Practice side tinted blue, test side tinted orange, gap left plain grey.
Usage: .venv/bin/python scripts/split_map.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import water  # noqa: E402

CARD = json.loads((ROOT / "configs/case_lekki5km.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs/figures/fig14_m3_practice_test_split.png"


def main():
    with rasterio.open(ROOT / "outputs/aligned" / f"{CARD['case_id']}_reference.tif") as f:
        db, px = f.read(1), f.res[0]
    split = CARD["split"]
    areas = water.split_areas(db.shape, int(round(split["gap_m"] / px)), split["practice_side"])
    g = (np.clip((db + 25) / 25, 0, 1) * 255).astype("float32")
    rgb = np.stack([g, g, g])
    tint = {water.PRACTICE: (60, 120, 255), water.TEST: (255, 150, 30)}
    for label, colour in tint.items():
        m = areas == label
        for i, c in enumerate(colour):
            rgb[i][m] = 0.6 * rgb[i][m] + 0.4 * c
    with rasterio.open(OUT, "w", driver="PNG", width=db.shape[1], height=db.shape[0], count=3, dtype="uint8") as dst:
        dst.write(rgb.astype("uint8"))
    for label, name in ((water.PRACTICE, "practice"), (water.TEST, "test"), (water.GAP, "gap")):
        print(f"{name}: {(areas == label).sum()} pixels")
    print(f"Saved {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
