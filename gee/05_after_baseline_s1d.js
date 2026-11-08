// 05_after_baseline_s1d.js — Google Earth Engine Code Editor script (JavaScript)
// Purpose: VISUAL comparison of 30 June 2026 (flood day) against AFTER-event references,
// using ONLY Sentinel-1D on the same lane (descending, relative orbit 95). This is the user's
// choice (2026-09-28): keep one satellite, and use later dates because the before period
// (June; May had no S1D lane-95 images) was already flooded. The user's friend says the flood
// has since dried out (second-hand; timing unknown).
// Why August: southern Nigeria usually has a drier "August break" mid rainy season.
// July may still be wet (more rain reported 3 Jul). Both are shown so they can be compared.
// Display only: no thresholds, areas or exports.

// 1. WHERE
var lekki = ee.Geometry.Rectangle([3.45, 6.42, 3.60, 6.48]);
var orchid = ee.Geometry.Point([3.5566, 6.4317]);   // Orchid Road (OpenStreetMap/Nominatim)
var chevron = ee.Geometry.Point([3.5306, 6.4520]);  // Chevron Drive (OpenStreetMap/Nominatim)

// 2. WHAT: Sentinel-1D ONLY, same lane, wide land mode, VV only
var s1d = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(lekki)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filter(ee.Filter.eq('relativeOrbitNumber_start', 95))
  .filter(ee.Filter.eq('platform_number', 'D'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .select('VV');

// 3. List every S1D lane-95 picture from June to September, to see what exists
print('All S1D lane-95 pictures, Jun-Sep 2026:',
      s1d.filterDate('2026-06-01', '2026-10-01').aggregate_array('system:index'));

// 4. REFERENCES: July median and August median (middle value) + speckle filter
var july = s1d.filterDate('2026-07-05', '2026-08-01');   // after the 3 July rain
var aug  = s1d.filterDate('2026-08-01', '2026-09-01');
print('Number of July pictures:', july.size());
print('Number of August pictures:', aug.size());
var julyRef = july.median().focalMean(30, 'circle', 'meters');
var augRef  = aug.median().focalMean(30, 'circle', 'meters');

// 5. FLOOD DAY
var june30 = s1d.filterDate('2026-06-30', '2026-07-01').first().focalMean(30, 'circle', 'meters');

// 6. COLOUR TRICK: red = reference (the "dry" date), green + blue = 30 June.
//    Grey = same.  RED = darker on 30 June than the reference (possible flood water).
//    CYAN = brighter on 30 June.
Map.centerObject(orchid, 14);
Map.addLayer(ee.Image.cat([julyRef, june30, june30]), {min: -25, max: 0},
             'H) 30 June vs JULY (red = darker on 30 June)', false);
Map.addLayer(ee.Image.cat([augRef, june30, june30]), {min: -25, max: 0},
             'G) 30 June vs AUGUST (red = darker on 30 June)');

// 7. Markers
Map.addLayer(ee.Image().paint(lekki, 0, 2), {palette: 'yellow'}, 'Lekki box');
Map.addLayer(orchid, {color: 'yellow'}, 'Orchid Road');
Map.addLayer(chevron, {color: 'orange'}, 'Chevron Drive');
