# Boop - apply checklist (#19)

- **Confidence** 45/100 - 4 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://docs.boop.fun/temple-of-moon
- **Domain check** no red flags found (score 0, age 906d)
- **Source** https://www.airdropstop.com/airdrops/boop (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Read the Temple of Moon rules The Temple of Moon docs explain how phases and cult levels work. The Temple of Moon page is where the homepage banner leads.
2. 2 Step 2 : Launch a cult or buy into one Rewards go to those who trade or hold a cult&#x27;s token and to whoever launched it, so you take part by launching a cult or buying into an existing one on boop.fun . The leaderboard lists the top cults.
3. 3 Step 3 : Hold through the phase Cults unlock a larger share of each phase&#x27;s rewards as they ascend in levels. After a cult graduates, holder rewards are sent straight to your wallet with no claim, as described in the rewards docs .
4. 4 Step 4 : Stake BOOP for the staker airdrops BOOP stakers receive 5% of a graduated token&#x27;s supply, split by staked amount, and a 6.25% share of trading fees. You claim fee rewards on the staking page ; the staking docs explain how staking works.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://docs.boop.fun/temple-of-moon`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://docs.boop.fun/temple-of-moon
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Boop" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #20.
