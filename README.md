# crypto-airdrops-ops

Private workspace for crypto airdrop research, vetting and record keeping.

**Operator goal:** fully complete 25 free-entry airdrops, then keep going to 100.

**Current state (2026-11-22):** 17 candidates identified from public trackers, 0 verified
official, 0 started, 0 completed. See [ledger.md](ledger.md) and [ledger.xlsx](ledger.xlsx).

## Layout

| Path | Purpose |
|---|---|
| `ledger.md` | Human-readable candidate table with per-row source |
| `ledger.xlsx` | Same data with status validation, filters and a summary sheet |
| `tools/build_ledger.py` | Regenerates both files from the candidate list |
| `skills/airdrop-recon/` | Read-only vetting skill: official-domain check, scam checklist |
| `skills/airdrop-agent/` | SKILL.md of the `aa` toolkit used for radar, quests, testnets |
| `airships/` | Confirmation screenshots, one folder per project |
| `notes/` | Per-project scratch research |

## Safety rules

1. Burner wallet only. Never a wallet holding real funds.
2. Official domain typed or bookmarked, confirmed on the project's own docs. Never from a chat,
   a DM, a search ad, or a reply.
3. No seed phrase, no private key, no unlimited approval, no upfront "claim fee". All three are scams.
4. Revoke approvals after every quest session.
5. No mass identities, CAPTCHA-solving services, or fake accounts.

## Why the ledger has candidates, not completions

A candidate list is producible from public sources. Actually completing a drop needs decisions and
credentials that belong to the operator: which burner wallet, whether KYC is acceptable, and the
clicks on each site. Rows move through `identified -> vetted -> in-progress -> submitted -> paid`
only when real evidence exists.

## Regenerate the ledger

```bash
python tools/build_ledger.py
```

## The `aa` toolkit

Installed in a local venv (`airdrop-agent` v4.1.0, MIT). It lives outside this repo.

```bash
aa doctor      # environment check
aa status      # identities, wallets, mode
aa radar scan  # find candidates
```
