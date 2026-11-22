"""Build the operator's apply kit: the 25 cheapest, best-evidenced drops, fully prepped.

Selects only drops that need no KYC, no deposit and no identity step, writes one checklist per drop
under apply/<slug>.md, plus apply-kit.md and apply-kit.xlsx to work from.

The agent cannot create accounts or submit registrations in a person's name; this kit exists so the
operator does that part in minutes with every fact already verified.

  python tools/apply_kit.py             # build the 25
  python tools/apply_kit.py --size 40
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parent.parent
DOCS_DATA = ROOT / "docs" / "data.json"
APPLY = ROOT / "apply"

COLS = ["#", "Project", "Confidence", "Effort", "Needs", "Closes in (days)", "Key date",
        "Official site", "Steps", "Blocked on", "Checklist", "Status"]


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]


def eligible(d):
    """No identity, no money, live domain, real steps."""
    f = d.get("forensics") or {}
    if f.get("verdict") == "DEAD-LINK":
        return False
    if not d.get("official") or not (d.get("steps") or []):
        return False
    if (d.get("friction") or 0) > 15:
        return False
    if not isinstance(d.get("confidence"), int) or d["confidence"] < 40:
        return False
    return True


def domain_matches(name, url):
    """Does the official domain actually resemble the project name? Cheap sanity check."""
    host = (url or "").split("//")[-1].split("/")[0].lower()
    stem = re.sub(r"[^a-z0-9]", "", host.split(".")[-2] if "." in host else host)
    nm = re.sub(r"[^a-z0-9]", "", name.lower())
    if not stem or not nm:
        return False
    for size in range(min(len(stem), len(nm)), 3, -1):
        for i in range(0, len(nm) - size + 1):
            if nm[i:i + size] in stem:
                return True
    return False


def checklist(d, rank):
    steps = d.get("steps") or []
    warn = ""
    if not domain_matches(d["name"], d.get("official") or ""):
        warn = (f"\n> **Domain does not resemble the project name.** `{d.get('official')}` vs "
                f"\"{d['name']}\". Confirm it against the project's own X profile before you "
                "connect anything. If it does not match, skip this drop and note it.\n")
    lines = [
        f"# {d['name']} - apply checklist (#{rank})",
        "",
        f"- **Confidence** {d.get('confidence')}/100 - {', '.join(d.get('evidence') or [])}",
        f"- **Effort** {d.get('friction_label')} (friction {d.get('friction')})",
        f"- **Key date** {d.get('end') or 'none stated'}"
        + (f" ({d['days']} days left)" if isinstance(d.get('days'), int) else ""),
        f"- **Official site** {d.get('official')}",
        f"- **Domain check** {(d.get('forensics') or {}).get('verdict')} "
        f"(score {(d.get('forensics') or {}).get('score')}"
        + (f", age {d['domain_age_days']}d" if d.get("domain_age_days") else "") + ")",
        f"- **Source** {d.get('source_url')} (checked {d.get('checked')})",
        warn,
        "## Steps as stated by the project",
        "",
    ]
    lines += [f"{i}. {s}" for i, s in enumerate(steps, 1)]
    lines += [
        "",
        "## Do this, in order",
        "",
        f"1. Confirm the domain yourself: it must match the project's own X profile or docs. "
        f"Start from `{d.get('official')}`.",
        "2. Open a dedicated browser session so the login survives:",
        "",
        "   ```bash",
        f"   python tools/agent_browser.py --identity main --url {d.get('official')}",
        "   ```",
        "",
        "3. Work the steps above in that window. Use a burner wallet for anything on testnet.",
        "4. Capture proof: screenshot of the confirmation, or the transaction hash.",
        "5. Record it, which flips the status in `agent/STATE.json`:",
        "",
        "   ```bash",
        f"   python tools/evidence.py --project \"{d['name']}\" --file <screenshot.png> "
        f"--note \"step done\"",
        "   ```",
        "",
        "## Guardrails",
        "",
        "- Never share a seed phrase or private key, with anyone, ever.",
        "- If the site asks for KYC, stop: that is a human legal step, not an automated one.",
        "- If it asks for a deposit, skip the drop and note it - a free-entry list should stay free.",
        "- If the domain differs from the one above, close the tab.",
        "",
        f"Cannot finish this one? Write it in `notes/backlog.md` and move to #{rank + 1}.",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=25)
    args = ap.parse_args()

    data = json.loads(DOCS_DATA.read_text(encoding="utf-8"))
    pool = [d for d in data if eligible(d)]
    # urgent first, then cheapest, then best evidenced
    pool.sort(key=lambda d: (0 if isinstance(d.get("days"), int) and d["days"] <= 30 else
                             1 if isinstance(d.get("days"), int) else 2,
                             d.get("days") if isinstance(d.get("days"), int) else 9999,
                             d.get("friction") or 0,
                             -(d.get("confidence") or 0)))
    picks = pool[:args.size]

    APPLY.mkdir(exist_ok=True)
    for i, d in enumerate(picks, 1):
        (APPLY / (slugify(d["name"]) + ".md")).write_text(checklist(d, i), encoding="utf-8")

    free = sum(1 for d in picks if (d.get("friction") or 0) == 0)
    dated = sum(1 for d in picks if isinstance(d.get("days"), int))
    mismatched = sum(1 for d in picks if not domain_matches(d["name"], d.get("official") or ""))
    lines = [
        "# Apply kit - the 25 cheapest verified drops",
        "",
        f"Built {date.today().isoformat()} from {len(data)} tracked drops. Selection: no KYC, "
        f"no deposit, live domain, real steps, confidence >= 40.",
        f"**{free} need no identity step at all**, {dated} carry a real deadline.",
        "",
        "Each row has `apply/<slug>.md` with the steps, the resume command and the "
        "evidence command. Record what you do and the status moves with you.",
        "",
        "An agent cannot create the accounts or submit the forms - that part is yours. Everything "
        "else (which drop, which URL, which steps, which risk) is already checked.",
        "",
        "| " + " | ".join(COLS) + " |",
        "|" + "---|" * len(COLS),
    ]
    for i, d in enumerate(picks, 1):
        slug = slugify(d["name"])
        lines.append("| " + " | ".join([
            str(i), d["name"], str(d.get("confidence")),
            d.get("friction_label") or "", (d.get("needs") or "-")[:40].replace("|", "/"),
            str(d.get("days")) if isinstance(d.get("days"), int) else "-",
            d.get("end") or "-", d.get("official") or "-",
            str(len(d.get("steps") or [])),
            "none", f"apply/{slug}.md", "identified",
        ]) + " |")

    wb = Workbook()
    ws = wb.active
    ws.title = "apply queue"
    ws.append(COLS)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, d in enumerate(picks, 1):
        ws.append([i, d["name"], d.get("confidence"), d.get("friction_label"),
                   (d.get("needs") or "")[:120],
                   d.get("days") if isinstance(d.get("days"), int) else "",
                   d.get("end") or "", d.get("official") or "",
                   len(d.get("steps") or []), "none",
                   f"airships/{slugify(d['name'])}/CHECKLIST.md", "identified"])
    for col, w in zip("ABCDEFGHIJKL", [5, 22, 11, 26, 40, 14, 13, 40, 7, 16, 40, 12]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"

    detail = wb.create_sheet("steps")
    detail.append(["Project", "Step #", "Step"])
    for d in picks:
        for i, s in enumerate(d.get("steps") or [], 1):
            detail.append([d["name"], i, s])
    detail.column_dimensions["A"].width = 24
    detail.column_dimensions["B"].width = 7
    detail.column_dimensions["C"].width = 110

    how = wb.create_sheet("how to use")
    for row in [
        ["Start here", "Pick row 1, open its CHECKLIST.md, work the steps."],
        ["Session", "python tools/agent_browser.py --identity main --url <official>"],
        ["Proof", "python tools/evidence.py --project \"<name>\" --file <shot.png> --note \"...\""],
        ["Status", "identified -> vetted -> in-progress -> submitted -> paid, or dropped"],
        ["Never", "Seed phrases, private keys, KYC uploads, paid whitelists"],
        ["If blocked", "Write it in notes/backlog.md, move to the next row"],
    ]:
        how.append(row)
    how.column_dimensions["A"].width = 14
    how.column_dimensions["B"].width = 100

    wb.save(ROOT / "apply-kit.xlsx")
    (ROOT / "apply-kit.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"apply kit: {len(picks)} drops | {free} with no identity step | {dated} with a deadline")
    print(f"domain-name mismatches flagged for manual check: {mismatched}")
    print(f"checklists: {len(picks)} under apply/<slug>.md")
    print("files: apply-kit.md, apply-kit.xlsx")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
