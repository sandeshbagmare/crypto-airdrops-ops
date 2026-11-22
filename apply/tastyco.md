# TastyCo - apply checklist (#22)

- **Confidence** 90/100 - 7 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect + social tasks (friction 15)
- **Key date** 2027-10-25 (336 days left)
- **Official site** https://app.tastyco.io/en/quests
- **Domain check** no red flags found (score 0)
- **Source** https://99airdrops.com/airdrops/tastyco/ (checked 2026-11-23)

## Steps as stated by the project

1. Open the TastyCo quest app . The task list stays blurred behind "Connect wallet to unlock quests" until you connect a wallet.
2. Connect a wallet to sign in, create your profile and unlock the tasks.
3. Connect Telegram through the bot, then join Discord and follow TastyCo on X and Instagram. Warning Use the Discord invite in the footer of tastyco.io. Older invites in TastyCo's Telegram posts and link page are dead, which makes it easy for fake ones to circulate.
4. Take the weekly quiz and come back on consecutive days for the streak points.
5. Share your referral link if you want referral points.
6. Optional: complete the TaskOn campaign before 25 October 2026.
7. Wait for the token launch. No claim page exists yet.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://app.tastyco.io/en/quests`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://app.tastyco.io/en/quests
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "TastyCo" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #23.
