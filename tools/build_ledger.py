"""Build ledger.md and ledger.xlsx from the researched candidate list."""
import datetime as dt
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent  # repo root, not tools/
TODAY = "2026-11-22"

# Source: airdropvillage.io/airdrops (updated daily, Nov 2026 list)
# and airdroplet.com/testnet-airdrops (16 dossiers, checked Aug-Nov 2026)
AV = "https://www.airdropvillage.io/airdrops"
AD = "https://airdroplet.com/testnet-airdrops"
N99 = "https://99airdrops.com/airdrops/november-2026/"

ROWS = [
    # name, category, chain, cost, ends, risk, source, status, notes
    ("Remix", "campaign", "multi", "free entry", "2026-12-01", "medium", AV, "identified", "Prize pool ~$169,500; medium difficulty"),
    ("Mantle", "campaign", "Mantle", "free entry", "2026-12-08", "low", AV, "identified", "~$4,000 pool, rated 4.50"),
    ("Tribe", "points", "unknown", "free entry", "2026-12-31", "low", AV, "identified", "Easy difficulty, rated 3.65"),
    ("HANDLE", "points", "unknown", "free entry", "2026-12-31", "unknown", AV, "identified", "Ends 31 Dec 2026"),
    ("ZXOXO", "points", "unknown", "free entry", "2026-12-31", "unknown", AV, "identified", "Ends 31 Dec 2026"),
    ("Octos", "points", "unknown", "free entry", "2026-12-31", "unknown", AV, "identified", "Ends 31 Dec 2026"),
    ("Clocked", "competition", "unknown", "free entry", "no fixed deadline", "unknown", AV, "identified", "~$200,000, tagged NEW"),
    ("Formation", "points", "unknown", "free entry", "not published", "low", AV, "identified", "Easy, rated 4.00"),
    ("GenLayer", "testnet", "GenLayer", "no deposit, $0 fees", "open", "medium", AD, "identified", "Bradbury testnet + points; KYC required; 15 min start"),
    ("DOHM Finance", "testnet", "unknown", "no deposit, $0 fees", "open", "high", AD, "identified", "Incentivized testnet; high risk flag"),
    ("Gyndore", "testnet", "unknown", "no deposit, $0 fees", "open", "medium", AD, "identified", "DropWave Season 1 + public testnet"),
    ("Push Chain", "points", "Push Chain", "no deposit, $0 fees", "open", "medium", AD, "identified", "Season 3; reward route unconfirmed"),
    ("Hotstuff", "testnet", "unknown", "no deposit, $0 fees", "open", "high", AD, "identified", "Public testnet + Expeditions; high risk"),
    ("Namada", "staking", "Namada", "no deposit", "open", "high", AD, "identified", "NAM shielded set rewards; high risk"),
    ("Canopy Network", "testnet", "Canopy", "no deposit, $0 fees", "open", "medium", AD, "identified", "Public testnet rewards"),
    ("Polaris", "testnet", "unknown", "no deposit, $0 fees", "open", "medium", AD, "identified", "Testnet V2; reward route unconfirmed"),
    ("XyloNet", "points", "XyloNet", "free", "open", "unknown", AD, "identified", "Testnet points; transactions required"),
]

HEADERS = ["Project", "Category", "Chain", "Cost", "Ends", "Risk", "Source", "Status",
           "Notes", "Wallet used", "Completed on", "Proof path", "Verified"]

def md_row(r):
    return "| " + " | ".join([
        r[0], r[1], r[2], r[3], r[4], r[5],
        f"[src]({r[6]})", r[7], r[8], "", "", "", TODAY,
    ]) + " |"

def build_md():
    lines = [
        "# Airdrop ledger",
        "",
        f"Last updated **{TODAY}**. Sources are listed per row. Nothing here is a promise of a reward.",
        "",
        "**Status meanings**",
        "",
        "| Status | Meaning |",
        "|---|---|",
        "| identified | Found on a public tracker; not independently verified |",
        "| vetted | Official domain confirmed on the project's own docs |",
        "| in-progress | Tasks started on a burner wallet |",
        "| submitted | All tasks done, confirmation captured in `airships/` |",
        "| paid | Tokens received in the burner wallet |",
        "| dropped | Scam, expired, paid-only, or otherwise disqualified |",
        "",
        f"**Candidate count: {len(ROWS)}. Completed: 0. Verified official: 0.**",
        "",
        "| " + " | ".join(HEADERS) + " |",
        "|" + "---|" * len(HEADERS),
    ]
    lines += [md_row(r) for r in ROWS]
    lines += [
        "",
        "## What is missing from this table",
        "",
        "Every row still needs an official-domain check before any wallet connects. A tracker listing is",
        "not verification: tracker entries have been used to funnel users to phishing clones.",
        "",
        "## Why it is not full of completed drops",
        "",
        "Completing a drop needs decisions and credentials that belong to the operator: which burner",
        "wallet to use, whether KYC is acceptable, and the actual clicks on each site. A list of",
        "candidates is what can be produced without those.",
        "",
    ]
    (ROOT / "ledger.md").write_text("\n".join(lines), encoding="utf-8")

def build_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = "candidates"
    ws.append(HEADERS)
    head_fill = PatternFill("solid", fgColor="1F3864")
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = head_fill
        c.alignment = Alignment(vertical="center")
    for r in ROWS:
        ws.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], "", "", "", TODAY])
    widths = [18, 14, 12, 20, 18, 10, 42, 14, 52, 16, 14, 22, 12]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:M{ws.max_row}"
    dv = DataValidation(
        type="list",
        formula1='"identified,vetted,in-progress,submitted,paid,dropped"',
        allow_blank=True,
    )
    ws.add_data_validation(dv)
    dv.add(f"H2:H{ws.max_row}")

    summary = wb.create_sheet("summary")
    summary.append(["Metric", "Value"])
    for c in summary[1]:
        c.font = Font(bold=True)
    summary.append(["Candidates identified", len(ROWS)])
    summary.append(["Vetted (official domain confirmed)", 0])
    summary.append(["In progress", 0])
    summary.append(["Submitted with proof", 0])
    summary.append(["Paid", 0])
    summary.append(["Target set by operator", 25])
    summary.append(["Last updated", TODAY])
    summary.column_dimensions["A"].width = 34
    summary.column_dimensions["B"].width = 16

    wb.save(ROOT / "ledger.xlsx")

if __name__ == "__main__":
    build_md()
    build_xlsx()
    print(f"ledger.md + ledger.xlsx written, {len(ROWS)} rows")
