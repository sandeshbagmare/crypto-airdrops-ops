"""Build the redemption workbook: one Excel file you work through, then come back to later.

Every drop gets a row with the exact URL, the steps, what you have to type, and empty columns for
status / proof / payout so the file doubles as the record you redeem from months later.

  python tools/redeem_kit.py
  python tools/redeem_kit.py --open      # build, then open it

Inputs it reads (public values only, never a secret):
  agent/operator-inputs.json   {"email": "...", "wallet": "0x...", "x": "...", "telegram": "..."}
"""
import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
DOCS_DATA = ROOT / "docs" / "data.json"
PREFLIGHT = ROOT / "data" / "preflight.json"
BATCH = ROOT / "data" / "preflight-batch.json"
ENTRY = ROOT / "data" / "entry-points.json"
INPUTS = ROOT / "agent" / "operator-inputs.json"
OUT = ROOT / "data" / "redeem.xlsx"

COLS = [("#", 5), ("Project", 24), ("Closes in (days)", 9), ("Key date", 11),
        ("Official site", 44), ("Steps as stated (paste-ready)", 70), ("What you must type", 34),
        ("Blocker", 16), ("Domain check", 17), ("Evidence", 28), ("Status", 12),
        ("Done on", 11), ("Tx hash / proof", 26), ("Payout received", 16), ("Notes", 30)]

HEAD = "1F6F43"
RED = PatternFill("solid", fgColor="F8D7DA")
AMBER = PatternFill("solid", fgColor="FFF3CD")
GREEN = PatternFill("solid", fgColor="D4EDDA")
GREY = PatternFill("solid", fgColor="E9ECEF")

GROUPS = [
    ("1 - Ready now", ("ready",), (), "No identity step seen. Work these first, top to bottom."),
    ("2 - Email only", (), ("email",), "One public email + a confirm click. Nothing else."),
    ("3 - Wallet only", (), ("wallet_signature",),
     "A burner address + one approval you make yourself."),
    ("4 - Login session", (), ("login",), "Log in once in the agent profile, then it continues."),
    ("5 - KYC or terms", (), ("kyc", "terms"),
     "Legal/identity steps. Your decision, never automated."),
    ("6 - Dead or unknown", ("unknown", "refused", "no-url", "unreachable"),
     ("domain", "no-official-site", "site-unreachable", "unknown", "no-url"),
     "Not actionable: dead domain, no domain, or a page with nothing to read."),
]

STATUS = ["todo", "in progress", "submitted", "pending", "claimed", "dropped"]
HUMAN = {
    "": "nothing but the site's own steps",
    "email": "your email, then click the confirmation link",
    "wallet_signature": "a burner wallet address you control + your own approval",
    "login": "log in / create the account yourself in the profile window",
    "kyc": "identity documents - legal step, yours alone",
    "terms": "accept the terms in your own name",
    "domain": "nothing - the domain check flagged it, do not touch it",
    "no-official-site": "find the domain on the project's own X profile first",
    "site-unreachable": "retry later; it did not load",
    "unknown": "read the page yourself - it rendered nothing to the detector",
    "no-url": "find the domain on the project's own X profile first",
}


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().strip())


def load():
    raw = json.loads(DOCS_DATA.read_text(encoding="utf-8"))
    drops, seen = [], set()
    for d in raw:                      # the ledger repeats a few names; one row each
        slug = slugify(d["name"])
        if slug in seen:
            continue
        seen.add(slug)
        drops.append(d)
    pre = {}
    for src in (PREFLIGHT, BATCH):
        try:
            pre.update(json.loads(src.read_text(encoding="utf-8")))
        except Exception:
            pass
    try:
        opt = json.loads(INPUTS.read_text(encoding="utf-8"))
    except Exception:
        opt = {}
    try:
        entry = json.loads(ENTRY.read_text(encoding="utf-8"))
    except Exception:
        entry = {}
    for p in pre.values():
        if p.get("status") != "ready":
            continue
        txt = [e for e in (p.get("evidence") or []) if e.endswith(".txt")]
        chars = p.get("text_chars")
        if chars is None and txt and (ROOT / txt[0]).exists():
            chars = (ROOT / txt[0]).stat().st_size
        if chars is not None and chars < 400:
            p["status"] = "unknown"
            p["blocked_on"] = "unknown"
    return drops, pre, opt, entry


def click_hint(slug, entry):
    e = entry.get(slug) or {}
    nxt = e.get("next_click") or ""
    if not nxt or nxt.startswith("page failed"):
        return ""
    if nxt.startswith("no obvious"):
        return ""
    hint = f" | press: {nxt[:40]}"
    for f in (e.get("forms") or []):
        names = [x.get("name") or x.get("placeholder") or x.get("type") for x in
                 (f.get("fields") or [])]
        names = [n for n in names if n][:3]
        if names:
            hint += f" | fields: {', '.join(names)}"
            break
    return hint


def what_to_type(blocked, opt):
    email = opt.get("email") or "<your email - see agent/operator-inputs.json>"
    wallet = opt.get("wallet") or "<burner address - run tools/burner_wallet.py>"
    if blocked in ("email",):
        return f"email: {email}"
    if blocked in ("wallet_signature",):
        return f"wallet: {wallet}"
    if blocked == "login":
        return f"log in yourself; email: {email}"
    if blocked in ("kyc", "terms"):
        return "you, in your own name"
    if not blocked:
        return "nothing - just the site's steps"
    return HUMAN.get(blocked, "")


def rows_for(drops, pre, opt, entry=None, statuses=(), blockers=()):
    out = []
    for d in drops:
        slug = slugify(d["name"])
        p = pre.get(slug) or {}
        blocked = p.get("blocked_on") or ""
        status = p.get("status") or "not checked"
        if statuses and status not in statuses:
            continue
        if blockers and blocked not in blockers:
            continue
        out.append({
            "slug": slug, "d": d, "p": p, "blocked": blocked,
            "row": [None, d["name"],
                    d.get("days") if isinstance(d.get("days"), int) else "-",
                    d.get("end") or "-", p.get("official") or d.get("official") or "",
                    "\n".join(f"{i}. {s}" for i, s in enumerate(d.get("steps") or [], 1))
                    or "no steps extracted - read the site",
                    what_to_type(blocked, opt) + click_hint(slug, entry or {}),
                    blocked or "none",
                    p.get("domain_verdict") or "not checked",
                    (p.get("evidence") or ["-"])[0],
                    "todo", "", "", "", ""],
        })
    out.sort(key=lambda r: (r["d"].get("days") if isinstance(r["d"].get("days"), int) else 99999,
                            -(r["d"].get("confidence") or 0)))
    return out


def add_sheet(wb, title, rows, note):
    ws = wb.create_sheet(title)
    ws["A1"] = note
    ws["A1"].font = Font(italic=True, color="444444")
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(COLS))
    ws.append([])
    ws.append([h for h, _ in COLS])
    for j, (_, w) in enumerate(COLS, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
        c = ws.cell(row=2, column=j)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=HEAD)
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, r in enumerate(rows, 1):
        r["row"][0] = i
        ws.append(r["row"])
        rr = ws.max_row
        for j in range(1, len(COLS) + 1):
            c = ws.cell(row=rr, column=j)
            c.alignment = Alignment(vertical="top", wrap_text=j in (6, 7, 9, 15))
        url = r["row"][4]
        if url.startswith("http"):
            ws.cell(row=rr, column=5).hyperlink = url
            ws.cell(row=rr, column=5).font = Font(color="0563C1", underline="single")
        fill = {"ready": GREEN, "blocked": AMBER}.get(r["p"].get("status"), GREY)
        ws.cell(row=rr, column=8).fill = fill
    last = max(ws.max_row, 3)
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUS) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"K3:K{last + 200}")
    ws.freeze_panes = "C3"
    ws.auto_filter.ref = f"A2:{get_column_letter(len(COLS))}{last}"
    return ws


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", action="store_true")
    args = ap.parse_args()

    drops, pre, opt, entry = load()
    wb = Workbook()
    wb.remove(wb.active)

    # cover sheet
    ws = wb.create_sheet("Start here")
    ws["A1"] = "Airdrop redemption workbook"
    ws["A1"].font = Font(bold=True, size=16)
    ws["A2"] = f"Built {date.today()} from {len(drops)} tracked drops, each live-checked in a browser."
    ws["A4"] = "How to use this file"
    ws["A4"].font = Font(bold=True)
    steps = [
        "1. Work sheet '1 - Ready now' first. Those pages showed no identity step at all.",
        "2. Then '2 - Email only': paste the email shown in column G, submit, click the confirm link.",
        "3. Then '3 - Wallet only': connect the burner address shown in column G, approve yourself.",
        "4. Set Status as you go (dropdown in column K). 'submitted' = a form was sent.",
        "5. When a drop pays out, fill 'Payout received' and the tx hash. This file is your record.",
        "6. Never paste a seed phrase or private key into any column, ever.",
    ]
    for i, s in enumerate(steps, start=5):
        ws.cell(row=i, column=1, value=s)
    ws["A12"] = "The three public inputs this file depends on"
    ws["A12"].font = Font(bold=True)
    ws["A13"] = "email"
    ws["B13"] = opt.get("email") or "NOT SET - add it to agent/operator-inputs.json"
    ws["A14"] = "wallet address"
    ws["B14"] = opt.get("wallet") or "NOT SET - run tools/burner_wallet.py yourself"
    ws["A15"] = "x / telegram handles"
    ws["B15"] = f"x: {opt.get('x','-')}  telegram: {opt.get('telegram','-')}"
    ws["A17"] = ("Column G tells you the one thing to type. Everything else is already researched, "
                 "and nothing in this workbook is a secret.")
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 96
    for r in (5, 6, 7, 8, 9, 10):
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)

    counts = {}
    for title, statuses, blockers, note in GROUPS:
        rows = rows_for(drops, pre, opt, entry, statuses, blockers)
        add_sheet(wb, title[:31], rows, note)
        counts[title] = len(rows)

    # the whole ledger, for completeness
    allrows = rows_for(drops, pre, opt, entry)
    add_sheet(wb, "All drops", allrows, "Every tracked drop, whatever its status.")

    # blank redemption log
    ws = wb.create_sheet("Redemption log")
    ws.append(["Project", "Claim window / deadline", "Claimed on", "Amount received", "Wallet used",
               "Tx hash", "Still claimable?", "Notes"])
    for j in range(1, 9):
        ws.cell(row=1, column=j).font = Font(bold=True, color="FFFFFF")
        ws.cell(row=1, column=j).fill = PatternFill("solid", fgColor=HEAD)
    for w, j in zip((24, 24, 12, 18, 46, 40, 14, 40), range(1, 9)):
        ws.column_dimensions[get_column_letter(j)].width = w
    dv = DataValidation(type="list", formula1='"yes,no,expired"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add("G2:G400")
    ws.freeze_panes = "A2"

    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)}")
    for k, v in counts.items():
        print(f"  {k:22} {v:4} rows")
    if not opt.get("wallet"):
        print("\nno wallet address set -> sheet 3 shows a placeholder. "
              "Run tools/burner_wallet.py yourself (it never writes the key to disk).")
    if args.open:
        os.startfile(OUT)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
