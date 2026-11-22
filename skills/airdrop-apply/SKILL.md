---
name: airdrop-apply
description: Work through the active airdrop ledger in a crypto-airdrops-ops repo, prioritise by deadline, verify each official domain and walk the operator through completing one drop at a time. Use when asked to apply for the airdrops in the repo, pick the next airdrop to do, or check whether a listed drop is still live and safe.
---

# Airdrop apply

Turns the repo ledger into completed drops **with the operator in the loop at every step**. It never
holds a key, never signs, never passes KYC, and never claims on its own.

## Setup

Read `ledger.md` (or `ledger.xlsx`) first. If the repo has scripts, use them:

```bash
python tools/scrape_trackers.py   # refresh candidates
python tools/build_ledger.py      # rebuild ledger.md + ledger.xlsx
python tools/triage.py <url>      # domain + TLS + punycode risk check
```

Tools an agent may need, installed by the operator, never silently:

- a browser: Playwright (`pip install playwright && playwright install chromium`) or the
  `playwright-cli` skill
- for Telegram-gated drops: the operator's own Telegram app. Never ask for a login code, a phone
  number, a session file or a 2FA password
- Python 3.10+ for the repo scripts

## Priority order

1. Drops closing soonest (`Days left` smallest and >= 0)
2. `Risk` low or medium before unknown
3. `Cost` empty or "free"/no deposit before anything needing capital
4. Ties broken by `Pool (source-stated)` size, which is a signal only, never a promise

Drops with KYC, a required deposit, or a high risk rating go last, and only with explicit consent.

## The loop, one drop at a time

1. **Confirm it is live.** Open the row's source link. If the campaign ended, set `Apply status` to
   `dropped` with the reason and move on. Never guess.
2. **Find the official domain** from the project's own docs or its verified X profile. Not from the
   tracker's outbound link, not from a search ad, not from a reply.
3. **Triage it:** `python tools/triage.py <official-url>`. A `SCAM-LIKELY` verdict stops the drop
   dead. Record the verdict.
4. **Set `vetted`** only now, with the official URL recorded.
5. **Read the requirements** and state them to the operator in plain words: account? email? Telegram?
   X post? testnet faucet? deposit? KYC? Estimated time from `Time to start`.
6. **Ask before each commitment.** Creating an account, connecting a wallet, signing anything,
   posting publicly, submitting identity documents: each is a separate yes.
7. **Operator performs** the credential and identity steps. The agent does not type passwords, does
   not scan QR sessions, does not upload documents.
8. **Capture proof** into `airships/<project>/`: confirmation screenshot or tx hash.
9. **Set `submitted`** with the date and proof path. Then `paid` when tokens actually arrive.
10. **Revoke approvals** you granted, and never leave funds in a connected wallet.

## Hard refusals

- No seed phrase, private key, keystore or session file, ever, from anyone.
- No unlimited token approvals and no blind signing.
- No paying to claim, no "gas fee" to an address you do not control.
- No mass identities, no CAPTCHA-solving services, no proxy rotation, no fake phone or email
  accounts. These break every program's terms and disqualify whole farms at snapshot.
- No KYC on the operator's behalf and no fabricated identity documents.

## Reporting

For each drop report: name, official URL, triage verdict, exact requirements, honest time estimate,
what remains for the operator, and the single next action. If a drop is a dead end, say so and move
to the next row. Never mark a row complete without evidence in `airships/`.
