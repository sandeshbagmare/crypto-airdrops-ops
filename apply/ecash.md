# eCash - apply checklist (#9)

- **Confidence** 60/100 - 4 concrete steps, official site linked, deadline stated
- **Effort** free / no identity (friction 0)
- **Key date** 2027-10-29 (340 days left)
- **Official site** https://ecash.com/how-to-claim
- **Domain check** no red flags found (score 0, age 11439d)
- **Source** https://www.airdropstop.com/airdrops/ecash (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Move BTC into self-custody Keep the BTC at an address whose keys you control before block 973,728. For BTC left on an exchange, crediting is up to that exchange. The access guide explains the custody options.
2. 2 Step 2 : Get the official eCash wallet Download the wallet from the eCash download page , since splitting your coins later is done with it.
3. 3 Step 3 : Hold through the mainnet snapshot Nothing needs to be registered or claimed. ECX is credited to your address at block 973,728, estimated for 29 October 2026; the eCash homepage shows the countdown.
4. 4 Step 4 : After the fork, split before moving BTC Once the mainnet fork has happened, wait for the official wallet guidance, read the coin-splitting guide , then split with the official wallet. Do this before any BTC is moved, or that transaction can replay on eCash and send your ECX to the recipient.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://ecash.com/how-to-claim`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://ecash.com/how-to-claim
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "eCash" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #10.
