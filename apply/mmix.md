# MMIX - apply checklist (#1)

- **Confidence** 90/100 - 5 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** social tasks (friction 5)
- **Key date** 2026-11-23 (0 days left)
- **Official site** https://hub.mmix.io
- **Domain check** no red flags found (score 0)
- **Source** https://99airdrops.com/airdrops/mmix/ (checked 2026-11-23)

## Steps as stated by the project

1. Do the one-time tasks: follow on X, join Discord, join Telegram.
2. Before 23 November 2026, 21:00 UTC, like, repost and comment on the 17 November announcement for the 200 points.
3. Give a wallet address. The form asks for "The wallet that will mint on Ethereum. Use one you control, not an exchange address." You type the address in; a new, empty wallet is the safer choice.
4. Go back to the hub. The whitelist task checks itself and can take up to a day to show the 1.1x multiplier. Do it before 25 November 2026, 21:00 UTC.
5. Check in each day and submit one X post a week if you want to keep adding points.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://hub.mmix.io`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://hub.mmix.io
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "MMIX" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #2.
