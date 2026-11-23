"""Walk the queue in a real window, prefilled, and stop at the submit button.

This is the part an agent may do: open the official page in the persistent profile, type the public
email and public wallet address into the obvious fields, mark the button that finishes the job, save a
screenshot, and hand the mouse back to you. It never submits, never signs, never types a secret, never
touches a password field.

  python tools/guided_apply.py --sheet email --limit 10       # the 58 email drops, in deadline order
  python tools/guided_apply.py --sheet wallet --limit 5 --headed
  python tools/guided_apply.py --project Globe

Controls while the window is open: press Enter in this terminal to save and move to the next drop,
or type `skip`, `done` (submitted), or `quit`.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH = ROOT / "data" / "preflight-batch.json"
PREFLIGHT = ROOT / "data" / "preflight.json"
ENTRY = ROOT / "data" / "entry-points.json"
INPUTS = ROOT / "agent" / "operator-inputs.json"
LOG = ROOT / "data" / "guided-log.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

SHEETS = {"ready": ("ready",), "email": ("email",), "wallet": ("wallet_signature",),
          "login": ("login",), "kyc": ("kyc", "terms")}

FILL = """(args) => {
  const email = args.email, wallet = args.wallet;
  const fill = [];
  const boxes = Array.from(document.querySelectorAll('input,textarea'));
  for (const el of boxes) {
    const t = (el.type || '').toLowerCase();
    if (['hidden', 'password', 'checkbox', 'radio', 'file', 'submit', 'button'].includes(t)) continue;
    if (el.disabled || el.readOnly) continue;
    const hint = ((el.name || '') + ' ' + (el.placeholder || '') + ' ' +
                  (el.id || '') + ' ' +
                  ((el.labels && el.labels[0] && el.labels[0].innerText) || '')).toLowerCase();
    let value = '';
    if (/(e-?mail)/.test(hint) || t === 'email') value = email;
    else if (/(wallet|address|0x|eth)/.test(hint)) value = wallet;
    if (!value) continue;
    el.focus();
    el.value = value;
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.dispatchEvent(new Event('change', {bubbles: true}));
    fill.push({hint: hint.trim().slice(0, 50), value: value.slice(0, 46)});
  }
  // mark, never press: outline every control that looks like the finishing move
  const mark = /(submit|claim|apply|join|register|sign ?up|waitlist|enter|confirm|continue)/i;
  const buttons = [];
  document.querySelectorAll('button,[type=submit],[role=button],a').forEach(b => {
    const label = (b.innerText || b.value || '').trim();
    if (!label || !mark.test(label)) return;
    b.style.outline = '3px solid #22c55e';
    b.style.outlineOffset = '2px';
    buttons.push(label.slice(0, 40));
  });
  const bar = document.createElement('div');
  bar.textContent = 'PREFILLED by airdrops-ops - you press the green button. ' +
    'Nothing was submitted.';
  bar.style.cssText = 'position:fixed;left:0;right:0;top:0;z-index:2147483647;padding:10px 14px;' +
    'background:#111827;color:#fff;font:600 14px system-ui;border-bottom:3px solid #22c55e';
  document.body.appendChild(bar);
  return {filled: fill, marked: buttons};
}"""


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().strip())


def load_queue():
    pre = {}
    for src in (PREFLIGHT, BATCH):
        try:
            pre.update(json.loads(src.read_text(encoding="utf-8")))
        except Exception:
            pass
    try:
        opt = json.loads(INPUTS.read_text(encoding="utf-8"))
    except Exception:
        opt = {}
    try:
        entry = json.loads(ENTRY.read_text(encoding="utf-8"))
    except Exception:
        entry = {}
    return pre, opt, entry


def pick(pre, sheet, project):
    want = SHEETS.get(sheet)
    rows = []
    for slug, p in pre.items():
        if project and slug != slugify(project):
            continue
        if want:
            ok = (p.get("status") in want if sheet == "ready"
                  else (p.get("blocked_on") in want))
            if not ok:
                continue
        if not (p.get("official") or "").startswith("http"):
            continue
        rows.append((slug, p))
    rows.sort(key=lambda s: (s[1].get("days") if isinstance(s[1].get("days"), int) else 9999,
                             -(s[1].get("confidence") or 0)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", default="email", choices=list(SHEETS))
    ap.add_argument("--project", default="")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--identity", default="main")
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--headed", action="store_true", default=True)
    args = ap.parse_args()

    pre, opt, entry = load_queue()
    queue = pick(pre, args.sheet, args.project)[:args.limit]
    if not queue:
        print("nothing in that sheet")
        return 1

    email = opt.get("email") or ""
    wallet = opt.get("wallet") or ""
    if not email:
        print("no email in agent/operator-inputs.json - nothing to prefill")
        return 2
    if args.sheet == "wallet" and not wallet:
        print("no wallet in agent/operator-inputs.json.\n"
              "Run `python tools/burner_wallet.py --i-am-the-operator` yourself first - "
              "the address must be yours.")
        return 2

    from playwright.sync_api import sync_playwright
    profile = ROOT / "agent" / "sessions" / args.identity
    profile.mkdir(parents=True, exist_ok=True)
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else {}

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=str(profile), headless=args.headless, user_agent=UA,
            viewport={"width": 1280, "height": 950})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for i, (slug, p) in enumerate(queue, 1):
            url = p["official"]
            print(f"\n[{i}/{len(queue)}] {p.get('project')}  closes in {p.get('days')}d\n  {url}")
            rec = {"project": p.get("project"), "at": datetime.now().strftime("%Y-%m-%d %H:%M")}
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=35000)
                page.wait_for_timeout(2500)
                res = page.evaluate(FILL, {"email": email, "wallet": wallet})
                rec["filled"] = res.get("filled") or []
                rec["marked"] = res.get("marked") or []
                hint = (entry.get(slug) or {}).get("next_click") or ""
                if hint:
                    print(f"  guide says: {hint}")
                print(f"  prefilled {len(rec['filled'])} field(s), marked "
                      f"{len(rec['marked'])} button(s)")
            except Exception as e:
                rec["error"] = f"{type(e).__name__}: {e}"[:200]
                print(f"  could not open/prefill: {rec['error'][:90]}")
            folder = ROOT / "airships" / slug
            folder.mkdir(parents=True, exist_ok=True)
            try:
                page.screenshot(path=str(folder / "prefilled.png"), full_page=False)
                rec["evidence"] = f"airships/{slug}/prefilled.png"
            except Exception:
                pass

            print("  -> press the green button yourself, then: [Enter] next | "
                  "done | skip | quit")
            try:
                answer = input().strip().lower()
            except EOFError:
                answer = "quit"
            rec["human"] = answer or "next"
            rec["final_url"] = page.url
            log[slug] = rec
            if answer == "quit":
                break
        ctx.close()

    LOG.write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
    done = sum(1 for v in log.values() if v.get("human") == "done")
    print(f"\nlogged {len(log)} drops in {LOG.relative_to(ROOT)} | marked done by you: {done}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
