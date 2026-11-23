"""Turn the live batch into the two artefacts the operator asked for: an Excel registry and a report.

Reads docs/data.json (the ledger) + data/preflight.json (what the real browser saw) and writes:

  data/blockers.xlsx     every drop, its live status, its blocker, and the one action that unblocks it
  notes/batch-report.md  the same thing as a readable table
  agent/handoffs/*.json  one handoff packet per blocked drop (AGENTS.md section 8 shape)
  agent/STATE.json       the machine queue, refreshed from the same records

  python tools/blocker_workbook.py
"""
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
DOCS_DATA = ROOT / "docs" / "data.json"
PREFLIGHT = ROOT / "data" / "preflight.json"
BATCH = ROOT / "data" / "preflight-batch.json"
XLSX = ROOT / "data" / "blockers.xlsx"
REPORT = ROOT / "notes" / "batch-report.md"
HANDOFFS = ROOT / "agent" / "handoffs"
STATE = ROOT / "agent" / "STATE.json"
SESSIONS = ROOT / "agent" / "sessions.json"
CREDS_NOTE = ROOT / "notes" / "credentials-context.md"

COLS = [("Project", 26), ("Confidence", 11), ("Days left", 9), ("Key date", 11),
        ("Live status", 12), ("Blocked on", 17), ("What the human must do", 52),
        ("What the agent already did", 44), ("Domain check", 18), ("Official site", 46),
        ("Resume command", 52), ("Evidence", 32), ("Source", 22), ("Checked", 11)]

RED = PatternFill("solid", fgColor="F8D7DA")
AMBER = PatternFill("solid", fgColor="FFF3CD")
GREEN = PatternFill("solid", fgColor="D4EDDA")
GREY = PatternFill("solid", fgColor="E9ECEF")

HUMAN_ACTION = {
    "kyc": "Pass KYC in your own name (legal step, agent cannot). Then finish the steps in apply/.",
    "wallet_signature": "Connect a burner wallet and approve the signature yourself.",
    "captcha": "Solve the bot check in the browser window, then finish the steps.",
    "email": "Enter your email and click the confirmation link in your inbox.",
    "login": "Log in / create the account in the shared profile, then the agent can continue.",
    "terms": "Read and accept the project terms in your own name.",
    "domain": "Do not touch it: the domain check flagged it. Verify from the project's own X profile.",
    "no-official-site": "No official domain was extracted. Find it from the project's own profile first.",
    "site-unreachable": "The page did not load. Try the URL yourself; record 403/404 in fetch-report.",
    "unknown": "Needs manual reading - the live page did not expose a clear step.",
    "": "Nothing blocking: work the steps in the checklist.",
}


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]


def resume_cmd(slug, official, blocked_on):
    if blocked_on in ("domain", "no-official-site", "site-unreachable"):
        return f"python tools/triage.py {official or '<url>'}   # then re-run bulk_apply"
    return (f"./.venv/Scripts/python.exe tools/agent_browser.py --identity main --url "
            f"{official or '<url>'}")


def row_values(d, slug, p):
    steps = d.get("steps") or []
    did = "; ".join(p.get("agent_can") or []) or "not reached"
    must = "; ".join(p.get("human_must") or []) or HUMAN_ACTION.get("")
    return [
        d["name"], d.get("confidence"), d.get("days"), d.get("end"),
        p.get("status", "not checked"), p.get("blocked_on", "") or "none",
        must if p.get("human_must") else HUMAN_ACTION.get(""),
        f"opened live site, saved page text + screenshot, read {len(steps)} steps ({did[:120]})",
        p.get("domain_verdict", "not checked"),
        p.get("official") or d.get("official") or "",
        resume_cmd(slug, p.get("official") or d.get("official"), p.get("blocked_on")),
        (p.get("evidence") or ["-"])[0],
        d.get("source_url") or d.get("source") or "",
        p.get("at", "")[:10] or d.get("checked", ""),
    ]


def paint(ws, rows, status_of):
    for i, (row, status) in enumerate(rows, start=2):
        fill = {"ready": GREEN, "blocked": AMBER, "refused": RED,
                "unreachable": GREY, "no-url": GREY}.get(status, GREY)
        for j in range(1, len(COLS) + 1):
            c = ws.cell(row=i, column=j)
            c.alignment = Alignment(vertical="top", wrap_text=j in (7, 8, 11))
            if j in (5, 6):
                c.fill = fill
                c.font = Font(bold=True)


def sheet(wb, title, headers, widths, rows, status_idx=None):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for j, (h, w) in enumerate(zip(headers, widths), start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
        ws.cell(row=1, column=j).font = Font(bold=True, color="FFFFFF")
        ws.cell(row=1, column=j).fill = PatternFill("solid", fgColor="343A40")
    for r in rows:
        ws.append(r)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{max(len(rows) + 1, 2)}"
    if status_idx:
        for i, r in enumerate(rows, start=2):
            st = r[status_idx - 1]
            fill = {"ready": GREEN, "blocked": AMBER, "refused": RED}.get(st)
            if fill:
                ws.cell(row=i, column=status_idx).fill = fill
    return ws


def write_credentials_context(records):
    """The roster of identities and logins, deliberately free of any secret material."""
    try:
        sess = json.loads(SESSIONS.read_text(encoding="utf-8"))
    except Exception:
        sess = {}

    by_host = defaultdict(list)
    for d, slug, p in records:
        bo = p.get("blocked_on")
        if bo in ("login", "email", "wallet_signature", "kyc", "captcha"):
            host = (p.get("official") or d.get("official") or "").split("//")[-1].split("/")[0]
            by_host[host].append((d["name"], bo, d.get("days")))

    lines = [
        "# Credentials context - identities and logins, no secrets",
        "",
        f"Generated {date.today()} from `data/preflight.json` and `agent/sessions.json`.",
        "",
        "## What this file is, and what it will never hold",
        "",
        "This is the map of *which* identity a drop needs, not the credential itself. AGENTS.md rule 1",
        "forbids an agent from reading, storing, transmitting or typing a seed phrase, private key,",
        "password, session token or 2FA secret. So there is no password, key or token anywhere in this",
        "repo, and there will not be one. Secret material lives in exactly two places, both human",
        "owned: your password manager, and the browser profile directory below (gitignored, it is",
        "equivalent to a login).",
        "",
        "| Where | What it holds | Owner | In git |",
        "|---|---|---|---|",
        "| `agent/sessions/<identity>/` | Playwright profile: cookies, localStorage, logged-in tabs | you | no |",
        "| your password manager | passwords, 2FA seeds, recovery codes | you | never |",
        "| `notes/credentials-context.md` | this roster: who logs in where, and when | agent | yes |",
        "| `agent/handoffs/<slug>.json` | which step is blocked and what you do there | agent | yes |",
        "",
        "## Identity roster",
        "",
        "| Identity | Profile | Sites with a live session | Last used |",
        "|---|---|---|---|",
    ]
    if sess:
        for name, s in sess.items():
            sites = ", ".join(s.get("sites") or {}) or "none"
            lines.append(f"| `{name}` | `{s.get('profile','')}` | {sites} | "
                         f"{s.get('updated','')[:10]} |")
    else:
        lines.append("| `main` | `agent/sessions/main` | none yet | - |")

    lines += [
        "",
        "Out of the box there is **one** identity, `main`. One identity per real-world persona: do not",
        "mix personas in one profile, and do not create identities you would be uncomfortable",
        "defending to a project's compliance team.",
        "",
        "## Logins this batch needs from you, grouped by site",
        "",
        "Sorted by how soon the drop closes. Each line: drop, the blocker, days left.",
        "",
        "| Site | Drops waiting on a human | Blocker | Soonest |",
        "|---|---|---|---|",
    ]
    for host, items in sorted(by_host.items(), key=lambda kv: -len(kv[1])):
        days = [i[2] for i in items if isinstance(i[2], int)]
        soon = min(days) if days else "-"
        names = ", ".join(f"{n} ({b})" for n, b, _ in items[:6])
        if len(items) > 6:
            names += f", +{len(items) - 6} more"
        lines.append(f"| `{host}` | {len(items)} | {names} | {soon}d |")

    lines += [
        "",
        "## The one-time steps per identity",
        "",
        "1. `./.venv/Scripts/python.exe tools/agent_browser.py --identity main --url <official>`",
        "2. Log in yourself in the window that opens. The agent never types the password.",
        "3. Leave the window open until the session is written, then close it. Cookies with an",
        "   expiry survive a restart; a site that issues a session cookie (no expiry) will not, and",
        "   that is a site behaviour, not something to work around.",
        "4. Tell the agent which drops you finished so it can re-run `tools/bulk_apply.py` and move",
        "   them from `blocked` to `ready`.",
        "",
        "## Deliberate gaps",
        "",
        "- No email account, phone number, burner wallet or social handle is recorded here, because",
        "  none was supplied and inventing one would be fraud.",
        "- No KYC, no deposits, no signatures: those stay with the human by design.",
        "",
    ]
    CREDS_NOTE.write_text("\n".join(lines), encoding="utf-8")
    return CREDS_NOTE


def main():
    drops = json.loads(DOCS_DATA.read_text(encoding="utf-8"))
    pre = {}
    for src in (PREFLIGHT, BATCH):   # BATCH wins: bulk_apply owns it, auto_apply rewrites PREFLIGHT
        try:
            pre.update(json.loads(src.read_text(encoding="utf-8")))
        except Exception:
            pass

    # A page that rendered almost no text cannot be called "ready": the detector had nothing to
    # read. Those go to unknown so nobody reads a green cell as "verified, go".
    for slug, p in pre.items():
        if p.get("status") != "ready":
            continue
        txt = [e for e in (p.get("evidence") or []) if e.endswith(".txt")]
        if txt and (ROOT / txt[0]).exists() and (ROOT / txt[0]).stat().st_size < 400:
            p["status"] = "unknown"
            p["blocked_on"] = "unknown"
            p.setdefault("human_must", []).append(
                "page rendered almost no text (JS-only shell) - read it yourself before acting")
            p["agent_can"] = (p.get("agent_can") or []) + ["kept the screenshot as the only evidence"]

    seen, records = set(), []
    for d in drops:
        slug = slugify(d["name"])
        if slug in seen:
            continue
        seen.add(slug)
        p = pre.get(slug) or {}
        records.append((d, slug, p))

    records.sort(key=lambda t: (0 if (t[2].get("blocked_on") in ("", None)) else 1,
                                t[0].get("days") if isinstance(t[0].get("days"), int) else 9999,
                                -(t[0].get("confidence") or 0)))

    blocked = [r for r in records if r[2].get("status") == "blocked"]
    ready = [r for r in records if r[2].get("status") == "ready"]
    refused = [r for r in records if r[2].get("status") in ("refused", "unreachable", "no-url")]
    unknown = [r for r in records if r[2].get("status") == "unknown"]
    unchecked = [r for r in records if not r[2]]

    wb = Workbook()
    wb.remove(wb.active)
    headers = [h for h, _ in COLS]
    widths = [w for _, w in COLS]

    allrows = [row_values(d, s, p) for d, s, p in records]
    sheet(wb, "All drops", headers, widths, allrows, status_idx=5)

    b_rows = [row_values(d, s, p) for d, s, p in blocked]
    ws = sheet(wb, "Blocked", headers, widths, b_rows, status_idx=5)
    paint(ws, [(r, "blocked") for r in b_rows], None)

    sheet(wb, "Ready", headers, widths,
          [row_values(d, s, p) for d, s, p in ready], status_idx=5)
    sheet(wb, "Refused - dead - no site", headers, widths,
          [row_values(d, s, p) for d, s, p in refused], status_idx=5)
    if unknown:
        sheet(wb, "Unknown - read it yourself", headers, widths,
              [row_values(d, s, p) for d, s, p in unknown], status_idx=5)
    if unchecked:
        sheet(wb, "Not checked yet", headers, widths,
              [row_values(d, s, p) for d, s, p in unchecked], status_idx=5)

    # summary sheet first
    sc = Counter((p.get("blocked_on") or "none") for _, _, p in records if p)
    stat = Counter(p.get("status", "not checked") for _, _, p in records if p)
    ws = wb.create_sheet("Summary", 0)
    ws.append(["What the batch found"])
    ws["A1"].font = Font(bold=True, size=14)
    ws.append([])
    ws.append(["Live status", "Drops"])
    ws.append(["total tracked", len(records)])
    for k, v in stat.most_common():
        ws.append([k, v])
    ws.append([])
    ws.append(["Blocked on", "Drops", "Who unblocks it"])
    for k, v in sc.most_common():
        ws.append([k, v, HUMAN_ACTION.get(k, "")])
    ws.append([])
    ws.append(["generated", str(date.today())])
    for j, w in enumerate((30, 10, 90), start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A3"
    XLSX.parent.mkdir(exist_ok=True)
    wb.save(XLSX)

    # handoff packets + STATE.json
    HANDOFFS.mkdir(parents=True, exist_ok=True)
    state = {"identity": "main", "generated": str(date.today()), "count": len(records), "drops": {}}
    wrote = 0
    for d, slug, p in records:
        if not p:
            continue
        bo = p.get("blocked_on") or ""
        state["drops"][slug] = {
            "project": d["name"], "confidence": d.get("confidence"), "days_left": d.get("days"),
            "end": d.get("end"), "official": p.get("official") or d.get("official"),
            "blocked_on": bo, "status": p.get("status"),
            "next_action": ("human: " + HUMAN_ACTION[bo]) if p.get("status") == "blocked"
                           else ("work the checklist" if p.get("status") == "ready"
                                 else "skip: " + p.get("status", "")),
            "evidence": p.get("evidence") or [], "updated": str(date.today()),
        }
        if p.get("status") in ("blocked", "refused", "unreachable", "no-url"):
            packet = {
                "project": d["name"],
                "official_url": p.get("official") or d.get("official") or "",
                "blocked_on": bo or "unknown",
                "why_agent_cannot": (", ".join(p.get("human_must") or [])
                                     or "no live page reached")[:300],
                "what_human_must_do": HUMAN_ACTION.get(bo, HUMAN_ACTION["unknown"]),
                "where_to_resume": resume_cmd(slug, p.get("official") or d.get("official"), bo),
                "evidence_so_far": p.get("evidence") or [],
                "steps_from_source": d.get("steps") or [],
                "created": str(date.today()),
                "status": "open",
            }
            (HANDOFFS / f"{slug}.json").write_text(
                json.dumps(packet, indent=1, ensure_ascii=False), encoding="utf-8")
            wrote += 1
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")

    # readable report
    lines = [
        "# Batch report - live check of every drop",
        "",
        f"Generated {date.today()} by `tools/bulk_apply.py` + `tools/blocker_workbook.py`.",
        "One row per drop. `Ready` means no identity step was detected on the live page;",
        "`Blocked` means a human must cross one line the agent is not allowed to cross.",
        "",
        "| Status | Drops |",
        "|---|---|",
    ]
    for k, v in stat.most_common():
        lines.append(f"| {k} | {v} |")
    lines += ["", "| Blocked on | Drops | Who unblocks it |", "|---|---|---|"]
    for k, v in sc.most_common():
        lines.append(f"| {k} | {v} | {HUMAN_ACTION.get(k, '')} |")
    lines += ["", f"Full registry: `data/blockers.xlsx`. Handoffs: `agent/handoffs/`.", ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {XLSX.relative_to(ROOT)}  ({len(records)} drops)")
    print(f"wrote {REPORT.relative_to(ROOT)}")
    print(f"wrote {write_credentials_context(records).relative_to(ROOT)}")
    print(f"wrote {wrote} handoff packets, refreshed agent/STATE.json")
    print("status:", dict(stat))
    print("blocked_on:", dict(sc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
