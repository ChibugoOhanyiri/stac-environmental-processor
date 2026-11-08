# STAC Environmental Processor: did the satellite see the Lagos flood?

**In one sentence:** a tool that takes a reported flood, finds the radar satellite pictures of it, prepares them the same way every time, and shows what changed on the ground, with a receipt so anyone can check the work.

**First case: Lekki, Lagos, 30 June 2026.** On the flood morning (Sentinel-1 radar, 06:29), about **10% of land** in a 5 km area of Lekki showed radar brightening, against **under 1%** on an equally rainy day and on a dry day processed the same way. That held on an area the rules had never seen, under 9 different rule settings and against a dry-season baseline. It is *measured surface change consistent with the reported flood*, **not** a validated flood map: no source shows the water's edge at that time, so no accuracy number is claimed.

| Start here | What it is |
|---|---|
| [REPORT.md](REPORT.md) | The story and results in plain English |
| **[Live map](https://chibugoohanyiri.github.io/stac-environmental-processor/)** ([source](web/index.html)) | Clickable map: switch between flood day and control days |
| [evaluation/ASSESSMENT.md](evaluation/ASSESSMENT.md) | How sure we are, what was tested, failure cases |
| [catalog/](catalog/) | Results as a STAC catalogue (standard "library cards" for satellite data) |
| [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) | Reproducibility checks (a fresh install gives byte-identical files) |

**Status (2026-11-07):** milestones M1–M7 done; M8 (report, video script, CV and interview notes) drafted; video not recorded; viewer not deployed; repository private. **Cost: $0** (free tiers; [cost-ledger.csv](cost-ledger.csv)).
**Built with AI assistance:** the author directed the work, made the case and scope decisions and ran the first Earth Engine scripts; Claude (Anthropic) wrote and ran the Python code and drafted documents ([REPORT.md, "Who did what"](REPORT.md#who-did-what)).

## Run it
From the project folder on macOS (the project's computer since 2026-11-04; Python 3.13 from Homebrew):
```text
/opt/homebrew/bin/python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env            (then put your Earth Engine project ID in .env)
.venv/bin/python -c "import ee; ee.Authenticate(auth_mode='localhost')"
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python src/preprocess.py --config configs/case.json --dry-run
.venv/bin/python src/preprocess.py --config configs/case.json
```
Then the M3–M5 steps (5 km Lekki square; each command is explained in its file's header):
```text
.venv/bin/python src/preprocess.py --config configs/case_lekki5km.json      (also the control_*, after_*, dryseason_ref_* cards)
.venv/bin/python scripts/make_labels.py          (pixel labels + fig15)
.venv/bin/python scripts/sensitivity.py          (M4 rule-choice check)
.venv/bin/python src/catalog.py                  (STAC catalogue in catalog/, schema-validated)
cd catalog && ../.venv/bin/rustac serve collection.json --load-collection-items     (local search API, port 7822)
.venv/bin/python scripts/api_check.py            (in another terminal: tests searches, writes API_CAPABILITIES.md)
.venv/bin/python scripts/build_viewer.py         (then open web/index.html in a browser: the clickable map)
```
On Windows, use `py -m venv .venv` and `.venv\Scripts\python` instead. The last command saves two aligned GeoTIFFs and a receipt in `outputs/aligned/`. On the Mac, `outputs` is a shortcut (symlink) to `../stac-outputs`, so generated files live outside the repository. To study another place or date, copy `configs/case.json` and edit the copy; the code does not change. Receipts from real runs: [evidence/runs/](evidence/runs/README.md).


## Read in this order
1. INVESTIGATION.md — evidence and unresolved choices.
2. PRD.md — the complete version 1 and success criteria.
3. MILESTONES.md — the work broken into checkpoints.
4. ARCHITECTURE.md and DATA_AND_VALIDATION.md — implementation and scientific methods.
5. COSTS_AND_OPERATIONS.md — free options, budget and maintenance.


**Primary user:** An environmental GIS analyst investigating a documented flood event retrospectively. This is a portfolio research tool, not an emergency-warning service.

**Geography:** Lagos, flood of 30 June 2026 (Lekki and Victoria Island focus). Chosen 2026-09-27 from dated news and official statements plus a same-morning radar pass. Analysis area: a 5 km square of central Lekki (decision S22), after a 1 km square around Orchid Road. Pixel-level suitability checked in M1–M4.

**Capabilities:** Python, raster operations, metadata standards, cloud processing, reproducibility and scientific evaluation.

No measured accuracy or impact is claimed. Read the current milestone status before running code. This folder does not depend on either of the other projects.


Practical blank registers and review checklists are in `templates/`. `LICENSING.md` records the publication gate. No service has been purchased or deployed. Source dates describe research, not successful execution of the full pipeline.

See GLOSSARY.md for short explanations of the main technical terms.
