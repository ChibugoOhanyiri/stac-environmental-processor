# Investigation A — event and imagery feasibility

> **Update 2026-09-27:** the primary case is now Lagos, 30 June 2026 (DECISIONS S11; evidence/EVENT_EVIDENCE_2026.md). The 2024 analysis below is kept as the original investigation and fallback.

Checked 2026-09-23. Verdict: **Lagos July 3, 2024 is a promising metadata-level candidate, not yet a validated flood case.** No authenticated raster processing or independent flood-extent validation has been completed. See evidence/SCENE_INVENTORY.md for actual catalogue records.

## Candidate comparison
| Candidate | Event evidence | Satellite evidence | Decision |
|---|---|---|---|
| Lagos, July 3, 2024 | Contemporary reporting documents widespread flooding and an official response [S1]. | Live CDSE query returned matching-orbit S1 scenes June 21, July 3 and July 15; S2 event tile almost entirely cloud-covered. | First feasibility experiment. |
| Lagos, 28-30 June 2026 | Updated 2026-09-27: Vanguard (30 Jun and 1 Jul 2026) reports rain beginning Sunday 28 June, more than 12 hours of heavy rain on Tuesday 30 June easing about 14:00, and the Ojota-Maryland bridge submerged by about 11:00 [S9, S10]. NiMet had issued a flash-flood alert for 30 June [S11]. The user personally experienced the 2026 flooding (their account is context, not ground truth). | Live query 2026-09-27: S1D descending orbit 95 on 18 Jun, **30 Jun 05:29 UTC** and 12 Jul, all the same satellite and track. S2 tile cloud is 89-100% around the event (23 Jun: 51.76%). See evidence/LIVE_2026_*_SUMMARY.json. | **Primary case from 2026-09-27 (S11).** Evidence table: evidence/EVENT_EVIDENCE_2026.md. Caveat: Lekki flooded before (28 Jun, and through June) and after (3 Jul), so baseline and after images need inspection. |
| Lokoja, late September 2022 | Copernicus documents flooding, with July baseline and late-September satellite illustrations [S2]. | Provider evidence establishes visible large-scale flooding; exact local scene search still needed. | Recommended fallback if Lagos fails; ask before changing the primary geography. |
| Port Harcourt | User-preferred second geography. | No exact event or acquisition suitability verified here. | Transfer experiment after first case; outside required v1. |

The discovery bounding box is [3.25, 6.40, 3.65, 6.70] in longitude/latitude. It is deliberately a search envelope, not an administrative boundary or an approved flood-extent AOI. Select a roughly 5 × 5 km analysis area only after intersecting event evidence, valid imagery and comparable observations. A 1 × 1 km chip is sufficient for the first raster smoke test.

## What the live search established
Search window: 2024-06-20 through 2024-07-15 UTC. Collections: sentinel-1-grd and sentinel-2-l2a. The two responses contain 4 and 5 items respectively, with no next-page link. Counts describe that request, not all possible overlapping products from every collection.

For Sentinel-1, use the descending relative-orbit-95 June 21 / July 3 / July 15 sequence as the candidate series. Do not use the ascending June 26 scene as an interchangeable baseline. The July 3 acquisition is approximately 06:30 WAT; establish rainfall/flood onset and persistence before interpreting it as an event observation. A June baseline may already contain seasonal water or earlier flooding.

Sentinel-2 event-day tile cloud metadata is 99.99%; neighbouring dates are also very cloudy. This is whole-tile metadata, not a measured clear-pixel percentage for our final AOI. Optical validation is unlikely to be straightforward, but inspect the actual AOI mask before rejecting every pixel.

## Event-timing evidence (added 2026-09-27, news-level only)
- THISDAY (S. Ehigiator, 2024-07-03) [S7]: heavy rainfall "began around 3 am on Wednesday" (≈02:00 UTC); listed flooded areas include Iyana-Oworo, Ketu-Alapere, Oshodi-Mafoluku, Iyana Ipaja, Egbeda-Akowonjo, Ogba, Okota, Ikate and the Lekki-Ajah axis. The Environment Commissioner expected flooding to last "about 1-2 hour" as tide levels fell.
- Secondary reporting quotes about nine to ten hours of rain from the early morning [S8]. Wikipedia's "2024 Lekki flood" page dates the event 4 July, while the sources it cites are dated 3 July. Treat Wikipedia as a pointer, not evidence.
- Interpretation (provisional): the 05:30 UTC / 06:30 WAT S1 pass falls about 3.5 h into ongoing rain. This is plausible timing for observing standing water, but it is not necessarily peak extent. Flooding was reported as short-lived and tide-modulated, and rain, wind and wet soil during the pass can change backscatter. No rain-gauge, tide-gauge or hourly observation has been obtained yet. Timing is **plausible, not verified**.
- AOI note: most named mainland locations and the Lekki-Ajah axis appear to fall inside the discovery bbox (approximate, from general geography, not yet digitised). Ibeju-Lekki lies east of the 3.65° E edge and is outside it.

## Why radar first
Radar can observe through cloud, but smooth water is not its only dark surface. Urban structures can obscure water or create bright double-bounce responses. Wind, wet soil, vegetation, incidence angle and tides alter backscatter. A simple dark-pixel threshold will not map every flooded street. Sentinel-1 IW GRD pixel spacing and effective spatial resolution are different; record both from the product documentation, rather than calling it a precise 10 m street map [S3].

For optical imagery, green/NIR water indices can support interpretation where clear, but clouds, shadows and turbid water complicate results. Resampling a coarser band onto a finer grid creates no new ground detail.

## Sample-job feasibility and next decision
Completed: unauthenticated live catalogue requests, saved full metadata, identified candidate orbit-compatible observations.
Not completed: authenticated asset access, calibrated/terrain-corrected sample, pixel inspection, openEO resource estimate, job execution, reference-label audit.

Next experiment: authenticate personally to CDSE/openEO; inspect collection bands, backscatter units and processing options; process only a 1 km chip for the candidate pair. Use provider-supported calibration and terrain correction. Export a small image and metadata. Record job ID, duration, valid pixels, settings and credits. Do not blindly apply a threshold to raw digital numbers or assume a COG is analysis-ready.

Proceed only if imagery overlaps the final AOI, compatible pixels can be produced, event timing is defensible, and interpretable water-change evidence exists. If timing fails, publish the acquisition-gap finding and evaluate a different event. If imagery works but independent labels do not exist, retain a surface-water-change study with qualitative assessment; do not claim validated flood accuracy.

## Reference evidence
Seek dated/geolocated official reports, independently interpreted clear high-resolution imagery or suitable in-situ observations. Verify usage rights and temporal match. News photographs establish an event but usually cannot provide a complete extent polygon. Never use an unverified social-media photograph as ground truth.

Copernicus Global Flood Monitoring can provide a useful comparison where available, but its Sentinel-1 derivation means agreement with our S1 output is not independent validation. Audit reference date, sensor and method. Persistent water and tidal margins need separate treatment.

## Sources
All accessed 2026-09-23 unless otherwise indicated. Summaries are interpretations, not copied methods.
- S1 https://www.channelstv.com/2024/07/03/lagos-calls-for-calm-after-wednesdays-torrential-rainfall/ — event reporting, not a scientific reference map.
- S2 https://global-flood.emergency.copernicus.eu/news/110-floods-in-nigeria-june-to-september-2022/ — official fallback event context.
- S3 https://documentation.dataspace.copernicus.eu/Data/Sentinel1.html and https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html — sensor/product and preprocessing information.
- S4 https://documentation.dataspace.copernicus.eu/APIs/STAC.html — catalogue documentation. Live endpoint: https://stac.dataspace.copernicus.eu/v1
- S5 https://documentation.dataspace.copernicus.eu/APIs/openEO/openeo-community-examples/python/FloodNDWI/flood_SAR.html — official example of SAR flood processing; adapt and evaluate, do not assume transfer.
- S6 https://documentation.dataspace.copernicus.eu/Quotas.html — account quotas; the published openEO 10,000-credit boost is labelled temporary. Rechecked 2026-09-27: still 10,000 openEO credits/month for free users, labelled a temporary boost.
- S7 https://www.thisdaylive.com/2024/07/03/torrential-rain-causes-widespread-flooding-in-lagos/ — accessed 2026-09-27; rain-start time and affected areas (news, not a reference map). S1's Channels TV URL returned HTTP 403 on 2026-09-27.
- S9 https://www.vanguardngr.com/2026/06/floods-displace-lagos-residents-shut-businesses-disrupt-traffic/ — accessed 2026-09-27.
- S10 https://www.vanguardngr.com/2026/07/lagos-submerged-as-floods-sack-homes-paralyse-traffic-halts-businesses/ — accessed 2026-09-27. Weekday wording differs between the two articles; 30 June 2026 is a Tuesday.
- S11 https://www.channelstv.com/2026/06/30/nimet-alerts-lagos-others-to-flash-flooding-in-coastal-areas/ — seen in search results 2026-09-27, not opened.
- S12 https://dataspace.copernicus.eu/news/2026-4-16-sentinel-1d-user-data-opening-17042026 and https://dataspace.copernicus.eu/news/2026-4-2-sentinel-1d-user-data-opening-and-future-plans — accessed 2026-09-27. S1D data open from 17 Apr 2026; the constellation moves to S1C+S1D (6-day revisit), with S1A phased out about early July 2026. Neither page states Browser/Sentinel Hub/openEO availability.
- S13 https://openeo.dataspace.copernicus.eu/openeo/1.2/collections/SENTINEL1_GRD — read 2026-09-27. The summary lists platforms sentinel-1a and sentinel-1b only, and describes the data as "processed to a calibrated, ortho-corrected product".
- S8 https://en.wikipedia.org/wiki/2024_Lekki_flood — accessed 2026-09-27; secondary pointer only (date inconsistency noted).

STAC standardises descriptions and discovery of imagery. openEO runs processing. Neither provides automatic proof that a flood was observed.
