# MovitOn - apply checklist (#8)

- **Confidence** 60/100 - 5 concrete steps, official site linked, deadline stated
- **Effort** wallet connect + social tasks (friction 15)
- **Key date** 2027-10-28 (339 days left)
- **Official site** https://hub.moviton.com
- **Domain check** no red flags found (score 0, age 2927d)
- **Source** https://www.airdropstop.com/airdrops/moviton (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the MovitOn Loyalty Program Go to the MovitOn rewards site , where the program runs under the line &quot;Complete Tasks &gt; Earn Move Points &gt; Get Airdrop Eligibility&quot;.
2. 2 Step 2 : Connect a wallet Link your wallet through the rewards site. Your points history and rewards are shown only after a wallet is connected and you sign in.
3. 3 Step 3 : Complete tasks to earn Move Points The program runs on the sequence &quot;Complete Tasks &gt; Earn Move Points &gt; Get Airdrop Eligibility&quot;. As of 28 October 2026 the rewards site does not list specific tasks.
4. 4 Step 4 : Check your points history Come back to the rewards site to review the points and rewards credited to your wallet.
5. 5 Step 5 : Follow MovitOn for TGE and claim news MovitOn has given no snapshot or claim timing so far. Watch its Telegram channel and X account for announcements.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://hub.moviton.com`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://hub.moviton.com
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "MovitOn" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #9.
