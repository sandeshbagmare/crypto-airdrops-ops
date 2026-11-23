"""For the drops that are one human click away, find the exact click.

Opens each actionable page (status ready, or blocked only on an email) and records the control that
actually starts the application: the button/link label, where it goes, and any form on the page with
its fields. Read-only - it never clicks, never types, never submits.

  python tools/entry_points.py --workers 6
  python tools/entry_points.py --project "Globe"

  writes data/entry-points.json
"""
import argparse
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFLIGHT = ROOT / "data" / "preflight.json"
BATCH = ROOT / "data" / "preflight-batch.json"
OUT = ROOT / "data" / "entry-points.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

CTA = re.compile(r"(claim|apply|join|register|sign ?up|waitlist|whitelist|participat|"
                 r"earn|get (?:started|access|points)|verify|mint|submit)", re.I)
NOISE = re.compile(r"^(learn|about|read|explore|docs?|blog|faq|entertainment|news|"
                   r"careers?|contact|privacy|terms)", re.I)
NOISE_ANY = re.compile(r"(learn (?:about|what|how|more)|see how|new to the project|"
                       r"read more|what is)", re.I)
STRONG = re.compile(r"(claim|apply|join|register|sign ?up|waitlist|whitelist|participat|earn|"
                    r"submit|verify|mint|get started|connect)", re.I)


def rank(ctas):
    """Best first: a real application control, not a nav link."""
    scored = []
    for c in ctas:
        label = c["label"]
        if NOISE.match(label) or NOISE_ANY.search(label) or len(label) > 45:
            continue
        score = 3 if STRONG.search(label) else (1 if CTA.search(label) else 0)
        if c["tag"] == "button" or c["href"].startswith("#"):
            score += 1
        if "connect wallet" in label.lower():
            score += 1
        scored.append((score, label, c))
    scored.sort(key=lambda t: -t[0])
    keep = [c for _, _, c in scored][:6]
    best = scored[0] if scored and scored[0][0] > 0 else None
    return keep, (best[1] if best else "")

JS = """() => {
  const clean = s => (s||'').replace(/\\s+/g,' ').trim().slice(0,60);
  const cta = [];
  document.querySelectorAll('button,a,[role=button]').forEach(el => {
    const t = clean(el.innerText);
    if (!t) return;
    cta.push({tag: el.tagName.toLowerCase(), label: t,
              href: el.getAttribute('href') || '',
              disabled: !!el.disabled || el.getAttribute('aria-disabled') === 'true'});
  });
  const forms = Array.from(document.querySelectorAll('form')).slice(0,5).map(f => ({
    action: f.getAttribute('action') || '',
    method: (f.getAttribute('method') || 'get').toLowerCase(),
    fields: Array.from(f.querySelectorAll('input,select,textarea'))
      .filter(i => (i.type||'').toLowerCase() !== 'hidden')
      .map(i => ({type: i.type||i.tagName.toLowerCase(), name: i.name||'',
                  placeholder: i.placeholder||'', required: !!i.required}))
  }));
  return {cta, forms, has_wallet: !!window.ethereum,
          title: document.title};
}"""


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().strip())


def load():
    pre = {}
    for src in (PREFLIGHT, BATCH):   # BATCH wins: auto_apply rewrites PREFLIGHT
        try:
            pre.update(json.loads(src.read_text(encoding="utf-8")))
        except Exception:
            pass
    return pre


def targets(pre, only="", blockers=("email",)):
    out = []
    for slug, p in pre.items():
        if only and slugify(only) != slug:
            continue
        ok = p.get("status") == "ready" or p.get("blocked_on") in blockers
        if ok and (p.get("official") or "").startswith("http"):
            out.append((slug, p))
    out.sort(key=lambda s: (s[1].get("days") if isinstance(s[1].get("days"), int) else 9999))
    return out


def run(items):
    from playwright.sync_api import sync_playwright
    found = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA, viewport={"width": 1280, "height": 900})
        for slug, p in items:
            page = ctx.new_page()
            rec = {"project": p.get("project"), "official": p.get("official"),
                   "at": datetime.now().strftime("%Y-%m-%d %H:%M"), "ctas": [], "forms": []}
            try:
                page.goto(p["official"], wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(2500)
                info = page.evaluate(JS)
                ctas = [c for c in info["cta"] if CTA.search(c["label"])]
                seen, uniq = set(), []
                for c in ctas:
                    key = c["label"].lower()
                    if key in seen:
                        continue
                    seen.add(key)
                    uniq.append(c)
                keep, best = rank(uniq)
                rec.update(ctas=keep, forms=info["forms"], has_wallet=info["has_wallet"],
                           page_title=(info["title"] or "")[:100])
                rec["next_click"] = best or ("a form field on the page" if info["forms"]
                                             else "no obvious control - read it")
                print(f"  {slug[:34]:36} {rec['next_click'][:44]:46} forms={len(info['forms'])}")
            except Exception as e:
                rec["next_click"] = f"page failed: {type(e).__name__}"
                print(f"  {slug[:34]:36} FAILED {type(e).__name__}")
            found[slug] = rec
            page.close()
        browser.close()
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--project", default="")
    ap.add_argument("--blockers", default="email",
                    help="comma list: email,wallet_signature,login,kyc,terms")
    args = ap.parse_args()

    pre = load()
    items = targets(pre, args.project, tuple(b.strip() for b in args.blockers.split(",") if b.strip()))
    if not items:
        print("nothing actionable found")
        return 1
    print(f"probing {len(items)} actionable pages")
    chunks = [items[i::args.workers] for i in range(args.workers)]
    merged = {}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for part in ex.map(run, chunks):
            merged.update(part)

    prev = {}
    try:
        prev = json.loads(OUT.read_text(encoding="utf-8"))
    except Exception:
        pass
    prev.update(merged)
    OUT.write_text(json.dumps(prev, indent=1, ensure_ascii=False), encoding="utf-8")
    with_click = sum(1 for v in merged.values() if v.get("next_click")
                     and not v["next_click"].startswith("page failed"))
    print(f"\n{len(merged)} pages probed, {with_click} have an identifiable control")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print("next: python tools/redeem_kit.py")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
