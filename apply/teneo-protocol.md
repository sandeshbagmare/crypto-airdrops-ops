# Teneo Protocol - apply checklist (#22)

- **Confidence** 60/100 - 4 concrete steps, official site linked, deadline stated
- **Effort** free / no identity (friction 0)
- **Key date** 2027-10-27 (338 days left)
- **Official site** https://teneo-protocol.ai/community-node
- **Domain check** no red flags found (score 0, age 468d)
- **Source** https://www.airdropstop.com/airdrops/teneo-protocol (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Install the Community Node extension Add the Teneo Community Node extension to Chrome. The homepage also links to a Community Node page .
2. 2 Step 2 : Run a node and earn Teneo Points Run a node through the extension to earn Teneo Points. The project also lists quests that move you up its leaderboard.
3. 3 Step 3 : Try the Beacon beta app Download the app from Google Play , or for desktop as a Mac , Windows or Linux build. The project says the app earns Fragments and that it is in beta.
4. 4 Step 4 : Check the homepage for updates Return to the Teneo Protocol homepage to see whether the project has announced a token, a claim or an end date. As of 27 October 2026 it names none of them.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://teneo-protocol.ai/community-node`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://teneo-protocol.ai/community-node
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Teneo Protocol" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #23.
