"""Deep-verify each airdrop from its own guide page.

For every record with a detail URL it extracts: what the project is, the step-by-step
requirements, who is behind it, costs, risks and any deadline, then scores confidence
from the evidence actually found. Results are cached so runs are incremental.

Usage:
    python tools/verify.py            # verify what is not yet verified
    python tools/verify.py --limit 20 # cap this run
    python tools/verify.py --refresh  # ignore the cache
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "airdrops.json"
OUT = ROOT / "data" / "verified.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
CACHE_DAYS = 7
WORKERS = 5


def text(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace(chr(0xC2), "").replace(chr(0xE2) + chr(0x80) + chr(0x99), "'")
    return re.sub(r"\s+", " ", s).strip()


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,application/xhtml+xml"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def sections(html):
    out = {}
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>(.*?)(?=<h2|$)", html, re.S):
        out[text(m.group(1)).lower()] = m.group(2)
    return out


def pick(secs, *keys, startswith=None):
    for k, v in secs.items():
        if startswith and k.startswith(startswith):
            return text(v)
        if any(key in k for key in keys):
            return text(v)
    return ""


def ldjson_desc(html):
    for m in re.finditer(r"application/ld\+json[^>]*>(.*?)</script>", html, re.S):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        for node in data.get("@graph", [data]):
            if node.get("@type") in ("Article", "NewsArticle", "BlogPosting"):
                return text(node.get("description", "")) or text(node.get("headline", ""))
    return ""


def first_external(text_blob, skip):
    for url in re.findall(r"\b((?:https?://)?[a-z0-9][a-z0-9.-]{2,40}\.[a-z]{2,10}(?:/[^\s,)]*)?)", text_blob):
        low = url.lower()
        if any(s in low for s in skip):
            continue
        if low.startswith(("http", "www")) or "." in low:
            return url if "://" in url else "https://" + url.lstrip("/")
    return ""


def verify_one(rec):
    url = rec.get("source_url") or ""
    result = {"url": url, "name": rec.get("name", ""), "checked": datetime.now().strftime("%Y-%m-%d"),
              "ok": False, "error": ""}
    try:
        html = fetch(url)
    except urllib.error.HTTPError as e:
        result["error"] = f"HTTP {e.code}"
        return result
    except Exception as e:
        result["error"] = type(e).__name__
        return result

    secs = sections(html)
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    steps_html = ""
    for k, v in secs.items():
        if "step" in k or "how to" in k or "claim" in k:
            steps_html = v
            break
    steps = [text(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", steps_html, re.S)]
    steps = [s for s in steps if 15 <= len(s) <= 320][:12]

    skip = ("99airdrops.com", "airdropstop.com", "twitter.com", "x.com", "discord.gg",
            "discord.com", "t.me", "telegram", "google.com", "w3.org", "youtube.com",
            "facebook.com", "instagram.com", "reddit.com", "linkedin.com", "tiktok.com")
    official = ""
    for href in re.findall(r'href="(https?://[^"]+)"', steps_html or html, re.I):
        low = href.lower()
        if any(s in low for s in skip):
            continue
        if any(bad in low for bad in (".css", ".js", ".png", ".jpg", ".svg", ".webp", "cdn.", "wp-content")):
            continue
        official = href.split("?")[0].rstrip("/")
        break

    meta = re.search(r'<meta name="description" content="([^"]{20,400})"', html)
    result.update({
        "ok": True,
        "page_title": text(title.group(1))[:140] if title else "",
        "what_it_is": (ldjson_desc(html) or pick(secs, startswith="what ") or
                       (text(meta.group(1)) if meta else ""))[:600],
        "steps": steps,
        "who_is_behind": pick(secs, "behind")[:400],
        "costs": pick(secs, "cost", "fee")[:400],
        "risks": pick(secs, "risk", "eligib")[:400],
        "official_url": official or first_external(
            pick(secs, "step") or " ".join(steps), skip),
        "section_count": len(secs),
    })
    for s in steps:
        d = re.search(r"(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", s)
        if d:
            result["deadline_hint"] = d.group(0)
            break
    return result


def confidence(rec, v, source_count):
    """0-100, built only from evidence that was actually found."""
    score, why = 0, []
    if v.get("steps"):
        score += 25
        why.append(f"{len(v['steps'])} concrete steps")
    if v.get("official_url"):
        score += 20
        why.append("official site linked")
    if v.get("deadline_hint") or rec.get("end_date"):
        score += 15
        why.append("deadline stated")
    if v.get("who_is_behind"):
        score += 15
        why.append("operator/team named")
    if v.get("costs"):
        score += 10
        why.append("costs disclosed")
    if source_count > 1:
        score += 10
        why.append(f"{source_count} sources agree it exists")
    if v.get("risks"):
        score += 5
        why.append("risks disclosed")
    if not v.get("steps"):
        score -= 15
        why.append("no steps found (-15)")
    if v.get("error"):
        return 0, [f"unreachable: {v['error']}"]
    return max(0, min(100, score)), why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    records = json.loads(DATA.read_text(encoding="utf-8"))
    cache = {}
    if OUT.exists() and not args.refresh:
        try:
            cache = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    sources = {}
    for r in records:
        k = re.sub(r"[^a-z0-9]", "", r["name"].lower())
        sources[k] = sources.get(k, 0) + 1

    cutoff = (datetime.now() - timedelta(days=CACHE_DAYS)).strftime("%Y-%m-%d")
    todo = [r for r in records
            if (r.get("source_url") or "").startswith("http")
            and (args.refresh or r["source_url"] not in cache
                 or cache[r["source_url"]].get("checked", "") < cutoff)]
    if args.limit:
        todo = todo[:args.limit]
    print(f"to verify: {len(todo)} (cached: {len(cache)})")

    def work(rec):
        v = verify_one(rec)
        k = re.sub(r"[^a-z0-9]", "", rec["name"].lower())
        v["confidence"], v["evidence"] = confidence(rec, v, sources.get(k, 1))
        v["sources"] = sources.get(k, 1)
        return v

    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for v in pool.map(work, todo):
            cache[v["url"]] = v
            done += 1
            if done % 25 == 0:
                print(f"  {done}/{len(todo)}")
                OUT.write_text(json.dumps(cache, indent=1, ensure_ascii=False), encoding="utf-8")

    OUT.write_text(json.dumps(cache, indent=1, ensure_ascii=False), encoding="utf-8")
    ok = sum(1 for v in cache.values() if v.get("ok"))
    confs = [v.get("confidence", 0) for v in cache.values() if v.get("ok")]
    print(f"verified {ok}/{len(cache)} reachable; avg confidence "
          f"{sum(confs)/len(confs):.0f}" if confs else "nothing verified")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
