"""Phishing triage for airdrop links. Read-only: DNS, RDAP, TLS cert.

Usage: python tools/triage.py <url-or-domain> [...]
Exit 0 = all clear enough to consider, 1 = at least one high risk.
"""
import json
import re
import socket
import ssl
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

BRANDS = ["uniswap", "binance", "metamask", "coinbase", "ethereum", "solana",
          "arbitrum", "optimism", "polygon", "aave", "curve", "layerzero", "monad"]
OUT = Path(__file__).resolve().parent.parent / "notes" / "triage-log.jsonl"
UA = "airdrops-ops-triage/1.0"


def norm(target):
    if "://" not in target:
        target = "https://" + target
    return urlparse(target)


def rdap(domain):
    """Registration data. Distinguishes 'not registered' (404) from 'could not ask' (429/5xx)."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f"https://rdap.org/domain/{domain}",
                headers={"Accept": "application/rdap+json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode())
            ev = {e.get("eventAction"): (e.get("eventDate") or "")[:10]
                  for e in d.get("events", [])}
            return {"registered": ev.get("registration"), "expires": ev.get("expiration"),
                    "nameservers": len(d.get("nameservers", [])), "exists": True}
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"exists": False, "error": "HTTP 404 (not registered)"}
            if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
            return {"exists": None, "error": f"HTTP {e.code} (unknown)"}
        except Exception as e:
            if attempt < 2:
                time.sleep(1.0)
                continue
            return {"exists": None, "error": type(e).__name__}
    return {"exists": None, "error": "gave up"}


def dns(host):
    try:
        return {"ips": sorted({ai[4][0] for ai in socket.getaddrinfo(host, 443)}),
                "resolves": True}
    except socket.gaierror:
        return {"ips": [], "resolves": False}


def cert(host):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=15) as s:
            with ctx.wrap_socket(s, server_hostname=host) as ss:
                c = ss.getpeercert()
        issuer = dict(x[0] for x in c.get("issuer", ()))
        return {"issuer": issuer.get("organizationName", "?"),
                "not_before": c.get("notBefore"), "not_after": c.get("notAfter")}
    except Exception as e:
        return {"error": type(e).__name__}


def homoglyph(host):
    """Decode any punycode label and see if it impersonates a known brand."""
    for label in host.split("."):
        if not label.startswith("xn--"):
            continue
        try:
            decoded = label[4:].encode().decode("punycode")
        except Exception:
            continue
        for b in BRANDS:
            if b in decoded.lower() and decoded.lower() != b:
                return f"punycode label {label} decodes to '{decoded}' (impersonates {b})"
        return f"punycode label {label} decodes to '{decoded}'"
    for b in BRANDS:
        if b in host.replace("-", "") and not re.match(rf"^(www\.)?{b}\.", host):
            return f"brand '{b}' embedded in non-canonical host"
    return None


def age_days(iso):
    if not iso:
        return None
    try:
        d = datetime.strptime(iso[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - d).days
    except ValueError:
        return None


def classify(rep):
    """Refine the raw verdict. A dead link is not a scam, and saying so matters.

    - DEAD-LINK: domain is unregistered or does not resolve. The tracker has a stale row.
    - SCAM-LIKELY: homoglyph, punycode, http-only, recent registration *and* a live host.
    """
    rdap_info = rep.get("rdap") or {}
    dns_info = rep.get("dns") or {}
    if rdap_info.get("exists") is False or dns_info.get("resolves") is False:
        return "DEAD-LINK"
    if rdap_info.get("exists") is None and not dns_info.get("resolves"):
        return "UNCHECKED"
    score = rep.get("score") or 0
    if score >= 60:
        return "SCAM-LIKELY"
    if score >= 25:
        return "SUSPICIOUS"
    return "no red flags found"


def triage(target):
    u = norm(target)
    host = (u.hostname or "").lower()
    domain = ".".join(host.split(".")[-2:]) if host else ""
    findings, score = [], 0

    h = homoglyph(host)
    if h:
        findings.append(("HIGH", h))
        score += 40

    if u.scheme != "https":
        findings.append(("HIGH", f"scheme is {u.scheme}, not https"))
        score += 30

    d = rdap(domain)
    if d.get("exists") is False:
        findings.append(("HIGH", f"{domain} is not registered in RDAP"))
        score += 35
    age = age_days(d.get("registered"))
    if age is not None:
        if age < 90:
            findings.append(("HIGH", f"domain only {age} days old (registered {d['registered']})"))
            score += 35
        elif age < 365:
            findings.append(("MEDIUM", f"domain {age} days old"))
            score += 15
        else:
            findings.append(("OK", f"domain registered {d['registered']} ({age} days)"))

    n = dns(host) if host else {"resolves": False}
    if not n.get("resolves"):
        findings.append(("HIGH", "host does not resolve"))
        score += 25

    c = cert(host) if n.get("resolves") else {"error": "no dns"}
    if c.get("error"):
        findings.append(("MEDIUM", f"TLS: {c['error']}"))
        score += 10
    else:
        findings.append(("OK", f"TLS issued by {c['issuer']}"))

    verdict = "SCAM-LIKELY" if score >= 60 else "SUSPICIOUS" if score >= 25 else "no red flags found"
    report = {"target": target, "host": host, "score": score, "verdict": verdict,
              "findings": findings, "rdap": d, "dns": n, "cert": c,
              "checked": datetime.now().isoformat(timespec="seconds")}
    report["verdict"] = classify(report)
    return report


def main(args):
    if not args:
        print(__doc__)
        return 1
    bad = 0
    for t in args:
        r = triage(t)
        print(f"\n=== {t}")
        print(f"    verdict: {r['verdict']}  (risk score {r['score']})")
        for level, msg in r["findings"]:
            print(f"    [{level:6}] {msg}")
        if r["verdict"] == "SCAM-LIKELY":
            bad += 1
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main(sys.argv[1:]))
