# Trueo - apply checklist (#3)

- **Confidence** 90/100 - 5 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect + social tasks (friction 15)
- **Key date** 2027-01-31 (69 days left)
- **Official site** https://trueo.com
- **Domain check** no red flags found (score 0, age 5309d)
- **Source** https://99airdrops.com/airdrops/trueo/ (checked 2026-11-23)

## Steps as stated by the project

1. Open trueo.com and connect a wallet you control. Signing in is a message signature and costs no gas.
2. Get TYD with USDC on the app's TYD page.
3. Pick one of the activities the app names: trade or propose a market, fund someone else's proposal, provide liquidity in a market, or stake TRUE.
4. If you propose a market, keep to events that resolve before 31 January 2027, as the page asks.
5. Follow @Trueo_ on X for the Ethereum launch and any reward terms. TRUE holders will be able to migrate, and Trueo says: "There will be no migration cut-off."

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://trueo.com`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://trueo.com
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Trueo" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #4.
