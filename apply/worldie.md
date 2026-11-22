# Worldie - apply checklist (#16)

- **Confidence** 90/100 - 4 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect (friction 10)
- **Key date** 2027-10-18 (329 days left)
- **Official site** https://worldie.world
- **Domain check** no red flags found (score 15, age 101d)
- **Source** https://99airdrops.com/airdrops/worldie/ (checked 2026-11-23)

## Steps as stated by the project

1. Follow Worldie's X account, @worldiedotworld, for news. Its last post was on 1 October 2026.
2. Use only worldie.world if the site returns. Warning Worldie has announced no new address and no airdrop. Don't connect a wallet to any site in Worldie's name unless Worldie's own X account links to it.
3. Expect the points, invite and leaderboard pages to stay paused even if the site returns. They were switched off before it went down, and nothing says points turn into tokens.
4. Trade $WORLDIE or launch a market only if you want to, and only with money you can lose. Warning Buying at the moment a token launches is very expensive. The docs say: "Pons taxes buys at 99% at launch, decaying to zero over three seconds". A buy in that window loses almost all of its value to the tax.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://worldie.world`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://worldie.world
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Worldie" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #17.
