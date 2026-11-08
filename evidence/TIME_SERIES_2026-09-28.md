# Time series — Sentinel-1D VV at three Lekki spots, Jun–Sep 2026

Run by the user on 2026-09-28 with gee/06_time_series.js (GEE Code Editor). Exact values from the GEE chart CSV (downloaded by the user, saved as `evidence/time_series_2026-09-28.csv`, 2 decimals shown). Chart image: docs/figures/fig07_time_series_chart.png.

Method: mean of VV dB values in a circle (Orchid and Chevron: 50 m radius; pond: 30 m) for every S1D descending lane-95 pass. This is a viewing simplification: the averaging was done in dB, not linear power.

| Pass | Orchid Road | Chevron Drive | Twin Lakes pond (control) |
|---|---|---|---|
| Jun 6, 2026 | -4.85 | -8.98 | -19.97 |
| Jun 18, 2026 | -5.54 | -8.07 | -21.08 |
| Jun 30, 2026 | -5.28 | -8.86 | -20.82 |
| Jul 12, 2026 | -4.50 | -8.15 | -20.38 |
| Jul 24, 2026 | -6.13 | -9.44 | -22.30 |
| Aug 5, 2026 | -8.12 | -9.56 | -19.25 |
| Aug 17, 2026 | -7.62 | -10.37 | -21.11 |
| Aug 29, 2026 | -7.47 | -9.82 | -18.76 |
| Sep 10, 2026 | -7.37 | -10.05 | -20.95 |
| Sep 22, 2026 | -7.60 | -11.15 | -21.18 |

Orchid mean: 6 Jun–12 Jul = −5.04 dB (4 passes); 5 Aug–22 Sep = −7.64 dB (5 passes); difference ≈ 2.6 dB.

## What it shows (provisional)
1. **The control works.** The pond stays very dark (about −19 to −22 dB) on every pass. That is water, as expected, so the method behaves sensibly.
2. **Orchid Road had two "states".** Brighter (about −5 dB) from **6 Jun to 12 Jul**, then a drop over late July to about −7.5 dB from **5 Aug onwards**. This step of about 2.5 dB is much larger than the pass-to-pass wobble within each state.
3. **30 June is not special.** It looks like the rest of the June–mid-July period. That is consistent with the user's first-hand account (flooding already large on 27 Jun, still present on 2 Jul) and the friend's report (from early June).
4. **Orchid got BRIGHTER in the wet period, not darker.** Candidate explanations (not yet distinguishable):
   - **double bounce**: water on the ground next to walls sends the echo back strongly;
   - **wet surfaces/soil**: wet material reflects radar more strongly, even without standing water;
   - other seasonal or construction changes.
5. **Chevron Drive** shows a weaker, gradual decline (about −8.5 to −10.5 dB). The pattern is less clear.
6. **Correction:** S1D *did* fly lane 95 over Lekki on **6 Jun 2026**. The earlier note "first S1D lane-95 pass = 18 Jun" came from a CDSE query starting 10 Jun and was wrong. May still had none (gee/04 v1).

## Detective test: open plot near Orchid (gee/06 v3; chart = docs/figures/fig08)
Open plot (empty lot, ~75 × 40 m; circle 15 m radius at 3.5549, 6.4319, confirmed inside the plot by the user, fig09). Exact values from the chart CSV (downloaded by the user, saved as `evidence/time_series_open_plot_2026-09-28.csv`; it also repeats the other three spots, identical to the first CSV):

| Jun 6 | Jun 18 | Jun 30 | Jul 12 | Jul 24 | Aug 5 | Aug 17 | Aug 29 | Sep 10 | Sep 22 |
|---|---|---|---|---|---|---|---|---|---|
| -3.25 | -5.66 | -3.33 | -5.52 | -6.92 | -9.19 | -9.35 | -6.73 | -8.74 | -8.59 |

- Mean 6 Jun–12 Jul = -4.44 dB (4 passes); mean 5 Aug–22 Sep = -8.52 dB (5 passes). The open plot was about **4.1 dB LOUDER** in the flood weeks, the same direction as Orchid (built-up).
- **Pre-stated rule** (HANDOFF, before the result): open ground *darker* → flood water; *louder* like Orchid → general wetness. **Result: louder → points to wet ground rather than standing, calm water on this plot at 06:29 on the pass dates.**
- Caveats: one small plot (only ~7 pixels, so noisy: ±2 dB jumps between passes); grass or vegetation changes; shallow water roughened by rain/wind, or water with grass sticking out, can also look bright. So standing water is **not ruled out**, only not shown.
- **Implication for M1:** the radar clearly shows a *wet period* (Jun–mid-Jul) vs a *dry period* (Aug–Sep) at both built-up and open spots, matching the reported flood timing. But the classic "flood water = dark" signal does **not** appear at these Lekki spots. A simple dark-pixel flood map would miss this flood here.

## Not established
Whether Orchid's bright period is flood water, wet ground, or something else; any flood area; any accuracy. One spot per place: no spatial pattern yet.
