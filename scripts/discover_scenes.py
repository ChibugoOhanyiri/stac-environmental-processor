"""Small, read-only CDSE STAC metadata client. No imagery or processing jobs."""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

ENDPOINT = "https://stac.dataspace.copernicus.eu/v1"
COLLECTIONS = ("sentinel-1-grd", "sentinel-2-l2a")
ROOT = Path(__file__).resolve().parents[1]


def validate_bbox(values):
    if len(values) != 4 or not all(math.isfinite(x) for x in values):
        raise ValueError("bbox needs four finite numbers: west south east north")
    w, s, e, n = values
    if not (-180 <= w < e <= 180 and -90 <= s < n <= 90):
        raise ValueError("bbox must be ordered longitude/latitude; no dateline crossing")
    return values


def validate_interval(value):
    parts = value.split("/")
    if len(parts) != 2:
        raise ValueError("Use start/end ISO timestamps with explicit time zones")
    times = [datetime.fromisoformat(x.replace("Z", "+00:00")) for x in parts]
    if any(x.tzinfo is None for x in times) or times[0] >= times[1]:
        raise ValueError("Time zones are required and start must precede end")
    return value


def check_url(url):
    parsed = urlparse(url)
    if (parsed.scheme != "https" or parsed.netloc != "stac.dataspace.copernicus.eu"
            or parsed.username or parsed.password):
        raise ValueError("Only the public CDSE HTTPS catalogue is allowed")
    return url


def fetch_json(url):
    check_url(url)
    request = Request(url, headers={"Accept": "application/geo+json, application/json",
                                   "User-Agent": "chibugo-stac-learning/1.0"})
    with urlopen(request, timeout=30) as response:
        check_url(response.geturl())
        raw = response.read(10_000_001)
    if len(raw) > 10_000_000:
        raise ValueError("Metadata response exceeds the 10 MB safety bound")
    return json.loads(raw)


def collect_pages(url, fetch=fetch_json, max_pages=5):
    """Deduplicate by collection + ID; fail visibly rather than silently truncate."""
    if not 1 <= max_pages <= 20:
        raise ValueError("max_pages must be between 1 and 20")
    items, seen_urls = {}, set()
    for _ in range(max_pages):
        check_url(url)
        if url in seen_urls:
            raise ValueError("Catalogue pagination loop detected")
        seen_urls.add(url)
        page = fetch(url)
        if page.get("type") != "FeatureCollection" or not isinstance(page.get("features"), list):
            raise ValueError("Expected a STAC FeatureCollection")
        for item in page["features"]:
            if not item.get("id") or not isinstance(item.get("properties"), dict):
                raise ValueError("Malformed item: missing ID or properties")
            items[(item.get("collection", ""), item["id"])] = item
        links = [x for x in page.get("links", []) if x.get("rel") == "next"]
        if not links:
            return list(items.values())
        if len(links) != 1 or links[0].get("method", "GET").upper() != "GET":
            raise ValueError("Unsupported pagination; inspect provider documentation")
        url = urljoin(url, links[0]["href"])
    raise ValueError("Page limit reached; narrow the query or explicitly raise max-pages")


def summarise(item):
    p = item["properties"]
    return {"id": item["id"], "collection": item.get("collection"),
            "datetime_utc": p.get("datetime", p.get("start_datetime")),
            "orbit_direction": p.get("sat:orbit_state"),
            "relative_orbit": p.get("sat:relative_orbit"),
            "polarizations": p.get("sar:polarizations"),
            "tile_cloud_percent": p.get("eo:cloud_cover"), "bbox": item.get("bbox")}


def comparable_radar(a, b):
    """Metadata screen only: never proves matching footprint, calibration or flood."""
    keys = ("platform", "sat:orbit_state", "sat:relative_orbit", "sar:instrument_mode")
    pa, pb = a["properties"], b["properties"]
    return (all(pa.get(k) is not None and pa.get(k) == pb.get(k) for k in keys)
            and bool(pa.get("sar:polarizations"))
            and set(pa["sar:polarizations"]) == set(pb.get("sar:polarizations", [])))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Contact the public catalogue; no image downloads")
    parser.add_argument("--collection", choices=COLLECTIONS, default=COLLECTIONS[0])
    parser.add_argument("--bbox", nargs=4, type=float, default=[3.25, 6.4, 3.65, 6.7])
    parser.add_argument("--interval", default="2024-06-20T00:00:00Z/2024-07-15T23:59:59Z")
    parser.add_argument("--max-pages", type=int, default=5)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "scene-summary.json")
    args = parser.parse_args(argv)
    try:
        bbox = validate_bbox(args.bbox)
        interval = validate_interval(args.interval)
        if args.live:
            query = urlencode({"collections": args.collection, "bbox": ",".join(map(str, bbox)),
                               "datetime": interval, "limit": 100})
            items = collect_pages(ENDPOINT + "/search?" + query, max_pages=args.max_pages)
            source = {"mode": "live", "endpoint": ENDPOINT, "bbox": bbox, "interval": interval}
        else:
            fixture = ROOT / "evidence" / (args.collection + ".json")
            data = json.loads(fixture.read_text(encoding="utf-8"))
            if any(x.get("rel") == "next" for x in data.get("links", [])):
                raise ValueError("Saved fixture has unread pagination")
            items = data["features"]
            source = {"mode": "saved metadata", "capture_date": "2026-09-23",
                      "file": fixture.name, "note": "bbox/interval options only affect live searches"}
        result = {"generated_at_utc": datetime.now(timezone.utc).isoformat(),
                  "source": source, "count": len(items), "items": [summarise(i) for i in items],
                  "limitation": "Metadata only. No pixels processed; event suitability is unverified."}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Saved {len(items)} scene summaries to {args.output}")
        return 0
    except HTTPError as exc:
        print(f"Catalogue HTTP {exc.code}; check availability or rate limits. No processing job ran.", file=sys.stderr)
    except (ValueError, OSError, URLError, KeyError) as exc:
        print(f"Metadata search failed: {type(exc).__name__}. Check query, input files and connectivity.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
