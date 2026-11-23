"""Run the whole pipeline in the right order, with timings and a clear failure report.

  python tools/refresh.py                    # scrape, verify, forensics, ledger, site, kit
  python tools/refresh.py --skip-scrape      # reuse existing candidates
  python tools/refresh.py --verify-limit 100 --skip scrape,forensics

Each step is independent: a failure is reported and the run continues, because a blocked tracker
should not stop the ledger from rebuilding.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

STEPS = [
    ("scrape", ["tools/scrape_trackers.py"], "refresh candidates from the five trackers"),
    ("verify", ["tools/verify.py", "--limit", "120"], "deep-verify guide pages (7-day cache)"),
    ("dates", ["tools/extract_dates.py"], "lift deadlines out of verified text"),
    ("dedupe", ["tools/dedupe.py"], "merge the same project listed by several sources"),
    ("forensics", ["tools/forensics_all.py"], "RDAP/DNS/TLS check on official domains (14-day cache)"),
    ("ledger", ["tools/build_ledger.py"], "rebuild ledger.md, ledger.xlsx, docs/data.json"),
    ("site", ["tools/build_site.py"], "rebuild docs/index.html"),
    ("queue", ["tools/agent_bootstrap.py"], "rebuild agent/STATE.json and handoff packets"),
    ("kit", ["tools/apply_kit.py"], "rebuild the 25-drop apply kit and checklists"),
    ("capability", ["tools/capability_matrix.py"], "classify what an agent vs a human must do"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip", default="", help="comma-separated step names to skip")
    ap.add_argument("--verify-limit", default="")
    args = ap.parse_args()

    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    results = []
    started = time.time()

    for name, cmd, why in STEPS:
        if name in skip:
            results.append((name, "skipped", 0.0, why))
            print(f"[skip] {name}")
            continue
        if name == "verify" and args.verify_limit:
            cmd = ["tools/verify.py", "--limit", args.verify_limit]
        t0 = time.time()
        print(f"[run ] {name}: {why}")
        r = subprocess.run([PY] + cmd, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        elapsed = time.time() - t0
        tail = (r.stdout or "").strip().splitlines()
        summary = tail[-1][:110] if tail else (r.stderr or "").strip().splitlines()[-1][:110]
        status = "ok" if r.returncode == 0 else f"FAILED ({r.returncode})"
        results.append((name, status, elapsed, summary))
        print(f"      {status} in {elapsed:.0f}s - {summary}")

    total = time.time() - started
    failed = [r for r in results if r[1].startswith("FAILED")]
    print(f"\n{len(results)} steps in {total:.0f}s | {len(failed)} failed")
    for name, status, elapsed, summary in results:
        print(f"  {name:11} {status:16} {elapsed:5.0f}s  {summary[:80]}")
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
