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

## Logins this batch needs from you, grouped by site

Sorted by how soon the drop closes. Each line: drop, the blocker, days left.

| Site | Drops waiting on a human | Blocker | Soonest |
|---|---|---|---|
| `hub.axisrobotics.ai` | 1 | Axis Robotics (login) | 334d |
| `www.melee.markets` | 1 | Melee (login) | 342d |
| `www.thekleos.pro` | 1 | Kleos (wallet_signature) | 357d |
| `play.coinzilla.com` | 1 | Coinzilla (email) | 360d |

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
