"""M5: check the local STAC API answers searches with the items we expect.

Start the server first (separate terminal). It must run INSIDE catalog/, because it resolves the
item links from the folder it is started in:
    cd catalog && ../.venv/bin/rustac serve collection.json --load-collection-items
Then: .venv/bin/python scripts/api_check.py   (talks only to 127.0.0.1; no internet)
Writes API_CAPABILITIES.md from what the server itself advertises, plus the search test results.
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "http://127.0.0.1:7822"
ORCHID = [3.55, 6.425, 3.56, 6.435]          # small box inside the 5 km square
IKEJA = [3.33, 6.58, 3.36, 6.61]             # elsewhere in Lagos: must return nothing
CHECKS = [  # (name, search body, expected item ids)
    ("Orchid box, flood week", {"bbox": ORCHID, "datetime": "2026-06-25T00:00:00Z/2026-07-05T00:00:00Z"},
     {"lekki-5km-2026-06-30-flood"}),
    ("Orchid box, September", {"bbox": ORCHID, "datetime": "2026-09-01T00:00:00Z/2026-09-30T23:59:59Z"},
     {"lekki-5km-2026-09-10-control-wet", "lekki-5km-2026-09-22-control-dry"}),
    ("Orchid box, any date", {"bbox": ORCHID},
     {"lekki-5km-2026-06-30-flood", "lekki-5km-2026-07-12-after", "lekki-5km-2026-09-10-control-wet",
      "lekki-5km-2026-09-22-control-dry"}),
    ("Ikeja box (outside), any date", {"bbox": IKEJA}, set()),
    ("Orchid box, 2025 (before data)", {"bbox": ORCHID, "datetime": "2025-01-01T00:00:00Z/2025-12-31T23:59:59Z"}, set()),
]


def call(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def main() -> int:
    try:
        landing = call("/")
    except OSError as exc:
        print(f"STOPPED: no server at {API} ({exc}). Start it first (see the docstring).")
        return 1
    conformance = call("/conformance")["conformsTo"]
    results, ok_all = [], True
    for name, body, expected in CHECKS:
        got = {f["id"] for f in call("/search", {**body, "limit": 50})["features"]}
        ok = got == expected
        ok_all &= ok
        results.append((name, body, sorted(expected), sorted(got), ok))
        print(f"{'PASS' if ok else 'FAIL'}  {name}: got {sorted(got)}")
    lines = ["# Local STAC API capabilities (M5)", "",
             f"Checked {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by scripts/api_check.py against "
             f"`rustac serve` (in-memory backend) at {API}. Local only; not deployed.", "",
             f"Landing page title: {landing.get('title', '(none)')}", "",
             "## Conformance classes the server advertises (its own list, not tested one by one)", ""]
    lines += [f"- {c}" for c in conformance]
    lines += ["", "## What we actually tested", "", "| Search | Expected items | Returned | Result |", "|---|---|---|---|"]
    lines += [f"| {n} `{json.dumps(b)}` | {', '.join(e) or 'none'} | {', '.join(g) or 'none'} | {'PASS' if ok else 'FAIL'} |"
              for n, b, e, g, ok in results]
    lines += ["", "Only the searches above are claimed to work. Other advertised features (e.g. filters, sorting) "
              "were not tested here."]
    (ROOT / "API_CAPABILITIES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote API_CAPABILITIES.md")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
