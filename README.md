# crypto-airdrops-ops

Public research ledger of active crypto airdrops: requirements, deadlines, time to start, risk and
source-stated pool size.

**548 projects tracked as of 2026-11-23**, from five sources: airdroplet (dossiers), airdropvillage
(badges), 99airdrops (cards), airdropstop and airdrops.io (both client-rendered, parsed with
Playwright). Every row carries its source URL; nothing is invented.

airdrops.io also publishes per-project requirement flags, so the ledger can tell you which drops
need Telegram, an X post, an email address or KYC before you start: 34 need Telegram, 69 need an
X post, 54 need email, 19 require KYC.

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
