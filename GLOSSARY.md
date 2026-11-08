# Plain-English glossary

Each term: a five-year-old version first, then the proper meaning, then an example from this project. We add terms as they come up while building.

**Remote sensing** — Learning about something without touching it, from far away. Satellites "sense" the Earth from space. Example: we study Lagos floods from satellites about 700 km up.

**Sensor** — The satellite's "eye". It measures energy (light or radio waves) coming back from the ground.

**Passive sensor (optical)** — A camera that needs the Sun as its torch, so clouds and night block it. Example: Sentinel-2. Its 3 July 2024 image was 99.99% cloud.

**Active sensor (radar / SAR)** — Brings its own torch: it shouts radio waves at the ground and listens for the echo. Works through cloud and at night. Example: Sentinel-1. SAR = Synthetic Aperture Radar.

**Backscatter** — How loud the echo is. Calm water acts like a mirror and bounces the shout away, so water looks **dark**. Buildings act like corners and bounce it straight back, so they look **bright**. That is why flooded streets between buildings are hard to see.

**STAC (SpatioTemporal Asset Catalog)** — A library catalogue card for satellite pictures. *Spatio* = where, *Temporal* = when, *Asset* = the actual files, *Catalog* = the organised list. It tells you a picture exists and where to fetch it. It is not the picture.

**Orbit direction** — Satellites circle the Earth from pole to pole. *Descending* = moving north to south (over Lagos about 06:30 local time). *Ascending* = moving south to north (about 19:00).

**Relative orbit (track)** — The satellite's lane number, like a bus route. Same lane plus same direction means it looks at the ground from the same angle. Only then is a before/after comparison fair. Example: orbit 95 descending.

**AOI (Area of Interest)** — The box of ground we study.

**bbox** — A rectangle written as four numbers: west, south, east, north (in degrees). Ours is 3.25, 6.40, 3.65, 6.70.

**UTC / WAT** — UTC is the world's reference clock. WAT (West Africa Time) = UTC + 1 hour. Satellite times are in UTC: 05:29 UTC = 06:29 in Lagos.

**CRS (Coordinate Reference System)** — The "address system" that says where each pixel sits on Earth.

**Pixel** — One tiny square of a picture, holding one measured value.

**Calibration** — Turning the sensor's raw numbers into real measurements, like converting a thermometer's squiggles into degrees C.

**dB (decibel)** — A way of writing very big and very small numbers on a squashed scale. Radar echo strength is often shown in dB.

**Nodata** — "We didn't see here." It is not dry ground.

**COG (Cloud-Optimised GeoTIFF)** — A map image arranged so you can read a small piece without downloading the whole thing. It says nothing about whether the data is calibrated.

**IoU** — Overlap divided by combined area: how well two maps agree.

**CLI** — Commands typed into a terminal.

**Manifest** — A receipt listing inputs, settings and outputs.

## The Sentinel family and data types (added 2026-09-27)

**Sentinel-1 — the radar satellite.** Shouts microwaves and listens for the echo; works day, night and through cloud. Used for floods, oil spills, ships, sea ice and ground sinking (InSAR). **Our main data.**

**Sentinel-2 — the colour camera.** Photographs sunlight in 13 "colours" (bands), some invisible to our eyes. Used for crops, forests, land cover and water. Blocked by cloud. Our backup data.

**Sentinel-3 — the ocean and big-picture watcher.** Sees the whole Earth almost daily but in blurry pixels (about 300 m–1 km). Used for sea temperature, ocean colour, fires and sea height.

**Sentinel-5P — the air sniffer.** Measures gases in the air: NO₂ (traffic and factory pollution), methane, ozone, carbon monoxide. Pixels are several km wide.

**Sentinel-6 — the sea-level ruler.** Measures the height of the ocean surface very precisely, to track sea-level rise. Relevant background for coastal Lagos.

**Contributing missions** — Satellites from other agencies and companies that share data through Copernicus, including some very sharp cameras and radar, and elevation data.

**CLMS (Copernicus Land Monitoring Service)** — Ready-made maps made *from* satellite data: land cover, vegetation greenness, water bodies. "Cooked meals", not raw ingredients.

**Global mosaic** — Many passes stitched together into one mostly cloud-free picture of the world, like a patchwork quilt.

**SAR (Synthetic Aperture Radar)** — A sharp picture needs a big antenna. The satellite has a small one, but it records echoes all along its path and combines them, pretending to be a kilometres-long antenna. That's the "synthetic" (fake) "aperture" (opening).

**Optical / multispectral** — Measures reflected sunlight in several colour bands. Plants reflect lots of invisible near-infrared light; water absorbs it and looks dark. This difference is how we spot water in optical images (water indices such as NDWI).

**DEM (Digital Elevation Model)** — A grid where each pixel stores ground height, like the spot heights and contours of a survey, but for everywhere. **DSM** (surface model) includes buildings and trees; **DTM** (terrain model) is bare ground. Copernicus DEM (30 m) is a surface model. Used for: where water flows and pools, radar terrain correction, 3D maps and digital twins.

## Words from the Copernicus Browser (added 2026-09-27)

**IW (Interferometric Wide swath)** — Sentinel-1's normal mode over land: it sweeps a wide strip about 250 km across. You can see it in our scene names: S1D_**IW**_GRDH…

**Polarisation (VV, VH, HH, HV)** — The direction the radar wave "wiggles" when sent, then when received. VV = sent up-down, heard up-down; good for water and flat surfaces. VH = sent up-down, heard side-to-side; more sensitive to plants and messy surfaces. Our scenes are "1SDV" = dual polarisation, VV + VH.

**Pixel spacing vs resolution** — "10 m × 10 m" is how far apart the pixels are. The true sharpness for Sentinel-1 IW GRD is coarser (about 20 m). Like printing a blurry photo on finer paper: more dots, not more detail.

**Gamma0 (γ⁰)** — A calibrated radar echo value, adjusted for the angle the radar looked from. It is "cleaned" echo loudness, comparable between places and dates.

**Orthorectified** — Pixels moved to their true map position using a DEM, fixing the distortion that hills and slopes cause in radar images. (This is the terrain correction step.)

**Linear vs decibel (dB)** — Two ways of writing the same echo value. Linear numbers are tiny and bunched (0.001, 0.05…). dB spreads them out (−30, −13…), so dark water stands out better to the eye. Never compare a linear number with a dB number.

## Comparing two radar pictures (added 2026-09-28)

**Speckle** — The grainy "salt and pepper" in every radar picture. Normal noise, like static on an old TV.

**Speckle filter** — Calming the noise by averaging each pixel with its neighbours (e.g. within 30 m). Blurrier but easier to read. Used here for display only.

**Difference image** — Subtract the before picture from the flood-day picture, pixel by pixel. Negative numbers mean the pixel got darker (possible new water); positive numbers mean it got brighter.

**Change-colour composite (RGB trick)** — Put the before picture in the red channel and the flood-day picture in green and blue. Unchanged = grey; got darker = red; got brighter = cyan.

**Confounder** — Something else that can cause the same signal and fool us. Example: wind roughening the lagoon makes water look brighter, like land.

**Time series** — The same measurement repeated over many dates and drawn as a line graph, like a temperature chart. Here: radar echo (dB) at one spot for every satellite pass. It shows *when* a spot changed and when it went back to normal.

**Control** — A spot where we already know the answer (e.g. a permanent pond is always water). If our method gets the control wrong, we can't trust it elsewhere.

**Double bounce** — Radar hits flat water, bounces onto a wall and comes straight back to the satellite. Flooded streets between buildings can look *brighter*, not darker.

**Resolution (in practice)** — The smallest thing the satellite can tell apart. Sentinel-1 pixels are 10 m, but true sharpness is about 20 m. A 90 × 60 m plot is only about 9 × 6 pixels; a single narrow street is less than one.

**Inspector (GEE)** — A tool: click the map, and it tells you the coordinates and pixel values there. Like pointing a GPS at a spot. It shows the *last* click.

## M2 words (added 2026-10-01)

**Settings card (config file)** — The order slip: WHAT to make (place, dates, satellite). The code is the kitchen: HOW to make it. A new case means a new card, with the same code. Ours: configs/case.json.

**JSON** — A simple text format of "label": value pairs that people and computers can both read.

**Virtual environment (.venv)** — A private drawer of Python tools for one project, so versions never clash with other projects.

**Pinning** — Writing down exact tool versions (requirements.txt) so the recipe still works later.

**Authentication / credential** — Proving to Google who you are; the "permission slip" saved on your laptop (never in the repo).

**Dry run** — A rehearsal: search and check everything, but download nothing.

**Aligned grid** — Two pictures with exactly the same corners, pixel size and map system, so pixel 1 in one is the same ground as pixel 1 in the other.

**Unit test** — A tiny automatic check of one piece of code (e.g. "an empty search must stop the run").

**Fingerprint (SHA-256 hash)** — A long code computed from a file's bytes. The same file always gives the same code, and any change gives a different one. Used to prove two runs made identical files.

**Run manifest (receipt)** — The record of one run: when, which pictures, which settings, which tool versions, which code version, and the files made.
