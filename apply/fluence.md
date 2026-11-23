# Fluence - apply checklist (#22)

- **Confidence** 45/100 - 4 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://flt.fluence.ai
- **Domain check** no red flags found (score 0, age 3263d)
- **Source** https://www.airdropstop.com/airdrops/fluence (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the Fluence token app Go to the Fluence token app , which also holds staking, liquidity and DAO voting sections.
2. 2 Step 2 : Find the Pointless program card Look for the card titled Pointless program, which carries a Farm points button.
3. 3 Step 3 : Press Farm points The Farm points button on the Pointless program card opens the Pointless site. The token app does not describe what is there.
4. 4 Step 4 : Check what the Pointless site asks of you Check what the Pointless site asks of you before taking part. The token app does not say what that is.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://flt.fluence.ai`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://flt.fluence.ai
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Fluence" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #23.
