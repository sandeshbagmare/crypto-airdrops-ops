---
name: airdrop-recon
description: Find, vet and track crypto airdrop opportunities without risking a funded wallet. Use when the user asks about new airdrops, whether a drop or link is legit, how to register for a token distribution, or what to farm next.
---

# Airdrop Recon

Research first, claim second, and never with money at risk. Nothing in this skill signs a
transaction, connects a funded wallet, or pays a fee.

## Hard rules (never break)

1. Never connect a wallet holding real funds to an unvetted site. Use a fresh burner wallet only.
2. Never approve unlimited token allowances. Never blind-sign on mainnet.
3. Any "claim" that wants an upfront fee, a gas top-up, your seed phrase, or a Telegram DM from
   "support" is a scam. No exceptions.
4. Never pay for a whitelist, guaranteed allocation, or airdrop-list spot.
5. No mass-identity farming, CAPTCHA-solving services, or fake phone/email accounts. It breaks every
   program's terms and is the usual reason whole farms get disqualified at snapshot.
6. Report only what a source actually says, with URL and date. Never invent a deadline, allocation,
   or eligibility rule. If a number is not in a source, say it is not published.

## Why "register and wait" is usually wrong

Most current drops are **retroactive**: they reward wallets that already used the protocol before an
announced snapshot. A form you "register" on is rarely how allocation happens, and the format is a
favourite for phishing. Before acting, establish which kind a project is:

| Kind | How it works | Effort |
|---|---|---|
| Retroactive | You already used the product pre-snapshot; nothing to register | zero if you qualify |
| Points/quest | Ongoing tasks on the official app or Galxe/Zealy | recurring |
| Testnet | Real interactions on a testnet, often needs a faucet | medium |
| Signup list | Email/wallet registration before TGE | low, and the most faked |

## Recon pass

1. Search for candidates: `web_search` for the protocol category plus "airdrop", "points program",
   "token launch", "snapshot". Prefer primary sources (project blog, docs, official X account).
2. Confirm the official domain from the project's own docs or its verified X bio. Never from a reply,
   DM, YouTube comment, or sponsored search result.
3. For each candidate record: project, official URL, drop type, funding/backers, chain, cost to
   participate, snapshot status, and source URL + date.
4. Cross-check the domain age and registration with `whois`/RDAP via bash when a site is new.
5. Drop anything you cannot confirm on a primary source. An unconfirmed opportunity is a scam until
   proven otherwise.

## Vetting checklist

Answer every line before the user touches a wallet:

- Is the domain the official one, spelled exactly, on the project's own docs page?
- Is the site brand-new (registered within weeks) while the project is supposedly old?
- Does it ask for a seed phrase, private key, or a "wallet validation/sync"? Stop: scam.
- Does it ask for an unlimited approval or a signature with no readable message? Stop.
- Is there an official announcement of this exact drop, or only a screenshot circulating?
- Does the claim require paying gas to an address you do not control? Stop.
- Does the "team" contact you first? Legitimate teams do not DM first.
- Is the token already tradable, or is this a pre-launch promise of future value?

## Registering safely

1. Create a dedicated burner wallet for the project. Never reuse the main wallet.
2. Fund it with the minimum the task needs, on the right chain, and nothing more.
3. Log in on the official domain only, typed or bookmarked, not clicked from chat.
4. Screenshot the confirmation and store it in `airships/` under the project name.
5. After the task, revoke any approvals you granted (revoke.cash or the chain's equivalent).
6. Never leave funds in a wallet that has been connected to a quest site.

## Ledger

Keep one row per project in `ledger.md`: project, official URL, type, wallet label, tasks done,
snapshot status, expected date, source URL, verification date. Update it instead of trusting memory.

## Reporting to the user

Lead with the verdict: worth trying, watch, or scam. Then the one-line reason, the official URL, and
the single next step. State plainly what you could not verify.
