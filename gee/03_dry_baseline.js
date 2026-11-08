// 03_dry_baseline.js — Google Earth Engine Code Editor script (JavaScript)
// Purpose: VISUAL test of the user's first-hand account that Lekki (Orchid) was flooded
// for the whole of their stay (27 Jun–2 Jul 2026, corrected; flooding already large on arrival). If so, the 18 June image is
// already wet, and 18 Jun vs 30 Jun shows no change. So compare both dates against a
// DRY-SEASON baseline instead.
// Baseline: median of Jan to mid-Mar 2026 images on the same lane (descending, relative orbit 95).
// These come from Sentinel-1A (S1D data only open from 17 Apr 2026), a twin satellite on
// the same track (see DECISIONS S12). Display only: no thresholds, areas or exports.
// Written 2026-09-28.

// 1. WHERE
var lekki = ee.Geometry.Rectangle([3.45, 6.42, 3.60, 6.48]);
var orchid = ee.Geometry.Point([3.5566, 6.4317]);   // Orchid Road (OpenStreetMap/Nominatim)
var chevron = ee.Geometry.Point([3.5306, 6.4520]);  // Chevron Drive (OpenStreetMap/Nominatim)

// 2. WHAT: same lane, same mode, VV only
var lane95 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(lekki)
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filter(ee.Filter.eq('relativeOrbitNumber_start', 95))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .select('VV');

// 3. DRY-SEASON BASELINE: the "median" (middle value) of several dry-season pictures.
//    The middle value ignores odd days and calms speckle.
var dry = lane95.filterDate('2026-01-01', '2026-03-15');
print('Number of dry-season pictures:', dry.size());
print('Dry-season pictures used:', dry.aggregate_array('system:index'));
var dryBaseline = dry.median().focalMean(30, 'circle', 'meters');

// 4. THE TWO RAINY-SEASON DATES (same speckle filter)
var june18 = lane95.filterDate('2026-06-18', '2026-06-19').first().focalMean(30, 'circle', 'meters');
var june30 = lane95.filterDate('2026-06-30', '2026-07-01').first().focalMean(30, 'circle', 'meters');

// 5. COLOUR TRICK again: red = dry baseline, green + blue = the later date.
//    Grey = same as dry season.  RED = darker than dry season (possible water).  CYAN = brighter.
Map.centerObject(lekki, 13);
Map.addLayer(ee.Image.cat([dryBaseline, june18, june18]), {min: -25, max: 0},
             'C) 18 June vs DRY season (red = darker)');
Map.addLayer(ee.Image.cat([dryBaseline, june30, june30]), {min: -25, max: 0},
             'D) 30 June vs DRY season (red = darker)');

// 6. Markers for places named in the evidence
Map.addLayer(ee.Image().paint(lekki, 0, 2), {palette: 'yellow'}, 'Lekki box');
Map.addLayer(orchid, {color: 'yellow'}, 'Orchid Road');
Map.addLayer(chevron, {color: 'orange'}, 'Chevron Drive');
