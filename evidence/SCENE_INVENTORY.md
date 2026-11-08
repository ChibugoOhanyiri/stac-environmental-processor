# Scene inventory

Metadata captured 2026-09-23; report assembled 2026-09-25. Full JSON responses are beside this file. No imagery pixels have been read.

Search bbox: [3.25, 6.40, 3.65, 6.70]. Interval: 2024-06-20T00:00:00Z/2024-07-15T23:59:59Z. This is a discovery envelope, not the final analysis boundary.

| Collection | Scene ID | Acquisition UTC | Direction / relative orbit | Tile cloud % |
|---|---|---|---|---|
| sentinel-1-grd | `S1A_IW_GRDH_1SDV_20240621T053018_20240621T053047_054417_069F0A_DD9B_COG` | 2024-06-21T05:30:18.437523Z | descending / 95 | not applicable |
| sentinel-1-grd | `S1A_IW_GRDH_1SDV_20240626T180210_20240626T180235_054498_06A1D2_3AD3_COG` | 2024-06-26T18:02:10.270216Z | ascending / 1 | not applicable |
| sentinel-1-grd | `S1A_IW_GRDH_1SDV_20240703T053017_20240703T053046_054592_06A521_BC59_COG` | 2024-07-03T05:30:17.566088Z | descending / 95 | not applicable |
| sentinel-1-grd | `S1A_IW_GRDH_1SDV_20240715T053017_20240715T053046_054767_06AB2E_1FD1_COG` | 2024-07-15T05:30:17.448459Z | descending / 95 | not applicable |
| sentinel-2-l2a | `S2A_MSIL2A_20240623T100031_N0510_R122_T31NEH_20240623T153951` | 2024-06-23T10:00:31.024000Z | descending / 122 | 85.98 |
| sentinel-2-l2a | `S2B_MSIL2A_20240628T095549_N0510_R122_T31NEH_20240628T125340` | 2024-06-28T09:55:49.024000Z | descending / 122 | 90.35 |
| sentinel-2-l2a | `S2A_MSIL2A_20240703T100031_N0510_R122_T31NEH_20240703T152144` | 2024-07-03T10:00:31.024000Z | descending / 122 | 99.99 |
| sentinel-2-l2a | `S2B_MSIL2A_20240708T095549_N0510_R122_T31NEH_20240708T131730` | 2024-07-08T09:55:49.024000Z | descending / 122 | 100.0 |
| sentinel-2-l2a | `S2A_MSIL2A_20240713T100031_N0510_R122_T31NEH_20240713T154556` | 2024-07-13T10:00:31.024000Z | descending / 122 | 95.32 |

The June 21 / July 3 / July 15 Sentinel-1 observations share descending relative orbit 95. July 3 at 05:30 UTC is 06:30 WAT. Matching metadata is necessary but does not establish matching usable pixels or event timing. The June 26 ascending scene is not an interchangeable baseline.
Sentinel-2 cloud values describe the whole tile, not the final AOI. Missing radar cloud metadata is not zero cloud or proof of flood visibility.
