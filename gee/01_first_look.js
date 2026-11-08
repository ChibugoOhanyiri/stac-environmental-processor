// 01_first_look.js — Google Earth Engine Code Editor script (JavaScript)
// Purpose: list Sentinel-1 descending IW scenes over Lekki, 15 Jun–15 Jul 2026,
// and display the 18 Jun (before) and 30 Jun (flood-day) VV images.
// First run: 2026-09-28 by the user in the Code Editor (Cloud project on the Community Tier).
// Results: evidence/GEE_FIRST_LOOK_2026-09-28.md
// Viewing only: no export, no analysis. COPERNICUS/S1_GRD values are already
// calibrated, ortho-corrected sigma0 in dB (per the GEE catalogue).

// 1. WHERE: a rough box over Lekki (west, south, east, north in degrees)
var lekki = ee.Geometry.Rectangle([3.45, 6.42, 3.60, 6.48]);

// 2. WHAT + WHEN: Sentinel-1 radar, same lane direction, 15 June – 15 July 2026
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(lekki)
  .filterDate('2026-06-15', '2026-07-15')
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));

// 3. List the names of every picture found (like reading catalogue cards)
print('Pictures found:', s1.aggregate_array('system:index'));

// 4. Put the 18 June and 30 June pictures on the map
var june18 = s1.filterDate('2026-06-18', '2026-06-19').first();
var june30 = s1.filterDate('2026-06-30', '2026-07-01').first();
Map.centerObject(lekki, 12);
Map.addLayer(june18.select('VV'), {min: -25, max: 0}, 'VV 18 June 2026 (before)');
Map.addLayer(june30.select('VV'), {min: -25, max: 0}, 'VV 30 June 2026 (flood day)');
Map.addLayer(ee.Image().paint(lekki, 0, 2), {palette: 'red'}, 'Lekki box');
