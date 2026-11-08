# Feasibility result

## M1 RESULT — 2026-09-28: GO, option A (the user's decision), pending the M1 learning checkpoint
**Case:** Lagos flood, 30 June 2026, Lekki (S11). **Data:** Sentinel-1D only, descending, relative orbit 95 (S17), via Google Earth Engine (S14).

| M1 acceptance check (MILESTONES.md) | Result |
|---|---|
| Matching coverage/orbit | ✅ S1D lane-95 passes every 12 days, 6 Jun–22 Sep 2026, all covering Lekki (evidence/TIME_SERIES_2026-09-28.md) |
| Valid georeferencing | ✅ outputs/sample.tif: EPSG:32631, 10 m, 100 × 100 px, plausible origin (evidence/SAMPLE_2026-09-28.md) |
| Sample units documented | ✅ dB σ⁰ (GEE, calibrated + ortho-corrected), all 10,000 px valid |
| Event interpretation justified or explicitly rejected | ✅ **Justified at level 2 only.** The flood *happened* (dated news, named official, NiMet: EVENT_EVIDENCE_2026.md). The radar shows a clear **wet period (6 Jun–mid-Jul) vs a dry period (Aug–Sep)** at built-up and open spots, matching the reported timing. **Rejected:** a classic "dark = standing water" signal at the tested Lekki spots; the open plot got *louder* (wet ground). So a simple dark-pixel flood map would miss this urban flood. |

**Decision (user, option A):** continue with Lekki 2026. The claim is **"measured surface change consistent with the reported flood"** (PRD level 2), not "validated flood extent". M2–M3 will map wet-vs-dry change with explicit classes (possible standing water / wetter than normal / permanent water / unchanged / can't tell), test larger open areas for dark standing water, and add rainfall and permanent-water context.

**Timing:** the S1D pass at 06:29 WAT fell inside the flood period, but flooding began before the earliest available S1D pass (6 Jun; none in May), so there is **no clean pre-flood S1D image**. The dry reference is after the event (August), per S17.

**Cost:** $0. GEE Community Tier (no billing), CDSE free account (unused). EECU usage not yet recorded.

---
# Earlier record (2026-09-25/27) — partial, not a flood-analysis result
Status on 2026-09-25: metadata discovery and a tested metadata client only.

## Evidence completed
- Existing saved CDSE responses contain four Sentinel-1 and five Sentinel-2 records for the documented Lagos search.
- A candidate same-orbit radar sequence exists. Event-day optical tile cloud metadata is 99.99%.
- The included Python starter reads saved records or performs an explicit live metadata query; it downloads no imagery and submits no processing job.

> **2026-09-27:** gates below now apply to the primary case, Lagos 30 June 2026 (S1D descending 95: 18 Jun / 30 Jun / 12 Jul). Event-level timing evidence: EVENT_EVIDENCE_2026.md. Rain started 28 June; the 06:29 WAT pass fell before the reported ~11:00 peak inundation of the Ojota-Maryland bridge.

## Unfinished gates — required before M1 completion
1. Establish flood onset/persistence relative to the July 3 06:30 WAT radar acquisition. *2026-09-27 partial:* news reports rain from about 03:00 WAT, so the pass is about 3.5 h into the rain. Persistence was reported as short and tide-dependent. No gauge data yet. See INVESTIGATION.md.
2. Choose a bounded analysis area from event evidence plus footprints, not city name alone.
3. Authenticate personally to the selected processing provider; inspect actual collection/band units and preprocessing capabilities.
4. Run one 1 km calibrated/terrain-corrected sample, measure credits/time, inspect masks and compare observations.
5. Audit independent reference evidence and persistent-water/tidal context.
6. Record go/no-go: flood-consistent study, surface-water-change-only study, or different event with user agreement.

No accuracy, observed flood extent, processing runtime or paid cost is established. No paid resources have been created. If credentials or free quota are missing, pause at that gate; do not pretend sample feasibility is verified.

## First resume instructions
Run offline tests, generate a saved-data summary, read it with the user and explain the time/orbit problem. Then collect timing/reference evidence and inspect provider processing capabilities. Only request the user's account access when a concrete sample process and cost boundary are ready. A catalogue query and a processing job are different operations.

A 2026-09-25 live metadata refresh also returned the same four radar IDs. See VERIFICATION.md. This does not close the pixel/timing gates.
