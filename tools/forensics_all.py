"""Run domain forensics for every drop's official site, cached and threaded.

Writes data/forensics.json keyed by domain, plus notes/watchlist.md listing anything risky.
Domains are checked once and reused for 14 days, so repeat runs are cheap.

  python tools/forensics_all.py            # all known official domains
  python tools/forensics_all.py --refresh  # ignore the cache
  python tools/forensics_all.py --limit 40
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

DOCS_DATA = ROOT / "docs" / "data.json"
OUT = ROOT / "data" / "forensics.json"
WATCH = ROOT / "notes" / "watchlist.md"
CACHE_DAYS = 14
WORKERS = 3


def domain_of(url):
    host = (url or "").split("//")[-1].split("/")[0].split(":")[0].lower()
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    from triage import triage

    data = json.loads(DOCS_DATA.read_text(encoding="utf-8"))
    cache = {}
    if OUT.exists() and not args.refresh:
        try:
            cache = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    domains = {}
    for d in data:
        off = d.get("official") or ""
        if off.startswith("http"):
            domains.setdefault(domain_of(off), off)

    cutoff = (datetime.now() - timedelta(days=CACHE_DAYS)).strftime("%Y-%m-%d")
    todo = [(dom, url) for dom, url in domains.items()
            if args.refresh or dom not in cache or cache[dom].get("checked_on", "") < cutoff]
    if args.limit:
        todo = todo[:args.limit]
    print(f"domains: {len(domains)} | to check: {len(todo)} | cached: {len(cache)}")

    def work(item):
        dom, url = item
        try:
            rep = triage(url)
            return dom, {"domain": dom, "url": url, "verdict": rep["verdict"],
                         "score": rep["score"], "findings": rep["findings"],
                         "checked_on": datetime.now().strftime("%Y-%m-%d")}
        except Exception as e:
            return dom, {"domain": dom, "url": url, "verdict": "check failed", "score": None,
                         "findings": [["WARN", str(e)[:80]]],
                         "checked_on": datetime.now().strftime("%Y-%m-%d")}

    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for dom, rec in pool.map(work, todo):
            cache[dom] = rec
            done += 1
            if done % 40 == 0:
                print(f"  {done}/{len(todo)}")
                OUT.write_text(json.dumps(cache, indent=1, ensure_ascii=False), encoding="utf-8")

    OUT.write_text(json.dumps(cache, indent=1, ensure_ascii=False), encoding="utf-8")

    risky = sorted([c for c in cache.values() if c.get("verdict") in ("SUSPICIOUS", "SCAM-LIKELY")],
                   key=lambda c: -(c.get("score") or 0))
    young = [c for c in cache.values()
             if any("days old" in m for _, m in c.get("findings", []))]
    lines = [
        "# Watchlist - domains that need a human look before any wallet connects",
        "",
        f"Generated {datetime.now().strftime('%Y-%m-%d')} from `tools/triage.py` "
        f"({len(cache)} domains checked).",
        "",
        "A young domain is not automatically a scam - new projects legitimately launch new sites.",
        "It *is* a reason to confirm the domain against the project's own X profile or docs before",
        "connecting anything. Nothing here is an accusation.",
        "",
        f"## Flagged: {len(risky)} of {len(cache)}",
        "",
        "| Domain | Verdict | Score | Why |",
        "|---|---|---|---|",
    ]
    for c in risky[:80]:
        why = "; ".join(m for _, m in c.get("findings", []) if _ != "OK")[:120]
        lines.append(f"| {c['domain']} | {c['verdict']} | {c['score']} | {why} |")
    lines += ["", f"## Domains under a year old: {len(young)}", "",
              "| Domain | Age signal |", "|---|---|"]
    for c in young[:60]:
        sig = next((m for _, m in c.get("findings", []) if "days old" in m), "")
        lines.append(f"| {c['domain']} | {sig} |")
    lines += ["", "Regenerate: `python tools/forensics_all.py`.", ""]
    WATCH.parent.mkdir(exist_ok=True)
    WATCH.write_text("\n".join(lines), encoding="utf-8")

    print(f"clean: {sum(1 for c in cache.values() if c.get('verdict') == 'no red flags found')}, "
          f"suspicious: {sum(1 for c in cache.values() if c.get('verdict') == 'SUSPICIOUS')}, "
          f"scam-likely: {sum(1 for c in cache.values() if c.get('verdict') == 'SCAM-LIKELY')}")
    print(f"watchlist: notes/watchlist.md")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
