# SoSoValue - apply checklist (#9)

- **Confidence** 60/100 - 6 concrete steps, official site linked, deadline stated
- **Effort** wallet connect (friction 10)
- **Key date** 2027-05-21 (179 days left)
- **Official site** https://ssi.sosovalue.com/reward
- **Domain check** no red flags found (score 0)
- **Source** https://www.airdropstop.com/airdrops/sosovalue (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the SSI rewards site Go to the SSI reward page and read the Epoch 5 details, which show the 21 May to 17 November 2026 schedule and the 15,000,000 SOSO pool.
2. 2 Step 2 : Connect a wallet Use the Connect Wallet button on the SSI site so your holdings and points are tied to one wallet.
3. 3 Step 3 : Get an SSI token Buy one of the SSI index tokens through the SSI site. Points are only counted for SSI tokens you hold, stake or lock.
4. 4 Step 4 : Hold or stake your SSI Keep the tokens in your wallet, stake them on the rewards page, or lock them in a Uni LP position. Your daily share of the 100,000,000 points depends on how much you hold and stake compared with other users.
5. 5 Step 5 : Optionally stake SOSO for a boost Staking SOSO beside your SSI tokens increases your loyalty points. A boost of at least 1% is required to take part in it.
6. 6 Step 6 : Wait for the distribution Rewards are paid after Epoch 5 ends, following SoSoValue&#x27;s final announcement. The EXP page separately lists Season 3 activity.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://ssi.sosovalue.com/reward`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://ssi.sosovalue.com/reward
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "SoSoValue" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #10.
