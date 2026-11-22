"""CI gate: validate drop dossiers before they can merge.

Checks every drops/*.md against its data/drops/*.json record and fails on anything a reviewer could
otherwise miss: schema, confidence consistency, placeholder text, unsafe official URLs, and the
presence of the sections that make a dossier usable.

  python tools/validate_drops.py                 # all dossiers
  python tools/validate_drops.py --changed       # only files changed vs origin/main
  python tools/validate_drops.py --slug yakkamon
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DROPS = ROOT / "drops"
DATA_DROPS = ROOT / "data" / "drops"

REQUIRED_SECTIONS = ["## What it is", "## Official site", "## What it needs", "## Steps",
                     "## Evidence", "## Reviewer checklist"]
TRACKER_DOMAINS = ("99airdrops.com", "airdropstop.com", "airdrops.io", "airdroplet.com",
                   "airdropvillage.io", "cryptorank.io")
BANNED = (r"\bTODO\b", r"\bTBD\b", r"lorem ipsum")
# Secret *requests* are forbidden; secret *warnings* are required practice.
SECRET_RE = re.compile(r"\b(seed\s?phrase|private\s?key|mnemonic|recovery\s?phrase)\b", re.I)
NEGATION = re.compile(r"\b(never|not|no|nothing|none|without|don't|do not|nobody|no one|avoid|refuse)\b", re.I)
SCHEMA = {"name": str, "slug": str, "confidence": int, "source_url": str, "checked": str,
          "dossier": str}


def changed_slugs():
    try:
        out = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"], cwd=ROOT,
                             capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return None
    slugs = set()
    for line in out.splitlines():
        m = re.match(r"(?:drops|data/drops)/(.+)\.(md|json)$", line.strip())
        if m:
            slugs.add(m.group(1))
    return slugs


def check(slug):
    errors, warnings = [], []
    md_path, json_path = DROPS / f"{slug}.md", DATA_DROPS / f"{slug}.json"

    if not md_path.exists():
        errors.append("missing dossier markdown")
    if not json_path.exists():
        errors.append("missing data/drops json")
        return errors, warnings
    try:
        d = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"invalid json: {e}"], warnings

    for key, typ in SCHEMA.items():
        if key not in d:
            errors.append(f"missing key: {key}")
        elif not isinstance(d[key], typ):
            errors.append(f"{key} must be {typ.__name__}")
    if errors:
        return errors, warnings

    if not 0 <= d["confidence"] <= 100:
        errors.append(f"confidence out of range: {d['confidence']}")
    if not d["source_url"].startswith("http"):
        errors.append("source_url must be a URL")
    if d["dossier"] != f"drops/{slug}.md":
        errors.append("dossier path does not match slug")

    steps = d.get("steps") or []
    if not isinstance(steps, list):
        errors.append("steps must be a list")
        steps = []
    if d["confidence"] >= 40 and not steps:
        errors.append(f"confidence {d['confidence']} but no steps extracted")
    if any(len(s.strip()) < 10 for s in steps):
        warnings.append("a step is under 10 characters")

    ev = d.get("evidence") or []
    if not ev:
        errors.append("no evidence listed")
    joined = " ".join(ev).lower()
    if d.get("official") and "official site linked" not in joined:
        errors.append("official URL present but evidence does not mention 'official site linked'")
    if "official site linked" in joined and not d.get("official"):
        errors.append("evidence claims an official site but none is stored")

    off = (d.get("official") or "").strip()
    if off:
        if not off.startswith("https://"):
            errors.append(f"official URL must be https: {off}")
        if any(t in off.lower() for t in TRACKER_DOMAINS):
            errors.append(f"official URL points at a tracker, not the project: {off}")
        if re.search(r"\b(bit\.ly|t\.co|goo\.gl|tinyurl\.com)\b", off, re.I):
            errors.append("official URL uses a link shortener")

    blob = (md_path.read_text(encoding="utf-8") if md_path.exists() else "")
    for sec in REQUIRED_SECTIONS:
        if sec not in blob:
            errors.append(f"dossier missing section: {sec}")
    for pat in BANNED:
        if re.search(pat, blob, re.I):
            errors.append(f"banned content in dossier: {pat}")
    for sentence in re.split(r"(?<=[.!?])\s+", blob):
        if SECRET_RE.search(sentence) and not NEGATION.search(sentence):
            errors.append("secret request detected (mentions seed/private key without a warning): "
                          + sentence.strip()[:90])
            break
    if d["name"] not in blob.splitlines()[0]:
        errors.append("dossier H1 does not match record name")
    if "http://" in blob:
        warnings.append("dossier contains an http:// link")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed", action="store_true")
    ap.add_argument("--slug", default="")
    args = ap.parse_args()

    slugs = ([args.slug] if args.slug else
             (sorted(changed_slugs() or []) if args.changed else
              sorted(p.stem for p in DROPS.glob("*.md"))))
    if key := args.changed and not slugs:
        print("no dossier changes in this PR")
        return 0

    failed = 0
    for slug in slugs:
        errors, warnings = check(slug)
        if errors:
            failed += 1
            print(f"FAIL {slug}")
            for e in errors:
                print(f"   x {e}")
        else:
            print(f"PASS {slug}" + (f"  ({len(warnings)} warning)" if warnings else ""))
        for w in warnings:
            print(f"   ! {w}")
    print(f"\n{len(slugs)} dossier(s) checked, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
