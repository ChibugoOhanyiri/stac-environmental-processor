# Earth Engine scripts — what each one asks and what we found

These are **JavaScript** scripts for the Google Earth Engine **Code Editor** (https://code.earthengine.google.com). To run one: open the Code Editor, paste the whole file into the middle box and press **Run**. They only **display** things: no thresholds, flood areas or exports. The Python pipeline comes in Milestone 2.

**Data used by all of them:** `COPERNICUS/S1_GRD`, Sentinel-1 radar, already calibrated and in dB. The main case is the Lagos flood of **30 June 2026**, Lekki.

**One rule to remember:** dB numbers are negative. *The farther from zero, the quieter the echo.* Quiet (−20) = dark = usually calm water. Loud (−5) = bright = buildings.

Each script exists because the one before it raised a new question. One question per run.

| # | Script | Question it answers | What we found | Figure / evidence |
|---|---|---|---|---|
| 01 | [01_first_look.js](01_first_look.js) | Does Earth Engine have the 30 June Sentinel-1D picture, and what does it look like? | **Yes.** 5 descending pictures 15 Jun–15 Jul, including S1D 30 Jun 05:29 UTC. Lagoon black, buildings bright, "cloud-like" blobs on water = wind/rain (radar sees through cloud). | fig01, fig02; evidence/GEE_FIRST_LOOK_2026-09-28.md |
| 02 | [02_change_view.js](02_change_view.js) | Can we *see* the flood if the computer colours the differences between 18 Jun and 30 Jun? | **Not really.** Land mostly grey (no change); lagoon cyan (roughened). No coherent new-water patches. | fig03 |
| 03 | [03_dry_baseline.js](03_dry_baseline.js) | If 18 Jun was already flooded, does comparing with the **dry season** (Jan–Mar) help? | Written as an alternative; not the main route. It uses Sentinel-1A (twin satellite), and we chose Sentinel-1D only (S17). | — |
| 04 | [04_may_baseline.js](04_may_baseline.js) | The user's idea: compare 30 Jun with **May** (before the flood started)? | **v1 failed:** 0 Sentinel-1D pictures on our lane in May (the satellite was still moving into position), so the map turned magenta. A useful *failure example*. v2 uses Sentinel-1A. | fig04 (failure) |
| 05 | [05_after_baseline_s1d.js](05_after_baseline_s1d.js) | The user's idea: keep **Sentinel-1D only** and compare 30 Jun with **after** the flood (July, August)? | July looks similar to 30 Jun. August differs: more cyan (30 Jun *brighter*) over built-up land. Hard to judge by eye. | fig05, fig06 |
| 06 | [06_time_series.js](06_time_series.js) | Stop guessing dates: how does the echo change **over time** at specific spots? | Pond (control) always ≈ −20 dB ✅. **Orchid ≈ −5.0 dB in Jun–mid-Jul, then ≈ −7.6 dB from Aug**, i.e. louder during the flood weeks. 30 Jun is not special on its own. | fig07; evidence/TIME_SERIES_2026-09-28.md, time_series_2026-09-28.csv |
| 06 v3 | same file | **Detective test:** is Orchid's loud echo *flood water* (double bounce) or just *wet ground*? We added open ground (an empty plot the user found near Orchid). | **Louder** in Jun–mid-Jul (≈ −4.5 dB) than Aug–Sep (≈ −8.5 dB), like Orchid, so it points to **wet ground**, not calm standing water, at the pass times. Standing water is not ruled out. | fig08, fig09 |
| 07 | [07_export_sample.js](07_export_sample.js) | M1 output: can we get one small **real data file** out? A 1 km GeoTIFF around Orchid: VV + VH on 30 Jun, VV August median; dB; UTM 31N; 10 m. | ✅ Exported and verified: 100 × 100 px, EPSG:32631, 10 m, 3 bands, dB, no gaps. 30 Jun median about 1.5 dB louder than August. | evidence/SAMPLE_2026-09-28.md |

## Version notes
- **06 v2 → v3:** Claude mis-estimated the open plot's position and the circle landed on houses. v3 uses the user's own Inspector click (3.5549, 6.4319) with a 15 m radius, confirmed inside the plot by the user.
- Circle sizes: 50 m for Orchid/Chevron, 30 m for the pond, 15 m for the small plot. A circle must fit inside the thing it measures; Sentinel-1 pixels are 10 m, with true sharpness about 20 m.
- The averages are taken in dB, which is fine for viewing. The analysis version (M2+) will average in linear power first.

## Who did what
The user ran every script in their own Earth Engine account, made the observations, and chose the May idea, the Sentinel-1D-only rule, the after-flood reference and the open-plot location. Claude wrote the code and explanations. See LEARNING_LOG.md and DECISIONS.md (S11–S18).
