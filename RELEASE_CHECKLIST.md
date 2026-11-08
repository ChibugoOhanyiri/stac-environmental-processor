# Release checklist (M7) — checked 2026-11-07

| Check | Result | Evidence |
|---|---|---|
| Fresh clone from GitHub + fresh Python 3.13 venv from requirements.txt installs; `pip check` clean | ✅ | this run (scratch folder, deleted after) |
| All offline tests pass in the fresh clone (48) | ✅ | `python -m unittest discover -s tests` |
| Real rerun in the fresh clone (Earth Engine, 4 cards) gives **byte-identical** GeoTIFFs and label COGs to the committed/previous ones | ✅ | SHA-256 compared for flood event/reference/JRC files and all 4 labels.tif |
| Catalogue rebuilds and schema-validates in the fresh clone; viewer data rebuilds with no file changes | ✅ | `git status` clean after src/catalog.py + scripts/build_viewer.py |
| Empty search stops with a clear message | ✅ | test_empty_search_stops_loudly |
| Impossible date stops before going online | ✅ | test_impossible_date_is_caught_offline (added after the 2026-06-31 mistake) |
| Earth Engine refusal (quota, bad request) gives a plain STOPPED message, no traceback | ✅ | test_earth_engine_refusal_gives_a_plain_stop |
| No credentials in the repo; .env git-ignored; receipts contain no project ID, keys or signed URLs | ✅ | .gitignore; receipt checks (evidence/runs/README.md) |
| No billed services; no CI that calls paid services | ✅ | cost-ledger.csv (all $0); tests are offline |
| Exported outputs carry metadata and checksums | ✅ | receipts (SHA-256), STAC Items (projection, sar, sat, classification) |
| Versions pinned | ✅ | requirements.txt (re-tested 2026-11-07) |

## Known limits of the release (not hidden)
- Reproducibility holds while Earth Engine's stored Sentinel-1 and JRC data stay unchanged; a provider reprocessing would change values (the receipts' image IDs and hashes would show it).
- Backscatter COGs are local-only (git-ignored); they rebuild from the cards + receipts.
- Not tested: Windows after M5 (pystac/rustac), other browsers than Chrome, screen readers.
- The viewer is not deployed.

## Shut-down steps (nothing runs in the background)
Nothing is hosted and no scheduled jobs exist. To stop entirely: no action needed. To remove access: revoke the Earth Engine credentials file (`~/.config/earthengine/credentials`) and, if desired, delete the Cloud project in the Google Cloud console (the user's decision).
