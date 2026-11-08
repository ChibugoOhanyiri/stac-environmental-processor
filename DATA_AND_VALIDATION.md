# Data and validation

See INVESTIGATION.md and evidence/SCENE_INVENTORY.md for sources and actual acquisitions. Input status: metadata only; pixel-level suitability remains unverified.

## Data register
| Data | Role | Licence/access action | Principal limitation |
|---|---|---|---|
| Copernicus Sentinel-1 GRD | Main radar observations | Record applicable Copernicus terms and attribution from provider; asset credentials may be required | Raw values require correct calibration/preprocessing; urban flood ambiguity |
| Sentinel-2 L2A | Optional clear-pixel interpretation | Preserve source IDs, processing baseline, attribution and band resolution | Event-day tile has extreme cloud cover |
| Historical water/reference layers | Persistent-water context | Select exact product/version and licence at M1 | A historical product is not a contemporaneous event label |
| Event reports and independent reference observations | Timing and validation | Record publisher, date, coordinates, evidence type and reuse permission | Point evidence cannot validate a complete map |

No imagery is bundled in this pack. Metadata responses contain provider links; don't commit credentials or signed temporary download URLs during later work.

## Processing protocol to implement
1. Validate AOI and date windows, inspect full footprints and timestamps; bound downloads.
2. Inspect S1 band meaning, radiometric units, calibration, noise removal, terrain correction and incidence effects. Use provider-supported processing; record parameters.
3. Align same-orbit observations to a common projected grid and intersect valid masks.
4. Build a transparent baseline using labelled development examples: compare a simple calibrated backscatter threshold with a before/event change rule. Do not mix linear power and dB thresholds.
5. Separate persistent water from candidate new water; retain unknown/ambiguous pixels. Document tides, vegetated water and built-up blind spots.
6. If optical data are usable, mask cloud/shadow first, apply correct scale/offset, calculate an appropriate water index and record resampling choices. Do not fill a cloudy event with another date and label it event truth.
7. Export COGs and statistics with CRS, nodata, source dates, process parameters and input links.

## Evaluation design
Before tuning, divide reference locations into spatially separated development and final assessment areas. Define labels: new water, persistent water, non-water and unobservable. Use temporally compatible independent references if available. Set aside final references; do not tune thresholds on them.

Report a confusion matrix, water precision/recall/F1 and IoU where binary reference masks are defensible. Include sample counts, valid-area coverage, uncertainty and errors by urban/open/vegetated setting. If a stratified sampling design is used to estimate area accuracy, apply appropriate area weights; do not present raw class-balanced accuracy as population accuracy.

Where only sparse reference points exist, report point-level agreement and limitations, not full-map accuracy. With only qualitative evidence, publish qualitative assessment and sensitivity analysis; do not invent precision/recall. A S1-derived comparison product is method agreement, not independent ground truth.

Test stability over reasonable threshold choices and baseline dates. Show at least one failure example each for urban structures, tidal/permanent water and poor observations. Preserve unknown coverage in every denominator.

## Engineering tests
Known synthetic array: mask nodata before differences; unchanged values remain unchanged. Raster integration: reject mismatched CRS/grid/units unless explicitly transformed. Area check: known projected cells have expected area. Export check: valid STAC assets resolve and polygons are inside the AOI. Failure check: empty catalogue, missing metadata and expired credentials remain distinguishable.

The included metadata code tests are only the first engineering check. No scientific accuracy test has passed yet.
