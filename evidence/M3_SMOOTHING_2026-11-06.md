# M3 smoothing check (2026-11-06)

**Code:** src/water.py `smooth_db` (boxcar average in linear power; nodata excluded and preserved; tests in tests/test_water.py with synthetic arrays). **Command:** `.venv/bin/python scripts/smoothing_check.py`. **Data:** 5 km Lekki square, land that JRC says is never water (occurrence 0, 88.3% of pixels); same August reference median for all three rows.

## Measured: share of land pixels changed by more than 3 dB (flood/control date minus August)
| Window | 30 Jun flood: louder / quieter | 10 Sep wet: louder / quieter | 22 Sep dry: louder / quieter |
|---|---|---|---|
| 1×1 (none) | 20.8% / 3.2% | 7.5% / 4.9% | 6.6% / 7.3% |
| 3×3 (30 m) | 16.2% / 0.7% | 3.0% / 1.0% | 2.4% / 1.9% |
| **5×5 (50 m)** | **13.5% / 0.2%** | **1.5% / 0.2%** | **1.2% / 0.5%** |
| 7×7 (70 m) | 11.9% / 0.1% | 1.0% / 0.1% | 0.8% / 0.3% |
| 9×9 (90 m) | 10.8% / 0.1% | 0.8% / 0.1% | 0.6% / 0.2% |

## Reading
- Smoothing removes most grain: the dry control's "louder" share falls from 6.6% to 1.2% at 5×5, while the flood day keeps 13.5%. The flood-day / control contrast grows from about 3× to about 10×.
- Trade-off: bigger windows blur. A 50 m window is wider than many Lekki streets, so narrow flooded streets surrounded by dry plots can be averaged away, and the edge of any changed area becomes fuzzy by about 25 m.
- **Provisional choice: 5×5 (50 m)**, because it brings both controls to about 1–1.5% false "louder" with the smallest window that does so (7×7 gains only ~0.4 points). Chosen from the controls only; no flood reference was used, so it does not count as tuning on final checks (DATA_AND_VALIDATION.md). To be revisited in M4 sensitivity tests.
- The 3 dB line is still an example, not yet the method's threshold.
