# Milestones

Complete v1 planning estimate: 55–103 focused learning/build hours, excluding provider queues and access delays.

Work in order within this independent project. Effort estimates are focused human learning/build hours, not deadlines; remote compute and access delays may add time. Re-estimate after M1. Do not assume weekly availability. Budget entries draw from the same project allowance, not additional allocations.

## M1 — Feasibility: do the observations support this event?

**Status:** ✅ **Complete 2026-09-28**: GO (option A, S19); learning checkpoint answered (LEARNING_LOG.md). See evidence/FEASIBILITY_RESULT.md. History: 2026-09-27: offline tests re-run on the user's laptop (pass); news-level event timing recorded; blocked on the user's free CDSE account for the calibrated chip. Primary case switched to 30 June 2026 (S11); event evidence in evidence/EVENT_EVIDENCE_2026.md. A pixel check of the 18 Jun / 30 Jun / 12 Jul S1D series is still needed. 2026-09-28: GEE confirmed to carry the S1D scenes; first visual look done (evidence/GEE_FIRST_LOOK_2026-09-28.md). See HANDOFF.md for next steps.

1. **Purpose:** Feasibility: do the observations support this event?
2. **Prerequisites:** None; read investigation and existing scene inventory.
3. **Build:** Metadata search and one real calibrated 1 km chip.
4. **Learn:** Python dictionaries/JSON, UTC/WAT, orbit, calibration and pixel masks.
5. **Tasks:** Run included offline tests and review captured catalogue responses. → Check event timing against the July 3 06:30 WAT acquisition; narrow a candidate AOI. → Authenticate to processing, inspect bands/units and run a bounded sample with recorded credits.
6. **Outputs:** evidence/SCENE_INVENTORY.md; outputs/sample.tif; evidence/FEASIBILITY_RESULT.md
7. **Acceptance checks:** Matching coverage/orbit; valid georeferencing; sample units documented; event interpretation justified or explicitly rejected.
8. **Failures and troubleshooting:** 403: authenticate through provider; empty pixels: check overlap; incompatible units/orbits: select a proper pair; missing event evidence: do not force a flood claim.
9. **Effort and cost:** 6–12 focused hours. $0 target; any paid job requires approval.
10. **Done when:** Record go/no-go and user learning checkpoint. Currently partial: metadata complete, raster/timing gate open.

**Teaching checkpoint:** Explain the input → transformation → output in your own words. Claude should ask one relevant question, update LEARNING_LOG.md with your response and leave the next command.

## M2 — Reproducible preprocessing

**Status:** ✅ Complete 2026-11-04. Built and verified 2026-10-01 (3 identical runs); cross-machine identical run 4 (Mac); process graph saved in the receipt from run 5; the user's learning checkpoint answered (LEARNING_LOG.md 2026-11-04).

1. **Purpose:** Reproducible preprocessing
2. **Prerequisites:** M1 go decision and agreed AOI.
3. **Build:** Config-driven cloud process and aligned rasters.
4. **Learn:** Functions, configuration, grids, nodata and process graphs.
5. **Tasks:** Move sample workflow into a CLI module. → Persist inputs, process graph, package lock and run ID. → Align before/event/after rasters and compare units and masks.
6. **Outputs:** src/preprocess.py; configs/case.json; outputs/aligned/; run-manifest.json
7. **Acceptance checks:** Repeat small run; verify grid/CRS/units and common valid coverage; failed job is recoverable.
8. **Failures and troubleshooting:** Misalignment: inspect transforms; quota failure: shrink AOI or wait; retry only transient errors.
9. **Effort and cost:** 8–14 hours. Free quota first; cumulative STAC spending ≤$50.
10. **Done when:** One repeatable real-data command produces comparable arrays and provenance.

**Teaching checkpoint:** Explain the input → transformation → output in your own words. Claude should ask one relevant question, update LEARNING_LOG.md with your response and leave the next command.

## M3 — Transparent water-change baseline

**Status:** ✅ Complete 2026-11-07 (evidence/M3_SUMMARY_2026-11-07.md). Checkpoint: the user did not know why rules were fixed on the west half first; Claude re-explained (exam analogy); repeat before the final report.

1. **Purpose:** Transparent water-change baseline
2. **Prerequisites:** M2 and development reference plan.
3. **Build:** A baseline method and uncertainty classes.
4. **Learn:** Array masks, thresholds, linear vs dB values and confounding.
5. **Tasks:** Define persistent/new/unknown classes. → Implement simple threshold and change comparison on development areas. → Export statistics using valid coverage and inspect urban/tidal errors.
6. **Outputs:** src/water.py; src/quality.py; outputs/change.tif; development-results.csv
7. **Acceptance checks:** Synthetic unchanged/nodata checks; class areas reconcile; no threshold tuned using final references.
8. **Failures and troubleshooting:** All pixels water: units/threshold error; urban misses: document limitations; tidal changes: separate context.
9. **Effort and cost:** 8–14 hours. $0–10 allowance within STAC total, not extra.
10. **Done when:** Baseline and limitations documented with reproducible outputs.

**Teaching checkpoint:** Explain the input → transformation → output in your own words. Claude should ask one relevant question, update LEARNING_LOG.md with your response and leave the next command.

## M4 — Scientific assessment

**Status:** ✅ Built 2026-11-07, qualitative route (evaluation/ASSESSMENT.md, evaluation/metrics.json, scripts/sensitivity.py). No accuracy metrics: no flood-boundary reference exists.

1. **Purpose:** Scientific assessment
2. **Prerequisites:** M3; references audited and frozen.
3. **Build:** Evaluation and sensitivity study.
4. **Learn:** Precision, recall, IoU, bias and independent evidence.
5. **Tasks:** Finalise spatial development/test separation. → Evaluate frozen method on held-out references if valid. → Run threshold/baseline sensitivity and catalogue failure cases.
6. **Outputs:** evaluation/; outputs/metrics.json; report-results.md
7. **Acceptance checks:** Reference provenance and sample counts included; distinguish agreement from validation; qualitative-only route clearly labelled.
8. **Failures and troubleshooting:** Reference time mismatch: exclude or downgrade claim; sparse samples: no full-map accuracy claim.
9. **Effort and cost:** 8–16 hours. Free-first; stay within remaining STAC allowance.
10. **Done when:** A defensible claim and an explicit uncertainty statement are recorded.

**Teaching checkpoint:** Explain the input → transformation → output in your own words. Claude should ask one relevant question, update LEARNING_LOG.md with your response and leave the next command.

## M5 — Derived STAC catalogue and discovery API

**Status:** ✅ Built 2026-11-07 (S28): catalog/ (Collection + 4 Items, schema-validated), src/catalog.py, tests/test_catalog.py (7 checks), local API via rustac with 5/5 search checks passing (API_CAPABILITIES.md).

1. **Purpose:** Derived STAC catalogue and discovery API
2. **Prerequisites:** M3 outputs; M4 determines claim labels.
3. **Build:** Validated derived items and a local searchable API.
4. **Learn:** Metadata schemas, asset links, API conformance and indexes.
5. **Tasks:** Generate STAC items for output assets with input lineage. → Choose and configure a maintained lightweight STAC server. → Implement/test spatial and temporal discovery and document supported conformance.
6. **Outputs:** catalog/; api/; API_CAPABILITIES.md
7. **Acceptance checks:** STAC schema validation; asset links resolve; bbox/date searches return known expected items.
8. **Failures and troubleshooting:** Broken paths: use portable/public URLs; unsupported extensions: advertise only tested capabilities.
9. **Effort and cost:** 8–16 hours. $0 local target; public hosting optional.
10. **Done when:** Derived results are discoverable through a tested local API, not merely labelled STAC.

**Teaching checkpoint:** Explain the input → transformation → output in your own words. Claude should ask one relevant question, update LEARNING_LOG.md with your response and leave the next command.

## M6 — Interactive evidence viewer

**Status:** ✅ Built 2026-11-07: web/index.html (Leaflet 1.9.4 + Esri street/satellite basemaps), web/data/ from scripts/build_viewer.py, web/demo-checklist.md (checked in Chrome). Not deployed (needs the user's approval).

1. **Purpose:** Interactive evidence viewer
2. **Prerequisites:** M4–M5.
3. **Build:** A public-ready static map of precomputed outputs.
4. **Learn:** Frontend state, map CRS, legends and accessibility.
5. **Tasks:** Create layer/date controls and comparison view. → Show uncertainty, provenance and downloads. → Test browser/mobile, attribution, size and CORS before optional Cloudflare deployment.
6. **Outputs:** web/; viewer-build/; demo-checklist.md
7. **Acceptance checks:** Map aligns; legends match classes; no secret/client compute; precomputed label visible.
8. **Failures and troubleshooting:** Misplaced layer: inspect CRS/bounds; large payload: simplify display copy without changing analytical output.
9. **Effort and cost:** 6–12 hours. $0 target; shared hosting allowance applies.
10. **Done when:** A reviewer can inspect results without an active processing account.

**Teaching checkpoint:** Explain the input → transformation → output in your own words. Claude should ask one relevant question, update LEARNING_LOG.md with your response and leave the next command.

## M7 — Operational and reproducibility release

**Status:** ✅ Done 2026-11-07: fresh-clone install + 48 tests + real rerun byte-identical (RELEASE_CHECKLIST.md); clearer failure messages (impossible dates, Earth Engine refusals); cost-ledger.csv all $0.

1. **Purpose:** Operational and reproducibility release
2. **Prerequisites:** M1–M6.
3. **Build:** Reliable CLI, clean setup and release bundle.
4. **Learn:** Error handling, caching, versioning and operational cost.
5. **Tasks:** Add bounded retries/log redaction and run resumption. → Verify clean-environment sample, docs and dependency lock. → Record resource use and shutdown steps.
6. **Outputs:** requirements lock; tests/; RELEASE_CHECKLIST.md; cost-ledger.csv
7. **Acceptance checks:** Clean rerun; empty search and failed job tests; no billed CI; exported metadata and checksums.
8. **Failures and troubleshooting:** Version drift: pin working versions; missing asset: reconstruct via manifest; avoid embedding credentials.
9. **Effort and cost:** 5–9 hours. Remaining approved allowance only.
10. **Done when:** Version 1 can be reproduced and operated within documented limits.

**Teaching checkpoint:** Explain the input → transformation → output in your own words. Claude should ask one relevant question, update LEARNING_LOG.md with your response and leave the next command.

## M8 — Report, video and interview defence

**Status:** Drafted 2026-11-07: REPORT.md, VIDEO_SCRIPT.md (not recorded), CV_BULLETS.md, INTERVIEW_QA.md, README rewritten in plain English. Waiting for the user: read and correct, record the video, practise the interview answers (the user's own explanation of one function and one failure case is still to be heard).

1. **Purpose:** Report, video and interview defence
2. **Prerequisites:** M7 with actual results.
3. **Build:** Final report and portfolio evidence.
4. **Learn:** Scientific writing and explaining engineering decisions.
5. **Tasks:** Finish report using measured results and failures. → Record 3–5 minute demo. → Draft truthful CV bullets and practise explaining data flow and limitations.
6. **Outputs:** REPORT.md; model/method card; video link; CV_BULLETS.md
7. **Acceptance checks:** Every claim traces to evidence; user explains one key function and one failure case.
8. **Failures and troubleshooting:** Unclear ownership: contribution statement; unsupported result: remove or relabel.
9. **Effort and cost:** 6–10 hours. $0 target.
10. **Done when:** Full v1 release complete; later Port Harcourt/monitoring extensions remain separate.

**Teaching checkpoint:** Explain the input → transformation → output in your own words. Claude should ask one relevant question, update LEARNING_LOG.md with your response and leave the next command.
