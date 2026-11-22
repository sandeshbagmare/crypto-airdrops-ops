# Ekiden

**Confidence 90/100** - documentation quality, not a payout forecast.
**Status** Early / speculative | **Key date** 6 Oct | **Days left** n/a

## What it is

Ekiden is an invite-only perps exchange on Canton that pays XP for trading fees. No token is confirmed, and a 6 Oct bug liquidated some accounts.

## Official site

https://app.ekiden.fi

## What it needs

Nothing stated in the source.

## Steps

1. Open app.ekiden.fi , press Connect and sign in with Google or a Canton Console Wallet. Ekiden says: "Google is the fastest option for a new account. Your Party ID is provisioned during the sign-in flow; no browser extension is required."
2. Enter your code and accept the terms, including the box that reads "I acknowledge that I am trading with real money".
3. Fund your account: "In the app, open Deposit/Withdraw and select EVM to Canton Bridge." You'll need ETH for gas, and the deposit arrives as USDCx. Warning Check the Canton recipient before you send. The docs say: "Transactions sent to a different recipient cannot be reassigned automatically."
4. Move margin into your trading account and trade. XP shows on the Portfolio page and the leaderboard. Warning Leverage goes up to 20x, and a bad move can wipe out your margin. On 6 October 2026 a faulty update applied funding wrongly and liquidated some accounts.

## Who is behind it

The only named person is Vitali Dervoed, its founder and chief executive. Yellow reported that "Dervoed's background spans capital markets and roles tied to Neon EVM, RockawayX and Mango Markets." In May 2026, according to Yellow, "Ekiden has closed a $2 million seed round to develop trading infrastructure aimed at professional and algorithmic participants in on-chain derivatives." It added: "The 

## Costs

Taking part costs money: XP comes only from trading, and every trade pays a fee. While mainnet is closed, "we lower the fees, making them as low as 0.01% for the maker, 0.0350% for the taker, which corresponds to the standard $10M+ tier." The normal schedule starts at 0.02% maker and 0.05% taker. Ekiden's September recap says "deposits and withdrawals moved to a flat 1 USDC." It also covers Canton

## Risks

There are no full terms of use, no privacy policy and no list of excluded countries. The app blocks some locations, including sanctioned ones, without naming them. The only terms text sits in the sign-in window: "This Interface and the Ekiden Protocol are made available by the Ekiden Holding Foundation". It doesn't say where that foundation is. After the 6 October bug Ekiden wrote: "We are reviewi

## Pool (as stated by the source)

_Source states no pool size._

## Domain forensics

Verdict: **no red flags found** (risk score 0) | domain age 628 days

- **OK** domain registered 2025-03-04 (628 days)
- **OK** TLS issued by Google Trust Services

## Evidence

- 4 concrete steps
- official site linked
- deadline stated
- operator/team named
- costs disclosed
- risks disclosed

Source: https://99airdrops.com/airdrops/ekiden/ (checked 2026-11-23)

## Reviewer checklist

- [ ] official domain matches the project's own docs or verified X profile
- [ ] no deposit, fee or paid whitelist required
- [ ] deadline confirmed on the official site
- [ ] steps reproduce on the official site, not only on the tracker
- [ ] `python tools/triage.py <official>` returns clean
