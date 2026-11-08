# GEE first look — 2026-09-28

Run by the user in the Google Earth Engine Code Editor using gee/01_first_look.js. Evidence: the user's screenshot of the Console and map, shared in the Claude session. This was a visual look only: nothing was measured or exported.

## Scenes returned (COPERNICUS/S1_GRD, IW, DESCENDING, intersecting the Lekki box 3.45,6.42,3.60,6.48, 2026-06-15 to 2026-07-15)
| # | GEE system:index | Matching CDSE STAC item (same datatake) |
|---|---|---|
| 0 | S1A_IW_GRDH_1SDV_20260623T052957_20260623T053026_065092_083464_A0C9 | S1A_…_065092_083464_8C89_COG |
| 1 | S1C_IW_GRDH_1SDV_20260706T052906_20260706T052928_008418_010A7A_7DCA | **Not returned** by the 2026-09-27 CDSE STAC query (see below) |
| 2 | S1D_IW_GRDH_1SDV_20260618T052918_20260618T052940_003286_005C0A_AFED | S1D_…_003286_005C0A_D21C_COG |
| 3 | S1D_IW_GRDH_1SDV_20260630T052917_20260630T052946_003461_0061CA_3AD2 | S1D_…_003461_0061CA_9070_COG |
| 4 | S1D_IW_GRDH_1SDV_20260712T052918_20260712T052947_003636_0067B4_02E5 | S1D_…_003636_0067B4_AE53_COG |

## Findings
1. **GEE carries Sentinel-1D.** The 30 Jun 2026 flood-day scene is available. This resolves DECISIONS S13 for the GEE route.
2. **Same acquisition, different file names.** The satellite, times, absolute orbit and datatake ID match between GEE and CDSE, but the last 4 characters differ (e.g. 3AD2 vs 9070). In Sentinel-1 naming, that last block is a product identifier, so the two services hold different *product files* of the same acquisition. CDSE's are "_COG" conversions. For lineage, record both, and match on satellite + start time + absolute orbit + datatake, not the full name.
3. **Discrepancy to investigate:** GEE has an S1C descending scene on 6 Jul 2026 05:29 UTC that the CDSE STAC query did not return. It is probably on the same track, consistent with the new 6-day S1C/S1D pattern, but its relative orbit is not yet checked. Possible causes: a missing COG item in CDSE, or a footprint difference. Not yet resolved.
4. **Visual impression (not a measurement):** the image on top was the 30 Jun VV layer. Lagos Lagoon appears mostly black (smooth water). The Atlantic appears dark grey with lighter blotches. Built-up Lekki and VI appear bright. Blotchy lighter areas on the lagoon and sea could be wind-roughened water or rain effects. Comparing with 18 Jun is still needed.

## User's visual comparison (18 Jun vs 30 Jun, by eye)
The user flipped layers and reported they "can't really tell" any difference on land, except a **grey coverage on 30 June** over the lagoon. Interpretation: lagoon surface roughened by wind/rain on the flood morning (brighter echo). This is a confounder: weather can make water look less like water. Next: pixel-by-pixel change view (gee/02_change_view.js), with a speckle filter for display only.

## Change-colour view (gee/02_change_view.js, layer A; the user's screenshot 2026-09-28)
- The user reported: red "close to the Atlantic, even the lagoon, and tiny on the road and even buildings/lands".
- Claude's reading of the screenshot (visual, not measured):
  - **Lagoon:** teal/cyan, i.e. brighter on 30 Jun. Consistent with wind/rain roughening.
  - **Sea strip near the beach:** dark with a reddish tint, i.e. darker on 30 Jun. The sea is water on both days, so this is a sea-surface change (wind/waves), not flooding.
  - **Land:** mostly grey (little change) with **scattered single red/cyan specks**. These look like residual speckle or small objects (vehicles, construction), not coherent patches.
  - **Two dark round ponds** near the Lekki Conservation Centre / Twin Lakes area: dark on both dates → grey-black = **persistent water**, a useful control.
- **Provisional finding:** no large, coherent "got darker" patches on land inside the Lekki box at 06:29 WAT on 30 Jun, in this display. Candidate explanations, all unverified: urban water hidden or brightened by buildings (double bounce); a pass before peak inundation (~11:00); a wet 18 Jun baseline; rain-roughened flood water; the 30 m smoothing hiding narrow streets. This is a feasibility finding, not a failure; see DECISIONS S16.

## May baseline attempt (gee/04_may_baseline.js v1)
The May 2026 filter for platform D on lane 95 returned **0 images** (Console: `May pictures used: []`), so the colour composite rendered as solid magenta (a missing band, not a result). Explanation: consistent with ESA's constellation transition, and CDSE lists the first S1D lane-95 pass over Lagos as 18 Jun 2026 (*corrected 2026-09-28: GEE shows an S1D lane-95 pass on 6 Jun; the CDSE query began 10 Jun. See TIME_SERIES_2026-09-28.md*). Lesson for the Python pipeline: fail clearly on empty searches (PRD F7). v2 uses all lane-95 May images (expected S1A).

## After-event S1D references (gee/05_after_baseline_s1d.js; the user's screenshots 2026-09-28)
- The user reported: July comparison (layer H) has more scattered red; August (layer G) has less red, but one stand-out red area in the **south-east**.
- Claude's reading (visual only):
  - **At the Orchid and Chevron markers:** no coherent red patch in either layer.
  - **Layer G (vs August):** noticeably more **cyan** across built-up land, i.e. 30 Jun **brighter** than August. Candidate explanations: double bounce from water between buildings on 30 Jun; wet surfaces from rain during the pass; seasonal or other differences in August. Not distinguishable by eye.
  - Water bodies (lagoon, Twin Lakes ponds) behave as expected (dark in both; lagoon cyan = roughened on 30 Jun).
- **Conclusion so far:** visual inspection has reached its limit. Next step: measure values over time at specific points (the Inspector tool + a time-series chart), including a permanent-water control and the user's south-east red area.

## Not established
No water classification, no areas, no change detection, no accuracy. Visual inspection only.
