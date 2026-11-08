# M3 control test: is the flood-day "louder" signal more than rain and radar grain? (2026-11-04)

**Question:** on 30 Jun 2026, 20% of the 5 km Lekki square was louder (VV) by more than 3 dB than the August median. Would an ordinary wet day, or an ordinary dry day, show the same?

**Method:** same 5 km square, same satellite lane (S1D, descending 95), same August reference median (5, 17, 29 Aug), same code. Only the single "event" date changes. Cards: configs/control_wet_2026-09-10.json, configs/control_dry_2026-09-22.json. Receipts in evidence/runs/. Counts: `scripts/value_summary.py <case_id>`. Rain: `scripts/rainfall.py configs/case_lekki5km.json <dates>` (NASA GPM IMERG V07, mean over the square, 48 h and 7 days before 05:29 UTC).

## Rain before each pass (IMERG, measured)
| Date | 48 h before | 7 days before | Role |
|---|---|---|---|
| 30 Jun | 48.2 mm | 79.2 mm | flood day |
| 5 Aug | 0.4 | 9.6 | reference |
| 17 Aug | 0.2 | 0.9 | reference |
| 29 Aug | 12.1 | 42.9 | reference (not fully dry) |
| 10 Sep | 49.4 | 62.6 | wet control |
| 22 Sep | 2.7 | 8.2 | dry control |
| 4 Oct | 0.6 | 11.5 | not used |

## Result (VV, 250,000 pixels each, measured)
| Event date | Louder by >3 dB | Quieter by >3 dB | Median change | Below −18 dB on that date |
|---|---|---|---|---|
| **30 Jun (flood day)** | **51,082 (20.4%)** | 9,374 (3.7%) | **+0.99 dB** | 8,979 |
| 10 Sep (wet control) | 19,501 (7.8%) | 13,865 (5.5%) | +0.22 dB | 10,510 |
| 22 Sep (dry control) | 18,194 (7.3%) | 18,149 (7.3%) | +0.02 dB | 7,264 |
August reference: 9,150 below −18 dB. Pictures: fig11 (flood day), fig12 (wet control), fig13 (dry control).

## Reading
- **Grain alone** (dry control) moves about 7% of pixels louder and 7% quieter by >3 dB, evenly balanced. That is the "nothing happened" level for a single picture against a 3-picture median.
- **Rain alone** (wet control, same 48 h rain as flood day) adds little: 7.8% louder, median +0.22 dB.
- **Flood day** is 2.6 times the controls for "louder", lopsided (louder far more than quieter) and clustered (fig11 vs fig12). Something beyond normal grain and a comparable rain total changed the surface on 30 Jun.
- This is **consistent with** urban flooding (double bounce, PRD claim level 2). It is **not proof** and not a flood map.

## Limits (stated, not hidden)
- One wet control only. We do not know whether 10 Sep had flooding (none searched for yet); if it did, the contrast would be understated, not overstated.
- IMERG is a ~10 km satellite estimate; Lagos rain varies street by street. News says rain on 30 Jun continued until ~14:00, after the 06:29 pass, so the pass saw the flood mid-event.
- Season differs (June vs September vegetation, soil moisture before the 48 h window: 7-day totals 79 vs 63 mm).
- The IMERG run type (early/late/final) for 2026 dates was not checked; values may be revised.

## Split by JRC permanent water (added 2026-11-04, run 20261104T124806Z)
JRC Global Surface Water 1.4 `occurrence` was added to the 5 km card as a context layer (same grid; event/reference files byte-identical to the earlier run). Always-water = occurrence > 50% (9,019 px, 3.6%); never-water = occurrence 0 (88.3%).

| Event date | Always-water: louder >3 dB | Always-water: quieter | Never-water: louder >3 dB | Never-water median change |
|---|---|---|---|---|
| 30 Jun (flood) | 20.9% | 8.5% | **20.8%** | **+1.02 dB** |
| 10 Sep (wet) | 13.7% | 11.4% | 7.5% | +0.24 dB |
| 22 Sep (dry) | 17.5% | 6.4% | 6.6% | −0.01 dB |

**Reading:** open water is jumpy on every date (17.5% "louder" even on the dry control), most likely because wind roughens the surface; so change on permanent water says little. The flood-day contrast lives on **land that is never water** (20.8% vs 6.6–7.5% on controls), which is where street flooding would be. Practical rule for M3: treat JRC always-water as its own class and do not count its changes as flood evidence. Median VV over always-water is only about −15 dB in August (not the −20 dB textbook value), probably because of wind and 30 m JRC edges sampled onto 10 m; so a fixed −18/−20 dB water threshold would miss part of the lagoon here.
