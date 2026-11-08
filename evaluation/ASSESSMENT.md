# M4 scientific assessment (2026-11-07)

**Route: qualitative assessment with controls and sensitivity** (DATA_AND_VALIDATION.md: "with only qualitative evidence, publish qualitative assessment and sensitivity analysis; do not invent precision/recall").

## 1. Reference audit (what outside evidence exists)
| Reference | What it can support | What it cannot support |
|---|---|---|
| News reports, 29 Jun–12 Jul 2026 (evidence/EVENT_EVIDENCE_2026.md) | Flooding happened in Lekki/VI on 30 Jun, same morning as the pass; named districts and roads | Where the water edge was; depth; timing at 06:29 |
| The user's first-hand account (stay at Orchid, 27 Jun–2 Jul) | Persistent flooding around Orchid in that week | A map; independent verification (author's own account) |
| NASA GPM IMERG V07 rainfall | Heavy rain before the 30 Jun pass (48 mm/48 h); which dates are wet/dry | Street-level rain (≈10 km grid); flooding itself |
| JRC Global Surface Water 1.4 | Where water normally is (1984–2021) | Flood-day water; water bodies created after 2021 |
| OpenStreetMap place positions | Approximate positions of named places | Flood extent |
**Conclusion:** no reference gives a flood boundary at the time of the pass. Therefore **no precision, recall, F1 or IoU is reported**, and none should be quoted.

## 2. What was tested instead
| Test | Result | Evidence |
|---|---|---|
| Controls (equally rainy 10 Sep, dry 22 Sep) | Flood day ≈10% land louder vs <1% | M3_CONTROL_TEST, M3_LABELS |
| Unseen test area (rules fixed on the west half) | 9.4% vs 0.73–0.79% | M3_LABELS |
| Persistence (next heavy rain, 12 Jul) | 43% of test-side red repeats (chance 9%) | M3_PERSISTENCE_AND_REFERENCE |
| Different "normal" (January, twin S1A) | 17.2% vs 2.4%; 81% overlap with August result | M3_PERSISTENCE_AND_REFERENCE |
| Named places (OSM, 250 m) | All 5 higher than controls; 2 of 5 above area average | M3_SUMMARY, m3_point_checks_5km.csv |
| **Sensitivity (this milestone)**: windows 3/5/7 px × change 3.0/3.5/4.0 dB, test side | Flood/control ratio **6×–15×** in all 9 combinations; flood-day land louder **5.3%–17.4%** | evidence/m4_sensitivity_5km.csv (scripts/sensitivity.py) |

## 3. The defensible claim
> On 30 June 2026 at 06:29 (Sentinel-1D), about 10% (range 5–17% depending on reasonable rule choices) of land in a 5 km area of central Lekki showed radar brightening, 6–15 times the rate on an equally rainy day and a dry day processed the same way. The pattern held on an unseen half of the area, repeated in the next heavy rain and held against a dry-season baseline. This is **measured surface change consistent with the reported urban flooding** (PRD level 2). It is **not** a validated flood-extent map, and it does not identify individual flooded streets.

## 4. Uncertainty statement
- **Robust:** that a strong, unusual brightening occurred on flood morning (all 9 rule combinations, two baselines, unseen area).
- **Uncertain:** how much area (factor ~3 across rule choices) and exactly where (point checks weak).
- **Unknown:** depth, duration within the day, water under dense trees or in narrow streets erased by smoothing.

## 5. Failure cases (kept, not hidden)
1. **Dark-water rule nearly useless here:** −17 dB catches only 33% of known water (wind on the lagoon); new dark water ≈0%.
2. **Lagoon is noisy on dry days** (17.5% louder on the dry control): handled by the always-water label.
3. **Dark sand strip** at the south edge: dark on all dates, not JRC water; correctly "no change", but shows dark ≠ water.
4. **Agungi** (named in news): only 2.6% red within 250 m, below the area average.
5. **Location ambiguity:** the M1 "Orchid" point is 1.5 km from OSM's Orchid Road midpoint.
6. **Unexplained compact red block** (practice side, fig11/fig15): possibly construction; not interpreted.

## 6. Who did what
Method design, code, runs and write-up: Claude (AI), in sessions with the user. Decisions to widen the area (S22), grow in steps (S23), go ahead with the split and labels, and the persistence idea: the user. The user's first-hand flood account: the user.
