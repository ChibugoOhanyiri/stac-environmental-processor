"""Offline checks on the committed STAC catalogue (catalog/). No network, no Earth Engine.

Risks checked: a card that describes a different map than the file it points to (pixel counts),
wrong place (bbox outside the study square), wrong time (datetime not the satellite pass in the
receipt), a legend that disagrees with the code's labels, and broken committed links.
Run: .venv/bin/python -m unittest discover -s tests -v
"""
import importlib.util
import json
import unittest
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "catalog"
spec = importlib.util.spec_from_file_location("water", ROOT / "src/water.py")
water = importlib.util.module_from_spec(spec)
spec.loader.exec_module(water)
CARD = json.loads((ROOT / "configs/case_lekki5km.json").read_text(encoding="utf-8"))


def items():
    collection = json.loads((CAT / "collection.json").read_text(encoding="utf-8"))
    for link in collection["links"]:
        if link["rel"] == "item":
            path = (CAT / link["href"]).resolve()
            yield path, json.loads(path.read_text(encoding="utf-8"))


@unittest.skipUnless((CAT / "collection.json").exists(), "catalogue not built")
class CatalogTests(unittest.TestCase):
    def test_has_the_four_comparisons(self):
        self.assertEqual(len(list(items())), 4)

    def test_pixel_counts_match_the_label_file(self):
        for path, item in items():
            with rasterio.open(path.parent / item["assets"]["labels"]["href"]) as f:
                labels = f.read(1)
            for code, name in water.LABEL_NAMES.items():
                self.assertEqual(item["properties"]["lekki:label_pixel_counts"][name], int((labels == code).sum()),
                                 f"{item['id']}: {name}")

    def test_bbox_is_the_study_square(self):
        a = CARD["area"]
        for _, item in items():
            w, s, e, n = item["bbox"]
            self.assertTrue(w < a["centre_lon"] < e and s < a["centre_lat"] < n, item["id"])
            self.assertAlmostEqual((e - w) * 111_320 * np.cos(np.radians(a["centre_lat"])), 5000, delta=150)
            self.assertAlmostEqual((n - s) * 110_574, 5000, delta=150)

    def test_datetime_is_the_satellite_pass_in_the_receipt(self):
        for path, item in items():
            receipt = json.loads((path.parent / item["assets"]["receipt"]["href"]).read_text(encoding="utf-8"))
            stamp = receipt["inputs"]["event"]["gee_image_ids"][0].split("_")[4]       # 20260630T052917
            self.assertEqual(item["properties"]["datetime"][:19].replace("-", "").replace(":", ""), stamp)

    def test_legend_matches_the_code(self):
        for _, item in items():
            classes = item["assets"]["labels"]["classification:classes"]
            self.assertEqual({c["value"]: c["description"] for c in classes}, water.LABEL_NAMES)

    def test_committed_links_resolve(self):
        for path, item in items():
            for key, asset in item["assets"].items():
                if "local-only" in asset.get("roles", []):
                    continue                                       # git-ignored imagery, rebuilt locally
                self.assertTrue((path.parent / asset["href"]).resolve().exists(), f"{item['id']} {key}")

    def test_claim_is_stated_on_every_item(self):
        for _, item in items():
            self.assertIn("Not a validated flood-extent map", item["properties"]["lekki:claim"])


if __name__ == "__main__":
    unittest.main()
