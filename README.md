# crypto-airdrops-ops

Public research ledger of active crypto airdrops: requirements, deadlines, time to start, risk and
source-stated pool size.

**548 projects tracked as of 2026-11-23**, from five sources: airdroplet (dossiers), airdropvillage
(badges), 99airdrops (cards), airdropstop and airdrops.io (both client-rendered, parsed with
Playwright). Every row carries its source URL; nothing is invented.

airdrops.io also publishes per-project requirement flags, so the ledger can tell you which drops
need Telegram, an X post, an email address or KYC before you start: 34 need Telegram, 69 need an
X post, 54 need email, 19 require KYC.

## For autonomous agents

Start at **[AGENTS.md](AGENTS.md)** - it is the whole operating context: schema, script order,
selection policy, per-drop loop, handoff contract, session model and the four hard boundaries.

- `agent/STATE.json` - live queue, 522 drops with `status`, `blocked_on`, `next_action`
- `agent/handoffs/*.json` - 393 pre-written packets for every drop that needs a human (KYC, login,
  wallet signature, email), each with the exact steps, official URL and resume command
- `agent/sessions/<identity>/` - Playwright persistent profiles; you log in once, the session
  survives restarts. Gitignored, because a profile is equivalent to a login.
- `BLOCKERS.md` - what is deliberately not automated, and why

Classified queue: 231 need a wallet signature, 129 need nothing human-only, 95 need a Telegram/X
session, 43 need KYC, 24 need an email click. An agent can work the 129 alone; the rest resume from
its handoff file the moment the operator does their part.

```bash
python tools/agent_bootstrap.py --top 30     # rebuild the queue and packets
python tools/agent_browser.py --identity main --url <official>   # login window + saved session
```

## Browser site

**https://sandeshbagmare.github.io/crypto-airdrops-ops/** - searchable, filterable by confidence,
shows each project's steps, official site, who is behind it, costs and risks. Served from `docs/`
via GitHub Pages; regenerate with `python tools/build_site.py`.

## How confidence is scored

Confidence is computed only from evidence found in a project's own guide page:

| Evidence | Points |
|---|---|
| Concrete steps listed | +25 |
| Official site linked in the guide | +20 |
| Deadline or snapshot stated | +15 |
| Operator or team named | +15 |
| Costs and fees disclosed | +10 |
| A second independent source lists it | +10 |
| Risks or eligibility caveats disclosed | +5 |
| No steps found | -15 |

It measures **how well documented** a drop is. It is not a prediction that it pays, and a high score
is not an endorsement.

## Legal and ethical scope

This repo aggregates **publicly available** information and links back to the original source for
every row. That is the ordinary activity of a news aggregator or a search index. Specific care:

- **No accusations.** The repo does not label any named project a scam. Where a source reports risk,
  that risk is quoted with attribution. Unverifiable claims about real companies would be defamatory.
- **No credentials.** Nothing here asks for, stores or transmits a seed phrase, private key, session
  file or identity document. Those are refused by design in every script and skill.
- **No bypassing access controls.** Only public pages are fetched, at a modest rate. When a site
  blocks automated access with HTTP 403 or a bot challenge, the source is recorded as blocked and its
  rows keep their last-checked date rather than being scraped around.
- **No financial advice and no solicitation.** Pool sizes are quoted as the source states them, never
  as an expected return. Nothing here is an offer, a recommendation, or a promise of profit.
- **Trademarks** belong to their owners; project names are used descriptively to identify the drop.
- Airdrop terms are set by each project. Following them is the operator's responsibility, and the
  rules below exist to keep participation honest rather than sybil-farmed.

## What's here

| Path | Purpose |
|---|---|
| `ledger.md` | The table, with a "closing within 30 days" section up top |
| `ledger.xlsx` | Same data: filters, `Apply status` dropdown, summary sheet |
| `data/airdrops.json` | Machine-readable source of truth, with per-record provenance |
| `tools/scrape_trackers.py` | Fetches all five trackers; renders two of them with Playwright |
| `tools/build_ledger.py` | Rebuilds `ledger.md` + `ledger.xlsx` from the JSON |
| `tools/triage.py` | Domain forensics: RDAP age, punycode/homoglyph, TLS, DNS, scam verdict |
| `tools/monitor.py` | Nightly diff of trackers, append-only change log |
| `skills/` | Agent skills: `airdrop-recon`, `airdrop-apply`, `airdrop-agent` |
| `airships/` | Proof per project: confirmation screenshots, tx hashes |
| `.github/workflows/update.yml` | Refreshes everything daily at 03:30 UTC |

## Automated updates

`.github/workflows/update.yml` runs the scrape and rebuild every day and commits the result. No
laptop needs to stay on. Manual run:

```bash
python tools/scrape_trackers.py
python tools/build_ledger.py
```

## Fields, and what they mean

| Field | Meaning |
|---|---|
| `Status` | The tracker's own call, e.g. `Wait`, `No fixed deadline` |
| `KYC / requirements` | Concatenated tracker facts: deposit, fees, capital, KYC |
| `Time to start` | Tracker's stated time to begin the tasks |
| `Risk` | Tracker's risk rating. `high` is a warning, not a detail |
| `Days left` | Computed from `Ends`. Negative means it closed |
| `Pool (source-stated)` | Prize size **as stated by the source**. Not an expected payout |
| `Apply status` | `identified -> vetted -> in-progress -> submitted -> paid`, or `dropped` |

## Reading this honestly

- A tracker listing is **not** verification. Before any wallet connects, confirm the official domain
  on the project's own docs and run `python tools/triage.py <url>`.
- Pool size is not profit. Allocation per participant is usually unknown and often tiny.
- `Wait` means the source itself says the reward route is unconfirmed.
- Many drops require identity verification or a working testnet wallet. Those are operator steps.

## Safety rules

1. Burner wallet only. Never one holding real funds.
2. Official domain typed or bookmarked, never clicked from chat, DM, or a search ad.
3. No seed phrase, no private key, no unlimited approval, no upfront claim fee. All scams.
4. Revoke approvals after every session.
5. No mass identities, CAPTCHA services, or fake accounts.

## Skills

```bash
cp -r skills/* ~/.agents/skills/     # install for your agent
```

- **airdrop-recon** - read-only vetting: official-domain check, scam checklist
- **airdrop-apply** - works the ledger one drop at a time, operator approves every commitment
- **airdrop-agent** - SKILL.md for the `aa` CLI toolkit (radar, quests, testnets)
