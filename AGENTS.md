# AGENTS.md - operating context for autonomous agents

Read this file first, in full, before touching anything. It is the single source of truth for how
this repo works, what is safe to do without a human, and exactly when to stop and hand off.

## 1. What this repo is

A public, self-refreshing ledger of crypto airdrops. 500+ projects, each with a source link, an
evidence-based confidence score, extracted steps, official site, costs and risks.

- Human-readable table: `ledger.md`
- Spreadsheet: `ledger.xlsx`
- Machine-readable truth: `data/airdrops.json` (candidates) + `data/verified.json` (deep checks)
- Browser site: `docs/index.html` + `docs/data.json` (GitHub Pages)
- Source health: `data/fetch-report.md`
- What could not be automated, and why: `BLOCKERS.md`

## 2. Ground rules (non-negotiable, regardless of agent capability)

These are not capability limits. An agent with full shell and browser access still must not do them,
because they either destroy the operator's money, break platform terms, or are fraud.

1. **Never handle secrets.** No seed phrase, private key, keystore, session token, 2FA secret or
   password is to be read, stored, transmitted or typed. The human logs in; the agent uses the
   resulting browser profile.
2. **Never sign or approve on-chain transactions on the operator's behalf**, and never connect a
   wallet holding real funds. Testnet burners only, and only after the human approves the action.
3. **Never pass KYC** or upload identity documents, and never invent an identity. This is a legal
   boundary, not a technical one.
4. **Never bypass anti-bot protection**: no CAPTCHA-solving services, no proxy rotation to evade
   limits, no forged device fingerprints, no mass account creation. A blocked source is recorded as
   blocked.
5. **Never claim completion without evidence.** A row moves to `submitted` only with a screenshot or
   transaction hash stored under `airships/<project>/`.
6. **Respect each project's terms.** Some forbid automation entirely. If a project's terms say so,
   the agent prepares the packet and the human performs the steps.

## 3. Data schema

`data/airdrops.json` - one object per project:

| Field | Meaning |
|---|---|
| `name`, `slug` | project identity |
| `source`, `source_url` | where it was found; always keep for provenance |
| `status` | the tracker's own label, e.g. `Live`, `Wait`, `No fixed deadline` |
| `end_date`, `prize` | as stated by the source. `prize` is a pool size, never an expected payout |
| `kyc` | requirement flags, e.g. `Requires: Telegram, X post` |
| `cost`, `fees` | deposits or fees stated by the source |
| `fetched` | last successful fetch date |
| `stale_since` | present when the source became unreachable; rows are kept, not deleted |

`data/verified.json` - keyed by source URL:

| Field | Meaning |
|---|---|
| `what_it_is` | one-paragraph description from the project's own guide |
| `steps[]` | the actual instructions extracted from the guide |
| `official_url` | site linked by the guide, not by the tracker |
| `who_is_behind` | operator, company, backers if disclosed |
| `costs`, `risks` | what the guide says about money and danger |
| `confidence` | 0-100 evidence score (see below) |
| `evidence[]` | the reasons behind that score |
| `checked` | date of verification |

## 3b. Publishing as a pull request

`python tools/pr_drop.py --top 10` writes `drops/<slug>.md` (human dossier) and
`data/drops/<slug>.json` (machine record), commits them on `verify/<slug>`, pushes, and opens a PR.
Each dossier now carries **domain forensics** from `tools/triage.py`: RDAP age, TLS issuer, DNS, plus
a verdict. A `SCAM-LIKELY` verdict stops publication entirely - the drop is never given a branch.

Gates, in order:
1. `validate-drops` (CI) - schema, evidence-consistency, secret *requests* (warnings allowed), https
   official URL, no tracker or shortener as "official", required sections.
2. Human review of the dossier.
3. Optional: add the `auto-merge` label and `auto-merge.yml` merges it once CI is green.

## 4. Confidence score

Computed only from evidence found in the guide: steps +25, official site +20, deadline +15, named
operator +15, costs disclosed +10, second independent source +10, risks disclosed +5, no steps -15.

It measures **documentation quality**. It is not a probability of payment and not an endorsement.
A 90 can mean "well documented, and by the way it is shutting down with no token".

## 5. Scripts, in order

```bash
python tools/scrape_trackers.py     # refresh candidates from 5 trackers
python tools/verify.py --limit 150  # deep-verify guides, 7-day cache, incremental
python tools/build_ledger.py        # rebuild ledger.md + ledger.xlsx + docs/data.json
python tools/build_site.py          # rebuild docs/index.html
python tools/triage.py <url>        # domain forensics before any wallet touches a site
python tools/agent_bootstrap.py     # create session dirs + per-drop handoff packets
python tools/agent_browser.py --identity <id> --url <official>  # persistent login session
```

## 6. Selection policy

Work the queue in this order and stop at the first drop you can actually advance:

1. `days left` smallest and >= 0 (closing soonest)
2. `confidence` highest
3. `cost` empty or free
4. anything with KYC or a required deposit goes last, and only with explicit human consent

Never start a second drop before the first is either `submitted` or `dropped` with a reason.

## 7. Per-drop loop

1. Read the row plus its `verified.json` entry.
2. `python tools/triage.py <official_url>` - a `SCAM-LIKELY` verdict ends the drop immediately.
3. Confirm the official domain against the project's own docs or verified X profile. Never use a
   tracker outbound link, a search ad, or a reply.
4. Start the browser session: `python tools/agent_browser.py --identity <name> --url <official>`.
   If the profile has no session, the **human** logs in during that window. Cookies persist under
   `agent/sessions/<name>/`. The agent must not type the password.
5. Execute only the steps that need no secret and no identity: reading requirements, filling a
   public form field the human reviewed, capturing screenshots, checking eligibility text.
6. When a step needs a human, write a handoff packet (section 8) and stop that drop.
7. On success: store proof in `airships/<project>/`, set status `submitted`, record the date.
8. On failure: set status `dropped`, record the reason. Move to the next drop.

## 8. Handoff contract

Every blocked step produces `agent/handoffs/<project>-<step>.json`:

```json
{
  "project": "Remix",
  "official_url": "https://...",
  "blocked_on": "kyc | password | wallet_signature | captcha | phone | unknown",
  "why_agent_cannot": "one sentence",
  "what_human_must_do": "numbered, concrete",
  "where_to_resume": "exact command or URL",
  "evidence_so_far": ["airships/remix/step1.png"],
  "created": "YYYY-MM-DD",
  "status": "open | taken | done"
}
```

`agent/STATE.json` is the machine queue: one entry per drop with `status`, `blocked_on`, `next_action`
and `updated`. Update it on every transition. Never leave it stale - it is how the next agent resumes.

## 9. Browser sessions

`agent/sessions/<identity>/` holds a Playwright persistent profile (cookies, localStorage). It is
gitignored and must never be committed: it is equivalent to a login.

- One identity per real-world persona.
- The human performs the first login. Sessions then survive restarts.
- If a site logs the session out, the human logs in again. The agent does not attempt credential
  recovery, password reset, or "remember me" manipulation.
- Verified behaviour: a cookie **with an expiry** survives a full browser restart in the same profile
  (tested). A *session* cookie - no expiry, closed with the tab - is discarded by Chromium by design.
  If a login refuses to persist, that site issued a session cookie; do not work around it, log in
  again in the same window before the session ends.

## 10. Failure modes and what to do

| Symptom | Action |
|---|---|
| guide page 403/blocked | record blocked in `data/fetch-report.md`; keep last-checked data |
| official site not found | confidence drops; do not guess a domain |
| CAPTCHA | stop, write handoff with `blocked_on: captcha` |
| login wall | start session, hand off to human |
| KYC demanded | handoff with `blocked_on: kyc`, drop goes last in queue |
| wallet signature needed | handoff with `blocked_on: wallet_signature`, never pre-approve |
| terms forbid automation | prepare packet, hand off, mark `blocked_on: terms` |
| tracker data stale | trust `verified.json` and the official site over the tracker |

## 11. Reporting

Lead with the verdict: what advanced, what is blocked and why, what the human must do next. Cite the
source and the checked date for every factual claim. Never report "done" without evidence in
`airships/`. If something was impossible, write it in `BLOCKERS.md` rather than silently skipping it.
