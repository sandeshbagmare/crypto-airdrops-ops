"""Probe airdrops.io listing cards for a per-project end date.

Prints, for the first few cards, the card text so the layout can be confirmed before any scraping
logic is committed. Read-only.
"""
import re
import sys

from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
DATE_RE = re.compile(r"\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", re.I)


def main(url="https://airdrops.io/latest/"):
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        pg = b.new_page(user_agent=UA)
        pg.goto(url, wait_until="domcontentloaded", timeout=90000)
        pg.wait_for_timeout(3000)
        cards = pg.evaluate("""() => {
            const out = [];
            document.querySelectorAll('li[data-search], article, .card, div[data-status]').forEach(el => {
                const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
                if (t.length > 20 && t.length < 400) out.push(t);
            });
            return out.slice(0, 8);
        }""")
        print(f"cards found: {len(cards)}")
        dated = 0
        for c in cards:
            m = DATE_RE.search(c)
            if m:
                dated += 1
            print(("- DATED " if m else "  ------ ") + c[:150])
        print(f"\nof first {len(cards)} cards, {dated} contain a date phrase")
        b.close()
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main(*(sys.argv[1:] or [])))
