# Credentials context - identities and logins, no secrets

Generated 2026-11-23 from `data/preflight.json` and `agent/sessions.json`.

## What this file is, and what it will never hold

This is the map of *which* identity a drop needs, not the credential itself. AGENTS.md rule 1
forbids an agent from reading, storing, transmitting or typing a seed phrase, private key,
password, session token or 2FA secret. So there is no password, key or token anywhere in this
repo, and there will not be one. Secret material lives in exactly two places, both human
owned: your password manager, and the browser profile directory below (gitignored, it is
equivalent to a login).

| Where | What it holds | Owner | In git |
|---|---|---|---|
| `agent/sessions/<identity>/` | Playwright profile: cookies, localStorage, logged-in tabs | you | no |
| your password manager | passwords, 2FA seeds, recovery codes | you | never |
| `notes/credentials-context.md` | this roster: who logs in where, and when | agent | yes |
| `agent/handoffs/<slug>.json` | which step is blocked and what you do there | agent | yes |

## Identity roster

| Identity | Profile | Sites with a live session | Last used |
|---|---|---|---|
| `selftest` | `agent/sessions/selftest` | example.com | 2026-11-23 |

Out of the box there is **one** identity, `main`. One identity per real-world persona: do not
mix personas in one profile, and do not create identities you would be uncomfortable
defending to a project's compliance team.

## Public identifiers the tools will prefill

| Use | Value | Note |
|---|---|---|
| signup email | `sandeshbagmare@users.noreply.github.com` | git config user.email on this machine. It is a GitHub noreply alias, so it forwards to your verified inbox but is not your private address. Replace it with a dedicated throwaway inbox if you prefer. |
| burner wallet | `not set` | run tools/burner_wallet.py yourself |
| X handle | `not set` | public handle |
| Telegram | `not set` | public handle |

An email address and a wallet address are public values. A password, seed phrase, private key
or 2FA code is not, and none of those is stored anywhere in this repo.

## Logins this batch needs from you, grouped by site

Sorted by how soon the drop closes. Each line: drop, the blocker, days left.

| Site | Drops waiting on a human | Blocker | Soonest |
|---|---|---|---|
| `apps.apple.com` | 4 | Zoi Network (login), LETSTOP (login), ONE Fight Arena (login), HaHa Wallet (wallet_signature) | -d |
| `github.com` | 3 | Flop Labs (login), Bitcoin Quantum (login), Refrax (login) | -d |
| `di.xyz` | 2 | Decentralized Intelligence (wallet_signature), DI (wallet_signature) | 360d |
| `hub.mmix.io` | 1 | MMIX (kyc) | 0d |
| `app.doppler.finance` | 1 | Doppler Finance (wallet_signature) | 5d |
| `globemarkets.xyz` | 1 | Globe (email) | 7d |
| `app.infinifi.xyz` | 1 | infiniFi (wallet_signature) | 8d |
| `yakkamon.com` | 1 | Yakkamon (email) | 9d |
| `www.bybit.com` | 1 | Bybit WSOT 2026 (login) | 9d |
| `defi.xstocks.fi` | 1 | xStocks (wallet_signature) | 11d |
| `migrate.abs.xyz` | 1 | Abstract (wallet_signature) | 22d |
| `app.perle.xyz` | 1 | Perle (kyc) | 118d |
| `ssi.sosovalue.com` | 1 | SoSoValue (wallet_signature) | 179d |
| `www.bigcoin.tech` | 1 | Bigcoin (wallet_signature) | 250d |
| `claim.ethena.fi` | 1 | Ethena (wallet_signature) | 311d |
| `app.ekiden.fi` | 1 | Ekiden (wallet_signature) | 317d |
| `task.simplechain.com` | 1 | SimpleChain (wallet_signature) | 318d |
| `www.wick.xyz` | 1 | Wick (wallet_signature) | 324d |
| `ammora.org` | 1 | Ammora (wallet_signature) | 327d |
| `airdrop.neosoul.ai` | 1 | NeoSoul (wallet_signature) | 333d |
| `app.startale.com` | 1 | Startale (login) | 333d |
| `hub.axisrobotics.ai` | 1 | Axis Robotics (login) | 334d |
| `teneo-protocol.ai` | 1 | Teneo Protocol (login) | 338d |
| `app.origami.tech` | 1 | Origami Tech (email) | 341d |
| `www.melee.markets` | 1 | Melee (login) | 342d |
| `amahub.ama.one` | 1 | Amadeus Protocol (wallet_signature) | 342d |
| `app.stablestock.finance` | 1 | StableStock (login) | 344d |
| `caster.trade` | 1 | Caster (email) | 344d |
| `beta.pursuit.games` | 1 | Pursuit (email) | 347d |
| `www.sogni.ai` | 1 | Sogni AI (email) | 351d |
| `app.katana.network` | 1 | Katana (wallet_signature) | 353d |
| `metamask.com` | 1 | MetaMask (wallet_signature) | 354d |
| `www.thekleos.pro` | 1 | Kleos (wallet_signature) | 357d |
| `www.ipx.exchange` | 1 | IPX (login) | 357d |
| `www.daejin.xyz` | 1 | Daejin (login) | 359d |
| `play.coinzilla.com` | 1 | Coinzilla (email) | 360d |
| `antseed.com` | 1 | Antseed (email) | -d |
| `app.ascendlaunch.xyz` | 1 | Ascend (wallet_signature) | -d |
| `token.chimpx.ai` | 1 | ChimpX (wallet_signature) | -d |
| `www.superboard.xyz` | 1 | Florin (login) | -d |
| `orvi.fun` | 1 | Memebook (ORVI) (login) | -d |
| `docs.onre.finance` | 1 | OnRe (kyc) | -d |
| `www.42.space` | 1 | 42 (wallet_signature) | -d |
| `www.acepyr.com` | 1 | Acepyr (email) | -d |
| `dexari.com` | 1 | Dexari (kyc) | -d |
| `duelbet.com` | 1 | DuelBet (login) | -d |
| `app.n1.xyz` | 1 | N1 (login) | -d |
| `app.ondoperps.xyz` | 1 | Ondo Perps (login) | -d |
| `app.txflow.com` | 1 | TxFlow (login) | -d |
| `montramarkets.xyz` | 1 | Montra (wallet_signature) | -d |
| `app.orbinum.network` | 1 | Orbinum (wallet_signature) | -d |
| `www.agent.family` | 1 | TermiX (login) | -d |
| `xyper.market` | 1 | Xyper (email) | -d |
| `breathofestova.com` | 1 | Breath of Estova (email) | -d |
| `www.imperial.space` | 1 | Imperial (login) | -d |
| `portal.nousresearch.com` | 1 | Nous Research (login) | -d |
| `www.oneswap.cc` | 1 | OnePump (email) | -d |
| `www.raycash.xyz` | 1 | Raycash (email) | -d |
| `www.renaiss.xyz` | 1 | Renaiss Protocol (login) | -d |
| `voice.cc` | 1 | VOICE (wallet_signature) | -d |
| `app.apyx.fi` | 1 | Apyx (wallet_signature) | -d |
| `app.arcus.xyz` | 1 | Arcus (wallet_signature) | -d |
| `hashcats.fun` | 1 | Hashcats (wallet_signature) | -d |
| `app.metric.xyz` | 1 | Metric (wallet_signature) | -d |
| `www.monetrix.xyz` | 1 | Monetrix (wallet_signature) | -d |
| `note.systems` | 1 | Note Systems (wallet_signature) | -d |
| `tranches.reflect.money` | 1 | Reflect (wallet_signature) | -d |
| `app.tydro.com` | 1 | Tydro (wallet_signature) | -d |
| `alphea.ai` | 1 | ALPHEA (email) | -d |
| `blackboard.fi` | 1 | Blackboard (login) | -d |
| `app.doma.xyz` | 1 | Doma Protocol (login) | -d |
| `www.frontiertraders.com` | 1 | Frontier Traders (login) | -d |
| `waitlist.titanx.cc` | 1 | Titan Exchange (email) | -d |
| `app.dowprotocol.com` | 1 | Dow Protocol (wallet_signature) | -d |
| `app.nowa.finance` | 1 | NOWA (wallet_signature) | -d |
| `node.optimai.network` | 1 | OptimAI Network (email) | -d |
| `turbocards.getoptimum.xyz` | 1 | Optimum (wallet_signature) | -d |
| `airdrop.ritualfoundation.org` | 1 | Ritual (wallet_signature) | -d |
| `app.passport.xyz` | 1 | human.tech (wallet_signature) | -d |
| `docs.robinhood.com` | 1 | vibe/vibe (wallet_signature) | -d |
| `dapp.4dlabs.space` | 1 | 4D Labs (login) | -d |
| `app.allox.ai` | 1 | AlloX (wallet_signature) | -d |
| `de1.ai` | 1 | De1 (email) | -d |
| `testnet.polyester.com` | 1 | Polyester (kyc) | -d |
| `www.useproto.xyz` | 1 | Proto (email) | -d |
| `psy.xyz` | 1 | Psy Protocol (QED) (email) | -d |
| `sandwatch.com` | 1 | Sandwatch (email) | -d |
| `community.vana.org` | 1 | Vana (login) | -d |
| `catalyst.app` | 1 | Catalyst (email) | -d |
| `beta.xo.market` | 1 | XO Market (login) | -d |
| `powerx.one` | 1 | PowerX One (login) | -d |
| `app.nuva.finance` | 1 | NUVA (wallet_signature) | -d |
| `rafa.ai` | 1 | RAFA Finance (wallet_signature) | -d |
| `app.synthra.org` | 1 | Synthra (login) | -d |
| `testnet.tzer0.fun` | 1 | Tzero (wallet_signature) | -d |
| `valdora.finance` | 1 | Valdora (wallet_signature) | -d |
| `voltrade.xyz` | 1 | Voltrade (email) | -d |
| `app.zaps.markets` | 1 | ZeruAI (login) | -d |
| `quest.dogeos.com` | 1 | DogeOS (login) | -d |
| `waitlist.rwaperp.xyz` | 1 | RWAPerp (wallet_signature) | -d |
| `pantherdao.app` | 1 | Panther Protocol (wallet_signature) | -d |
| `app.decibel.trade` | 1 | Decibel (wallet_signature) | -d |
| `anichess.com` | 1 | Anichess (login) | -d |
| `app.atoma.fi` | 1 | Atoma (login) | -d |
| `axiom.trade` | 1 | Axiom Exchange (login) | -d |
| `docs.aztec.network` | 1 | Aztec (email) | -d |
| `brevis.network` | 1 | Brevis (wallet_signature) | -d |
| `browser.cash` | 1 | Browser Cash (login) | -d |
| `app.carbon.inc` | 1 | Carbon (login) | -d |
| `app.citrea.xyz` | 1 | Citrea (wallet_signature) | -d |
| `blog.dgrid.ai` | 1 | DGrid AI (email) | -d |
| `debank.com` | 1 | DeBank (wallet_signature) | -d |
| `fareup.xyz` | 1 | FareUp (login) | -d |
| `usefirewall.com` | 1 | Firewall (email) | -d |
| `app.gammaswap.com` | 1 | GammaSwap (wallet_signature) | -d |
| `www.golfn.com` | 1 | GolfN (email) | -d |
| `app.gyro.finance` | 1 | Gyroscope (wallet_signature) | -d |
| `haust.network` | 1 | Haust Network (email) | -d |
| `quest.human.tech` | 1 | Human Passport (login) | -d |
| `infinitywarlords.com` | 1 | Infinity Warlords (login) | -d |
| `interstate.trade` | 1 | Interstate (login) | -d |
| `www.karrier.one` | 1 | Karrier One (email) | -d |
| `www.liquity.org` | 1 | Liquity (email) | -d |
| `app.loopingcollective.org` | 1 | LoopedHYPE (wallet_signature) | -d |
| `www.megaeth.com` | 1 | MegaETH (kyc) | -d |
| `www.miden.xyz` | 1 | Miden (email) | -d |
| `www.minionlab.ai` | 1 | MinionLab (login) | -d |
| `moca.network` | 1 | Moca Network (login) | -d |
| `myriad.markets` | 1 | Myriad Markets (email) | -d |
| `nakamoto.games` | 1 | Nakamoto Games (email) | -d |
| `learn.nosana.com` | 1 | Nosana (login) | -d |
| `onefootball.com` | 1 | OneFootball Club (email) | -d |
| `app.ostium.com` | 1 | Ostium (login) | -d |
| `ponder.one` | 1 | Ponder (wallet_signature) | -d |
| `app.0.xyz` | 1 | Project 0 (login) | -d |
| `app.rally.fun` | 1 | Rally (login) | -d |
| `www.reddio.com` | 1 | Reddio (email) | -d |
| `app.roachracingclub.com` | 1 | Roach Racing Club (login) | -d |
| `www.shiftrwa.xyz` | 1 | SHIFT (kyc) | -d |
| `senpi.ai` | 1 | Senpi AI (login) | -d |
| `www.thesingularity.network` | 1 | Singularity (kyc) | -d |
| `spacenation.online` | 1 | Space Nation (wallet_signature) | -d |
| `portal.swapper.finance` | 1 | Swapper Finance (wallet_signature) | -d |
| `airdrop.tari.com` | 1 | Tari (wallet_signature) | -d |
| `uprock.com` | 1 | UpRock (email) | -d |
| `app.valantis.xyz` | 1 | Valantis Labs (wallet_signature) | -d |
| `www.w.ai` | 1 | W.AI (email) | -d |
| `worldlibertyfinancial.com` | 1 | World Liberty (email) | -d |
| `predict.fun` | 1 | predict.fun (login) | -d |
| `www.cambrian.org` | 1 | Cambrian Network (email) | -d |
| `datahive.ai` | 1 | DataHive (email) | -d |
| `collect.fifa.com` | 1 | FIFA Collect (email) | -d |
| `askjune.ai` | 1 | June AI (login) | -d |
| `www.kiedex.app` | 1 | KieDex (email) | -d |
| `www.leap.xyz` | 1 | Leap (email) | -d |
| `lora.finance` | 1 | Lora Finance (login) | -d |
| `docs.navalabs.ai` | 1 | Nava AI (login) | -d |
| `www.picasso.markets` | 1 | Picasso Markets (wallet_signature) | -d |
| `pulsar.money` | 1 | Pulsar Money (email) | -d |
| `rax.finance` | 1 | RAX Finance (email) | -d |
| `alpha.xdfi.net` | 1 | xDFi (wallet_signature) | -d |
| `train.actionmodel.com` | 1 | Action Model (login) | -d |
| `hoppr.studio` | 1 | Hoppr (wallet_signature) | -d |
| `www.infinityg.ai` | 1 | Infinity Ground (login) | -d |
| `marsrallychampionship.com` | 1 | Mars Rally Championship (login) | -d |
| `morfi.markets` | 1 | Morfi (login) | -d |
| `app.paradex.trade` | 1 | Paradex (login) | -d |
| `plushie.ai` | 1 | Plushie AI (login) | -d |
| `points.quip.network` | 1 | Quip Network (wallet_signature) | -d |
| `www.spekter.games` | 1 | Spekter Agency (wallet_signature) | -d |
| `yeno.pro` | 1 | YeNo (login) | -d |
| `app.bitrobot.ai` | 1 | BitRobot (login) | -d |
| `waitlist.gte.xyz` | 1 | GTE (email) | -d |
| `phyt.fun` | 1 | Phyt.fun (email) | -d |
| `x365.ai` | 1 | x365 AI (email) | -d |
| `agdex.io` | 1 | AGDEX (wallet_signature) | -d |
| `www.arcterminal.ai` | 1 | ARC Terminal (wallet_signature) | -d |
| `restaking.affinedefi.com` | 1 | Affine (login) | -d |
| `aof.global` | 1 | Arena of Faith (wallet_signature) | -d |
| `blackpass.astranova.world` | 1 | Astra Nova (login) | -d |
| `blockstreet.money` | 1 | Block Street (wallet_signature) | -d |
| `app.calamity.online` | 1 | Calamity (wallet_signature) | -d |
| `chat.chainopera.ai` | 1 | ChainOpera AI (wallet_signature) | -d |
| `checkpoint.exchange` | 1 | Checkpoint (wallet_signature) | -d |
| `credible.finance` | 1 | Credible (login) | -d |
| `airdrop.din.lol` | 1 | DIN (wallet_signature) | -d |
| `prism.delpho.xyz` | 1 | Delpho (wallet_signature) | -d |
| `www.ethermax.tech` | 1 | Ethermax (wallet_signature) | -d |
| `fungolabs.org` | 1 | FungoLabs (login) | -d |
| `docs.giwa.io` | 1 | GIWA (wallet_signature) | -d |
| `www.gaianet.ai` | 1 | Gaia (email) | -d |
| `wallet.gooddollar.org` | 1 | GoodDollar (login) | -d |
| `www.hyperlynx.fi` | 1 | Hyperlynx (wallet_signature) | -d |
| `app.joule.finance` | 1 | Joule Finance (wallet_signature) | -d |
| `app.krain.ai` | 1 | KRAIN (wallet_signature) | -d |
| `app.kinza.finance` | 1 | Kinza Finance (wallet_signature) | -d |
| `app.liquidium.fi` | 1 | Liquidium (login) | -d |
| `www.litvmswap.com` | 1 | LitVMSwap (wallet_signature) | -d |
| `lithos.to` | 1 | Lithos (wallet_signature) | -d |
| `blog.magmastaking.xyz` | 1 | Magma (email) | -d |
| `app.marginly.com` | 1 | Marginly (wallet_signature) | -d |
| `mirraai.xyz` | 1 | Mirra AI (login) | -d |
| `claim.moonbirds.com` | 1 | Moonbirds (wallet_signature) | -d |
| `motoswap.org` | 1 | Motoswap (wallet_signature) | -d |
| `app.noon.capital` | 1 | Noon (wallet_signature) | -d |
| `pingnetwork.io` | 1 | Ping Network (email) | -d |
| `probable.markets` | 1 | Probable (wallet_signature) | -d |
| `gen2.puffpaw.xyz` | 1 | Puffpaw (wallet_signature) | -d |
| `app.re.xyz` | 1 | Re (wallet_signature) | -d |
| `www.runwago.com` | 1 | Runwago (wallet_signature) | -d |
| `strato.nexus` | 1 | STRATO (email) | -d |
| `orchestration.seismic.systems` | 1 | Seismic (kyc) | -d |
| `www.genesis.sky.trade` | 1 | SkyTrade (wallet_signature) | -d |
| `app.spark.finance` | 1 | Spark Finance (wallet_signature) | -d |
| `core.swarmbase.io` | 1 | SwarmBase (wallet_signature) | -d |
| `docs.talus.network` | 1 | Talus Network (login) | -d |
| `pro.teller.org` | 1 | Teller Protocol (wallet_signature) | -d |
| `app.usd.ai` | 1 | USD.ai (wallet_signature) | -d |
| `well.eco` | 1 | WELL3 (wallet_signature) | -d |
| `testnet.x1ecochain.com` | 1 | X1 EcoChain (email) | -d |
| `airdrops.xian.org` | 1 | Xian (wallet_signature) | -d |
| `yieldbasis.com` | 1 | Yield Basis (wallet_signature) | -d |
| `rewards.dtelecom.org` | 1 | dTelecom (wallet_signature) | -d |
| `airdrop.dagama.world` | 1 | daGama (wallet_signature) | -d |
| `waitlist.dropee.xyz` | 1 | Dropee (email) | -d |
| `testnet.knidos.xyz` | 1 | Knidos (wallet_signature) | -d |
| `app.prismax.ai` | 1 | PrismaX (wallet_signature) | -d |
| `robinhood.com` | 1 | Robinhood (email) | -d |
| `docs.concrete.xyz` | 1 | Concrete (wallet_signature) | -d |
| `app.dustswap.wtf` | 1 | Dustswap (wallet_signature) | -d |
| `app.hyperflash.xyz` | 1 | HyperFlash (login) | -d |
| `www.janusdefi.com` | 1 | Janus Protocol (email) | -d |
| `www.rtrigger.com` | 1 | Lowlife Forms (wallet_signature) | -d |
| `portal.openzk.net` | 1 | OpenZK (wallet_signature) | -d |
| `rewards.watt2trade.com` | 1 | Watt2Trade (wallet_signature) | -d |
| `wheelx.fi` | 1 | WheelX (wallet_signature) | -d |
| `drake.exchange` | 1 | Drake (wallet_signature) | -d |
| `app.fight.id` | 1 | Fight.ID (email) | -d |
| `docs.qms.finance` | 1 | QMS Network (wallet_signature) | -d |
| `testnet.dfusion.ai` | 1 | dFusion AI (login) | -d |
| `aid.gaib.ai` | 1 | GAIB AI (wallet_signature) | -d |
| `www.nulink.org` | 1 | NuLink (login) | -d |
| `nudge.xyz` | 1 | Nudge (email) | -d |
| `canborsa.com` | 1 | Canborsa (email) | -d |
| `nesa.ai` | 1 | Nesa AI (login) | -d |
| `www.neutral.trade` | 1 | Neutral Trade (wallet_signature) | -d |
| `onchain.cc` | 1 | Onchain.cc (wallet_signature) | -d |
| `reaperactual.com` | 1 | Reaper Actual (email) | -d |
| `sectoraorg.com` | 1 | Sectora (wallet_signature) | -d |
| `sweep.finance` | 1 | Sweep Finance (login) | -d |

## The one-time steps per identity

1. `./.venv/Scripts/python.exe tools/agent_browser.py --identity main --url <official>`
2. Log in yourself in the window that opens. The agent never types the password.
3. Leave the window open until the session is written, then close it. Cookies with an
   expiry survive a restart; a site that issues a session cookie (no expiry) will not, and
   that is a site behaviour, not something to work around.
4. Tell the agent which drops you finished so it can re-run `tools/bulk_apply.py` and move
   them from `blocked` to `ready`.

## Deliberate gaps

- No email account, phone number, burner wallet or social handle is recorded here, because
  none was supplied and inventing one would be fraud.
- No KYC, no deposits, no signatures: those stay with the human by design.
