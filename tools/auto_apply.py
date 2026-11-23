"""Pre-flight a drop in a real browser and do everything an agent legitimately can.

For each drop this: checks the domain, opens the official page in a persistent profile, saves the page
text and a screenshot as evidence, detects the live requirements (form fields, wallet buttons, CAPTCHA,
KYC demands, existing login), and writes a plan. It never submits a form, never enters a secret and
never signs anything - it stops exactly at the boundary and hands that step to the operator.

  python tools/auto_apply.py --project Yakkamon
  python tools/auto_apply.py --top 8            # pre-flight the queue in order
  python tools/auto_apply.py --top 5 --headed   # operator watches and can log in
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

DOCS_DATA = ROOT / "docs" / "data.json"
OUT_DIR = ROOT / "airships"
SUMMARY = ROOT / "data" / "preflight.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

WALLET_WORDS = re.compile(r"(connect wallet|connect your wallet|walletconnect|metamask|"
                          r"phantom|rainbow|coinbase wallet)", re.I)
KYC_WORDS = re.compile(r"(\bkyc\b|verify your identity|identity verification|proof of address|"
                       r"upload.*(passport|id\b))", re.I)
CAPTCHA_WORDS = re.compile(r"(captcha|recaptcha|hcaptcha|turnstile|cf-challenge|just a moment)", re.I)
LOGIN_WORDS = re.compile(r"(log ?in|sign ?in|connect wallet|create account|register)", re.I)


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]


def drop_for(project, data):
    want = slugify(project)
    for d in data:
        if slugify(d["name"]) == want:
            return d
    return None


def preflight(d, headed=False):
    from playwright.sync_api import sync_playwright
    from triage import triage

    url = d.get("official") or ""
    slug = slugify(d["name"])
    folder = OUT_DIR / slug
    folder.mkdir(parents=True, exist_ok=True)
    result = {"project": d["name"], "slug": slug, "official": url, "at":
              datetime.now().strftime("%Y-%m-%d %H:%M"), "steps_from_source":
              len(d.get("steps") or [])}

    if not url.startswith("http"):
        result.update(status="no-url", note="no official site extracted from the guide")
        return result

    try:
        rep = triage(url)
        result["domain_verdict"] = rep["verdict"]
        result["domain_score"] = rep["score"]
        if rep["verdict"] in ("DEAD-LINK", "SCAM-LIKELY"):
            result.update(status="refused",
                          note=f"domain check says {rep['verdict']} - not opening it")
            return result
    except Exception as e:
        result["domain_verdict"] = f"check failed: {type(e).__name__}"

    profile = ROOT / "agent" / "sessions" / "main"
    profile.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=str(profile), headless=not headed,
            user_agent=UA, viewport={"width": 1280, "height": 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(3500)
        except Exception as e:
            result.update(status="unreachable", note=f"{type(e).__name__}: {str(e)[:120]}")
            ctx.close()
            return result

        body = page.inner_text("body")[:20000]
        (folder / "page.txt").write_text(f"URL: {page.url}\nTITLE: {page.title()}\n\n{body}",
                                         encoding="utf-8")
        try:
            page.screenshot(path=str(folder / "landing.png"), full_page=False)
            result["screenshot"] = f"airships/{slug}/landing.png"
        except Exception:
            pass

        fields = page.evaluate("""() => Array.from(document.querySelectorAll('input,textarea,select'))
            .map(el => ({tag: el.tagName.toLowerCase(), type: el.type||'', name: el.name||'',
                         placeholder: el.placeholder||'', label: (el.labels&&el.labels[0]
                         &&el.labels[0].innerText||'').slice(0,60)}))
            .filter(f => (f.type||'').toLowerCase() !== 'hidden').slice(0, 12)""")
        buttons = page.evaluate("""() => Array.from(document.querySelectorAll('button,a'))
            .map(el => (el.innerText||'').trim()).filter(t => t && t.length < 40).slice(0, 60)""")
        has_eth = page.evaluate("() => !!window.ethereum")

        text = (body + " " + " ".join(buttons)).lower()
        result.update({
            "status": "open",
            "title": page.title()[:120],
            "fields": fields,
            "wallet_prompt": bool(WALLET_WORDS.search(text)) or has_eth,
            "kyc_prompt": bool(KYC_WORDS.search(text)),
            "captcha": bool(CAPTCHA_WORDS.search(text)),
            "login_prompt": bool(LOGIN_WORDS.search(text)),
            "injected_wallet": has_eth,
            "cookies": len(ctx.cookies()),
        })
        ctx.close()

    # what the agent may do next, and what it must not
    agent_can, human_must = [], []
    if result["fields"]:
        agent_can.append(f"pre-fill {len(result['fields'])} form field(s) for human review")
    if result["captcha"]:
        human_must.append("solve a CAPTCHA / bot check")
    if result["wallet_prompt"]:
        human_must.append("connect a wallet and approve the signature")
    if result["kyc_prompt"]:
        human_must.append("complete identity verification (KYC)")
    if not human_must:
        agent_can.append("read requirements and capture evidence - no identity step seen")
    result["agent_can"] = agent_can
    result["human_must"] = human_must
    result["status"] = "blocked" if human_must else "ready"
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default="")
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    data = json.loads(DOCS_DATA.read_text(encoding="utf-8"))
    if args.project:
        d = drop_for(args.project, data)
        if not d:
            print(f"no drop named {args.project}")
            return 2
        targets = [d]
    else:
        rows = [d for d in data if isinstance(d.get("confidence"), int) and d["confidence"] >= 40
                and (d.get("forensics") or {}).get("verdict") != "DEAD-LINK" and d.get("official")]
        rows.sort(key=lambda d: (0 if isinstance(d.get("days"), int) and d["days"] <= 30 else 1,
                                 d.get("days") if isinstance(d.get("days"), int) else 9999,
                                 d.get("friction") or 0, -(d.get("confidence") or 0)))
        targets = rows[:args.top or 5]

    summary = {}
    if SUMMARY.exists():
        try:
            summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
        except Exception:
            summary = {}

    for d in targets:
        try:
            r = preflight(d, args.headed)
        except Exception as e:
            r = {"project": d["name"], "slug": slugify(d["name"]), "status": "error",
                 "note": f"{type(e).__name__}: {str(e)[:120]}"}
        summary[r["slug"]] = r
        SUMMARY.parent.mkdir(exist_ok=True)
        SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
        flag = {"ready": "READY ", "blocked": "BLOCK "}.get(r.get("status"), r.get("status", "?"))
        print(f"  {flag} {r['project'][:24]:26} {r.get('domain_verdict','')[:18]:20} "
              f"agent: {len(r.get('agent_can') or [])} human: {len(r.get('human_must') or [])}")

    SUMMARY.parent.mkdir(exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    ready = sum(1 for v in summary.values() if v.get("status") == "ready")
    blocked = sum(1 for v in summary.values() if v.get("status") == "blocked")
    print(f"\npre-flighted: {len(targets)} | ready for agent-only work: {ready} | "
          f"needs one human touch: {blocked}")
    print("evidence: airships/<slug>/page.txt + landing.png | summary: data/preflight.json")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
