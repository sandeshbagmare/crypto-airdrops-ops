# Fraction AI - apply checklist (#23)

- **Confidence** 45/100 - 5 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://fractionai.xyz/dapp/index
- **Domain check** no red flags found (score 0, age 1152d)
- **Source** https://www.airdropstop.com/airdrops/fraction-ai (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open Index Go to Index , the Fraction AI app, from the Start Trading button on the homepage at fractionai.xyz .
2. 2 Step 2 : Take the guided tour Index opens with a welcome guide named Aria that offers a Perps tour and a Tokens tour. Pick one to see how that part of the app works.
3. 3 Step 3 : Try perps with paper funds Open the perps view and open a practice position in a market of your choice using the paper balance, without real money.
4. 4 Step 4 : Read an agent&#x27;s record In a market, compare each agent&#x27;s side, 30-day return, Sharpe ratio and recent trades before you form your own view.
5. 5 Step 5 : Browse the Tokens tab Open the Tokens tab to see lists such as Trending, New and Smart money, and use the token checks before any purchase.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://fractionai.xyz/dapp/index`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://fractionai.xyz/dapp/index
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Fraction AI" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #24.
