"""Read-only airdrop monitor. Fetches public trackers, reports only what changed.

Safe by construction: no wallet, no auth, no POST, one GET per source per run,
and it never deletes or rewrites the ledger.
"""
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "notes" / ".monitor_state.json"

SOURCES = {
    "airdroplet": "https://airdroplet.com/testnet-airdrops",
    "airdropvillage": "https://www.airdropvillage.io/airdrops",
}
UA = "airdrops-ops-monitor/1.0 (+personal research)"
TAG = re.compile(r"<[^>]+>")
HEAD = re.compile(r"<h[23][^>]*>(.*?)</h[23]>", re.S | re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def clean(s):
    return re.sub(r"\s+", " ", TAG.sub(" ", s)).strip()


STOP = (
    "how ", "what ", "why ", "free ", "filter", "follow us", "faq", "browse",
    "compare", "prioritize", "stay safe", "latest", "view ", "share", "menu",
    "subscribe", "newsletter", "cookie", "about", "contact", "privacy",
    "help", "legal", "check the ", "search",
)


def projects(html):
    names = set()
    for raw in HEAD.findall(html):
        t = clean(raw).rstrip("↗  ").strip()
        if not (2 <= len(t) <= 48):
            continue
        if t.lower().startswith(STOP):
            continue
        if t.endswith(("?", ":")):
            continue
        names.add(t)
    return names


def load():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def main():
    old = load()
    new = {}
    lines = []
    changed = 0

    for key, url in SOURCES.items():
        try:
            html = fetch(url)
        except Exception as e:
            lines.append(f"- {key}: FETCH FAILED ({type(e).__name__})")
            new[key] = old.get(key, {"names": [], "digest": ""})
            continue

        names = sorted(projects(html))
        digest = hashlib.sha256(
            "|".join(names).encode("utf-8")
        ).hexdigest()[:16]
        prev = old.get(key, {})
        prev_names = set(prev.get("names", []))

        added = [n for n in names if n not in prev_names]
        gone = sorted(prev_names - set(names))
        if added or gone:
            changed += 1
            lines.append(f"- **{key}**: {len(added)} new, {len(gone)} gone")
            for n in added[:15]:
                lines.append(f"  - NEW: {n}")
            for n in gone[:10]:
                lines.append(f"  - GONE: {n}")
        else:
            lines.append(f"- {key}: unchanged ({len(names)} projects, digest {digest})")

        new[key] = {"names": names, "digest": digest,
                    "checked": dt.datetime.now().isoformat(timespec="seconds")}

    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"# Monitor run {stamp}\n\n" + "\n".join(lines) + "\n"
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(new, indent=1), encoding="utf-8")
    (ROOT / "notes" / "monitor-latest.md").write_text(report, encoding="utf-8")
    with (ROOT / "notes" / "monitor-log.md").open("a", encoding="utf-8") as f:
        f.write(report + "\n")

    print(report)
    print(f"changed_sources={changed}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
