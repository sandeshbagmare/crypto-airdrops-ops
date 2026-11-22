# Aura Protocol - apply checklist (#3)

- **Confidence** 90/100 - 7 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect (friction 10)
- **Key date** 2026-11-30 (7 days left)
- **Official site** https://docs.litvm.com/get-started-on-testnet/network-configuration
- **Domain check** no red flags found (score 0, age 579d)
- **Source** https://99airdrops.com/airdrops/aura-protocol/ (checked 2026-11-23)

> **Domain does not resemble the project name.** `https://docs.litvm.com/get-started-on-testnet/network-configuration` vs "Aura Protocol". Confirm it against the project's own X profile before you connect anything. If it does not match, skip this drop and note it.

## Steps as stated by the project

1. Add the LitVM LiteForge testnet to an EVM wallet: chain ID 4441, gas token zkLTC. Take the network address from LitVM's docs . Aura's wallet guide still lists the old Caldera address, "https://liteforge.rpc.caldera.xyz/http", which LitVM has replaced.
2. Get free test zkLTC from the faucet on the Incentives page. "Distribution happens every six hours per wallet."
3. Open beta.auralaunch.org/incentives , connect the wallet and link your X account. Warning Many unrelated crypto projects are called Aura. Use only auralaunch.org, beta.auralaunch.org and x.com/auralaunchorg, and never type a seed phrase anywhere.
4. Do the humanity check. The app says: "Complete the challenge and click on the button below to verify your humanity and ensure eligibility for airdrop rewards." Then claim the daily login bonus.
5. Make testnet transactions: stake, vote, buy in test sales or deploy a token. Each one is worth 15 points. Do the free social tasks too.
6. Keep going until you pass 10,000 points with at least one dApp transaction. Aura's own checklist: "Complete your humanity verification and make sure to complete at least one txn. Aim for at least 10k AURA points."
7. Optional: enter the Token Quest before 30 November 2026 at 14:00 UTC.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://docs.litvm.com/get-started-on-testnet/network-configuration`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://docs.litvm.com/get-started-on-testnet/network-configuration
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Aura Protocol" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #4.
