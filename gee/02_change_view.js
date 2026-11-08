// 02_change_view.js — Google Earth Engine Code Editor script (JavaScript)
// Purpose: VISUAL change view between 18 Jun (before) and 30 Jun 2026 (flood day), Lekki.
// Same satellite (S1D), same lane (descending, relative orbit 95), VV band, dB.
// Display only: no thresholds, no areas, no exports. Candidate changes are NOT flood proof.
// Written 2026-09-28 after the user found flipping two grey layers hard to compare by eye.

// 1. WHERE: the same rough box over Lekki (west, south, east, north)
var lekki = ee.Geometry.Rectangle([3.45, 6.42, 3.60, 6.48]);

// 2. WHAT: only Sentinel-1D, descending, lane 95, wide land mode
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(lekki)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filter(ee.Filter.eq('platform_number', 'D'))
  .filter(ee.Filter.eq('relativeOrbitNumber_start', 95));

var beforeImg = s1.filterDate('2026-06-18', '2026-06-19').first();
var floodImg  = s1.filterDate('2026-06-30', '2026-07-01').first();
print('Before image:', beforeImg.get('system:index'));
print('Flood-day image:', floodImg.get('system:index'));

// 3. SPECKLE FILTER (display only): average each pixel with neighbours within 30 m
var before = beforeImg.select('VV').focalMean(30, 'circle', 'meters');
var flood  = floodImg.select('VV').focalMean(30, 'circle', 'meters');

// 4A. COLOUR TRICK: red = before, green + blue = flood day.
//     Grey  = no change.
//     RED   = got DARKER on 30 June (possible new water, or other causes).
//     CYAN  = got BRIGHTER on 30 June (e.g. wind/rain-roughened water).
var rgb = ee.Image.cat([before, flood, flood]);
Map.centerObject(lekki, 13);
Map.addLayer(rgb, {min: -25, max: 0}, 'A) Change colours (red = darker on 30 June)');

// 4B. DIFFERENCE: flood day minus before, in dB (hidden at first; tick it in Layers)
//     BLUE = darker on 30 June, WHITE = no change, RED = brighter on 30 June.
var diff = flood.subtract(before);
Map.addLayer(diff, {min: -6, max: 6, palette: ['0000ff', 'ffffff', 'ff0000']},
             'B) Difference dB (blue = darker on 30 June)', false);

Map.addLayer(ee.Image().paint(lekki, 0, 2), {palette: 'yellow'}, 'Lekki box');
