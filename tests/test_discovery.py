"""Risk-based, offline tests; no credentials, imagery or billable jobs."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("discovery", ROOT / "scripts/discover_scenes.py")
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
BASE = d.ENDPOINT + "/search"


def item(identity):
    return {"id": identity, "collection": "test", "properties": {}}


def page(items, next_url=None):
    return {"type": "FeatureCollection", "features": items,
            "links": [{"rel": "next", "href": next_url}] if next_url else []}


class DiscoveryTests(unittest.TestCase):
    def test_bad_bbox_and_dates(self):
        for box in ([3, 7, 2, 8], [0, 0, float("nan"), 1], [0, -91, 1, 2]):
            with self.assertRaises(ValueError): d.validate_bbox(box)
        for interval in ("2024-01-01/2024-01-02", "2024-02-01T00:00:00Z/2024-01-01T00:00:00Z"):
            with self.assertRaises(ValueError): d.validate_interval(interval)

    def test_empty_is_valid(self):
        self.assertEqual(d.collect_pages(BASE, lambda _: page([])), [])

    def test_dedup_and_pagination(self):
        pages = {BASE: page([item("a")], BASE + "?page=2"),
                 BASE + "?page=2": page([item("a"), item("b")])}
        self.assertEqual(len(d.collect_pages(BASE, pages.__getitem__)), 2)

    def test_loop_fails(self):
        with self.assertRaises(ValueError): d.collect_pages(BASE, lambda _: page([], BASE))

    def test_no_silent_truncation(self):
        with self.assertRaises(ValueError):
            d.collect_pages(BASE, lambda _: page([], BASE + "?page=2"), max_pages=1)

    def test_external_next_link_rejected(self):
        with self.assertRaises(ValueError):
            d.collect_pages(BASE, lambda _: page([], "https://example.org/private"))

    def test_malformed_response_rejected(self):
        with self.assertRaises(ValueError): d.collect_pages(BASE, lambda _: {"error": "oops"})

    def test_missing_orbit_not_comparable(self):
        self.assertFalse(d.comparable_radar(item("a"), item("b")))

    def test_real_fixture_orbits(self):
        items = json.loads((ROOT / "evidence/sentinel-1-grd.json").read_text())["features"]
        desc = [x for x in items if x["properties"]["sat:orbit_state"] == "descending"]
        asc = [x for x in items if x["properties"]["sat:orbit_state"] == "ascending"]
        self.assertEqual(len(desc), 3)
        self.assertTrue(d.comparable_radar(desc[0], desc[1]))
        self.assertFalse(d.comparable_radar(desc[0], asc[0]))

    def test_missing_cloud_is_unknown(self):
        self.assertIsNone(d.summarise(item("a"))["tile_cloud_percent"])


if __name__ == "__main__": unittest.main()
