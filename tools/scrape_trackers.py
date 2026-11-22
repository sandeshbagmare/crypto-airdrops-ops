"""Scrape public airdrop trackers into data/airdrops.json. Read-only, one GET per source.

Every record keeps its source URL so the finished ledger is auditable back to origin.
"""
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "airdrops.json"
UA = "airdrops-ops-research/1.0 (+personal research)"

AD_URL = "https://airdroplet.com/testnet-airdrops"
AV_URL = "https://www.airdropvillage.io/airdrops"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=50) as r:
        return r.read().decode("utf-8", "replace")


def txt(s):
    s = re.sub(r"<[^>]+>", " ", s)
    # drop stray C1/Latin-1 debris from the trackers' double-encoded badges
    s = s.replace(chr(0xC2), "").replace(chr(0xE2) + chr(0x80) + chr(0x99), "'")
    return re.sub(r"\s+", " ", s).strip()


def field(label_html):
    return txt(label_html).replace("\u2197", "").strip()


def parse_airdroplet(html):
    out = []
    for a in re.split(r'(?=<article class="airdrop-card card-summary)', html)[1:]:
        h3 = re.search(r"<h3[^>]*>(.*?)</h3>", a, re.S)
        href = re.search(r'href="([^"]+)"', a)
        if not h3 or not href:
            continue
        score = re.search(r"score-(\w+)", a)
        desc = re.search(r"<h3[^>]*>.*?</h3>\s*<p>(.*?)</p>", a, re.S)

        rec = {
            "name": field(h3.group(1)),
            "slug": href.group(1).strip("/").split("/")[-1],
            "source": "airdroplet",
            "source_url": "https://airdroplet.com" + href.group(1),
            "description": txt(desc.group(1)) if desc else "",
            "score": score.group(1) if score else "",
            "status": "", "next_move": "", "recorded": "", "checked": "",
            "cost": "", "time_to_start": "", "fees": "",
            "risk": "", "kyc": "",
        }

        for d in re.findall(r'(<div class="card-datum[^"]*">.*?)(?=<div class="(?:card-datum|row-actions)|</article>)', a, re.S):
            span = re.search(r"<span>(.*?)</span>", d, re.S)
            strong = re.search(r"<strong>(.*?)</strong>", d, re.S)
            smalls = [txt(s) for s in re.findall(r"<small>(.*?)</small>", d, re.S)]
            if not span or not strong:
                continue
            label = txt(span.group(1))
            val = txt(strong.group(1))
            if "next move" in label.lower():
                rec["status"] = label.split("\u00b7")[0].strip()
                rec["next_move"] = val
                for s in smalls:
                    if s.lower().startswith("recorded"):
                        rec["recorded"] = s.split(":", 1)[-1].strip()
                    if s.lower().startswith("checked"):
                        rec["checked"] = s
            elif "cost" in label.lower():
                rec["cost"] = val
                if smalls:
                    rec["time_to_start"] = smalls[0]
                for s in smalls:
                    if s.lower().startswith("fees"):
                        rec["fees"] = s
            elif "catch" in label.lower():
                for s in smalls:
                    low = s.lower()
                    if "risk" in low:
                        rec["risk"] = s.split("\u00b7")[0].strip()
                    if "kyc" in low:
                        rec["kyc"] = s
        out.append(rec)
    return out


def parse_airdropvillage(html):
    """Village cards carry an h3 name plus an "Ends <date>" badge."""
    out = []
    marks = list(re.finditer(r'<h3[^>]*data-slot="tooltip-trigger"[^>]*>(.*?)</h3>', html, re.S))
    for i, m in enumerate(marks):
        name = txt(m.group(1)).strip()
        if not name:
            continue
        window = html[m.end(): marks[i + 1].start() if i + 1 < len(marks) else m.end() + 4000]
        ends = re.search(r"Ends\s*([0-9]{1,2}\s+[A-Za-z]{3}\s+[0-9]{4})", window)
        nodate = "No Fixed Deadline" in window
        money = re.search(r"\$([0-9][0-9,]{1,12})", window)
        out.append({
            "name": name,
            "slug": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
            "source": "airdropvillage",
            "source_url": AV_URL,
            "description": "",
            "score": "",
            "status": "No fixed deadline" if nodate else "",
            "next_move": "",
            "recorded": "",
            "checked": "",
            "cost": "",
            "time_to_start": "",
            "fees": "",
            "end_date": ends.group(1) if ends else "",
            "prize": money.group(1) if money else "",
            "risk": "",
            "kyc": "",
        })
    return out


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    records = []
    for name, url, fn in (("airdroplet", AD_URL, parse_airdroplet),
                          ("airdropvillage", AV_URL, parse_airdropvillage)):
        try:
            got = fn(get(url))
            print(f"{name}: {len(got)} records")
            records += got
        except Exception as e:
            print(f"{name} FAILED: {type(e).__name__}: {e}")
    for r in records:
        r["fetched"] = today
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(records, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"total {len(records)} -> {DATA}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
