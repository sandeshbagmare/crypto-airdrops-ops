# MINT - apply checklist (#15)

- **Confidence** 75/100 - 5 concrete steps, official site linked, operator/team named, costs disclosed, risks disclosed
- **Effort** free / no identity (friction 0)
- **Key date** none stated
- **Official site** https://mint.io/mntd
- **Domain check** no red flags found (score 0)
- **Source** https://99airdrops.com/airdrops/mint-io/ (checked 2026-11-23)

## Steps as stated by the project

1. Log in to mint.io and open the rewards panel on the $MNTD page.
2. Find the Airdrop $MNTD row and claim it. Claimed tokens start earning staking rewards straight away, according to MINT.
3. Your account has to pass MINT's checks first. The terms say: "Promotions are available only to verified Accounts in permitted jurisdictions".
4. If you earned $MNTD in a partner campaign rather than on MINT, MINT asks: "Got tokens to claim from external activations?" Those are claimed at getminted.io/claim instead. Warning Use only mint.io and getminted.io, and check the contract address against MINT's own post. Fake claim sites often copy new token launches.
5. If you missed Season 1, there's nothing to claim. Staking $MNTD for a status level is the only way into MINT's future airdrops, and it means buying a volatile token.

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://mint.io/mntd`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://mint.io/mntd
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "MINT" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #16.
