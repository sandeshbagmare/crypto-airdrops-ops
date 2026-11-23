# Flint - apply checklist (#12)

- **Confidence** 90/100 - 4 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** social tasks (friction 5)
- **Key date** 2027-11-20 (362 days left)
- **Official site** https://devnet.app.flint.trade
- **Domain check** no red flags found (score 15, age 173d)
- **Source** https://99airdrops.com/airdrops/flint-trade/ (checked 2026-11-23)

## Steps as stated by the project

1. Trade perps on Flint devnet. Open long or short positions, manage them and close them. Your rank is your P&amp;L on the 10,000 test USDC.
2. Send /register to the bot to get your registration link. The form asks for your X handle and a "Confirmation that you follow @Flint_Trade_ on X", and you accept the rules, terms and privacy notice.
3. Send product feedback or a bug report from the trading screen. Without it you get nothing: the rules require a "Completed registration form and product feedback or bug report(s) submitted before the End".
4. Finish both before 20 November 2026 at 11:00 UTC. Flint contacts winners on Telegram for a Solana wallet address. "If you do not give one within 14 days, you forfeit the prize."

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://devnet.app.flint.trade`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://devnet.app.flint.trade
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Flint" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #13.
