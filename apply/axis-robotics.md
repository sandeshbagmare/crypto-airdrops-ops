# Axis Robotics - apply checklist (#21)

- **Confidence** 90/100 - 6 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** email (friction 3)
- **Key date** 2027-10-23 (334 days left)
- **Official site** https://hub.axisrobotics.ai
- **Domain check** no red flags found (score 15, age 348d)
- **Source** https://99airdrops.com/airdrops/axis-robotics/ (checked 2026-11-23)

## Steps as stated by the project

1. Sign up at Axis Hub with email, Google, X or a wallet. Tasks are back since Season 2 started on 23 October. It runs in a desktop browser without a GPU.
2. Pick a pre-training task and finish it with the mouse or keyboard. Failed attempts aren't uploaded.
3. Try post-training tasks, where you take over when a trained policy slips. A run that uses up its 30-second takeover budget scores nothing.
4. Open Portfolio, go to History and press Sign on each run before the Friday cut-off. Warning Only runs signed on Base count. A run you don't sign before the cut-off doesn't count.
5. Check the Alliance tab for partner tasks, such as BitRobot's, that pay a partner reward on top of points.
6. If you contributed in Season 1, check your allocation at airdrop.axisrobotics.ai with your Axis Hub account or Sonar wallet, then claim it on Base. Warning The claim page says "airdrop.axisrobotics.ai is the only official site. Axis will never ask for your seed phrase or private key."

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://hub.axisrobotics.ai`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://hub.axisrobotics.ai
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Axis Robotics" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #22.
