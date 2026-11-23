# InterLink Labs - apply checklist (#25)

- **Confidence** 45/100 - 5 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://interlinklabs.ai/download
- **Domain check** no red flags found (score 0, age 779d)
- **Source** https://www.airdropstop.com/airdrops/interlink-labs (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Get an invite code from a member Joining requires a code from someone who is already a member, so ask an existing miner for theirs.
2. 2 Step 2 : Download the InterLink app Install the app from the download page or the App Store .
3. 3 Step 3 : Tap to mine every day Open the app and tap to mine. Each tap accumulates a free asset, and the project&#x27;s chain page says to transfer your ITL to the ITLX Wallet to make it an on-chain asset. Mining is free, and a mining group raises the rate for everyone in it.
4. 4 Step 4 : Follow the ITLG Mainnet KYC The app page carries the project&#x27;s posts about the upcoming ITLG KYC portal. Those posts name account metrics, badges and ITL balance as factors in receiving ITLG, and say that passing Level 1 KYC makes you eligible to sponsor others.
5. 5 Step 5 : Move ITL to the ITLX Wallet if you want it on-chain The ITLX Wallet is the project&#x27;s non-custodial wallet. According to the chain page, ITL transferred to it becomes an on-chain asset on Interlink Mainnet.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://interlinklabs.ai/download`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://interlinklabs.ai/download
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "InterLink Labs" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #26.
