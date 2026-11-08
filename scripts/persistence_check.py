"""M3: do the flood-day 'land got louder' pixels light up again on a later date? (the user's idea)

Labels 30 Jun and a later date with the same rules (configs/case_lekki5km.json), then reports, per area,
how many 30 Jun red pixels are red again, compared with how often ANY land pixel is red on the later
date (the chance level). Writes docs/figures/fig16_m3_persistence.png:
dark red = red on both dates, light red = 30 Jun only, orange = later date only, blue = always water.
Usage: .venv/bin/python scripts/persistence_check.py lagos-lekki-5km-after-2026-07-12 [first_case] [--no-figure]
(first_case defaults to the flood day vs August.)
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
A = ROOT / "outputs/aligned"


def labels_for(case, occ):
    r, nd = CARD["labels"], CARD["output"]["nodata"]
    with rasterio.open(A / f"{case}_event.tif") as e, rasterio.open(A / f"{case}_reference.tif") as f:
        ev, rf = e.read(1), f.read(1)
    return water.classify(water.smooth_db(ev, r["smooth_px"], nd), water.smooth_db(rf, r["smooth_px"], nd),
                          occ, nd, r["change_db"], r["water_db"], r["persistent_pct"])


def main(later_case, first_case=None, figure=True):
    with rasterio.open(A / f"{CARD['case_id']}_jrc_water_occurrence.tif") as f:
        occ = f.read(1)
    areas = water.split_areas(occ.shape, int(round(CARD["split"]["gap_m"] / CARD["output"]["pixel_size_m"])),
                              CARD["split"]["practice_side"])
    first, later = labels_for(first_case or CARD["case_id"], occ), labels_for(later_case, occ)
    red1, red2 = first == water.LAND_LOUDER, later == water.LAND_LOUDER
    land = (occ == 0) & (first != water.NOT_OBSERVED) & (later != water.NOT_OBSERVED)
    for code, name in ((water.PRACTICE, "practice (west)"), (water.TEST, "test (east)")):
        a = areas == code
        n1 = (red1 & a).sum()
        again = (red1 & red2 & a).sum() / n1 * 100
        chance = (red2 & land & a).sum() / (land & a).sum() * 100
        print(f"{name}: 30 Jun red {n1} px; red again later {again:.1f}% vs chance {chance:.1f}% "
              f"(x{again / chance:.1f}); later-date red overall {chance:.1f}% of land")
    if not figure:
        return
    rgb = np.full((3, *occ.shape), 235, dtype="uint8")
    for mask, colour in ((occ > CARD["labels"]["persistent_pct"], (40, 90, 200)), (red1 & ~red2, (245, 150, 150)),
                         (red2 & ~red1, (250, 170, 0)), (red1 & red2, (160, 0, 0))):
        for i in range(3):
            rgb[i][mask] = colour[i]
    rgb[:, areas == water.GAP] = (rgb[:, areas == water.GAP] * 0.6).astype("uint8")
    out = ROOT / "docs/figures/fig16_m3_persistence.png"
    with rasterio.open(out, "w", driver="PNG", width=occ.shape[1], height=occ.shape[0], count=3, dtype="uint8") as d:
        d.write(rgb)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--no-figure"]
    main(args[0] if args else "lagos-lekki-5km-after-2026-07-12", args[1] if len(args) > 1 else None,
         "--no-figure" not in sys.argv)
