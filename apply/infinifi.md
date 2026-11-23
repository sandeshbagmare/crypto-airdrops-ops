# infiniFi - apply checklist (#2)

- **Confidence** 60/100 - 6 concrete steps, official site linked, deadline stated
- **Effort** wallet connect (friction 10)
- **Key date** 2026-12-01 (8 days left)
- **Official site** https://app.infinifi.xyz/points
- **Domain check** no red flags found (score 0, age 930d)
- **Source** https://www.airdropstop.com/airdrops/infinifi (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the Points page Go to the infiniFi Points page and check that Chapter 1 is shown as active.
2. 2 Step 2 : Connect a wallet Press Connect Wallet on the Points page so your activity can be counted toward points.
3. 3 Step 3 : Deposit stablecoins to mint iUSD Follow the deposit guide to deposit USDC and receive iUSD, or use the infiniFi app directly.
4. 4 Step 4 : Hold, stake or lock your iUSD Minting and holding iUSD is listed at 15x. Minting and staking it, or minting and locking it, is listed at 7.5x. Locking means a slower exit.
5. 5 Step 5 : Check the partner tasks The Points page also lists tasks on partner protocols, such as supplying USDC to the infiniFi vault on Morpho. Read each row&#x27;s task and multiplier before acting.
6. 6 Step 6 : Follow the chapter dates Chapter 1 ends on 1 December 2026 at 15:59 UTC. The Points Program docs explain how points are earned.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://app.infinifi.xyz/points`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://app.infinifi.xyz/points
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "infiniFi" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #3.
