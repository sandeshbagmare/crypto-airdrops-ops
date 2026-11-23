# ARO Network - apply checklist (#17)

- **Confidence** 45/100 - 5 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://aro.network
- **Domain check** no red flags found (score 0, age 560d)
- **Source** https://www.airdropstop.com/airdrops/aro-network (checked 2026-11-23)

> **Domain does not resemble the project name.** `https://aro.network` vs "ARO Network". Confirm it against the project's own X profile before you connect anything. If it does not match, skip this drop and note it.

## Steps as stated by the project

1. 1 Step 1 : Open the ARO Network homepage Go to aro.network and choose the option to join the testnet. The Testnet S2 announcement appears there.
2. 2 Step 2 : Install the ARO app or node software S2 is offered with desktop and mobile apps, and the testnet also mentions running and testing ARO nodes or devices. The homepage does not say whether any hardware is needed. Install the option that suits you.
3. 3 Step 3 : Run it to earn Jades Keep the software running so it can earn Jades, the testnet&#x27;s reward.
4. 4 Step 4 : Review the S2 Badge and leaderboard Testnet S2 lists an S2 Badge and Jade bonus to win, plus a 30,000 USDT pool for the leaderboard. The homepage does not say how they are awarded.
5. 5 Step 5 : Invite friends if you want extra rewards Referring a friend carries a further 15% commission, according to the project.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://aro.network`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://aro.network
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "ARO Network" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #18.
