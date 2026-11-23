# Inverted Lambda - apply checklist (#11)

- **Confidence** 90/100 - 5 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect (friction 10)
- **Key date** 2027-11-08 (350 days left)
- **Official site** https://inverted-lambda.com/platform/beta
- **Domain check** no red flags found (score 15, age 265d)
- **Source** https://99airdrops.com/airdrops/inverted-lambda/ (checked 2026-11-23)

## Steps as stated by the project

1. On a desktop or laptop, open inverted-lambda.com/platform/beta . On 8 November 2026 this sent us to the homepage and opened a "Connect Wallet" box that said "Approve the connection in MetaMask."
2. Approve the connection and sign the message. In June the site said: "Signature required to log in. Please sign the message in MetaMask." It also had a "Referral code (optional)" field.
3. If you're asked for an access code, you need one from the team. The June site said "Enter your access code to continue." We closed the wallet box without connecting, so we don't know whether the beta still asks, and the site hasn't published how to get a code.
4. Pick a task and drive the arm with your keyboard. A phone can join as a tilt controller ("tilt the phone to aim"): the phone shows a code, and you press Connect phone on the desktop and type it in.
5. Finish the objective and let the upload complete. Check whether the points are confirmed or pending, and switch tasks when you reach a limit.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://inverted-lambda.com/platform/beta`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://inverted-lambda.com/platform/beta
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Inverted Lambda" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #12.
