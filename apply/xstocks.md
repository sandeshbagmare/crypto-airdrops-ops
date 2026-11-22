# xStocks - apply checklist (#5)

- **Confidence** 90/100 - 6 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect (friction 10)
- **Key date** 2026-12-04 (11 days left)
- **Official site** https://defi.xstocks.fi/points
- **Domain check** no red flags found (score 0, age 601d)
- **Source** https://99airdrops.com/airdrops/xstocks/ (checked 2026-11-23)

## Steps as stated by the project

1. Check you are allowed in. The terms say: "We currently do not permit participation by persons located in or associated with the United States or any sanctioned country." The list of other excluded countries is below.
2. Open defi.xstocks.fi/points from a link you typed yourself, connect that wallet and sign the message to register. Registering means you accept the xPoints terms. Never enter a seed phrase anywhere.
3. Hold the xStocks, or supply them to a lending market or a liquidity pool that accepts them. Points are tracked automatically.
4. Do the extras if you want: the daily spin, the social quests, protocol quests and your referral link.
5. Optionally, until 4 December 2026, buy xStocks inside Solflare for the 5% to 20% boost. Solflare does not sell xStocks in the US, Canada, the UK, Australia or Nigeria.
6. Stay active. "New accounts that show no activity and no eligibility within 7 days of registration will be automatically removed."

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://defi.xstocks.fi/points`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://defi.xstocks.fi/points
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "xStocks" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #6.
