# Doppler Finance - apply checklist (#2)

- **Confidence** 60/100 - 5 concrete steps, official site linked, deadline stated
- **Effort** wallet connect (friction 10)
- **Key date** 2026-11-28 (5 days left)
- **Official site** https://app.doppler.finance/airdrop
- **Domain check** no red flags found (score 0, age 686d)
- **Source** https://www.airdropstop.com/airdrops/doppler-finance (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the official claim portal Go to the XDP claim portal .
2. 2 Step 2 : Connect the Base wallet you registered Only the Base address entered during registration can claim its allocation, so connect that wallet.
3. 3 Step 3 : Review your XDP allocation Once the registered wallet is connected, the portal shows how much XDP is allocated to it.
4. 4 Step 4 : Approve the claim in your wallet Approve the transaction in your wallet to receive the XDP. Claims close on 28 November 2026 at 12:00 UTC.
5. 5 Step 5 : Optionally stake XDP for Season 3 points Staked XDP earns Doppler Points at a 20× boost during Season 3. Staking is done on the XDP Staking Portal , and the documentation covers eligibility.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://app.doppler.finance/airdrop`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://app.doppler.finance/airdrop
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Doppler Finance" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #3.
