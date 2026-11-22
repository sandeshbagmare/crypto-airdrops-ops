"""Scrape public airdrop trackers into data/airdrops.json. Read-only, one GET per source.

Every record keeps its source URL so the finished ledger is auditable back to origin.
Sources: airdroplet (dossiers), airdropvillage (badges), 99airdrops (cards).
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
N99_URL = "https://99airdrops.com/"


def txt(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace(chr(0xC2), "").replace(chr(0xE2) + chr(0x80) + chr(0x99), "'")
    return re.sub(r"\s+", " ", s).strip()


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=50) as r:
        return r.read().decode("utf-8", "replace")


def blank(name, slug, source, url):
    return {
        "name": name, "slug": slug, "source": source, "source_url": url,
        "description": "", "notes": "", "tags": "", "score": "", "status": "",
        "next_move": "", "recorded": "", "checked": "", "cost": "",
        "time_to_start": "", "fees": "", "end_date": "", "prize": "",
        "risk": "", "kyc": "",
    }


def parse_airdroplet(html):
    out = []
    for a in re.split(r'(?=<article class="airdrop-card card-summary)', html)[1:]:
        h3 = re.search(r"<h3[^>]*>(.*?)</h3>", a, re.S)
        href = re.search(r'href="([^"]+)"', a)
        if not h3 or not href:
            continue
        slug = href.group(1).strip("/").split("/")[-1]
        rec = blank(txt(h3.group(1)).replace("\u2197", "").strip(), slug,
                    "airdroplet", "https://airdroplet.com" + href.group(1))
        desc = re.search(r"<h3[^>]*>.*?</h3>\s*<p>(.*?)</p>", a, re.S)
        rec["description"] = txt(desc.group(1)) if desc else ""
        sc = re.search(r"score-(\w+)", a)
        rec["score"] = sc.group(1) if sc else ""

        for d in re.findall(r'(<div class="card-datum[^"]*">.*?)(?=<div class="(?:card-datum|row-actions)|</article>)',
                            a, re.S):
            span = re.search(r"<span>(.*?)</span>", d, re.S)
            strong = re.search(r"<strong>(.*?)</strong>", d, re.S)
            smalls = [txt(s) for s in re.findall(r"<small>(.*?)</small>", d, re.S)]
            if not span or not strong:
                continue
            label, val = txt(span.group(1)), txt(strong.group(1))
            low = label.lower()
            if "next move" in low:
                rec["status"] = label.split("\u00b7")[0].strip()
                rec["next_move"] = val
                for s in smalls:
                    if s.lower().startswith("recorded"):
                        rec["recorded"] = s.split(":", 1)[-1].strip()
                    if s.lower().startswith("checked"):
                        rec["checked"] = s
            elif "cost" in low:
                rec["cost"] = val
                if smalls:
                    rec["time_to_start"] = smalls[0]
                for s in smalls:
                    if s.lower().startswith("fees"):
                        rec["fees"] = s
            elif "catch" in low:
                for s in smalls:
                    if "risk" in s.lower():
                        rec["risk"] = s.split("\u00b7")[0].strip()
                    if "kyc" in s.lower():
                        rec["kyc"] = s
        out.append(rec)
    return out


def parse_airdropvillage(html):
    out = []
    marks = list(re.finditer(r'<h3[^>]*data-slot="tooltip-trigger"[^>]*>(.*?)</h3>', html, re.S))
    for i, m in enumerate(marks):
        name = txt(m.group(1)).strip()
        if not name:
            continue
        window = html[m.end(): marks[i + 1].start() if i + 1 < len(marks) else m.end() + 4000]
        ends = re.search(r"Ends\s*([0-9]{1,2}\s+[A-Za-z]{3}\s+[0-9]{4})", window)
        money = re.search(r"\$([0-9][0-9,]{1,12})", window)
        rec = blank(name, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
                    "airdropvillage", AV_URL)
        rec["end_date"] = ends.group(1) if ends else ""
        rec["prize"] = money.group(1) if money else ""
        if "No Fixed Deadline" in window:
            rec["status"] = "No fixed deadline"
        out.append(rec)
    return out


def parse_99airdrops(html):
    """99airdrops: one card-top .. card-foot block per project."""
    out = []
    for b in re.split(r'(?=<div class="card-top">)', html)[1:]:
        link = re.search(r'<h3>\s*<a href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        if not link:
            continue
        slug = link.group(1).strip("/").split("/")[-1]
        rec = blank(txt(link.group(2)).strip(), slug, "99airdrops",
                    "https://99airdrops.com" + link.group(1))
        label = re.search(r'<p class="label">(.*?)</p>', b, re.S)
        desc = re.search(r'<p class="desc">(.*?)</p>', b, re.S)
        tags = re.findall(r"<li[^>]*>(.*?)</li>", b, re.S)
        pot = re.search(r'<span class="pot[^"]*">(.*?)</span>', b, re.S)
        rec["description"] = txt(label.group(1)) if label else ""
        rec["notes"] = txt(desc.group(1)) if desc else ""
        rec["tags"] = ", ".join(txt(t) for t in tags if txt(t))[:120]
        rec["status"] = txt(pot.group(1)) if pot else ""
        if "tag-updated" in b:
            rec["status"] = (rec["status"] + " | recently updated").strip(" |")
        out.append(rec)
    return out


def dedupe(records):
    seen, out = {}, []
    for r in records:
        key = re.sub(r"[^a-z0-9]", "", r["name"].lower())
        if not key:
            continue
        if key in seen:
            prev = seen[key]
            for k, v in r.items():
                if not prev.get(k) and v:
                    prev[k] = v
            prev["source"] = prev["source"] + "+" + r["source"] \
                if r["source"] not in prev["source"] else prev["source"]
            continue
        seen[key] = r
        out.append(r)
    return out


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    records = []
    for name, url, fn in (
        ("airdroplet", AD_URL, parse_airdroplet),
        ("airdropvillage", AV_URL, parse_airdropvillage),
        ("99airdrops", N99_URL, parse_99airdrops),
    ):
        try:
            got = fn(get(url))
            print(f"{name}: {len(got)} records")
            records += got
        except Exception as e:
            print(f"{name} FAILED: {type(e).__name__}: {e}")
    before = len(records)
    records = dedupe(records)
    for r in records:
        r["fetched"] = today
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(records, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{before} raw -> {len(records)} unique -> {DATA}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
