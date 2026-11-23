# Minds Games - apply checklist (#5)

- **Confidence** 90/100 - 5 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect + email (friction 13)
- **Key date** 2027-10-12 (323 days left)
- **Official site** https://minds.games
- **Domain check** no red flags found (score 15, age 94d)
- **Source** https://99airdrops.com/airdrops/minds-games/ (checked 2026-11-23)

## Steps as stated by the project

1. Go to minds.games and choose "Claim a seat". Enter an email address and accept the campaign rules.
2. Connect your X account.
3. Verify a wallet by signing one message. The site says this involves no transaction and no gas. Warning A signature is all the wallet step needs. The rules say: "We will never ask for a seed phrase or private key." They also say wallet steps happen only on minds.games, so ignore links sent to you about the allowlist.
4. Create a Mind on HelloMinds, which is free, then use "Connect your Minds account" and approve the request so the site can map the Mind to your seat. Warning That approval gives minds.games access to your HelloMinds account. Read what the permission screen lists before you accept.
5. Watch @MindGames_AI on X for the allowlist results and the season dates. Neither had been published by 18 October 2026.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://minds.games`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://minds.games
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Minds Games" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #6.
