# Rabby Wallet - apply checklist (#10)

- **Confidence** 60/100 - 4 concrete steps, official site linked, deadline stated
- **Effort** wallet connect (friction 10)
- **Key date** 2027-10-29 (340 days left)
- **Official site** https://rabby.io/points
- **Domain check** no red flags found (score 0)
- **Source** https://www.airdropstop.com/airdrops/rabby-wallet (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the Rabby Points page Go to the Rabby Points page , which opens with the invitation to Rabby Points and two routes in: browser extension or mobile beta.
2. 2 Step 2 : Install the browser extension Download the Rabby Wallet browser extension from the install link on that page.
3. 3 Step 3 : Migrate your address and open Rabby Points Migrate your address into Rabby Wallet, then go to Rabby Points.
4. 4 Step 4 : Or use the Mobile Beta On mobile, download Rabby Wallet Mobile Beta, then connect your wallet and go to Rabby Points. The Google Play, Android APK and App Store listings showed as under review on 29 October 2026.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://rabby.io/points`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://rabby.io/points
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Rabby Wallet" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #11.
