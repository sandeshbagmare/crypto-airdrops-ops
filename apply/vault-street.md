# Vault Street - apply checklist (#19)

- **Confidence** 90/100 - 4 concrete steps, official site linked, deadline stated, operator/team named, costs disclosed, risks disclosed
- **Effort** wallet connect + social tasks (friction 15)
- **Key date** 2027-10-22 (333 days left)
- **Official site** https://vaultstreet.fun/whitelist
- **Domain check** SUSPICIOUS (score 35, age 41d)
- **Source** https://99airdrops.com/airdrops/vault-street/ (checked 2026-11-23)

## Steps as stated by the project

1. Open vaultstreet.fun/whitelist and sign in with X. The site says: "We only read your name, username and profile picture."
2. Like, repost and comment on the pinned post: "Interact with our pinned post on X."
3. "Post a tweet, thread or art about Vault Street and tag" its account @VaultStreet_rh, then paste the link to your post.
4. The game opens on 22 October at 17:00 UTC: "Open vaultstreet.fun/play, tap Connect wallet and sign a free message." Then you buy a bank, which the game calls a Treasury: "Pick one of 5 Treasuries ($2 to $45). It's your bank, yours forever, one per wallet."

## Do this, in order

1. Confirm the domain yourself: it must match the project's own X profile or docs. Start from `https://vaultstreet.fun/whitelist`.
2. Open a dedicated browser session so the login survives:

   ```bash
   python tools/agent_browser.py --identity main --url https://vaultstreet.fun/whitelist
   ```

3. Work the steps above in that window. Use a burner wallet for anything on testnet.
4. Capture proof: screenshot of the confirmation, or the transaction hash.
5. Record it, which flips the status in `agent/STATE.json`:

   ```bash
   python tools/evidence.py --project "Vault Street" --file <screenshot.png> --note "step done"
   ```

## Guardrails

- Never share a seed phrase or private key, with anyone, ever.
- If the site asks for KYC, stop: that is a human legal step, not an automated one.
- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.
- If the domain differs from the one above, close the tab.

Cannot finish this one? Write it in `notes/backlog.md` and move to #20.
