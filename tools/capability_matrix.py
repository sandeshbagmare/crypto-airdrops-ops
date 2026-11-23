"""Classify every drop by who can actually complete it: agent, agent+session, or human-only.

The point is to stop guessing. Each drop lands in one bucket based on what its steps demand, so the
answer to "can agents apply to most of this?" is a count, not an opinion.

  python tools/capability_matrix.py            # print and write notes/autonomy.md
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DATA = ROOT / "docs" / "data.json"
OUT = ROOT / "data" / "capability.json"
NOTE = ROOT / "notes" / "autonomy.md"

BUCKETS = [
    ("human_kyc", "KYC / identity documents", ("kyc", "passport", "proof of address",
                                              "identity verification")),
    ("human_money", "deposit, purchase or stake required", ("deposit", "minimum", "fund your",
                                                           "purchase", "buy ")),
    ("human_signature", "wallet connect or signature", ("connect", "sign the message",
                                                        "sign a message", "approve")),
    ("human_account", "needs a Telegram / Discord / X account", ("telegram", "discord",
                                                                "x post", "tweet", "follow @")),
    ("agent_email", "email form only", ("email", "e-mail", "waitlist")),
]


def classify(d):
    blob = " ".join([d.get("needs") or "", d.get("what") or "",
                     " ".join(d.get("steps") or [])]).lower()
    live = d.get("live_check") or ""
    if live == "ready":
        return "agent_live", "a real browser opened the live page and saw no identity step"
    if live == "refused":
        return "refused", "domain failed the safety check - drop is not real or not live"
    if live == "unreachable":
        return "unreachable", "official site did not load - source may be stale"
    for key, label, words in BUCKETS:
        if any(w in blob for w in words):
            return key, label
    if (d.get("steps") or []) and (d.get("forensics") or {}).get("verdict") != "DEAD-LINK":
        return "agent_read", "no identity step detected - reading and form fields only"
    return "unknown", "no usable steps extracted"


def main():
    data = json.loads(DOCS_DATA.read_text(encoding="utf-8"))
    counts, rows = {}, []
    for d in data:
        key, label = classify(d)
        counts[key] = counts.get(key, 0) + 1
        rows.append({"name": d["name"], "bucket": key, "label": label,
                     "confidence": d.get("confidence"), "friction": d.get("friction"),
                     "days": d.get("days"), "official": d.get("official")})

    OUT.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")

    order = ["agent_live", "agent_read", "agent_email", "human_account", "human_signature",
             "human_money", "human_kyc", "refused", "unreachable", "unknown"]
    labels = {k: v for k, _, v in [(b[0], b[1], b[2]) for b in BUCKETS]}
    labels["agent_read"] = "no identity step detected - reading and form fields only"
    labels["unknown"] = "no usable steps extracted"
    total = len(data)
    agent_can = counts.get("agent_live", 0) + counts.get("agent_read", 0) + counts.get("agent_email", 0)
    human_touch = counts.get("human_account", 0) + counts.get("human_signature", 0)

    lines = [
        "# What an agent can actually complete",
        "",
        f"{total} drops classified on {len(data)} rows of extracted steps. "
        "Buckets are decided by what the steps themselves demand, not by optimism.",
        "",
        "| Bucket | Drops | Share | Who finishes it |",
        "|---|---|---|---|",
    ]
    who = {"agent_live": "agent alone - confirmed on the live page",
           "agent_read": "agent alone (no identity)", "agent_email": "agent prepares, human clicks "
           "the confirmation link in their inbox", "human_account": "human logs in once, agent "
           "continues in that session", "human_signature": "human approves one wallet signature, "
           "agent continues", "human_money": "human decides whether to spend; usually skip",
           "human_kyc": "human only - legal identity step", "unknown": "needs manual reading",
           "refused": "nobody - domain failed the safety check",
           "unreachable": "nobody until the source is re-checked"}
    for key in order:
        if counts.get(key):
            lines.append(f"| {labels.get(key, key)} | {counts[key]} | "
                         f"{counts[key] * 100 / total:.0f}% | {who[key]} |")
    lines += [
        "",
        f"**Agent-completable without any human**: {agent_can} of {total} "
        f"({agent_can * 100 / total:.0f}%).",
        f"**One human touch unlocks**: {human_touch} more "
        f"({human_touch * 100 / total:.0f}%) - a login or a signature, then the agent continues.",
        f"**Human-only by law or by money**: {counts.get('human_kyc', 0) + counts.get('human_money', 0)}.",
        "",
        "Caveats that keep this honest:",
        "",
        "- Many of these sites forbid automation in their terms. A bucket says what is *possible*, "
        "not what is *permitted* - check the project's terms before letting an agent act.",
        "- \"Agent alone\" means no identity step is described in the source. The live page can still "
        "ask for one; `tools/auto_apply.py` checks that before doing anything.",
        "- Nothing here creates accounts. Registering as a person is a person's act.",
        "",
        "Regenerate: `python tools/capability_matrix.py`.",
    ]
    NOTE.write_text("\n".join(lines), encoding="utf-8")

    print(f"classified {total} drops")
    for key in order:
        if counts.get(key):
            print(f"  {key:18} {counts[key]:4}  {labels.get(key, '')[:60]}")
    print(f"agent-only: {agent_can} | one human touch: {human_touch} | human-only: "
          f"{counts.get('human_kyc', 0) + counts.get('human_money', 0)}")
    print("wrote notes/autonomy.md")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
