# Architecture

## Components and flow
Configuration → STAC search client → immutable scene manifest → cloud preprocessing → aligned arrays → water/change analysis → COG + statistics + derived STAC items → viewer and local discovery API.

A COG is a GeoTIFF organised so software can read parts of it efficiently. Its file layout says nothing by itself about calibration or scientific validity.

- Laptop: edit Python, run metadata search and tiny fixtures, inspect results, run the viewer and API locally. Avoid full-scene downloads.
- Google Earth Engine (primary processing route since 2026-09-27, DECISIONS S14): COPERNICUS/S1_GRD is already calibrated and ortho-corrected (dB, Sentinel-1 Toolbox). Store script, image IDs and export parameters. Discovery and lineage stay on CDSE STAC.
- CDSE/openEO (documented alternative): calibrated/terrain-corrected bounded processing after capability and account checks. Store the process graph and job metadata.
- Optional cloud notebook: array analysis on cropped outputs; no permanent server required.
- Cloudflare: publish static HTML/JavaScript and small derived assets. R2 only if required for larger files; configure CORS and range access.
- Local API: maintained STAC server backed by generated catalogue or indexed output metadata. Choose implementation after testing its footprint; no requirement to host it continuously.

## Suggested modules
`catalogue.py`: validate query and collect metadata. `preprocess.py`: construct/run documented process graph. `water.py`: baseline and change logic. `quality.py`: nodata/masks. `export.py`: rasters/statistics/STAC. `cli.py`: commands. Keep exploratory notebooks thin.

Version 1 initially uses a CLI and a static viewer (Leaflet is sufficient for modest overlays). Add the derived catalogue/API after the analysis is defensible; do not spend the first week configuring Kubernetes or multiple clouds.

## Data contracts
Run manifest: run_id, retrieval_time_utc, AOI_geojson, time_windows, source_item_ids, provider, processing_graph_hash, git_commit, package_versions, parameters, reference_version, outputs and checksums.
Output raster classes: explicit numeric codes for unchanged, candidate new water, persistent water, ambiguous and nodata. Define codes in metadata rather than choosing them implicitly in styling.
Statistics: valid_area_m2, candidate_change_area_m2, persistent_water_area_m2, unobserved_area_m2, method and units. Area is calculated in a suitable projected CRS, not square degrees.
Derived STAC items: geometry/bbox, observation time interval, processing time separately, projection metadata, asset roles/media types, input links and attribution.

## Reliability and trade-offs
Cloud processing avoids laptop limits but adds authentication and provider availability. Cache scene metadata and small outputs; never treat cached metadata as proof current asset access works. Retry transient requests a bounded number of times, respect 429/Retry-After and preserve failed job IDs. Key caches by inputs and parameters.

Sentinel-1 candidate series must share orbit direction/relative orbit and relevant acquisition settings. Work on one CRS, grid, pixel size and common coverage. Preserve native analytical resolution; resampling is for alignment, not enhancement. For Lagos, UTM zone 31N is a candidate working CRS; validate bounds before using it for another area.

Pipeline execution is on demand. Optional scheduling/monitoring of new acquisitions follows a working manual run and explicit cost review. A self-hosted STAC API and client querying CDSE are different components: document both accurately.
