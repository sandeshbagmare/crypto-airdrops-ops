# Garth - apply checklist (#24)

- **Confidence** 45/100 - 5 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://garthonqubic.com
- **Domain check** no red flags found (score 0, age 494d)
- **Source** https://www.airdropstop.com/airdrops/garth (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Get a Qubic mobile wallet Download the Qubic mobile wallet from Google Play and set it up. The Garth homepage names a wallet as the first requirement.
2. 2 Step 2 : Get some Qubic Add Qubic to that wallet. The homepage&#x27;s second step is to get some Qubic, which is then traded for Garth.
3. 3 Step 3 : Trade Qubic for Garth Place a limit order or use the qswap exchange to acquire Garth with your Qubic, as the Garth homepage outlines.
4. 4 Step 4 : Register your wallet on Zealy Open the Garth page on Zealy and register your wallet to participate in the airdrop.
5. 5 Step 5 : Check your mercy list status Use the status check on the Garth homepage to check whether your wallet is on the mercy list for the current epoch, and look at the weekly and Termination Party airdrop tabs.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://garthonqubic.com`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://garthonqubic.com
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Garth" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #25.
