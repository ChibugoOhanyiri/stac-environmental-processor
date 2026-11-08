# M3: do the same spots repeat, and is August the odd one out? (2026-11-07)

Rules unchanged (S26: 5×5 smoothing, 3.5 dB, −17 dB, JRC > 50%). Area: 5 km Lekki square, land = JRC occurrence 0. Scripts: `scripts/persistence_check.py`, `scripts/rainfall.py`. Receipts in evidence/runs/.

## 1. Persistence: the next pass, 12 Jul 2026 (the user's idea)
Card: configs/after_2026-07-12.json (S1D 12 Jul vs the same August median). Rain (IMERG): **83.6 mm in the 48 h before the pass, 187.9 mm in 7 days**: wetter than flood day, so this is "the next big rain", not "after it dried".

| Area | 30 Jun red pixels | Red again on 12 Jul | Chance level (any land red on 12 Jul) |
|---|---|---|---|
| Practice (west) | 8,916 | 65.7% | 10.4% (×6.3) |
| Test (east) | 11,179 | 42.6% | 9.2% (×4.6) |
Same check against the control days (test side): red again on 10 Sep 2.3%, on 22 Sep 1.8%.
Picture: fig16 (dark red = red on both 30 Jun and 12 Jul).

**Reading:** the same spots light up again in the next heavy rain and almost never on normal days. Consistent with recurring flooding at flood-prone places (news: rain again 3 Jul, drains full for hours). Not proof: a lasting surface change between July and August would also repeat; test 2 addresses that.

## 2. Is August the odd one out? Dry-season reference (January 2026)
S1D has no lane-95 passes before 6 Jun 2026, so the dry-season reference is its twin **Sentinel-1A** (median of 6, 18, 30 Jan 2026; IMERG ≤ 0.1 mm in the 48 h before each; 11 Feb excluded, 108 mm). Design: flood day (S1D) and the dry control 22 Sep (S1D) are both compared with the same S1A reference, so any twin-satellite offset (S12) affects both equally. Cards: configs/dryseason_ref_*.json; preprocess now allows a per-window platform (tested).

| Comparison (land) | Practice: louder | Test: louder |
|---|---|---|
| **30 Jun flood vs January (S1A)** | **14.2%** | **17.2%** |
| 22 Sep dry vs January (S1A) | 3.2% | 2.4% |
| 30 Jun flood vs August (S1D, earlier result) | 9.2% | 9.8% |
Overlap: **81% (test) and 85% (practice)** of the flood-vs-August red pixels are also red against the January reference.

**Reading:** the flood-day brightening appears whichever "normal" period is used (August after, January before), and is about 7× the dry control against the same January reference. So it is not an artefact of choosing August. The dry control's 2–3% vs January (vs ~0.8% vs August) is the combined effect of season, twin-satellite difference and grain; it applies equally to the flood comparison.

## Limits
One persistence date, and it was itself very wet; twin-satellite use only in the cancelling design (S12 not resolved for absolute values); the January reference is 5–6 months before, so real changes since then (construction) add to both runs; no located ground truth yet.
