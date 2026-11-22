"""Record proof for a drop and advance its status.

A row only becomes `submitted` when something is on disk to prove it. This tool creates
airships/<slug>/, copies or references the evidence, appends a line to data/evidence.json and updates
agent/STATE.json. It never invents proof: if you do not pass a file, nothing is recorded.

  python tools/evidence.py --project Yakkamon --file "C:/path/screenshot.png" --note "pre-registered"
  python tools/evidence.py --project Yakkamon --url https://yakkamon.com --note "submitted form"
  python tools/evidence.py --list
"""
import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "agent" / "STATE.json"
EVIDENCE = ROOT / "data" / "evidence.json"
AIRSHIPS = ROOT / "airships"
DOCS_DATA = ROOT / "docs" / "data.json"


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default="")
    ap.add_argument("--file", default="")
    ap.add_argument("--url", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--status", default="submitted",
                    choices=["vetted", "in-progress", "submitted", "paid", "dropped"])
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    evidence = {}
    if EVIDENCE.exists():
        try:
            evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        except Exception:
            evidence = {}

    if args.list:
        if not evidence:
            print("no evidence recorded yet")
            return 0
        for slug, items in evidence.items():
            print(f"{slug}: {len(items)} record(s)")
            for it in items[-3:]:
                print(f"   {it['at']}  {it['status']:12} {it.get('note','')[:50]}  {it.get('path','')}")
        return 0

    if not args.project:
        print("need --project (use --list to see what exists)")
        return 2
    if not args.file and not args.url:
        print("refusing to record 'submitted' without evidence: pass --file or --url")
        return 2

    slug = slugify(args.project)
    dest_dir = AIRSHIPS / slug
    dest_dir.mkdir(parents=True, exist_ok=True)

    stored = ""
    if args.file:
        src = Path(args.file)
        if not src.exists():
            print(f"file not found: {src}")
            return 2
        dest = dest_dir / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{src.name}"
        shutil.copy2(src, dest)
        stored = str(dest.relative_to(ROOT)).replace("\\", "/")
        print(f"evidence copied: {stored}")

    record = {"at": datetime.now().strftime("%Y-%m-%d %H:%M"), "status": args.status,
              "note": args.note[:200], "path": stored, "url": args.url}
    evidence.setdefault(slug, []).append(record)
    EVIDENCE.parent.mkdir(exist_ok=True)
    EVIDENCE.write_text(json.dumps(evidence, indent=1, ensure_ascii=False), encoding="utf-8")

    if STATE.exists():
        state = json.loads(STATE.read_text(encoding="utf-8"))
        drops = state.get("drops", {})
        if slug in drops:
            drops[slug]["status"] = args.status
            drops[slug]["updated"] = datetime.now().strftime("%Y-%m-%d")
            drops[slug]["next_action"] = ("wait for claim window" if args.status == "submitted"
                                         else "review evidence" if args.status == "paid" else "none")
            drops[slug]["evidence"] = [i.get("path") or i.get("url") for i in evidence[slug]]
            STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
            print(f"state: {slug} -> {args.status}")
        else:
            print(f"note: {slug} is not in agent/STATE.json (project name may differ)")

    print(f"recorded {len(evidence[slug])} evidence item(s) for {slug}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
