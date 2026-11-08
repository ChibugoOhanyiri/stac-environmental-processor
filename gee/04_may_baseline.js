// 04_may_baseline.js — Google Earth Engine Code Editor script (JavaScript)
// Purpose: VISUAL comparison of 30 June 2026 (flood day) against a MAY 2026 baseline,
// the user's suggestion (2026-09-28). The user was in Lagos 27 Jun–2 Jul with flooding
// already large on arrival; a friend (second-hand) says flooding began in early June.
// So 18 June is likely wet, and May may be the last "before" period.
// v1 (first run 2026-09-28) filtered May to Sentinel-1D and returned ZERO images: S1D was not yet
// flying lane 95 in May (constellation transition mid-Apr to mid-Jun; first S1D lane-95 pass over
// Lagos found so far = 6 Jun, per gee/06). v2 uses every lane-95 image in May (expected: Sentinel-1A, a twin, see S12)
// and prints the satellite of each.
// Check built in: layer F compares May against the dry season, to see whether May itself was wet.
// Display only: no thresholds, areas or exports.

// 1. WHERE
var lekki = ee.Geometry.Rectangle([3.45, 6.42, 3.60, 6.48]);
var orchid = ee.Geometry.Point([3.5566, 6.4317]);   // Orchid Road (OpenStreetMap/Nominatim)
var chevron = ee.Geometry.Point([3.5306, 6.4520]);  // Chevron Drive (OpenStreetMap/Nominatim)

// 2. WHAT: same lane (descending, relative orbit 95), wide land mode, VV only
var lane95 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(lekki)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filter(ee.Filter.eq('relativeOrbitNumber_start', 95))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .select('VV');

// 3. MAY BASELINE: every lane-95 picture in May 2026, median (middle value) + speckle filter
var may = lane95.filterDate('2026-05-01', '2026-06-01');
print('Number of May pictures:', may.size());
print('May pictures used:', may.aggregate_array('system:index'));
print('Satellite of each (A, C or D):', may.aggregate_array('platform_number'));
var mayBaseline = may.median().focalMean(30, 'circle', 'meters');

// 4. FLOOD DAY (S1D) and DRY SEASON (S1A, Jan to mid-Mar) for the check
var june30 = lane95.filter(ee.Filter.eq('platform_number', 'D'))
  .filterDate('2026-06-30', '2026-07-01').first().focalMean(30, 'circle', 'meters');
var dryBaseline = lane95.filterDate('2026-01-01', '2026-03-15').median()
  .focalMean(30, 'circle', 'meters');

// 5. COLOUR TRICK: red = earlier picture, green + blue = later picture.
//    Grey = no change.  RED = got darker (possible water).  CYAN = got brighter.
Map.centerObject(orchid, 14);
Map.addLayer(ee.Image.cat([dryBaseline, mayBaseline, mayBaseline]), {min: -25, max: 0},
             'F) CHECK: May vs dry season (red = May darker)', false);
Map.addLayer(ee.Image.cat([mayBaseline, june30, june30]), {min: -25, max: 0},
             'E) 30 June vs MAY (red = darker on 30 June)');

// 6. Markers
Map.addLayer(ee.Image().paint(lekki, 0, 2), {palette: 'yellow'}, 'Lekki box');
Map.addLayer(orchid, {color: 'yellow'}, 'Orchid Road');
Map.addLayer(chevron, {color: 'orange'}, 'Chevron Drive');
