// 07_export_sample.js — Google Earth Engine Code Editor script (JavaScript)
// Purpose: M1 output "outputs/sample.tif". Export ONE small real data file: a 1 km x 1 km square
// centred on Orchid Road, Lekki, as a GeoTIFF to the user's Google Drive.
// Bands (all Sentinel-1D, descending, lane 95, dB, already calibrated + ortho-corrected by GEE):
//   VV_20260630       flood-day VV
//   VH_20260630       flood-day VH (the other radar "flavour")
//   VV_AUG2026_MEDIAN dry reference (median of the August 2026 passes)
// No speckle filter, no thresholds: raw analysis-ready values for inspection.
// Grid: UTM zone 31N (EPSG:32631), 10 m pixels (ARCHITECTURE.md candidate working CRS for Lagos).
// Written 2026-09-28.

// 1. WHERE: a 1 km square (±500 m) around Orchid Road
var orchid = ee.Geometry.Point([3.5566, 6.4317]);
var square = orchid.buffer(500).bounds();

// 2. WHAT: Sentinel-1D only, same lane, wide land mode
var s1d = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(square)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filter(ee.Filter.eq('relativeOrbitNumber_start', 95))
  .filter(ee.Filter.eq('platform_number', 'D'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'));

var flood = s1d.filterDate('2026-06-30', '2026-07-01').first();
var aug = s1d.filterDate('2026-08-01', '2026-09-01');
print('Flood-day picture:', flood.get('system:index'));
print('August pictures in the median:', aug.aggregate_array('system:index'));

// 3. STACK the three layers into one file (like pages in one book)
var sample = ee.Image.cat([
  flood.select('VV').rename('VV_20260630'),
  flood.select('VH').rename('VH_20260630'),
  aug.select('VV').median().rename('VV_AUG2026_MEDIAN')
]).toFloat();

// 4. SHOW it before exporting
Map.centerObject(square, 15);
Map.addLayer(sample.select('VV_20260630'), {min: -25, max: 0}, 'VV 30 June (sample)');
Map.addLayer(ee.Image().paint(square, 0, 2), {palette: 'yellow'}, '1 km sample square');

// 5. EXPORT to Google Drive (goes to the Tasks tab; press RUN there)
Export.image.toDrive({
  image: sample,
  description: 'sample_lekki_orchid_1km_20260630',
  folder: 'stac-lagos-flood',
  fileNamePrefix: 'sample_lekki_orchid_1km_20260630',
  region: square,
  scale: 10,
  crs: 'EPSG:32631',
  fileFormat: 'GeoTIFF',
  maxPixels: 1e6
});
