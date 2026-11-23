# Ethos Network - apply checklist (#6)

- **Confidence** 60/100 - 4 concrete steps, official site linked, deadline stated
- **Effort** free / no identity (friction 0)
- **Key date** 2027-10-22 (333 days left)
- **Official site** https://app.ethos.network
- **Domain check** no red flags found (score 0, age 1579d)
- **Source** https://www.airdropstop.com/airdrops/ethos-network (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Open the Ethos app Go to the Ethos app .
2. 2 Step 2 : Read the Season 1 announcement The post XP becomes Karma explains who is eligible and how to earn Season Karma. Check it for the current rules.
3. 3 Step 3 : Earn Season Karma as the announcement describes Follow the earning rules in the announcement post. The blog post dated 22 October 2026 says Season 1 runs three months and the top 1,000 share 15,000 WHUF; the blog page gives no start or end date.
4. 4 Step 4 : Try the Curator Beta if it suits you The Curators v2 post describes a beta that rewards original content on X and launched alongside Karma Season 1.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://app.ethos.network`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://app.ethos.network
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Ethos Network" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #7.
