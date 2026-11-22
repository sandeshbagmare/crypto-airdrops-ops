# PERPTools - apply checklist (#13)

- **Confidence** 90/100 - 5 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect (friction 10)
- **Key date** 2027-10-05 (316 days left)
- **Official site** https://app.perptools.ai
- **Domain check** no red flags found (score 0, age 380d)
- **Source** https://99airdrops.com/airdrops/perptools/ (checked 2026-11-23)

## Steps as stated by the project

1. Connect a wallet and sign the one-time registration. It creates your trading account and costs only gas.
2. Deposit USDC from Arbitrum or Solana. The docs say other networks "are not supported at this time". There is no minimum for trading.
3. Trade spot as well if you like. PERPTools says spot counts toward Season 2 points, and it advertised 0% spot trading fees on 5 October 2026.
4. Share your referral link if you want to. You get points equal to 10% of what the people you refer earn, plus a USDC reward on their trading at a base rate of 10%. Self-referrals and bot accounts are banned.
5. Open the Points page after each Friday payout to see what you received.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://app.perptools.ai`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://app.perptools.ai
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "PERPTools" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #14.
