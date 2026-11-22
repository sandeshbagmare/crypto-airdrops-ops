# SimpleChain - apply checklist (#14)

- **Confidence** 90/100 - 11 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect + social tasks (friction 15)
- **Key date** 2027-10-07 (318 days left)
- **Official site** https://task.simplechain.com
- **Domain check** no red flags found (score 0)
- **Source** https://99airdrops.com/airdrops/simplechain/ (checked 2026-11-23)

## Steps as stated by the project

1. Open task.simplechain.com , connect an EVM wallet such as MetaMask and sign the login message. It costs no gas. Warning Use a wallet that holds no real funds. The login box comes already ticked to accept a Terms of Service and Privacy Policy that the portal doesn't link to.
2. Add the testnet to your wallet if it asks: Network name: SimpleChain Testnet
3. RPC URL: https://rpc-c.simplechain.com
4. Currency symbol: SRW
5. Block explorer: https://testnet-explorer.simplechain.com
6. Request test SRW from the faucet . You can ask once every 24 hours.
7. Link your X account and either Telegram or Discord in the portal. Several tasks won't count without them. Warning These links tie your social accounts to your wallet address, and the Telegram link asks for write access.
8. On the Daily tab, claim the check-in and the website visit every day.
9. On the OnChain tab, swap and add liquidity on the testnet exchange, and stake test SRW with a validator. Unstaking takes seven days. Warning When we checked on 7 October 2026, the exchange that the swap tasks open showed an expired security certificate. Don't click past a browser warning with a wallet you care about.
10. On the Social tab, follow, repost and reply on X, and join the Telegram group and the Discord server from the task cards.
11. Check your rank on the leaderboard .

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://task.simplechain.com`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://task.simplechain.com
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "SimpleChain" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #15.
