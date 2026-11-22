"""Open an official site in a persistent browser profile so a session survives restarts.

The human performs the login. This tool never sees, stores or types a password: it only keeps the
resulting cookies and localStorage in a per-identity profile directory under agent/sessions/.

  python tools/agent_browser.py --identity main --url https://example.org
  python tools/agent_browser.py --identity main --check        # is there a saved session?
  python tools/agent_browser.py --identity main --url ... --headless --seconds 30

Profiles are gitignored. A profile is equivalent to a login, so treat it like one.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "agent" / "sessions"
STATE = ROOT / "agent" / "sessions.json"


def profile(identity):
    safe = "".join(c for c in identity if c.isalnum() or c in "-_") or "main"
    p = SESSIONS / safe
    p.mkdir(parents=True, exist_ok=True)
    return p


def record(identity, url, cookies):
    data = {}
    if STATE.exists():
        try:
            data = json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    entry = data.setdefault(identity, {"sites": {}})
    entry["profile"] = f"agent/sessions/{identity}"
    entry["updated"] = datetime.now().isoformat(timespec="seconds")
    if url:
        host = url.split("//")[-1].split("/")[0]
        entry["sites"][host] = {"last_url": url, "cookies": cookies,
                                "at": datetime.now().strftime("%Y-%m-%d %H:%M")}
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--identity", default="main")
    ap.add_argument("--url", default="")
    ap.add_argument("--seconds", type=int, default=0, help="0 = wait until the window is closed")
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--set-cookie", default="", help="self-test: write a cookie, then re-run --check")
    ap.add_argument("--stale-after", type=int, default=14,
                    help="warn when the saved session is older than this many days")
    args = ap.parse_args()

    prof = profile(args.identity)

    if args.check:
        found = []
        for f in prof.rglob("Cookies"):
            found.append(str(f.relative_to(ROOT)))
        print(f"profile: {prof.relative_to(ROOT)}")
        print(f"cookie stores: {len(found)}")
        if STATE.exists():
            data = json.loads(STATE.read_text(encoding="utf-8"))
            entry = data.get(args.identity, {})
            print(f"recorded sites: {len(entry.get('sites', {}))}")
            for host, meta in list(entry.get("sites", {}).items())[:10]:
                print(f"  {host}  cookies={meta.get('cookies')}  last={meta.get('at')}")
            stamp = entry.get("updated", "")
            if stamp:
                try:
                    age = (datetime.now() - datetime.fromisoformat(stamp)).days
                    if age > args.stale_after:
                        print(f"WARNING: session last used {age} days ago - sites may have logged you "
                              f"out. Re-run without --check and log in again if a site asks.")
                    else:
                        print(f"session freshness: used {age} day(s) ago (limit {args.stale_after})")
                except ValueError:
                    pass
        else:
            print("no session recorded yet")
            print("start one with: python tools/agent_browser.py --identity main --url <official>")
        return 0

    if not args.url:
        print("need --url (or --check)")
        return 2

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=str(prof), headless=args.headless,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        if args.set_cookie:
            page.goto(args.url, wait_until="domcontentloaded", timeout=45000)
            ctx.add_cookies([{"name": "agent_selftest", "value": args.set_cookie,
                              "url": args.url}])
        else:
            page.goto(args.url, wait_until="domcontentloaded", timeout=45000)
        print(f"open: {page.title()[:80]} -> {page.url}")
        if not args.headless:
            print("Log in here if the site asks. The profile keeps the session after you close it.")
        if args.seconds:
            page.wait_for_timeout(args.seconds * 1000)
        else:
            try:
                page.wait_for_event("close", timeout=0)
            except Exception:
                pass
        cookies = len(ctx.cookies())
        record(args.identity, page.url, cookies)
        print(f"session saved: {cookies} cookies in {prof.relative_to(ROOT)}")
        ctx.close()
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
