# Perle - apply checklist (#8)

- **Confidence** 90/100 - 5 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** email (friction 3)
- **Key date** 2027-03-21 (118 days left)
- **Official site** https://app.perle.xyz
- **Domain check** no red flags found (score 0, age 683d)
- **Source** https://99airdrops.com/airdrops/perle-labs/ (checked 2026-11-23)

## Steps as stated by the project

1. Open app.perle.xyz and sign in with Google, an email code or a Solana wallet such as Phantom, Solflare or Backpack. The sign-up asks for no ID.
2. If you signed in with Google or email, link a Solana wallet in Settings. Keep a little SOL in it: the app checks for at least 0.001 SOL before it records an answer on Solana.
3. Open the Marketplace and do the Educational projects first. They are the qualification step that unlocks the other projects.
4. Check your points on the Dashboard and under Earnings.
5. If you took the six-month lock in March, claim your PRL at claim.perle.xyz before 21 March 2027.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://app.perle.xyz`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://app.perle.xyz
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Perle" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #9.
