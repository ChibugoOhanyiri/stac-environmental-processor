# Local STAC API capabilities (M5)

Checked 2026-11-07 07:01 UTC by scripts/api_check.py against `rustac serve` (in-memory backend) at http://127.0.0.1:7822. Local only; not deployed.

Landing page title: (none)

## Conformance classes the server advertises (its own list, not tested one by one)

- https://api.stacspec.org/v1.0.0/core
- https://api.stacspec.org/v1.0.0/ogcapi-features
- https://api.stacspec.org/v1.0.0/collections
- http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core
- http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson
- https://api.stacspec.org/v1.0.0/item-search

## What we actually tested

| Search | Expected items | Returned | Result |
|---|---|---|---|
| Orchid box, flood week `{"bbox": [3.55, 6.425, 3.56, 6.435], "datetime": "2026-06-25T00:00:00Z/2026-07-05T00:00:00Z"}` | lekki-5km-2026-06-30-flood | lekki-5km-2026-06-30-flood | PASS |
| Orchid box, September `{"bbox": [3.55, 6.425, 3.56, 6.435], "datetime": "2026-09-01T00:00:00Z/2026-09-30T23:59:59Z"}` | lekki-5km-2026-09-10-control-wet, lekki-5km-2026-09-22-control-dry | lekki-5km-2026-09-10-control-wet, lekki-5km-2026-09-22-control-dry | PASS |
| Orchid box, any date `{"bbox": [3.55, 6.425, 3.56, 6.435]}` | lekki-5km-2026-06-30-flood, lekki-5km-2026-07-12-after, lekki-5km-2026-09-10-control-wet, lekki-5km-2026-09-22-control-dry | lekki-5km-2026-06-30-flood, lekki-5km-2026-07-12-after, lekki-5km-2026-09-10-control-wet, lekki-5km-2026-09-22-control-dry | PASS |
| Ikeja box (outside), any date `{"bbox": [3.33, 6.58, 3.36, 6.61]}` | none | none | PASS |
| Orchid box, 2025 (before data) `{"bbox": [3.55, 6.425, 3.56, 6.435], "datetime": "2025-01-01T00:00:00Z/2025-12-31T23:59:59Z"}` | none | none | PASS |

Only the searches above are claimed to work. Other advertised features (e.g. filters, sorting) were not tested here.
