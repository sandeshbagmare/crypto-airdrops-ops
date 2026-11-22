"""Build ledger.md, ledger.xlsx and docs/ site from data/airdrops.json + data/verified.json."""
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
VERIFIED = ROOT / "data" / "verified.json"
DOCS = ROOT / "docs"

HEADERS = ["Project", "Confidence", "Status", "Official site", "What it needs",
           "Steps", "Key date", "Days left", "Pool (source-stated)", "What it is",
           "Apply status", "Source", "Verified"]

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
          "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
DATE_RE = re.compile(
    r"(?:by|on|until|before|ends?|snapshot)\s+(\d{1,2})\s+([A-Z][a-z]{2})",
    re.IGNORECASE)


def date_from_notes(notes):
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
    for fmt in ("%Y-%m-%d", "%d %b %Y", "%d %B %Y"):
        try:
            return (datetime.strptime(end_raw.strip(), fmt).date() - date.today()).days
        except ValueError:
            continue
    return ""


def key(name):
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def load():
    records = json.loads(DATA.read_text(encoding="utf-8"))
    verified = {}
    if VERIFIED.exists():
        raw = json.loads(VERIFIED.read_text(encoding="utf-8"))
        for v in raw.values():
            verified[key(v.get("name", ""))] = v
    return records, verified


def build(records, verified):
    rows, site = [], []
    for r in records:
        v = verified.get(key(r["name"]), {})
        end = r.get("end_date") or date_from_notes(r.get("notes", "")) or v.get("deadline_hint", "")
        dl = days_left(end)
        needs = r.get("kyc") or ""
        if r.get("cost") and r["cost"] not in needs:
            needs = "; ".join(x for x in (needs, r["cost"], r.get("fees", "")) if x)
        steps = v.get("steps") or []
        what = (v.get("what_it_is") or r.get("notes") or r.get("description") or "")[:300]
        conf = v.get("confidence", "")
        row = [r["name"], conf, r.get("status", "") or v.get("page_title", "")[:40],
               v.get("official_url", ""), needs[:120], len(steps) or "",
               end, dl, r.get("prize", ""), what, "identified",
               (r.get("source") or "").split("+")[0], v.get("checked", "")]
        rows.append(row)
        site.append({
            "name": r["name"], "confidence": conf, "status": r.get("status", ""),
            "official": v.get("official_url", ""), "needs": needs,
            "steps": steps, "end": end, "days": dl, "pool": r.get("prize", ""),
            "what": what, "behind": v.get("who_is_behind", ""),
            "costs": v.get("costs", ""), "risks": v.get("risks", ""),
            "evidence": v.get("evidence", []), "source": r.get("source", ""),
            "source_url": r.get("source_url", ""), "checked": v.get("checked", ""),
        })
    rows.sort(key=lambda x: (-(x[1] if isinstance(x[1], int) else -1), x[0]))
    site.sort(key=lambda x: (-(x["confidence"] if isinstance(x["confidence"], int) else -1), x["name"]))
    return rows, site


def md(all_rows, site):
    dated = [r for r in all_rows if isinstance(r[7], int)]
    soon = [r for r in dated if 0 <= r[7] <= 30]
    confed = [r for r in all_rows if isinstance(r[1], int)]
    lines = [
        "# Active airdrops",
        "",
        f"**{len(all_rows)} projects**, {len(confed)} deep-verified from their own guide pages.",
        f"Updated {date.today().isoformat()}. Every row carries its source; nothing is invented.",
        "",
        f"- {len(dated)} carry a dated deadline or snapshot, **{len(soon)} within 30 days**",
        f"- {sum(1 for r in all_rows if r[3])} have an official site extracted from the guide",
        f"- {sum(1 for r in all_rows if isinstance(r[5], int) and r[5])} have concrete steps listed",
        "",
        "**Confidence** is built only from evidence found in the guide: steps (25), official site (20),",
        "deadline (15), named operator (15), disclosed costs (10), second source (10), risks (5),",
        "minus 15 for no steps. It measures how well documented a drop is, **not** how likely it pays.",
        "",
        "## Closing within 30 days",
        "",
        "| Project | Ends | Days left | Confidence | What it needs |",
        "|---|---|---|---|---|",
    ]
    for r in soon:
        lines.append(f"| {r[0]} | {r[6]} | {r[7]} | {r[1]} | {(r[4] or '-')[:60]} |")
    lines += ["", "## Highest confidence", "",
              "| Project | Confidence | What it is | Official |",
              "|---|---|---|---|"]
    for s in site[:20]:
        lines.append(f"| {s['name']} | {s['confidence']} | {s['what'][:90]} | "
                     f"{s['official'] or '-'} |")
    lines += ["", "## All projects", "",
              "| " + " | ".join(HEADERS) + " |", "|" + "---|" * len(HEADERS)]
    for r in all_rows:
        cells = [str(c) if c != "" else "" for c in r]
        cells[3] = f"[site]({r[3]})" if r[3] else ""
        cells[11] = r[11]
        cells[9] = cells[9].replace("|", "/")[:160]
        cells[4] = cells[4].replace("|", "/")
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", "Full per-project detail: the [site](https://sandeshbagmare.github.io/crypto-airdrops-ops/) "
              "or `docs/data.json`.", ""]
    (ROOT / "ledger.md").write_text("\n".join(lines), encoding="utf-8")


def xlsx(all_rows):
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
    widths = [20, 10, 18, 34, 34, 8, 14, 9, 15, 60, 13, 16, 12]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:M{ws.max_row}"
    dv = DataValidation(type="list",
                        formula1='"identified,vetted,in-progress,submitted,paid,dropped"',
                        allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"K2:K{ws.max_row}")
    s = wb.create_sheet("summary")
    s.append(["Metric", "Value"])
    for c in s[1]:
        c.font = Font(bold=True)
    dated = [r for r in all_rows if isinstance(r[7], int)]
    for k, v in (
        ("Tracked projects", len(all_rows)),
        ("Deep-verified", sum(1 for r in all_rows if isinstance(r[1], int))),
        ("With steps", sum(1 for r in all_rows if isinstance(r[5], int) and r[5])),
        ("With official site", sum(1 for r in all_rows if r[3])),
        ("Dated deadline", len(dated)),
        ("Closing within 30 days", sum(1 for r in dated if 0 <= r[7] <= 30)),
        ("Avg confidence", round(sum(r[1] for r in all_rows if isinstance(r[1], int)) /
                                 max(1, sum(1 for r in all_rows if isinstance(r[1], int))))),
        ("Operator target", 100),
        ("Last updated", date.today().isoformat()),
    ):
        s.append([k, v])
    s.column_dimensions["A"].width = 30
    s.column_dimensions["B"].width = 14
    wb.save(ROOT / "ledger.xlsx")


def main():
    records, verified = load()
    rows, site = build(records, verified)
    md(rows, site)
    xlsx(rows)
    DOCS.mkdir(exist_ok=True)
    (DOCS / "data.json").write_text(json.dumps(site, ensure_ascii=False), encoding="utf-8")
    print(f"ledger.md + ledger.xlsx + docs/data.json from {len(rows)} records "
          f"({sum(1 for r in rows if isinstance(r[1], int))} verified, "
          f"{sum(1 for r in rows if r[3])} with official site)")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
