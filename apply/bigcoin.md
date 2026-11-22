# Bigcoin - apply checklist (#10)

- **Confidence** 60/100 - 3 concrete steps, official site linked, deadline stated
- **Effort** wallet connect (friction 10)
- **Key date** 2027-07-31 (250 days left)
- **Official site** https://www.bigcoin.tech
- **Domain check** no red flags found (score 0, age 606d)
- **Source** https://www.airdropstop.com/airdrops/bigcoin (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the BigCoin homepage Go to the official site at BigCoin , which is where the mining starts.
2. 2 Step 2 : Connect a wallet to start mining Use the Connect Wallet to Start Mining button on the homepage. The homepage also shows the total BIG mined so far.
3. 3 Step 3 : Check the hash rate leaderboard The homepage shows an Optimization Leaderboard for hash rate, with badges and rewards, dated 31 July to 4 August.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://www.bigcoin.tech`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://www.bigcoin.tech
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Bigcoin" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #11.
