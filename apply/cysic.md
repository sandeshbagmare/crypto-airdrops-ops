# Cysic - apply checklist (#21)

- **Confidence** 45/100 - 4 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://cysic.xyz
- **Domain check** no red flags found (score 0)
- **Source** https://www.airdropstop.com/airdrops/cysic (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the Cysic homepage Go to the Cysic homepage and find the NFT-to-CYS redemption section with its &quot;claim CYS&quot; button.
2. 2 Step 2 : Check the unlock schedule The redemption unlocks 50% of the CYS at TGE and the remaining 50% linearly over 6 months, so the full amount is not available at once.
3. 4 Step 4 : Read how contributors earn on the network The Cysic docs explain the roles of compute contributors, requesters and verifiers. Contributors enrol their machines, take on jobs and are paid once the results are verified.
4. 5 Step 5 : Note the app link in the blog navigation The Cysic blog&#x27;s navigation links to the Cysic app under the label &quot;Start earning with your device&quot;. Cysic does not say whether using the app affects the CYS claim.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://cysic.xyz`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://cysic.xyz
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Cysic" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #22.
