# Run receipts (M2)

Each run of `src/preprocess.py` writes a receipt (`run-manifest_<run_id>.json`) next to its outputs in `outputs/aligned/`. That folder is git-ignored (no imagery on GitHub), so the receipts that matter are copied here.

| Run ID | Code (git) | Unsaved code? | Event file SHA-256 (first 16) | Reference file SHA-256 (first 16) |
|---|---|---|---|---|
| 20261001T195653Z (run 1) | 8510d40 | yes: recipe not yet committed (flag added afterwards) | 5242bc6efaf39123 | 29b3dec174c85692 |
| 20261001T195804Z (run 2) | 8510d40 | yes: same | 5242bc6efaf39123 | 29b3dec174c85692 |
| **20261001T195856Z (run 3)** | **9a15ad7** | **no**: clean receipt, saved here | 5242bc6efaf39123 | 29b3dec174c85692 |
| **20261104T083738Z (run 4, Mac)** | **ba3fa0f** | **no**: clean receipt, saved here | 5242bc6efaf39123 | 29b3dec174c85692 |
| **20261104T113123Z (run 5, Mac, with recipe card)** | **bedb501** | **no**: clean receipt, saved here | 5242bc6efaf39123 | 29b3dec174c85692 |

**Reproducibility check (M2 acceptance):** three runs of the same command and settings card produced **byte-identical** GeoTIFFs. Runs 1 and 2 receipts were not kept in git because they point at a commit that did not yet contain the recipe; this table records their fingerprints.

**What each receipt contains:** run ID and times; a full copy of the settings card; the exact grid (EPSG:32631, 100 × 100 px, 10 m, top-left 561040, 711460); Earth Engine image IDs per role (event: S1D 30 Jun 2026; reference: S1D 5, 17 and 29 Aug 2026, median); tool versions (Python 3.14.4, earthengine-api 1.7.46, rasterio 1.5.2, GDAL 3.12.2, numpy 2.5.3); git commit + unsaved-changes flag; and per-file SHA-256, valid/nodata counts and median VV.

**Results (run 3):** event median VV −5.362 dB; reference median VV −6.916 dB; 10,000 valid pixels each, 0 nodata. Same grid confirmed (identical CRS, transform and shape). 71% of pixels are louder on 30 Jun than the August median (median difference +1.16 dB).

**Cross-machine check (2026-11-04):** after moving the project from Windows 11 (Python 3.14.4) to macOS arm64 (Python 3.13.16, same pinned package versions), run 4 produced GeoTIFFs **byte-identical** to runs 1–3 (same SHA-256), with the same medians (−5.362 / −6.916 dB) and the same Earth Engine image IDs. The quick-look figure (fig10) also regenerated identically. Caveat: this holds while Earth Engine's stored S1 images and processing stay unchanged; a provider reprocessing would change values, and the receipt's image IDs and hashes would reveal it.

**Recipe card / process graph (added 2026-11-04, run 5):** from run 5 each receipt also stores, per role, `process_graph`: Earth Engine's own serialised description of the exact expression sent to `computePixels` (collection load → bounds/date/satellite/lane/band filters → mosaic or median → select VV, VH → toFloat → unmask −9999). It is produced from the same object that is sent (`build_expression` in src/preprocess.py), so it cannot describe a different recipe. Checked: run 5 outputs are byte-identical to runs 1–4; the graph (~3.6 kB per role) contains no project ID, key, token or URL. Limit: it records *what was asked*, not Earth Engine's internal code version, so a provider-side change would still only show up through the hashes.
