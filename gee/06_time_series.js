// 06_time_series.js — Google Earth Engine Code Editor script (JavaScript)
// Purpose: stop guessing "before/after" dates. Chart the Sentinel-1D VV echo (dB) at a few
// spots for EVERY lane-95 pass, Jun–Sep 2026, to see when each spot looks unusual and
// when it returns to normal. Written 2026-09-28 after the user questioned the timelines.
// Spots: Orchid Road and Chevron Drive (named in the evidence / the user's stay), and the
// Twin Lakes pond area as an "always water" control (estate centre from OpenStreetMap;
// check with the Inspector that the circle sits on water).
// v2 (2026-09-28): added an OPEN-GROUND spot, an empty plot the user found near Orchid (bounded by
// Cityscape Blvd to the north and Buena Vista Estate to the west). The plot is only ~90 x 60 m, so it
// v2 used Claude's estimate (3.5543, 6.4319), which landed on houses west of the Buena Vista Estate
// road. v3 uses the user's own Inspector click (3.5549, 6.4319), which is inside the plot. The plot
// is ~75 x 40 m, so the radius is 15 m. Detective test: flood water
// should make open ground DARKER while built-up areas get BRIGHTER (double bounce).
// Simplification (viewing only): averages dB values inside each circle. The analysis version
// must average in linear power and then convert to dB (never mix linear and dB).

// 1. WHAT: Sentinel-1D only, same lane (descending, relative orbit 95), VV, Jun–Sep 2026
var s1d = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
  .filter(ee.Filter.eq('relativeOrbitNumber_start', 95))
  .filter(ee.Filter.eq('platform_number', 'D'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .filterDate('2026-06-01', '2026-10-01')
  .select('VV');

// 2. WHERE: small circles (radius in metres) around each spot; averaging calms speckle
var spots = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Point([3.5566, 6.4317]).buffer(50), {label: 'Orchid Road'}),
  ee.Feature(ee.Geometry.Point([3.5306, 6.4520]).buffer(50), {label: 'Chevron Drive'}),
  ee.Feature(ee.Geometry.Point([3.5297, 6.4327]).buffer(30), {label: 'Twin Lakes pond (water control)'}),
  ee.Feature(ee.Geometry.Point([3.5549, 6.4319]).buffer(15), {label: 'Open plot near Orchid'})
  // To add the user's south-east red area: copy the Inspector point, e.g.
  // , ee.Feature(ee.Geometry.Point([LON, LAT]).buffer(50), {label: 'SE red area'})
]);

// 3. THE GRAPH: one line per spot, one point per satellite pass
var chart = ui.Chart.image.seriesByRegion({
  imageCollection: s1d,
  regions: spots,
  reducer: ee.Reducer.mean(),
  band: 'VV',
  scale: 10,
  xProperty: 'system:time_start',
  seriesProperty: 'label'
}).setOptions({
  title: 'Sentinel-1D VV echo over time, Lekki (dB) — lower = darker/smoother',
  vAxis: {title: 'VV (dB)'},
  hAxis: {title: 'Date'},
  lineWidth: 1,
  pointSize: 5
});
print(chart);
print('Passes used:', s1d.aggregate_array('system:index'));

// 4. MAP: the 30 June picture with the measured circles on top
var june30 = s1d.filterDate('2026-06-30', '2026-07-01').first();
Map.centerObject(ee.Geometry.Point([3.5549, 6.4319]), 18);  // zoom to the open plot
Map.addLayer(june30, {min: -25, max: 0}, 'VV 30 June 2026');
Map.addLayer(spots, {color: 'yellow'}, 'Measured spots');
