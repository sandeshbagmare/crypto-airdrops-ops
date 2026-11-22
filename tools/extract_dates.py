"""Extract real deadlines from text already collected, without new crawling.

Scans the verified guide fields (page title, description, steps, risks) for date phrases, keeps only
future dates within a year, and ranks a date higher when it comes from the title. Every candidate
stores the phrase it came from so a wrong date is auditable instead of invisible.

  python tools/extract_dates.py            # write data/dates.json
  python tools/extract_dates.py --show 20  # print the strongest matches
"""
import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERIFIED = ROOT / "data" / "verified.json"
OUT = ROOT / "data" / "dates.json"

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}
MONTHS.update({"january": 1, "february": 2, "march": 3, "april": 4, "june": 6, "july": 7,
               "august": 8, "september": 9, "sept": 9, "october": 10, "november": 11,
               "december": 12})

ISO = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")
DMY = re.compile(r"\b(\d{1,2})\s+([A-Za-z]{3,9})\.?(?:\s*,?\s*(20\d{2}))?\b")
MDY = re.compile(r"\b([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?\b(?:\s*,?\s*(20\d{2}))?")
# Phrases that make a nearby date a deadline rather than background history.
SIGNAL = re.compile(
    r"(snapshot|ends?|closes?|deadline|claim|until|before|by|final|cut-?off|payout|"
    r"distribution|airdrop on|launch)", re.I)
FIELDS = [("page_title", 3), ("what_it_is", 2), ("steps", 1), ("risks", 1), ("deadline_hint", 2)]


def today():
    return date.today()


def candidates(text, year_hint):
    out = []
    for m in ISO.finditer(text):
        try:
            out.append((date(int(m.group(1)), int(m.group(2)), int(m.group(3))), m.group(0)))
        except ValueError:
            pass
    for m in DMY.finditer(text):
        mon = MONTHS.get(m.group(2).lower()[:4]) or MONTHS.get(m.group(2).lower()[:3])
        year = int(m.group(3)) if m.group(3) else year_hint
        if mon:
            try:
                out.append((date(year, mon, int(m.group(1))), m.group(0)))
            except ValueError:
                pass
    for m in MDY.finditer(text):
        mon = MONTHS.get(m.group(1).lower()[:4]) or MONTHS.get(m.group(1).lower()[:3])
        year = int(m.group(3)) if m.group(3) else year_hint
        if mon:
            try:
                out.append((date(year, mon, int(m.group(2))), m.group(0)))
            except ValueError:
                pass
    return out


def extract(rec):
    """Best deadline for one record, or None."""
    best = None
    for field, weight in FIELDS:
        value = rec.get(field)
        if isinstance(value, list):
            texts = [str(v) for v in value]
        elif value:
            texts = [str(value)]
        else:
            continue
        for text in texts:
            # a thrown date without a deadline word is weak evidence
            has_signal = bool(SIGNAL.search(text))
            for d, phrase in candidates(text, today().year):
                days = (d - today()).days
                if days < 0 or days > 400:
                    continue
                score = weight + (2 if has_signal else 0)
                if best is None or score > best["score"] or (
                        score == best["score"] and d < date.fromisoformat(best["date"])):
                    best = {"date": d.isoformat(), "days": days, "phrase": phrase.strip()[:40],
                            "field": field, "score": score,
                            "context": text[max(0, text.find(phrase) - 60):
                                            text.find(phrase) + 60].strip()[:160]}
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=0)
    args = ap.parse_args()

    raw = json.loads(VERIFIED.read_text(encoding="utf-8"))
    out, hits = {}, []
    for url, rec in raw.items():
        if not rec.get("ok"):
            continue
        found = extract(rec)
        if found:
            out[url] = dict(found, name=rec.get("name", ""))
            hits.append(out[url])

    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    hits.sort(key=lambda h: (-h["score"], h["days"]))
    soon = [h for h in hits if h["days"] <= 30]
    print(f"dates found: {len(hits)} of {len(raw)} verified pages")
    print(f"within 30 days: {len(soon)} | within 90: {sum(1 for h in hits if h['days'] <= 90)}")
    for h in hits[:args.show]:
        print(f"  {h['name'][:24]:26} {h['date']} ({h['days']:>4}d) "
              f"[{h['field']}/{h['score']}] {h['phrase']!r} :: {h['context'][:70]}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
