"""Rain before each satellite pass, from NASA GPM IMERG V07 in Earth Engine (free, read-only).

Totals rain over a settings card's square in the 48 hours and 7 days before 05:29 UTC (06:29 Lagos)
on each date. IMERG is a satellite rain estimate on a ~10 km grid: it says "how wet was the area",
not street-level rain. Usage:
  .venv/bin/python scripts/rainfall.py configs/case_lekki5km.json 2026-06-30 2026-08-05 ...
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import ee  # noqa: E402
import preprocess  # noqa: E402

PASS_TIME_UTC = "T05:29:00"


def main(card_path: str, dates: list[str]) -> None:
    card = preprocess.load_card(Path(card_path))
    ee.Initialize(project=preprocess.gee_project())
    a = card["area"]
    box = ee.Geometry.Point([a["centre_lon"], a["centre_lat"]]).buffer(a["half_size_m"]).bounds()
    rain = ee.ImageCollection("NASA/GPM_L3/IMERG_V07").select("precipitation")  # mm per hour, half-hourly
    for d in dates:
        end = ee.Date(d + PASS_TIME_UTC)
        row = []
        for hours in (48, 168):
            window = rain.filterDate(end.advance(-hours, "hour"), end)
            total = window.sum().multiply(0.5)  # each image covers half an hour
            mm = total.reduceRegion(ee.Reducer.mean(), box, 10000).get("precipitation").getInfo()
            row.append((mm, window.size().getInfo(), hours * 2))
        print(f"{d}: {row[0][0]:.1f} mm in 48 h ({row[0][1]}/{row[0][2]} half-hours), "
              f"{row[1][0]:.1f} mm in 7 days ({row[1][1]}/{row[1][2]})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2:])
