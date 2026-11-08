# M3 first look at the values (2026-11-04)

**What:** before choosing any water rule, count dark and changed pixels in the M2 outputs (1 km square, Orchid Road, Lekki; 100 × 100 pixels of 10 m; flood day = S1D 30 Jun 2026 single pass; reference = median of S1D 5, 17, 29 Aug 2026).
**Command:** `.venv/bin/python scripts/value_summary.py` (reads outputs/aligned/, run 5 files; nodata excluded; all 10,000 pixels valid).

## Measured (verified output)
| | Flood day | August | Both |
|---|---|---|---|
| VV below −18 dB | 2 px | 21 px | 0 |
| VV below −20 dB | 0 px | 2 px | 0 |
| VH below −25 dB | 22 px | 7 px | 0 |
| VV median | −5.4 dB | −6.9 dB | |

VV change: 2,220 px (22%) louder by more than 3 dB; 275 px (3%) quieter by more than 3 dB; median +1.16 dB.
VH change: 1,303 px louder by more than 3 dB; 586 px quieter; median +0.50 dB.

## What it means (interpretation, not a validated result)
- The classic "calm open water is dark" rule finds almost nothing here: 2 of 10,000 flood-day pixels are below −18 dB VV, fewer than in August. The thresholds above are common examples for looking, not tuned values.
- The square mostly got louder on flood day. That is consistent with M1 (evidence/FEASIBILITY_RESULT.md) and with water in streets reflecting off walls (double bounce), but also with wet roofs/soil, rain-roughened surfaces or other changes. It is not proof of flooding.
- Caution on single pixels: the flood day is one pass, the reference a median of three, so radar grain (speckle) alone makes many ±3 dB single-pixel differences. Any pixel rule needs smoothing or neighbourhood counts, and a noise check on two dry dates.
- A 1 km square that is almost all built-up cannot give separate development and assessment areas (DATA_AND_VALIDATION.md). This is a scope question for the user (see HANDOFF.md).

## 5 km square (S22, run 20261104T114705Z, same 4 images)
Command: `.venv/bin/python scripts/value_summary.py lagos-lekki-5km-2026-06-30` (250,000 valid pixels, 0 nodata). Picture: docs/figures/fig11_m3_5km_quicklook.png.

| VV | Flood day | August | Both |
|---|---|---|---|
| below −18 dB | 8,979 px | 9,150 px | 6,235 |
| below −20 dB | 4,060 px | 2,939 px | 984 |
| median | −6.2 dB | −7.5 dB | |

VV change: 51,082 px (20%) louder by >3 dB; 9,374 px (4%) quieter; median +0.99 dB. VH: 32,415 louder, 19,223 quieter, median +0.41 dB.

**Reading (not validated):** the bigger square now contains real dark surfaces (lagoon edge, channel, ponds) that are dark on both dates, i.e. persistent, so the dark-water rule has something to work on here. The flood-day vs August "below −18 dB" counts are about equal, so there is no large new dark area. The general brightening seen in 1 km repeats across the whole 5 km. The low overlap at −20 dB (984 of ~3–4 thousand) shows how much the single-pass flood picture's speckle moves pixels across a fixed line; smoothing is needed before classifying.
