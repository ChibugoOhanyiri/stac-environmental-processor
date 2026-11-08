# Costs and operations

Project-specific planning allowance: $0–50 for bounded EO processing. This is not authorisation to spend.


## Budget shared across all three projects
This table is one total budget, repeated for visibility. Do not add it three times. These are planning allowances, not vendor quotations or spending authorisation.

| Category | Maximum provisional allocation |
|---|---:|
| STAC EO processing | $50 |
| YOLO GPU processing | $60 |
| 3D reconstruction processing | $50 |
| Hosting/storage across projects | $20 |
| Unallocated contingency | $20 |
| Total | $200 |

Existing Claude subscription and internet excluded. API credits are not assumed included. Start at $0. Before any paid job record rate, estimated units, duration, storage, tax uncertainty and a stop condition; get approval. Budget alerts are notifications, not hard caps. Use request quotas, small AOIs, max job counts and provider-enforced limits where available. Track actual spend in a CSV: date, project, provider, units, cost, cumulative total, receipt reference. Stop before consuming the reserve without approval.

## Hosting choice
| Delivery | Benefits | Costs and maintenance |
|---|---|---|
| Repository + report + 3–5 minute video | Durable evidence, no running backend | Usually $0 hosting; refresh broken links and instructions |
| Add static interactive results viewer — recommended | Reviewer can inspect layers and evidence | Aim $0 within free allowances; check dependencies and maps monthly and before applications |
| Add live processing/query service | Demonstrates user-driven computation | Optional later; requires secrets, limits, uptime checks and recurring charges |

Cloudflare Workers static assets are suitable for the viewer. Current documented limits include 25 MiB per static asset and 20,000 files on Free. Dynamic Free Workers have 128 MB memory and 10 ms CPU/request: do not plan large raster operations or GPU training there [O1–O2]. R2 is an optional home for larger results; Standard storage is $0.015/GB-month beyond applicable allowances, plus operations; no egress charge [O3]. Basemap services have their own terms and quotas.

A public website can be static while the full processing engine remains runnable from its repository. Label precomputed outputs with run date and parameters. Do not fake a live processing button.

## Operational checklist
Before release: check source licence notices, secrets, dependency versions, browser console, mobile layout, CORS and a small reproducible example. Use a provider subdomain first; a purchased domain is optional.

After a processing session: export approved results and logs; stop GPU/compute sessions; delete temporary volumes only after verifying retained outputs; revoke temporary keys. Keep input manifests and hashes even when deleting caches. No always-on cron is required for version 1.

Monthly and before sharing: open the demo, verify download links, check billing and access, inspect dependency security updates and verify the repository still runs. A dormant archived demo should identify its data date rather than silently imply current conditions.

Platform limits/prices rechecked 2026-09-25; verify again immediately before provisioning:
- O1 https://developers.cloudflare.com/workers/platform/limits/
- O2 https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/
- O3 https://developers.cloudflare.com/r2/pricing/


## Cost categories and scenarios
- Existing Claude/Claude Code subscription: excluded from the $200 total. No extra subscription assumed.
- API calls: no paid LLM API is required by these three v1 designs. Introducing one is a new decision; a Claude subscription does not imply API credits.
- Processing: use verified free quota first. The project allowances above are contingencies, not measured forecasts. Estimate a paid run as provider rate × maximum runtime, plus storage and taxes, after a small benchmark.
- Storage: keep only required results. Illustrative R2 storage beyond any free allowance: 5 GB × $0.015 ≈ $0.075 per month, excluding operations/taxes. Actual request charges can dominate at high traffic.
- Static hosting: $0 target within applicable free limits; no purchased domain required. If 10 GB of otherwise billable Standard R2 storage were kept for 3 months, storage alone would be about $0.45 before operations/taxes.
- Live processing: not recommended for v1. Cost depends on accepted jobs, runtime and abuse prevention; do not give it an unlimited public endpoint or assume a spending alert stops jobs.
- Free notebook GPU: availability and session duration are not guaranteed. Export checkpoints/results before termination. Never run keepalive hacks to evade platform limits.

Use the shared allocations only once: STAC $50 + YOLO $60 + 3D $50 + shared hosting/storage $20 + contingency $20 = $200 total. Any reallocation requires a recorded decision, not silently increasing the total.

## Google Earth Engine (added 2026-09-27, DECISIONS S14)
Noncommercial tiers as of 2026-09-27 [G1]: **Community Tier**, 150 EECU-hours/month, **no billing account required**, for verified noncommercial projects. The Contributor Tier (1,000 EECU-hours) requires a billing account and is **not** to be enabled without approval. When quota runs out, the project enters a slower "restricted mode" rather than being charged. Use the user's personal Google account only; this is not SEE work. An EECU-hour is a unit of Google's computing time.
- G1 https://developers.google.com/earth-engine/guides/noncommercial_tiers
