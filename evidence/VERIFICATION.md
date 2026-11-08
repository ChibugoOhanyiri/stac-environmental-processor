# Pack verification — 2026-09-25

Executed in the assistant workspace, not on the user's laptop. Python 3.12.14.

- 10 offline risk-based tests passed.
- Saved radar/optical metadata summaries generated: 4 and 5 records.
- Live public CDSE radar query completed: 4 records; IDs match the saved response: True.
- Live query timestamp: 2026-09-25T20:35:33.224912+00:00.
- No authenticated processing, image download, raster analysis or scientific accuracy evaluation ran.
- No paid resources were deployed.

## Test output
```text
test_bad_bbox_and_dates (test_discovery.DiscoveryTests.test_bad_bbox_and_dates) ... ok
test_dedup_and_pagination (test_discovery.DiscoveryTests.test_dedup_and_pagination) ... ok
test_empty_is_valid (test_discovery.DiscoveryTests.test_empty_is_valid) ... ok
test_external_next_link_rejected (test_discovery.DiscoveryTests.test_external_next_link_rejected) ... ok
test_loop_fails (test_discovery.DiscoveryTests.test_loop_fails) ... ok
test_malformed_response_rejected (test_discovery.DiscoveryTests.test_malformed_response_rejected) ... ok
test_missing_cloud_is_unknown (test_discovery.DiscoveryTests.test_missing_cloud_is_unknown) ... ok
test_missing_orbit_not_comparable (test_discovery.DiscoveryTests.test_missing_orbit_not_comparable) ... ok
test_no_silent_truncation (test_discovery.DiscoveryTests.test_no_silent_truncation) ... ok
test_real_fixture_orbits (test_discovery.DiscoveryTests.test_real_fixture_orbits) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.001s

OK
```

The live summary is saved as LIVE_RADAR_SUMMARY.json. It is a metadata smoke check, not proof that downloadable/calibrated pixels are usable. Source JSON remains unchanged.

## Re-run on the user's laptop — 2026-09-27
Run by Claude Code on the user's Windows 11 laptop (not yet by the user): Python 3.14.4 via `py`. `py -m unittest discover -s tests -v` passed all 10 tests. The saved-data summaries produced 4 radar and 5 optical records in outputs/ (git-ignored). No network request was sent by the script. Free RAM at check time: 0.9 of 7.9 GB. Free disk: about 113 GB.
