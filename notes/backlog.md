# Backlog - what is next, in priority order

Living file. An agent that finishes one item takes the next and updates this list. Status values:
`ready`, `in-progress`, `blocked`, `done`.

## P0 - raises the value of every row

| # | Task | Why it matters | Status |
|---|---|---|---|
| 1 | **Date coverage.** `tools/extract_dates.py` lifts dates from verified text (24 found, 18 within 30 days). airdrops.io **cards carry no date** and project pages only show a global "ending soon" sidebar - verified with `tools/probe_io.py`, so that route is closed. Next: try alphadrops/cryptorank alternatives locally. | Dates are the weakest axis; the honest ceiling from current sources is ~24. | blocked on a dated source |
| 2 | **Dedup across sources.** Done: `tools/dedupe.py` found 4 groups (Orbinum, Rome, NUVA, FLOP) covering 8 rows; 548 -> 544 unique, merged with a `+` source list. | Corpus was already near-unique. | done |
| 3 | **Merge the 45 dossier PRs** in waves of 5 after reviewing each `drops/*.md`. | Merged dossiers become the permanent record the skills read. | blocked on human review |
| 4 | **Session freshness check.** Done: `agent_browser.py --check --stale-after 14` warns when a profile has not been used recently. | Sessions expire silently. | done |

## P1 - makes the queue smarter

| # | Task | Why | Status |
|---|---|---|---|
| 5 | **Eligibility score.** Done: `friction` 0-100 with driver labels (KYC 30, deposit 25, wallet 10, social 5, email 3), negations ignored ("no KYC" no longer counts) and conditional costs need a "required" word. 164 drops are free/no-identity, 43 need KYC. Site sorts by "Cheapest first". | Confidence says "well documented"; friction says "cheap to try". | done |
| 6 | **Claim-window monitor.** For each submitted drop, poll the official domain weekly for "claim" + a date, and open an issue when a window opens or closes in under 7 days. | The reward is lost at the claim step, not at the registration step. | ready |
| 7 | **Per-drop evidence folders.** `airships/<project>/` with screenshot + tx hash + the exact URL used. | A "submitted" row with no evidence is a claim, not a record. | ready |
| 8 | **Watchlist trend.** Store each domain's verdict history so a changed owner or a sudden registrar transfer is visible. | Domain handovers are the main way a clean link becomes dangerous. | ready |

## P2 - breadth

| # | Task | Why | Status |
|---|---|---|---|
| 9 | **Two more sources** with dated rows (cryptorank, alphadrops). | Volume is already 548; dates are the bottleneck, not drops. | ready |
| 10 | **Category tags.** testnet / points / quest / NFT / retroactive - so the site can filter by effort type. | "What kind of work is this" is the first question an operator asks. | ready |
| 11 | **Non-English trackers** (Japanese, Turkish, Vietnamese communities often list drops a month early). | Early listing = cheaper participation. | ready |
| 12 | **Changelog page** on the site: what changed each day, from `data/fetch-report.md`. | Trust comes from seeing the diffs, not the totals. | ready |

## Blocked - cannot be automated here, by design

| Task | Reason |
|---|---|
| Passing KYC | Legal boundary; identity acts cannot be delegated |
| Entering account passwords | The human logs in once; the profile persists |
| Signing transactions | Money risk; agent must never pre-approve |
| CAPTCHA solving, proxy rotation, mass accounts | Fraud, and grounds for voided allocations |
| airdrops.io from CI | Cloudflare blocks datacenter IPs (HTTP 403) |
| 15 airdropvillage rows | That source has no per-project page to verify against |

## Recently done

- 533 of 548 drops deep-verified; confidence + steps + official site + costs + risks extracted
- 448 official domains forensically checked (RDAP age, DNS, TLS) into `data/forensics.json`
- `notes/watchlist.md` separates **dead links** (59 - stale tracker rows) from **suspicious domains**
  (11 - young registrations, not accusations)
- 45 verification PRs, each with a dossier; CI gate `validate-drops` on every one
- Label-gated auto-merge, daily refresh now opens a PR instead of pushing to `main`
- Persistent browser sessions proven across restarts
