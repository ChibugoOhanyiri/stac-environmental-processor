# Product requirements — STAC Environmental Processor

## Problem and user journey
An analyst has a reported flood event but must discover whether satellites observed it, produce comparable imagery, analyse changes and explain uncertainty. The tool makes those steps reproducible and inspectable.

User journey: select an approved case → inspect available acquisitions → choose comparable baseline/event images → run a bounded pipeline → inspect water-change layers and uncertainty → download outputs and provenance.

## Complete version 1
1. Configurable AOI/date search using an existing STAC provider, saved metadata and explicit acquisition gaps.
2. Radar preprocessing via a documented cloud workflow; optional optical interpretation when usable.
3. Baseline and change analysis with nodata, persistent-water and ambiguous-pixel handling.
4. Georeferenced raster outputs, valid-area statistics and provenance manifest.
5. STAC catalogue describing derived outputs; a locally runnable discovery API with documented supported capabilities. Use a maintained STAC implementation rather than claiming compliance from a few custom routes.
6. Repeatable run command with job status, caching, failures and parameter tracking.
7. Static interactive viewer, report, evaluation, reproducible sample and video.

Required interface controls: layer toggle, baseline/event dates, uncertainty legend, source metadata, measured valid coverage, parameter display and downloadable evidence. Public arbitrary processing is optional after v1.

## Acceptance criteria
| ID | Requirement | Verification |
|---|---|---|
| F1 | Reproduce a search for an approved AOI/date interval | Saved request, item IDs and retrieval time; bounded pagination; duplicate handling |
| F2 | Process a documented sample twice | Same inputs/config produce comparable outputs within a stated numeric tolerance |
| F3 | Preserve CRS, transform, nodata and source units | Inspect raster metadata and alignment; known synthetic geometry check |
| F4 | Separate valid change, persistent water and unobserved/ambiguous areas | Legend and statistics agree; nodata never becomes dry land |
| F5 | Publish searchable derived assets | Schema validation, valid links and advertised API conformance tests |
| F6 | Explain each displayed statistic | Unit, valid denominator, method and input date visible |
| F7 | Demonstrate failures clearly | Empty search, missing band, clouded AOI and failed remote job produce actionable messages |
| F8 | Deliver evidence | Repository, small rerun, report, interactive viewer and video |

Scientific acceptance: evaluation follows DATA_AND_VALIDATION.md; results include failure cases and timing uncertainty. No fixed accuracy threshold is asserted before reference suitability is known. Freeze any quantitative target before the held-out evaluation. If references cannot justify a flood-accuracy claim, state the reduced claim explicitly rather than conceal the limitation.

## Out of scope
Real-time warning, rainfall-runoff prediction, street-level safety advice, flood depths, insured-loss estimates, automatic attribution to climate change, unrestricted public compute and nationwide processing. Port Harcourt is a later transfer case.

## Distinct claims
Observed surface-water change = a measured difference between observations. Evidence consistent with flooding = interpreted change linked to event context. Validated flood extent = tested against suitable references. Flood risk/prediction requires additional modelling and is not this product.
