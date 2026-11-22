# Ethena - apply checklist (#12)

- **Confidence** 75/100 - 6 concrete steps, official site linked, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect (friction 10)
- **Key date** 2027-09-30 (311 days left)
- **Official site** https://claim.ethena.fi
- **Domain check** no red flags found (score 0, age 1279d)
- **Source** https://99airdrops.com/airdrops/ethena/ (checked 2026-11-23)

## Steps as stated by the project

1. Check that you're eligible. Ethena's terms exclude "Prohibited Persons" from its campaigns and distributions, which covers citizens and residents of the United States and about 30 other jurisdictions.
2. Open claim.ethena.fi and connect the wallet you used. Warning Use only claim.ethena.fi and the two services it sends you to, Coinbase Token Manager and Sablier. No Season 6 claim exists yet, so a site that offers one isn't Ethena's.
3. For Season 5, follow the link to Coinbase Token Manager and claim your sENA.
4. For Exchange Rewards, follow the Sablier link for Ethereal or HyENA and claim your ENA.
5. For Season 6, there is nothing to claim yet. Connect your wallet on the app overview to see your final points, then wait for Ethena's announcement.
6. If you decide to leave, plan for the wait. Unstaking sENA takes 7 days, and unstaking sUSDe takes between 1 and 7 days.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://claim.ethena.fi`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://claim.ethena.fi
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Ethena" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #13.
