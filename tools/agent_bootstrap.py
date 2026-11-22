"""Turn the ledger into an actionable queue: agent/STATE.json + agent/handoffs/*.json.

Prioritises drops that close soonest, then best-evidenced, and pre-classifies what a human will have
to do (login, KYC, wallet signature) so an agent knows before it starts where it must stop.

  python tools/agent_bootstrap.py            # queue everything
  python tools/agent_bootstrap.py --top 25   # only the 25 most urgent
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT = ROOT / "agent"
HANDOFFS = AGENT / "handoffs"
DOCS_DATA = ROOT / "docs" / "data.json"
STATE = AGENT / "STATE.json"


def load():
    if not DOCS_DATA.exists():
        print("run tools/build_ledger.py first")
        raise SystemExit(2)
    return json.loads(DOCS_DATA.read_text(encoding="utf-8"))


def classify(d):
    """What will this drop force a human to do, given everything the sources state?"""
    blob = " ".join([
        d.get("needs") or "", d.get("what") or "",
        " ".join(d.get("steps") or []), d.get("behind") or "",
    ]).lower()
    if any(w in blob for w in ("kyc", "passport", "identity verification", "proof of address")):
        return "kyc", "identity verification is required and cannot be performed by an agent"
    if any(w in blob for w in ("sign the message", "sign a message", "approve", "connect")):
        return "wallet_signature", "a wallet connection or signature is required"
    if any(w in blob for w in ("telegram", "discord")):
        return "login", "the drop requires a Telegram or Discord account session"
    if any(w in blob for w in ("x post", "tweet", "follow @", "on x", "twitter")):
        return "login", "an X account post or follow is required"
    if any(w in blob for w in ("email", "e-mail", "inbox")):
        return "email", "an email confirmation link must be opened by the human"
    return "none", "no human-only step detected from the source; still confirm before submitting"


def bucket(d):
    days = d.get("days")
    conf = d.get("confidence") if isinstance(d.get("confidence"), int) else 0
    fr = d.get("friction") if isinstance(d.get("friction"), int) else 50
    if isinstance(days, int) and days >= 0:
        return (0, days, fr, -conf)
    return (1, 9999, fr, -conf)


def handoff(d, blocked, why):
    slug = re.sub(r"[^a-z0-9]+", "-", d["name"].lower()).strip("-")
    steps = d.get("steps") or []
    packet = {
        "project": d["name"],
        "official_url": d.get("official") or "",
        "source_url": d.get("source_url") or "",
        "blocked_on": blocked,
        "why_agent_cannot": why,
        "what_human_must_do": (steps[:8] or
                               ["Read the official site and follow its stated steps."]),
        "where_to_resume": (f"python tools/agent_browser.py --identity main --url "
                            f"{d.get('official') or d.get('source_url') or ''}"),
        "evidence_so_far": [],
        "confidence": d.get("confidence"),
        "evidence": d.get("evidence", []),
        "costs": d.get("costs", ""),
        "risks": d.get("risks", ""),
        "created": date.today().isoformat(),
        "status": "open",
    }
    HANDOFFS.mkdir(parents=True, exist_ok=True)
    path = HANDOFFS / f"{slug}.json"
    path.write_text(json.dumps(packet, indent=1, ensure_ascii=False), encoding="utf-8")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=0)
    args = ap.parse_args()

    data = load()
    data = [d for d in data if isinstance(d.get("confidence"), int) and d["confidence"] > 0]
    data.sort(key=bucket)
    if args.top:
        data = data[:args.top]

    queue = {}
    for d in data:
        blocked, why = classify(d)
        slug = re.sub(r"[^a-z0-9]+", "-", d["name"].lower()).strip("-")
        entry = {"project": d["name"], "confidence": d.get("confidence"),
                 "days_left": d.get("days"), "end": d.get("end") or "",
                 "official": d.get("official") or "", "blocked_on": blocked,
                 "friction": d.get("friction"),
                 "friction_label": d.get("friction_label") or "",
                 "next_action": "none" if blocked == "none" else f"hand off: {blocked}",
                 "status": "identified", "handoff": "", "updated": date.today().isoformat()}
        if blocked != "none":
            entry["handoff"] = str(handoff(d, blocked, why).relative_to(ROOT)).replace("\\", "/")
            entry["status"] = "blocked"
        else:
            entry["next_action"] = "triage, then run the browser session"
        queue[slug] = entry

    AGENT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"identity": "main", "generated": date.today().isoformat(),
                                 "count": len(queue), "drops": queue},
                                indent=1, ensure_ascii=False), encoding="utf-8")

    by_block = {}
    for e in queue.values():
        by_block[e["blocked_on"]] = by_block.get(e["blocked_on"], 0) + 1
    soon = sum(1 for e in queue.values() if isinstance(e["days_left"], int) and e["days_left"] <= 30)
    free = sum(1 for e in queue.values() if e.get("friction") == 0)
    print(f"queue: {len(queue)} drops, {soon} closing within 30 days, {free} with no identity step")
    print("blocked-on:", dict(sorted(by_block.items(), key=lambda x: -x[1])))
    print(f"state: {STATE.relative_to(ROOT)}  handoffs: {len(list(HANDOFFS.glob('*.json')))}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
