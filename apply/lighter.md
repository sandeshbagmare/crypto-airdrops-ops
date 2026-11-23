# Lighter - apply checklist (#14)

- **Confidence** 75/100 - 4 concrete steps, official site linked, operator/team named, costs disclosed, risks disclosed
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://docs.lighter.xyz/points-program/lighter-on-robinhood-chain-points
- **Domain check** no red flags found (score 0)
- **Source** https://99airdrops.com/airdrops/lighter/ (checked 2026-11-23)

## Steps as stated by the project

1. Read the program terms . They exclude the US, the UK, Canada and 15 other countries.
2. Set up Robinhood Wallet for the 2x rate, or open robinhoodchain.lighter.xyz with another wallet for 1x.
3. Get USDG on Robinhood Chain and deposit it as margin.
4. Trade perpetual futures. Part of your points balance updates as you trade, and the rest arrives in the Friday drop.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://docs.lighter.xyz/points-program/lighter-on-robinhood-chain-points`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://docs.lighter.xyz/points-program/lighter-on-robinhood-chain-points
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Lighter" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #15.
