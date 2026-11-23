# BULK - apply checklist (#13)

- **Confidence** 75/100 - 4 concrete steps, official site linked, operator/team named, costs disclosed, risks disclosed
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://app.bulk.trade
- **Domain check** no red flags found (score 0, age 1121d)
- **Source** https://99airdrops.com/airdrops/bulk/ (checked 2026-11-23)

## Steps as stated by the project

1. Sign up at app.bulk.trade through that link. A referred trader gets a "+5% Trading AURA boost".
2. Deposit USDC, the margin and settlement currency.
3. Trade, then check your AURA and your league on the AURA page .
4. Once you trade, you get your own referral link. BULK pays referrers "1 AURA for every 4 Trading AURA they earn" plus 10% of the net fees of the traders they bring in directly, paid weekly in USDC.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://app.bulk.trade`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://app.bulk.trade
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "BULK" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #14.
