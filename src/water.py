"""M3: turn the aligned radar pictures into honest per-pixel labels (built step by step).

Step 1 (this version): smooth out radar grain (speckle).
Analogy: one person shouting in a noisy room is hard to hear; ask the 25 people around them and
take the average, and the real message comes through. Each pixel is replaced by the average of its
neighbourhood (a "boxcar" window, e.g. 5 x 5 pixels = 50 m x 50 m at 10 m).

Two rules that matter (DATA_AND_VALIDATION.md):
- Average in LINEAR power, never in dB. dB is a log scale: the average of 0 dB and -10 dB is
  -2.6 dB (power 1.0 and 0.1 -> 0.55), not -5 dB. Averaging dB numbers would bias dark pixels.
- Nodata (unobserved) pixels never enter an average and stay nodata. A pixel whose window has too
  few observed neighbours becomes nodata too, rather than a guess.
"""
from __future__ import annotations

import numpy as np


def db_to_linear(db: np.ndarray) -> np.ndarray:
    return np.power(10.0, db / 10.0)


def linear_to_db(power: np.ndarray) -> np.ndarray:
    return 10.0 * np.log10(power)


def _window_sum(a: np.ndarray, size: int) -> np.ndarray:
    """Sum over a size x size window centred on each pixel (zeros outside the picture)."""
    r = size // 2
    padded = np.pad(a, r, mode="constant")
    c = np.cumsum(np.cumsum(padded, axis=0), axis=1)        # running totals ("integral image")
    c = np.pad(c, ((1, 0), (1, 0)), mode="constant")
    h, w = a.shape
    return (c[size:size + h, size:size + w] - c[:h, size:size + w]
            - c[size:size + h, :w] + c[:h, :w])


def smooth_db(db: np.ndarray, size: int, nodata: float, min_valid_fraction: float = 0.5) -> np.ndarray:
    """Average each pixel with its neighbours in linear power; return dB with nodata preserved.

    size: odd window width in pixels (5 -> 5 x 5). min_valid_fraction: share of the window that must
    be observed, else the result is nodata. Edge pixels use only the part of the window inside the picture.
    """
    if size < 1 or size % 2 == 0:
        raise ValueError("size must be an odd number of pixels (1, 3, 5, ...).")
    db = np.asarray(db, dtype="float64")
    valid = db != nodata
    power = np.where(valid, db_to_linear(np.where(valid, db, 0.0)), 0.0)
    total = _window_sum(power, size)
    count = _window_sum(valid.astype("float64"), size)
    inside = _window_sum(np.ones_like(power), size)             # window cells inside the picture
    ok = valid & (count > 0) & (count >= min_valid_fraction * inside)
    out = np.full(db.shape, nodata, dtype="float64")
    out[ok] = linear_to_db(total[ok] / count[ok])
    return out.astype("float32")


# ---------------------------------------------------------------------------
# Step 2: split the square into a practice area and a test area
# ---------------------------------------------------------------------------
# Analogy: practice questions vs the real exam. Rules are tuned on the practice side only and then
# checked once on the test side. A gap between them stops smoothing windows from mixing the two.
PRACTICE, TEST, GAP = 1, 2, 0


def split_areas(shape: tuple[int, int], gap_px: int, practice_side: str = "west") -> np.ndarray:
    """Return an array of the same shape: 1 = practice, 2 = test, 0 = gap (used by neither).

    The split is a vertical line through the middle; the gap is gap_px wide and centred on it.
    """
    if practice_side not in ("west", "east"):
        raise ValueError("practice_side must be 'west' or 'east'.")
    height, width = shape
    if gap_px < 0 or gap_px >= width:
        raise ValueError("gap_px must be between 0 and the picture width.")
    left_end = (width - gap_px) // 2                 # columns [0, left_end) are the west side
    right_start = left_end + gap_px                  # columns [right_start, width) are the east side
    areas = np.full(shape, GAP, dtype="uint8")
    west, east = (PRACTICE, TEST) if practice_side == "west" else (TEST, PRACTICE)
    areas[:, :left_end] = west
    areas[:, right_start:] = east
    return areas


# ---------------------------------------------------------------------------
# Step 3: put every pixel in one basket (label)
# ---------------------------------------------------------------------------
# Analogy: sorting laundry. Every pixel goes into exactly one basket, and "not seen" is its own
# basket, never mixed into "no change" (PRD F4: nodata never becomes dry land).
NO_CHANGE, PERSISTENT_WATER, NEW_DARK_WATER, LAND_LOUDER, CANT_TELL, NOT_OBSERVED = 0, 1, 2, 3, 4, 255
LABEL_NAMES = {NO_CHANGE: "no change", PERSISTENT_WATER: "always water", NEW_DARK_WATER: "new dark water",
               LAND_LOUDER: "land got louder", CANT_TELL: "can't tell", NOT_OBSERVED: "not observed"}


def classify(event_db, reference_db, occurrence, nodata: float, change_db: float, water_db: float,
             persistent_pct: float = 50.0) -> np.ndarray:
    """Label each pixel from SMOOTHED event/reference dB and JRC water occurrence (0-100 %).

    Order matters (first match wins):
      not observed  - either picture is nodata, or occurrence is nodata
      always water  - JRC says water in more than persistent_pct % of months (changes there are wind noise)
      new dark water - darker than water_db on the event, not on the reference, and quieter by > change_db
      land got louder - never-water land (occurrence 0) louder by > change_db (consistent with urban flooding)
      can't tell    - sometimes-water ground (0 < occurrence <= persistent_pct) changed by > change_db either way,
                      or never-water land that got quieter by > change_db without turning dark
      no change     - everything else
    """
    ev, rf, occ = (np.asarray(a, dtype="float64") for a in (event_db, reference_db, occurrence))
    seen = (ev != nodata) & (rf != nodata) & (occ != nodata)
    diff = np.where(seen, ev - rf, 0.0)
    labels = np.full(ev.shape, NO_CHANGE, dtype="uint8")
    always = seen & (occ > persistent_pct)
    dark_new = seen & ~always & (ev < water_db) & (rf >= water_db) & (diff < -change_db)
    land = occ == 0
    louder = seen & ~always & ~dark_new & land & (diff > change_db)
    unclear = seen & ~always & ~dark_new & ~louder & (np.abs(diff) > change_db)
    labels[unclear] = CANT_TELL
    labels[louder] = LAND_LOUDER
    labels[dark_new] = NEW_DARK_WATER
    labels[always] = PERSISTENT_WATER
    labels[~seen] = NOT_OBSERVED
    return labels
