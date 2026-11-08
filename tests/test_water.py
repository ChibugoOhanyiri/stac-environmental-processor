"""Offline tests for src/water.py with small SYNTHETIC arrays (made up for testing, not real data).

Each test checks a real risk: averaging in dB instead of linear power, nodata leaking into
averages or turning into numbers, and a smoothing step that changes an unchanged surface.
Run: .venv/bin/python -m unittest discover -s tests -v
"""
import importlib.util
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("water", ROOT / "src/water.py")
water = importlib.util.module_from_spec(spec)
spec.loader.exec_module(water)
ND = -9999.0


class SmoothTests(unittest.TestCase):
    def test_flat_surface_is_unchanged(self):
        db = np.full((7, 7), -12.0)
        np.testing.assert_allclose(water.smooth_db(db, 5, ND), -12.0, atol=1e-5)

    def test_average_is_in_linear_power_not_db(self):
        # Left column 0 dB, right column -10 dB; a 3x3 window over a 2-column picture sees both equally.
        db = np.array([[0.0, -10.0]] * 3)
        expected = 10 * np.log10((1.0 + 0.1) / 2)                    # -2.596 dB, not -5 dB
        self.assertAlmostEqual(float(water.smooth_db(db, 3, ND)[1, 0]), expected, places=4)

    def test_nodata_stays_nodata_and_does_not_leak(self):
        db = np.full((5, 5), -10.0)
        db[2, 2] = ND
        out = water.smooth_db(db, 3, ND)
        self.assertEqual(out[2, 2], ND)                               # unobserved stays unobserved
        np.testing.assert_allclose(out[out != ND], -10.0, atol=1e-5)  # neighbours not pulled toward -9999

    def test_mostly_unobserved_window_becomes_nodata(self):
        db = np.full((3, 3), ND)
        db[1, 1] = -10.0                                             # 1 of 9 observed (< 50%)
        self.assertEqual(water.smooth_db(db, 3, ND)[1, 1], ND)

    def test_even_window_rejected(self):
        with self.assertRaises(ValueError):
            water.smooth_db(np.zeros((3, 3)), 4, ND)



class SplitTests(unittest.TestCase):
    def test_practice_and_test_never_touch(self):
        areas = water.split_areas((10, 100), gap_px=25)
        practice_cols = np.where((areas == water.PRACTICE).any(axis=0))[0]
        test_cols = np.where((areas == water.TEST).any(axis=0))[0]
        self.assertGreaterEqual(test_cols.min() - practice_cols.max() - 1, 25)   # gap is really there

    def test_gap_wider_than_smoothing_window_reach(self):
        # A 5x5 window reaches 2 pixels sideways; with a 25 px gap no window sees both sides.
        areas = water.split_areas((5, 500), gap_px=25)
        for col in range(500):
            window = areas[:, max(0, col - 2):col + 3]
            self.assertFalse((window == water.PRACTICE).any() and (window == water.TEST).any())

    def test_halves_are_equal_and_sides_can_swap(self):
        a = water.split_areas((4, 500), gap_px=26)
        self.assertEqual((a == water.PRACTICE).sum(), (a == water.TEST).sum())
        b = water.split_areas((4, 500), gap_px=26, practice_side="east")
        self.assertEqual(b[0, 0], water.TEST)

    def test_bad_settings_rejected(self):
        with self.assertRaises(ValueError):
            water.split_areas((4, 10), gap_px=10)
        with self.assertRaises(ValueError):
            water.split_areas((4, 10), gap_px=2, practice_side="north")



class ClassifyTests(unittest.TestCase):
    ARGS = dict(nodata=ND, change_db=3.5, water_db=-17.0)

    def run1(self, ev, rf, occ):
        return int(water.classify(np.array([[ev]]), np.array([[rf]]), np.array([[occ]]), **self.ARGS)[0, 0])

    def test_unchanged_land_is_no_change(self):
        self.assertEqual(self.run1(-8.0, -8.0, 0), water.NO_CHANGE)

    def test_unobserved_is_never_no_change(self):
        for ev, rf, occ in ((ND, -8.0, 0), (-8.0, ND, 0), (-8.0, -8.0, ND)):
            self.assertEqual(self.run1(ev, rf, occ), water.NOT_OBSERVED)

    def test_always_water_wins_even_if_it_changed(self):
        self.assertEqual(self.run1(-5.0, -15.0, 90), water.PERSISTENT_WATER)   # wind-roughened lagoon

    def test_new_dark_water(self):
        self.assertEqual(self.run1(-20.0, -8.0, 0), water.NEW_DARK_WATER)

    def test_dark_on_both_days_is_not_new(self):
        self.assertEqual(self.run1(-20.0, -19.0, 0), water.NO_CHANGE)          # e.g. bare sand

    def test_land_louder(self):
        self.assertEqual(self.run1(-3.0, -8.0, 0), water.LAND_LOUDER)

    def test_small_change_is_no_change(self):
        self.assertEqual(self.run1(-6.0, -8.0, 0), water.NO_CHANGE)            # 2 dB < 3.5 dB

    def test_sometimes_water_change_is_cant_tell(self):
        self.assertEqual(self.run1(-3.0, -8.0, 20), water.CANT_TELL)

    def test_quieter_land_not_dark_is_cant_tell(self):
        self.assertEqual(self.run1(-12.0, -6.0, 0), water.CANT_TELL)

    def test_every_pixel_gets_exactly_one_label(self):
        rng = np.random.default_rng(0)
        ev, rf = rng.uniform(-25, 5, (50, 50)), rng.uniform(-25, 5, (50, 50))
        occ = rng.choice([0, 20, 90], (50, 50)).astype(float)
        ev[0, :5] = ND
        out = water.classify(ev, rf, occ, **self.ARGS)
        self.assertTrue(set(np.unique(out)) <= set(water.LABEL_NAMES))
        self.assertEqual(sum((out == k).sum() for k in water.LABEL_NAMES), out.size)


if __name__ == "__main__":
    unittest.main()
