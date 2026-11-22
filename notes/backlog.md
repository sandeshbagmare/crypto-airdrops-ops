# Backlog - what is next, in priority order

Living file. An agent that finishes one item takes the next and updates this list. Status values:
`ready`, `in-progress`, `blocked`, `done`.

## P0 - raises the value of every row

| # | Task | Why it matters | Status |
|---|---|---|---|
| 1 | **Date coverage.** Local crawl of `airdrops.io/project/<slug>/` pages for `claim deadline` text, then merge into `end_date`. | 524 of 548 rows have no date, so "days left" is empty where it matters most. Runs locally only (Cloudflare blocks runners). | ready |
| 2 | **Dedup across sources.** Same project appears under 2-3 trackers (e.g. Metamask, Grass). Merge into one row with a `sources[]` array. | Duplicates inflate the count and confuse the queue. Honest merge also *raises* confidence (second source = +10). | ready |
| 3 | **Merge the 45 dossier PRs** in waves of 5 after reviewing each `drops/*.md`. | Merged dossiers become the permanent record the skills read. | blocked on human review |
| 4 | **Session freshness check.** Add `--stale-after 14` to `agent_browser.py --check`, warn when a saved profile was last used long ago. | Sessions silently expire; a stale profile looks identical to a fresh one. | ready |

## P1 - makes the queue smarter

| # | Task | Why | Status |
|---|---|---|---|
| 5 | **Eligibility score.** Separate from confidence: weight "no KYC (0)", "no deposit (0)", "email only (5)", "wallet sign (10)", "KYC (30)" into a `friction` number that sorts the queue by how cheap a drop is to attempt. | Confidence says "well documented"; friction says "cheap to try". They answer different questions. | ready |
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
