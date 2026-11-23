# NeoSoul - apply checklist (#18)

- **Confidence** 90/100 - 5 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect + social tasks (friction 15)
- **Key date** 2027-10-22 (333 days left)
- **Official site** https://airdrop.neosoul.ai
- **Domain check** no red flags found (score 15, age 268d)
- **Source** https://99airdrops.com/airdrops/neosoul/ (checked 2026-11-23)

## Steps as stated by the project

1. Open airdrop.neosoul.ai from NeoSoul's own X post or site, and check the address.
2. If an amount shows, press Confirm before 22 October, 16:00 UTC. After the deadline the page shows: "The confirmation window has closed."
3. Wait for delivery. The page says tokens are sent within a set number of days of your first check, "and no later than Oct 23, 2026, 00:00 (UTC+8)". It also says: "Airdrops are sent in order of first airdrop queries."
4. Before you add DNA to a wallet or trade it, compare the contract with the one in NeoSoul's paper. Many look-alike tokens appear after a launch. Warning NeoSoul says: "NeoSoul will never DM you to ask for funds, seed phrases or private keys." Anyone who messages you about your DNA allocation isn't NeoSoul.
5. For future rewards, which nobody has promised, do the Questboard tasks at event.neosoul.ai . evoevo's own terms say: "New users should consider using a dedicated test wallet or a low-value wallet before connecting a wallet that holds significant assets."

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://airdrop.neosoul.ai`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://airdrop.neosoul.ai
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "NeoSoul" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #19.
