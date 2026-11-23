# Acki Nacki - apply checklist (#18)

- **Confidence** 45/100 - 5 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://ackinacki.com/wallet
- **Domain check** no red flags found (score 0, age 1109d)
- **Source** https://www.airdropstop.com/airdrops/acki-nacki (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the Acki Nacki App Start from the Acki Nacki App , which the project&#x27;s homepage calls its interface to the network.
2. 2 Step 2 : Mine NACKL Use the app&#x27;s mining feature, the first thing the homepage invites visitors to do. NACKL coins are described there as mined only as block rewards.
3. 3 Step 3 : Complete tasks and mint Popits Work through the tasks the app offers and mint Popits, the other two activities named on the homepage.
4. 4 Step 4 : Get the Acki Nacki Wallet The homepage links a wallet download for managing NACKL.
5. 5 Step 5 : Read the tokenomics The tokenomics paper explains the NACKL and SHELL tokens and how rewards are divided.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://ackinacki.com/wallet`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://ackinacki.com/wallet
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Acki Nacki" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #19.
