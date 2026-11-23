"""Publish one verification dossier per airdrop as its own pull request.

For each selected drop this writes drops/<slug>.md plus data/drops/<slug>.json, commits them on a
branch named verify/<slug>, pushes it, and opens a PR against main. The PR body carries the evidence
table so a reviewer can approve without opening the files.

  python tools/pr_drop.py --list                  # suggest what to publish next
  python tools/pr_drop.py --slug yakkamon         # one drop
  python tools/pr_drop.py --top 10 --dry-run      # what would happen
  python tools/pr_drop.py --top 10                # publish for real

Needs a GitHub token: taken from GITHUB_TOKEN, or from the git credential helper (same scope the
repo already pushes with). Never printed.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DATA = ROOT / "docs" / "data.json"
DROPS = ROOT / "drops"
DATA_DROPS = ROOT / "data" / "drops"
REPO = "sandeshbagmare/crypto-airdrops-ops"

sys.path.insert(0, str(ROOT / "tools"))
try:
    from triage import triage as run_triage
except Exception:  # triage is optional at import time
    run_triage = None


def forensics(url):
    """Domain forensics for the official site, or a note that it could not be checked."""
    if not url or not run_triage:
        return {"verdict": "not checked", "score": None, "findings": [], "age_days": None}
    try:
        rep = run_triage(url)
    except Exception as e:
        return {"verdict": "check failed", "score": None, "findings": [["WARN", str(e)[:80]]],
                "age_days": None}
    age = None
    for level, msg in rep.get("findings", []):
        if "domain" in msg:
            m = re.search(r"(\d+) days", msg)
            if m:
                age = int(m.group(1))
                break
    return {"verdict": rep.get("verdict"), "score": rep.get("score"),
            "findings": [[l, m] for l, m in rep.get("findings", [])], "age_days": age,
            "checked": rep.get("checked", "")}


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]


def load():
    return json.loads(DOCS_DATA.read_text(encoding="utf-8"))


def dossier(d):
    """Markdown dossier: everything known, plus what the operator must decide."""
    steps = d.get("steps") or []
    ev = d.get("evidence") or []
    lines = [
        f"# {d['name']}",
        "",
        f"**Confidence {d.get('confidence')}/100** - documentation quality, not a payout forecast.",
        f"**Status** {d.get('status') or 'unknown'} | **Key date** {d.get('end') or 'none stated'} "
        f"| **Days left** {d.get('days') if isinstance(d.get('days'), int) else 'n/a'}",
        "",
        "## What it is",
        "",
        d.get("what") or "_The source gives no description._",
        "",
        "## Official site",
        "",
        (d.get("official") or "_No official site could be extracted from the guide - verify manually._"),
        "",
        "## What it needs",
        "",
        d.get("needs") or "Nothing stated in the source.",
        "",
        "## Steps",
        "",
    ]
    lines += [f"{i}. {s}" for i, s in enumerate(steps, 1)] or ["_No steps extracted; read the source._"]
    lines += ["", "## Who is behind it", "", d.get("behind") or "_Not disclosed in the source._", ""]
    lines += ["## Costs", "", d.get("costs") or "_Not disclosed in the source._", ""]
    lines += ["## Risks", "", d.get("risks") or "_Not disclosed in the source._", ""]
    lines += ["## Pool (as stated by the source)", "", d.get("pool") or "_Source states no pool size._", ""]
    f = d.get("forensics") or {}
    lines += ["## Domain forensics", "",
              f"Verdict: **{f.get('verdict') or 'not checked'}**"
              + (f" (risk score {f['score']})" if f.get("score") is not None else "")
              + (f" | domain age {f['age_days']} days" if f.get("age_days") else ""), ""]
    for level, msg in (f.get("findings") or []):
        lines.append(f"- **{level}** {msg}")
    if not f.get("findings"):
        lines.append("_No forensics run for this drop._")
    lines += [""]
    lines += ["## Evidence", ""] + [f"- {e}" for e in ev] or ["- none"]
    lines += ["", f"Source: {d.get('source_url') or 'n/a'} (checked {d.get('checked') or 'n/a'})", ""]
    lines += [
        "## Reviewer checklist",
        "",
        "- [ ] official domain matches the project's own docs or verified X profile",
        "- [ ] no deposit, fee or paid whitelist required",
        "- [ ] deadline confirmed on the official site",
        "- [ ] steps reproduce on the official site, not only on the tracker",
        "- [ ] `python tools/triage.py <official>` returns clean",
        "",
    ]
    return "\n".join(lines)


def sh(*args, check=True):
    r = subprocess.run(list(args), cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(args[:3])} failed: {r.stderr[-300:]}")
    return r


def token():
    t = os.environ.get("GITHUB_TOKEN", "").strip()
    if t:
        return t
    r = subprocess.run(["git", "-c", "credential.interactive=false", "credential", "fill"],
                       input="protocol=https\nhost=github.com\n\n", capture_output=True,
                       text=True, timeout=30)
    for line in r.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("no GitHub token available")


def api(path, method="GET", body=None, tok=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"https://api.github.com{path}", data=data, method=method)
    for k, v in {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json", "User-Agent": "airdrop-ops"}.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
        return json.loads(raw) if raw else {}


def publish(d, tok, dry_run=False):
    slug = slugify(d["name"])
    branch = f"verify/{slug}"
    md_path = DROPS / f"{slug}.md"
    json_path = DATA_DROPS / f"{slug}.json"
    DROPS.mkdir(exist_ok=True)
    DATA_DROPS.mkdir(parents=True, exist_ok=True)

    record = dict(d)
    record["slug"] = slug
    record["dossier"] = f"drops/{slug}.md"
    record["published"] = date.today().isoformat()
    fx = forensics(d.get("official") or "")
    record["forensics"] = fx
    d = dict(d, forensics=fx)

    if fx.get("verdict") == "SCAM-LIKELY":
        return {"slug": slug, "branch": branch, "pr": None,
                "blocked": f"domain forensics: SCAM-LIKELY (score {fx.get('score')})"}
    if fx.get("verdict") == "DEAD-LINK":
        return {"slug": slug, "branch": branch, "pr": None,
                "blocked": "official domain is a dead link - row stays in the watchlist, "
                           "not published as a drop"}

    md_path.write_text(dossier(d), encoding="utf-8")
    json_path.write_text(json.dumps(record, indent=1, ensure_ascii=False), encoding="utf-8")

    if dry_run:
        return {"slug": slug, "branch": branch, "pr": None, "dry_run": True}

    sh("git", "fetch", "origin", "main", "-q")
    sh("git", "checkout", "-q", "-B", branch, "origin/main")
    sh("git", "add", f"drops/{slug}.md", f"data/drops/{slug}.json")
    sh("git", "commit", "-q", "-m",
       f"verify({slug}): dossier, confidence {d.get('confidence')}, {len(d.get('steps') or [])} steps")
    sh("git", "push", "-q", "-f", "origin", branch)

    body = "\n".join([
        f"## {d['name']}",
        "",
        f"- **Confidence** {d.get('confidence')}/100",
        f"- **Key date** {d.get('end') or 'none stated'}"
        + (f" ({d['days']} days left)" if isinstance(d.get('days'), int) else ""),
        f"- **Official** {d.get('official') or 'not extracted'}",
        f"- **Steps extracted** {len(d.get('steps') or [])}",
        f"- **Domain forensics** {(d.get('forensics') or {}).get('verdict')} "
        f"(score {(d.get('forensics') or {}).get('score')})",
        f"- **Source** {d.get('source_url') or 'n/a'} - checked {d.get('checked') or 'n/a'}",
        "",
        "**What it is**",
        "",
        (d.get("what") or "_none_")[:600],
        "",
        "**Evidence**",
        "",
    ] + [f"- {e}" for e in (d.get("evidence") or [])] + [
        "",
        "**Risks**",
        "",
        (d.get("risks") or "_not disclosed_")[:400],
        "",
        "---",
        f"Dossier: `drops/{slug}.md` | machine record: `data/drops/{slug}.json`",
        "CI must pass `validate-drops` before this can merge.",
    ])

    try:
        pr = api(f"/repos/{REPO}/pulls", "POST", {
            "title": f"verify({slug}): confidence {d.get('confidence')}, {len(d.get('steps') or [])} steps",
            "head": branch, "base": "main", "body": body,
        }, tok)
        num = pr.get("number")
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:200]
        if e.code == 422 and "already exists" in detail:
            for p in api(f"/repos/{REPO}/pulls?state=open&head=sandeshbagmare:{branch}", tok=tok):
                num = p.get("number")
            try:
                api(f"/repos/{REPO}/pulls/{num}", "PATCH", {
                    "title": f"verify({slug}): confidence {d.get('confidence')}, "
                             f"{len(d.get('steps') or [])} steps",
                    "body": body,
                }, tok)
            except Exception:
                pass
            return {"slug": slug, "branch": branch, "pr": num, "existing": True}
        return {"slug": slug, "branch": branch, "pr": None, "error": detail}

    labels = ["verification"]
    try:
        api(f"/repos/{REPO}/issues/{num}/labels", "POST", {"labels": labels}, tok)
    except Exception:
        pass
    return {"slug": slug, "branch": branch, "pr": num}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default="")
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = load()
    published = {p.stem for p in DROPS.glob("*.md")} if DROPS.exists() else set()
    try:
        refs = subprocess.run(["git", "ls-remote", "--heads", "origin", "verify/*"], cwd=ROOT,
                              capture_output=True, text=True, timeout=60).stdout
        for line in refs.splitlines():
            m = re.search(r"refs/heads/verify/(.+)$", line.strip())
            if m:
                published.add(m.group(1))
    except Exception:
        pass
    pool = [d for d in data if isinstance(d.get("confidence"), int) and d["confidence"] >= 40]

    if args.list:
        todo = [d for d in pool if slugify(d["name"]) not in published]
        todo.sort(key=lambda d: (0 if isinstance(d.get("days"), int) and d["days"] >= 0 else 1,
                                 d.get("days") if isinstance(d.get("days"), int) else 9999,
                                 -d["confidence"]))
        for d in todo[:15]:
            print(f"  {slugify(d['name'])[:34]:36} conf {d['confidence']:<4} "
                  f"days {str(d.get('days')):<6} {d['name'][:30]}")
        print(f"unpublished with confidence >=40: {len(todo)}")
        return 0

    if args.slug:
        target = [d for d in data if slugify(d["name"]) == args.slug]
        if not target:
            print(f"no drop matching {args.slug}")
            return 2
    else:
        todo = [d for d in pool if slugify(d["name"]) not in published]
        todo.sort(key=lambda d: (0 if isinstance(d.get("days"), int) and d["days"] >= 0 else 1,
                                 d.get("days") if isinstance(d.get("days"), int) else 9999,
                                 -d["confidence"]))
        target = todo[:args.top or 5]

    tok = "" if args.dry_run else token()
    created = []
    for d in target:
        try:
            r = publish(d, tok, args.dry_run)
            created.append(r)
            if r.get("blocked"):
                print(f"  {r['slug']:36} -> BLOCKED: {r['blocked']}")
            elif r.get("pr"):
                print(f"  {r['slug']:36} -> PR #{r['pr']}")
            else:
                print(f"  {r['slug']:36} -> dry run")
        except Exception as e:
            print(f"  FAILED {d['name'][:40]}: {e}")
            break

    if not args.dry_run and created:
        sh("git", "checkout", "-q", "main")
        print(f"back on main; {sum(1 for c in created if c.get('pr'))} PRs open")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
