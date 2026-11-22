"""Build ledger.md and ledger.xlsx from data/airdrops.json.

Every row keeps its source URL. Nothing is invented: empty fields stay empty.
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "airdrops.json"

HEADERS = ["Project", "Source", "Status", "KYC / requirements", "Cost", "Time to start",
           "Risk", "Key date in source", "Days left", "Pool (source-stated)", "Notes", "Tags",
           "Apply status", "Link", "Fetched"]

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
          "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
DATE_RE = re.compile(
    r"(?:by|on|until|before|ends?|snapshot)\s+(\d{1,2})\s+([A-Z][a-z]{2})",
    re.IGNORECASE)


def date_from_notes(notes):
    """Pull the first 'on 2 Dec'-style date out of a description. Year inferred."""
    if not notes:
        return ""
    m = DATE_RE.search(notes)
    if not m:
        return ""
    day, mon = int(m.group(1)), MONTHS.get(m.group(2).lower()[:3])
    if not mon or not 1 <= day <= 31:
        return ""
    try:
        d = date(date.today().year, mon, day)
    except ValueError:
        return ""
    if d < date.today():
        try:
            d = date(date.today().year + 1, mon, day)
        except ValueError:
            return ""
    return d.isoformat()


def days_left(end_raw):
    if not end_raw:
        return ""
    for fmt in ("%d %b %Y", "%Y-%m-%d", "%d %B %Y"):
        try:
            d = datetime.strptime(end_raw.strip(), fmt).date()
            return (d - date.today()).days
        except ValueError:
            continue
    return ""


def requirement(r):
    bits = []
    if r.get("kyc"):
        bits.append(r["kyc"])
    if r.get("cost"):
        bits.append(r["cost"])
    if r.get("fees"):
        bits.append(r["fees"])
    if not bits and r.get("status") == "No fixed deadline":
        bits.append("see source")
    return "; ".join(bits)


def rows():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    out = []
    for r in data:
        end = r.get("end_date", "") or date_from_notes(r.get("notes", ""))
        dl = days_left(end)
        out.append([
            r.get("name", ""), r.get("source", ""), r.get("status", "") or r.get("next_move", ""),
            requirement(r), r.get("cost", ""), r.get("time_to_start", ""), r.get("risk", ""),
            end, dl, r.get("prize", ""), (r.get("notes", "") or r.get("description", ""))[:110],
            r.get("tags", ""), "identified",
            r.get("source_url", ""), r.get("fetched", ""),
        ])
    out.sort(key=lambda x: (x[8] == "", x[8] if isinstance(x[8], int) else 9999, x[0]))
    return out


def build_md(all_rows):
    dated = [r for r in all_rows if isinstance(r[8], int)]
    soon = [r for r in dated if 0 <= r[8] <= 30]
    lines = [
        "# Active airdrops",
        "",
        f"**{len(all_rows)} projects** scraped from public trackers on "
        f"{date.today().isoformat()}. Sources are per row; nothing here is invented.",
        "",
        f"- {len(dated)} carry a dated deadline or snapshot, **{len(soon)} fall within 30 days**",
        f"- {sum(1 for r in all_rows if r[6])} carry a risk rating from the tracker",
        f"- {sum(1 for r in all_rows if 'KYC' in (r[3] or ''))} list KYC as a requirement",
        f"- sources: {sum(1 for r in all_rows if 'airdroplet' in r[1])} airdroplet, "
        f"{sum(1 for r in all_rows if 'airdropvillage' in r[1])} airdropvillage, "
        f"{sum(1 for r in all_rows if '99airdrops' in r[1])} 99airdrops, "
        f"{sum(1 for r in all_rows if 'airdropstop' in r[1])} airdropstop, "
        f"{sum(1 for r in all_rows if 'airdropsio' in r[1])} airdrops.io",
        "",
        "Read the source link before acting. A tracker listing is not verification: confirm the",
        "official domain, then run `python tools/triage.py <url>`.",
        "",
        "## Closing within 30 days",
        "",
        "| Project | Ends | Days left | Risk | Requirements |",
        "|---|---|---|---|---|",
    ]
    for r in soon:
        lines.append(f"| {r[0]} | {r[7]} | {r[8]} | {r[6] or '-'} | {(r[3] or '-')[:70]} |")
    lines += [
        "",
        "## All tracked projects",
        "",
        "| " + " | ".join(HEADERS) + " |",
        "|" + "---|" * len(HEADERS),
    ]
    for r in all_rows:
        cells = [str(c) for c in r]
        cells[13] = f"[source]({r[13]})" if r[13] else ""
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        "## Apply status values",
        "",
        "`identified` -> `vetted` -> `in-progress` -> `submitted` -> `paid`, or `dropped`.",
        "Only move a row forward with evidence in `airships/`.",
        "",
        "## Regenerate",
        "",
        "```bash",
        "python tools/scrape_trackers.py   # refresh data/airdrops.json",
        "python tools/build_ledger.py      # rebuild ledger.md + ledger.xlsx",
        "```",
        "",
    ]
    (ROOT / "ledger.md").write_text("\n".join(lines), encoding="utf-8")


def build_xlsx(all_rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "airdrops"
    ws.append(HEADERS)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for r in all_rows:
        ws.append(r)
    widths = [20, 16, 20, 40, 14, 15, 11, 16, 9, 15, 50, 26, 13, 44, 12]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:O{ws.max_row}"
    dv = DataValidation(type="list",
                        formula1='"identified,vetted,in-progress,submitted,paid,dropped"',
                        allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"M2:M{ws.max_row}")

    s = wb.create_sheet("summary")
    s.append(["Metric", "Value"])
    for c in s[1]:
        c.font = Font(bold=True)
    dated = [r for r in all_rows if isinstance(r[8], int)]
    for k, v in (
        ("Tracked projects", len(all_rows)),
        ("With a dated deadline or snapshot", len(dated)),
        ("Closing within 30 days", sum(1 for r in dated if 0 <= r[8] <= 30)),
        ("With risk rating", sum(1 for r in all_rows if r[6])),
        ("KYC required", sum(1 for r in all_rows if "KYC" in (r[3] or ""))),
        ("From airdroplet", sum(1 for r in all_rows if "airdroplet" in r[1])),
        ("From airdropvillage", sum(1 for r in all_rows if "airdropvillage" in r[1])),
        ("From 99airdrops", sum(1 for r in all_rows if "99airdrops" in r[1])),
        ("From airdropstop", sum(1 for r in all_rows if "airdropstop" in r[1])),
        ("From airdrops.io", sum(1 for r in all_rows if "airdropsio" in r[1])),
        ("Flagged as needing KYC", sum(1 for r in all_rows if "KYC" in (r[3] or ""))),
        ("Flagged needing Telegram", sum(1 for r in all_rows if "Telegram" in (r[3] or ""))),
        ("Flagged needing X post", sum(1 for r in all_rows if "X post" in (r[3] or ""))),
        ("Flagged needing email", sum(1 for r in all_rows if "Email" in (r[3] or ""))),
        ("Marked live by source", sum(1 for r in all_rows if (r[2] or "").lower().startswith("live"))),
        ("Marked potential/wait", sum(1 for r in all_rows if (r[2] or "").lower().startswith(("potential", "wait")))),
        ("Operator target", 100),
        ("Last updated", date.today().isoformat()),
    ):
        s.append([k, v])
    s.column_dimensions["A"].width = 30
    s.column_dimensions["B"].width = 14
    wb.save(ROOT / "ledger.xlsx")


def main():
    all_rows = rows()
    build_md(all_rows)
    build_xlsx(all_rows)
    print(f"ledger.md + ledger.xlsx rebuilt from {len(all_rows)} records")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
