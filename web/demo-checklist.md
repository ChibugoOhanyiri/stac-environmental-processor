# M6 viewer checklist (2026-11-07)

Open `web/index.html` directly in a browser (double-click), or serve it: `cd web && ../.venv/bin/python -m http.server 8765 --bind 127.0.0.1` then http://127.0.0.1:8765. Rebuild its data after any catalogue change: `.venv/bin/python scripts/build_viewer.py`. Needs internet only for the basemap (Esri street map or satellite photo) and the Leaflet 1.9.4 library (cdnjs).

Checked by Claude in Chrome on macOS, 2026-11-07 (served locally):
| Check | Result |
|---|---|
| Page loads, no console errors | ✅ |
| Map centres on the 5 km square; dashed outline shown | ✅ |
| Layer toggle (4 dates) switches overlay, legend and metadata | ✅ (30 Jun → 10 Sep checked) |
| Overlay lines up with the basemap (lagoon "always water" sits on the basemap lagoon) | ✅ by eye; UTM grid placed by lat/lon corners, ≈0.06° rotation ignored |
| Legend values match the catalogue (e.g. flood day 8.31% of the square "land got louder" = 20,781 / 250,000 px) | ✅ |
| Baseline and event dates, source scene counts, valid coverage (100%), rules, run ID / commit shown | ✅ |
| Downloads: label COG, STAC Item, receipt | ✅ links present (files in web/data/) |
| Claim text and "not a validated flood map" visible above the map | ✅ |
| Narrow (phone-width) layout stacks map above panel | ✅ |
| No secrets, no processing in the browser, no account needed | ✅ (receipts checked earlier: no project ID, keys or URLs) |
| Not checked | screen-reader pass, other browsers, slow networks |

**Note on numbers:** the legend shows shares of the *whole* square (including water). The report's "about 10%" is the share of *land* on the test side (9.4%) or the whole square's land (≈9.4–9.8%), so the two differ slightly by design.

**Not deployed.** Public hosting (e.g. GitHub Pages or Cloudflare Pages, both $0) needs the user's approval first.

**Fix 2026-11-08:** the user opened the page by double-clicking and OpenStreetMap's tile servers returned "403 Access blocked" (they refuse pages opened from a file). CARTO tiles now require a key. Switched to Esri World Street Map (default) and Esri World Imagery (option; a recent photo, not the flood day). Both checked in Chrome: they load, the layer switch works, and the lagoon overlay lines up with the lagoon in the satellite photo.
