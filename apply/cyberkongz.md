# CyberKongz - apply checklist (#20)

- **Confidence** 45/100 - 5 concrete steps, official site linked
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://www.cyberkongz.com/kong
- **Domain check** no red flags found (score 0)
- **Source** https://www.airdropstop.com/airdrops/cyberkongz (checked 2026-11-23)

## Steps as stated by the project

1. 1 Step 1 : Hold KONG in an Ethereum wallet Staking needs the token itself, and the whitepaper lists Ethereum as the network. The KONG page is where the project presents the token and its staking.
2. 2 Step 2 : Stake your KONG Open the KONG page and use its Stake Now button to stake. Staking is what starts the Kong Points count.
3. 3 Step 3 : Let Kong Points accrue Each staked KONG earns 1 KP every 24 hours, so your total grows daily while the stake stays in place.
4. 4 Step 4 : Check the NFT holder rewards If you hold a Genesis or Evo Kong, the same page lists seasonal KONG airdrops for you as well, and a WSK Pass or Genesis or Baby Kong opens the dynamic staking rewards.
5. 5 Step 5 : Wait for the season to end When a season closes, the KONG airdrop is distributed according to the points you accrued. Seasons last three to twelve months as set by CyberKongz; the whitepaper explains the 70/30 split.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://www.cyberkongz.com/kong`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://www.cyberkongz.com/kong
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "CyberKongz" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #21.
