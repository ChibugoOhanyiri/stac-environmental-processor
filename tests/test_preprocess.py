"""Offline tests for src/preprocess.py: no Earth Engine, no internet, no credentials.

Each test checks a real risk: misaligned grids, bad settings cards, silent empty searches.
Run: .venv\\Scripts\\python -m unittest discover -s tests -v
"""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preprocess", ROOT / "src/preprocess.py")
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)
CARD = json.loads((ROOT / "configs/case.json").read_text(encoding="utf-8"))


class FakeCollection:
    """Pretends to be an Earth Engine search that finds the given picture IDs."""
    def __init__(self, ids):
        self.ids = ids

    def __getattr__(self, name):            # filterBounds, filterDate, filter -> same object
        return lambda *a, **k: self

    def aggregate_array(self, _):
        return type("List", (), {"getInfo": lambda _self: self.ids})()


class FakeEE:
    def __init__(self, ids):
        self.ImageCollection = lambda _name: FakeCollection(ids)
        self.Filter = type("Filter", (), {"eq": staticmethod(lambda *a: None),
                                          "listContains": staticmethod(lambda *a: None)})


class GridTests(unittest.TestCase):
    def test_grid_corners_land_on_whole_pixels(self):
        g = pp.snap_grid(561553.7, 710967.2, 500, 10)
        self.assertEqual((g["x0"] % 10, g["y0"] % 10), (0, 0))
        self.assertEqual((g["width"], g["height"]), (100, 100))

    def test_same_centre_gives_identical_grid(self):
        # Two pictures of the same case must line up pixel for pixel.
        self.assertEqual(pp.snap_grid(561553.7, 710967.2, 500, 10),
                         pp.snap_grid(561553.7, 710967.2, 500, 10))

    def test_grid_covers_the_requested_square(self):
        g = pp.snap_grid(561553.7, 710967.2, 500, 10)
        self.assertLessEqual(g["x0"], 561553.7 - 500)
        self.assertGreaterEqual(g["y0"], 710967.2 + 500 - 10)


class CardTests(unittest.TestCase):
    def check_rejected(self, card):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "card.json"
            path.write_text(json.dumps(card), encoding="utf-8")
            with self.assertRaises(ValueError):
                pp.load_card(path)

    def test_real_card_loads(self):
        self.assertEqual(pp.load_card(ROOT / "configs/case.json")["case_id"], CARD["case_id"])

    def test_missing_section_rejected(self):
        card = copy.deepcopy(CARD)
        del card["satellite"]
        self.check_rejected(card)

    def test_dates_in_wrong_order_rejected(self):
        card = copy.deepcopy(CARD)
        card["dates"]["event"] = {"start": "2026-07-01", "end": "2026-06-30"}
        self.check_rejected(card)

    def test_zero_pixel_size_rejected(self):
        card = copy.deepcopy(CARD)
        card["output"]["pixel_size_m"] = 0
        self.check_rejected(card)


class SearchTests(unittest.TestCase):
    def test_empty_search_stops_loudly(self):
        # The 'magenta May' lesson: zero pictures must stop the run, not draw a broken map.
        with self.assertRaises(pp.EmptySearchError):
            pp.find_images(FakeEE([]), CARD, None, CARD["dates"]["event"])

    def test_found_pictures_are_returned(self):
        _, ids = pp.find_images(FakeEE(["S1D_x"]), CARD, None, CARD["dates"]["event"])
        self.assertEqual(ids, ["S1D_x"])


    def test_window_can_choose_a_twin_satellite(self):
        # Risk: the dry-season reference silently searches the wrong satellite.
        calls = []
        fake = FakeEE(["S1A_x"])
        fake.Filter = type("Filter", (), {"eq": staticmethod(lambda *a: calls.append(a)),
                                          "listContains": staticmethod(lambda *a: None)})
        window = {**CARD["dates"]["reference"], "platform_number": "A"}
        pp.find_images(fake, CARD, None, window)
        self.assertIn(("platform_number", "A"), calls)
        calls.clear()
        pp.find_images(fake, CARD, None, CARD["dates"]["event"])
        self.assertIn(("platform_number", CARD["satellite"]["platform_number"]), calls)



class FailureMessageTests(unittest.TestCase):
    def test_impossible_date_is_caught_offline(self):
        # The 2026-11-07 mistake: '2026-06-31' only failed after reaching Earth Engine.
        card = copy.deepcopy(CARD)
        card["dates"]["event"]["end"] = "2026-06-31"
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "card.json"
            path.write_text(json.dumps(card), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not a real calendar date"):
                pp.load_card(path)

    def test_earth_engine_refusal_gives_a_plain_stop(self):
        EEException = type("EEException", (Exception,), {})
        original = pp.run
        pp.run = lambda *a, **k: (_ for _ in ()).throw(EEException("Quota exceeded"))
        try:
            self.assertEqual(pp.main(["--config", str(ROOT / "configs/case.json")]), 1)
        finally:
            pp.run = original


if __name__ == "__main__":
    unittest.main()
