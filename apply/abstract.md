# Abstract - apply checklist (#6)

- **Confidence** 90/100 - 5 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect (friction 10)
- **Key date** 2026-12-15 (22 days left)
- **Official site** https://migrate.abs.xyz
- **Domain check** no red flags found (score 0, age 4556d)
- **Source** https://99airdrops.com/airdrops/abstract/ (checked 2026-11-23)

> **Domain does not resemble the project name.** `https://migrate.abs.xyz` vs "Abstract". Confirm it against the project's own X profile before you connect anything. If it does not match, skip this drop and note it.

## Steps as stated by the project

1. Open the Abstract Migration Hub and check that the address is exactly migrate.abs.xyz. Connect the wallet that holds your funds on Abstract.
2. Bridge your assets to another chain. The hub shows the routes it supports, and it also lists the native Abstract bridge , Stargate, Relay and Jumper as alternatives. Crypto Briefing reports a delay of about three hours on the native bridge.
3. Check what you hold inside apps. The terms say NFTs, staked or locked assets, liquidity positions and funds held through an app may need action outside the hub. Follow that app's own instructions, which the hub links under "All Project Specific Instructions".
4. Finish early. The terms say each exit has its own deadlines to start and to complete, which can fall before 15 December, and that a submitted transaction isn't necessarily a completed transfer.
5. Don't send new funds to Abstract.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://migrate.abs.xyz`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://migrate.abs.xyz
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Abstract" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #7.
