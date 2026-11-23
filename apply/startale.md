# Startale - apply checklist (#17)

- **Confidence** 60/100 - 5 concrete steps, official site linked, deadline stated
- **Effort** wallet connect + email (friction 13)
- **Key date** 2027-10-22 (333 days left)
- **Official site** https://app.startale.com
- **Domain check** no red flags found (score 0, age 7870d)
- **Source** https://www.airdropstop.com/airdrops/startale (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Create a Startale App account Open Startale App and sign up in one click, or connect a wallet. If you already have an account, use the log-in page .
2. 2 Step 2 : Send USDC to the Soneium deposit address In the app, go to Deposit, then Bridge to Soneium, then Transfer crypto, and send USDC to the address shown there. Only USDC sent to that address counts for Promotion 1, as set out in the October missions post .
3. 3 Step 3 : Deposit USDSC into an Earn vault Make the deposit from your Startale Smart Wallet on or after 22 October 2026, and keep at least 25 USDSC in the vault for 14 consecutive days. A balance that dips below 25 USDSC in that window earns no points.
4. 4 Step 4 : Keep checking in and finish monthly missions GM check-ins, monthly missions and liquidity provision also add STAR Points, according to the STAR Points update .
5. 5 Step 5 : Watch for the points to arrive Points for a completed promotion are distributed within 72 hours. The campaign period ends on 25 November 2026.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://app.startale.com`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://app.startale.com
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Startale" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #18.
