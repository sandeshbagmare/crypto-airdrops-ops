# Cycles - apply checklist (#11)

- **Confidence** 90/100 - 7 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** email (friction 3)
- **Key date** 2027-09-16 (297 days left)
- **Official site** https://apps.apple.com/us/app/cycles-pay/id6761496918
- **Domain check** no red flags found (score 0, age 14521d)
- **Source** https://99airdrops.com/airdrops/cycles/ (checked 2026-11-23)

> **Domain does not resemble the project name.** `https://apps.apple.com/us/app/cycles-pay/id6761496918` vs "Cycles". Confirm it against the project's own X profile before you connect anything. If it does not match, skip this drop and note it.

## Steps as stated by the project

1. Install Cycles Pay from the App Store or Google Play . You can also use the web app at pay.cycles.money , but the phone app holds your keys and signs for it. Warning The keys live on your phone, and Cycles can't restore them. The terms say: "IF YOU LOSE YOUR PRIVATE KEYS, YOUR FUNDS WILL BE PERMANENTLY INACCESSIBLE."
2. Sign up with an email code, Google or Apple, and choose a personal account. You don't need an invite code. A referral code is optional.
3. Skip identity checks unless you want bank transfers. Those go through banking partners that ask for KYC.
4. Fund the account with stablecoins from a wallet or an exchange. Warning This is real money in a beta app. The terms say: "THERE IS NO INSURANCE (SUCH AS FDIC COVERAGE), AND RETURNS ARE NOT GUARANTEED."
5. Use the app. Send a payment, create or pay an invoice, split an expense, or move part of your balance into a vault.
6. Open Points in the app to see the missions, the claims and your total.
7. If you used Cycles Pay before 16 September 2026, follow the in-app move from Neutron to Arc. Warning Cycles says its Neutron contracts stay active only until 1 November 2026. It also reported on 22 September that Neutron had halted, so move old balances as soon as the app lets you.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://apps.apple.com/us/app/cycles-pay/id6761496918`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://apps.apple.com/us/app/cycles-pay/id6761496918
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Cycles" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #12.
