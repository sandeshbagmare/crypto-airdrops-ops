"""Walk the whole ledger in a real browser and record exactly what each drop needs.

Every row gets: a domain check, the live page opened, a screenshot and page text saved as evidence,
and a verdict. The verdict is honest - the script never submits a form, never enters an email, never
connects a wallet and never signs anything. It stops at the boundary and records who has to cross it.

  python tools/bulk_apply.py --limit 12            # smoke test
  python tools/bulk_apply.py --workers 6           # whole ledger, parallel
  python tools/bulk_apply.py --only ready          # re-check a subset

Outputs:
  data/preflight.json           one record per drop (merged, never truncated)
  airships/<slug>/page.txt      page text as evidence
  airships/<slug>/landing.png   screenshot as evidence
"""
import argparse
import json
import re
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DOCS_DATA = ROOT / "docs" / "data.json"
PREFLIGHT = ROOT / "data" / "preflight.json"
BATCH = ROOT / "data" / "preflight-batch.json"
AIRSHIPS = ROOT / "airships"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

WALLET = re.compile(r"(connect wallet|connect your wallet|walletconnect|metamask|phantom|"
                    r"rainbow|coinbase wallet|connect to (claim|earn))", re.I)
KYC = re.compile(r"(\bkyc\b|verify your identity|identity verification|proof of address|"
                 r"upload.*(passport|\bid\b)|accredited investor)", re.I)
CAPTCHA = re.compile(r"(captcha|recaptcha|hcaptcha|turnstile|cf-challenge|just a moment)", re.I)
LOGIN = re.compile(r"(log ?in|sign ?in|create account|register|sign ?up)", re.I)
EMAIL = re.compile(r"(email|e-mail|waitlist|confirm your)", re.I)
TERMS = re.compile(r"(no bots|automation|sybil|one entry per person|terms of service)", re.I)

LOCK = threading.Lock()
DONE = {"n": 0}
TOTAL = {"n": 0}


def _atomic(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]


def host_of(url):
    try:
        return (urlparse(url).hostname or "").lower()
    except Exception:
        return ""


def tick(label):
    with LOCK:
        DONE["n"] += 1
        n, total = DONE["n"], TOTAL["n"]
    print(f"[{n:4}/{total}] {label}", flush=True)


def triage_cached(url, row):
    """Use the recorded forensic verdict; only call the network if the row has none."""
    f = row.get("forensics") or {}
    if f.get("verdict"):
        return f.get("verdict"), f.get("score")
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        from triage import triage
        rep = triage(url)
        return rep["verdict"], rep["score"]
    except Exception as e:
        return f"check failed: {type(e).__name__}", None


def inspect(page, slug, url):
    """Read the live page and say what a human would have to do here."""
    body = page.inner_text("body")[:20000]
    folder = AIRSHIPS / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "page.txt").write_text(
        f"URL: {page.url}\nTITLE: {page.title()}\nCHECKED: {datetime.now():%Y-%m-%d %H:%M}\n\n{body}",
        encoding="utf-8")

    shot = folder / "landing.png"
    try:
        page.screenshot(path=str(shot), full_page=False)
    except Exception:
        shot = None

    fields = page.evaluate("""() => Array.from(document.querySelectorAll('input,textarea,select'))
        .map(el => ({tag: el.tagName.toLowerCase(), type: el.type||'', name: el.name||'',
                     placeholder: el.placeholder||'',
                     label: (el.labels&&el.labels[0]&&el.labels[0].innerText||'').slice(0,60)}))
        .filter(f => (f.type||'').toLowerCase() !== 'hidden').slice(0, 15)""")
    buttons = page.evaluate("""() => Array.from(document.querySelectorAll('button,a'))
        .map(el => (el.innerText||'').trim()).filter(t => t && t.length < 40).slice(0, 80)""")
    has_eth = page.evaluate("() => !!window.ethereum")

    text = (body + " " + " ".join(buttons)).lower()
    email_field = any((f.get("type") or "").lower() == "email"
                      or "email" in (f.get("name") or "").lower()
                      or "email" in (f.get("placeholder") or "").lower()
                      for f in fields)
    res = {
        "text_chars": len(body.strip()),
        "title": page.title()[:120],
        "final_url": page.url,
        "fields": fields,
        "wallet_prompt": bool(WALLET.search(text)) or has_eth,
        "kyc_prompt": bool(KYC.search(text)),
        "captcha": bool(CAPTCHA.search(text)),
        "login_prompt": bool(LOGIN.search(text)),
        "email_prompt": bool(EMAIL.search(text)) or email_field,
        "terms_prompt": bool(TERMS.search(text)),
        "injected_wallet": has_eth,
        "evidence": [f"airships/{slug}/page.txt"] + ([f"airships/{slug}/landing.png"] if shot else []),
    }

    # the blocker that actually stops an agent, in the order AGENTS.md ranks them
    must, blocked_on = [], ""
    if res["kyc_prompt"]:
        must.append("complete identity verification (KYC)")
        blocked_on = "kyc"
    if res["wallet_prompt"]:
        must.append("connect a wallet and approve the signature")
        blocked_on = blocked_on or "wallet_signature"
    if res["captcha"]:
        must.append("solve a CAPTCHA / bot check")
        blocked_on = blocked_on or "captcha"
    if res["email_prompt"] and not blocked_on:
        must.append("enter an email and click the confirmation link")
        blocked_on = "email"
    if res["login_prompt"] and not blocked_on:
        must.append("log in or create the account (human session)")
        blocked_on = "login"
    if res["terms_prompt"] and not blocked_on:
        must.append("accept the project's terms in your own name")
        blocked_on = "terms"

    agent_can = []
    if fields:
        agent_can.append(f"pre-fill {len(fields)} form field(s) for review")
    agent_can.append("read requirements, capture evidence, record the packet")
    if not must and len(body.strip()) < 400:
        # a JS shell that rendered nothing is not ready; the detector had nothing to read
        must.append("page rendered almost no text (JS-only shell) - read it yourself")
        blocked_on = "unknown"
    if not must:
        blocked_on = ""

    res["human_must"] = must
    res["agent_can"] = agent_can
    res["blocked_on"] = blocked_on
    res["status"] = "blocked" if must else "ready"
    return res


def run_chunk(items, wid):
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA, viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        for row, slug in items:
            url = row.get("official") or ""
            rec = {"project": row["name"], "slug": slug, "official": url,
                   "at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                   "confidence": row.get("confidence"),
                   "days": row.get("days"),
                   "steps_from_source": len(row.get("steps") or [])}
            try:
                if not url.startswith("http"):
                    rec.update(status="no-url", blocked_on="no-official-site",
                               human_must=["find the official site from the project's own profile"],
                               agent_can=["keep the row, flag it for manual domain research"],
                               note="no official site extracted from the guide")
                    out[slug] = rec
                    tick(f"NOURL {slug}")
                    continue

                verdict, score = triage_cached(url, row)
                rec["domain_verdict"] = verdict
                rec["domain_score"] = score
                if verdict in ("DEAD-LINK", "SCAM-LIKELY"):
                    rec.update(status="refused", blocked_on="domain",
                               human_must=["nothing - the domain is dead or looks like a scam"],
                               agent_can=["refuse to open it, keep the row for the record"],
                               note=f"domain check says {verdict} - not opening it",
                               evidence=[])
                    out[slug] = rec
                    tick(f"REFUSE {slug} ({verdict})")
                    continue

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(2500)
                    rec.update(inspect(page, slug, url))
                except Exception as e:
                    rec.update(status="unreachable", blocked_on="site-unreachable",
                               human_must=["try the URL in your own browser"],
                               agent_can=["recorded the failure, kept the row"],
                               note=f"{type(e).__name__}: {str(e)[:150]}")
                    try:
                        page.goto("about:blank")
                    except Exception:
                        page = ctx.new_page()
                    out[slug] = rec
                    tick(f"UNREACH {slug}")
                    continue

                if verdict == "SUSPICIOUS":
                    rec["human_must"].append("confirm the domain against the project's own profile "
                                             "before touching it (forensics flags it)")
                    rec["status"] = "blocked"
                    rec["blocked_on"] = rec.get("blocked_on") or "domain"
                out[slug] = rec
                tick(f"{rec['status'].upper():5} {slug[:32]:34} {rec.get('blocked_on') or '-':18} "
                     f"{verdict[:14]}")
            except Exception:
                rec.update(status="error", blocked_on="unknown",
                           note=traceback.format_exc()[-300:])
                out[slug] = rec
                tick(f"ERROR {slug}")
        browser.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only", default="", help="re-check slugs with this current status")
    ap.add_argument("--offset", type=int, default=0)
    args = ap.parse_args()

    rows = json.loads(DOCS_DATA.read_text(encoding="utf-8"))
    prev = {}
    for src in (PREFLIGHT, BATCH):
        try:
            prev.update(json.loads(src.read_text(encoding="utf-8")))
        except Exception:
            pass

    seen, items = set(), []
    for row in rows:
        slug = slugify(row["name"])
        if slug in seen:
            continue
        seen.add(slug)
        if args.only and (prev.get(slug) or {}).get("status") != args.only:
            continue
        items.append((row, slug))
    items = items[args.offset:]
    if args.limit:
        items = items[:args.limit]

    TOTAL["n"] = len(items)
    print(f"inspecting {len(items)} drops with {args.workers} workers", flush=True)
    started = time.time()

    chunks = [items[i::args.workers] for i in range(args.workers)]
    merged = {}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for part in ex.map(lambda a: run_chunk(*a), [(c, i) for i, c in enumerate(chunks)]):
            merged.update(part)

    # two files on purpose: BATCH is written only by this tool and is the authoritative record,
    # PREFLIGHT is shared with auto_apply.py which rewrites it for its own top-N runs.
    prev.update(merged)
    _atomic(PREFLIGHT, prev)
    _atomic(BATCH, prev)

    counts = {}
    for v in merged.values():
        counts[v.get("status", "?")] = counts.get(v.get("status", "?"), 0) + 1
    print(f"\n{len(merged)} drops in {time.time() - started:.0f}s: " +
          " | ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print("evidence: airships/<slug>/ | record: data/preflight.json")
    print("next: python tools/blocker_workbook.py")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
