# Fetch report 2026-11-28

| Source | Records | Status | Error |
|---|---|---|---|
| airdroplet | 16 | ok | - |
| airdropvillage | 0 | EMPTY - suspect | returned no rows |
| 99airdrops | 185 | ok | - |
| airdropstop | 362 | ok | - |
| airdrops.io | 0 | EMPTY - suspect | returned no rows |

- refreshed this run: **497**
- retained from previous runs (source unavailable): **61**
- failing sources: airdropvillage, airdrops.io

Retained rows keep their original `fetched` date and carry `stale_since`, so a blocked
source never silently deletes records.

