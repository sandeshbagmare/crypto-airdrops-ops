"""Find and merge the same project listed by more than one tracker.

A drop found by two sources is a stronger signal than the same drop listed twice, so merging is not
just cleanup: it raises confidence (+10 in the scoring) and stops the queue from asking twice.

  python tools/dedupe.py            # report and write data/duplicates.json
  python tools/dedupe.py --show 20
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "airdrops.json"
OUT = ROOT / "data" / "duplicates.json"

SUFFIXES = (" airdrop", " airdrops", " token", " mainnet", " finance", " protocol", " network")
NOISE = re.compile(r"\b(the|official|airdrop|air drops|free|new|live|testnet|token|claim|guide)\b")


def key(name):
    n = name.lower().strip()
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    n = NOISE.sub(" ", n)
    n = re.sub(r"\s+", " ", n).strip()
    for s in SUFFIXES:
        if n.endswith(s.strip()):
            n = n[: -len(s.strip())].strip()
    return n or name.lower().strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=10)
    args = ap.parse_args()

    records = json.loads(DATA.read_text(encoding="utf-8"))
    groups = {}
    for r in records:
        groups.setdefault(key(r["name"]), []).append(r)

    dupes = {k: v for k, v in groups.items() if len(v) > 1}
    merged = {}
    for k, rows in sorted(dupes.items(), key=lambda kv: -len(kv[1])):
        best = max(rows, key=lambda r: (bool(r.get("prize")), bool(r.get("end_date")),
                                        len(r.get("notes") or "")))
        ends = sorted({r["end_date"] for r in rows if r.get("end_date")})
        merged[k] = {
            "canonical": best["name"],
            "names": sorted({r["name"] for r in rows}),
            "sources": sorted({(r.get("source") or "").split("+")[0] for r in rows}),
            "source_urls": sorted({r.get("source_url") or "" for r in rows}),
            "end_date": ends[0] if ends else "",
            "rows": len(rows),
        }

    OUT.write_text(json.dumps(merged, indent=1, ensure_ascii=False), encoding="utf-8")
    total_rows = sum(m["rows"] for m in merged.values())
    print(f"records: {len(records)} | unique keys: {len(groups)} | "
          f"duplicate groups: {len(merged)} covering {total_rows} rows")
    print(f"unique projects after merge: {len(records) - total_rows + len(merged)}")
    for k, m in list(merged.items())[:args.show]:
        print(f"  {m['canonical'][:22]:24} x{m['rows']}  from {', '.join(m['sources'])}"
              f"{'  end=' + m['end_date'] if m['end_date'] else ''}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
