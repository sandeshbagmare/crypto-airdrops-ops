"""Generate docs/index.html: a static, dependency-free browser for docs/data.json."""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Crypto airdrop ledger - verified</title>
<style>
  :root { --bg:#0f1216; --panel:#171b21; --line:#262c35; --ink:#e8edf4; --mut:#9aa6b5;
          --ok:#3fb950; --warn:#d29922; --bad:#f85149; --accent:#58a6ff; }
  * { box-sizing:border-box }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
  header { padding:28px 20px 18px; border-bottom:1px solid var(--line); }
  h1 { margin:0 0 6px; font-size:22px; letter-spacing:-.02em }
  .sub { color:var(--mut); font-size:13px; max-width:900px }
  .warn { margin-top:10px; padding:10px 12px; border:1px solid #4a3a12; background:#1e1a10;
          color:#e3c07a; border-radius:8px; font-size:13px }
  .wrap { max-width:1180px; margin:0 auto }
  .bar { display:flex; flex-wrap:wrap; gap:10px; padding:16px 20px; align-items:center;
         position:sticky; top:0; background:rgba(15,18,22,.94); backdrop-filter:blur(6px);
         border-bottom:1px solid var(--line); z-index:5 }
  input,select { background:var(--panel); color:var(--ink); border:1px solid var(--line);
                 border-radius:8px; padding:8px 10px; font-size:14px }
  input { flex:1 1 260px }
  .count { color:var(--mut); font-size:13px; margin-left:auto }
  main { padding:18px 20px 60px; display:grid; gap:12px;
         grid-template-columns:repeat(auto-fill,minmax(360px,1fr)) }
  .card { background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:14px 16px }
  .card h2 { margin:0 0 4px; font-size:16px; display:flex; gap:8px; align-items:baseline }
  .badge { font-size:11px; padding:2px 7px; border-radius:999px; border:1px solid var(--line);
           color:var(--mut); white-space:nowrap }
  .c80 { color:#0d1117; background:var(--ok); border-color:var(--ok) }
  .c60 { color:#0d1117; background:#7ee787; border-color:#7ee787 }
  .c40 { background:#1e2a1e; color:#7ee787; border-color:#2c4430 }
  .c20 { background:#2a2213; color:#e3c07a; border-color:#4a3a12 }
  .c0  { background:#2a1618; color:#f0a0a4; border-color:#4a2224 }
  .what { color:var(--ink); font-size:13.5px; margin:6px 0 8px }
  .meta { color:var(--mut); font-size:12.5px; display:flex; flex-wrap:wrap; gap:10px; margin-bottom:6px }
  details { margin-top:8px }
  summary { cursor:pointer; color:var(--accent); font-size:13px }
  ol { margin:8px 0 0 18px; padding:0; color:var(--mut); font-size:13px }
  li { margin-bottom:5px }
  .kv { font-size:12.5px; color:var(--mut); margin-top:8px; border-top:1px dashed var(--line); padding-top:8px }
  .kv b { color:var(--ink); font-weight:600 }
  a { color:var(--accent); text-decoration:none }
  a:hover { text-decoration:underline }
  .ev { font-size:11.5px; color:var(--mut); margin-top:6px }
  footer { color:var(--mut); font-size:12.5px; padding:0 20px 40px }
</style>
</head>
<body>
<header><div class="wrap">
  <h1>Crypto airdrop ledger</h1>
  <div class="sub">__COUNT__ projects, __VERIFIED__ deep-verified from their own guide pages.
    Updated __DATE__. Confidence reflects how well documented a drop is, not how likely it is to pay.</div>
  <div class="warn"><b>Not financial advice.</b> Every entry is aggregated from public trackers and
    project guides, with its source linked. A listing is not an endorsement. Always confirm the
    official domain before connecting a wallet, and never share a seed phrase.
    Domains are checked with RDAP, DNS and TLS; flagged ones are listed in
    <a href="https://github.com/sandeshbagmare/crypto-airdrops-ops/blob/main/notes/watchlist.md">the watchlist</a>.</div>
</div></header>
<div class="bar"><div class="wrap" style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;width:100%">
  <input id="q" placeholder="Search project, chain, what it needs...">
  <select id="conf">
    <option value="0">Any confidence</option>
    <option value="40">40+</option>
    <option value="60">60+</option>
    <option value="80">80+</option>
  </select>
  <select id="tag">
    <option value="">Any type</option>
  </select>
  <select id="sort">
    <option value="conf">Best evidenced</option>
    <option value="cheap">Cheapest first</option>
    <option value="soon">Closing soonest</option>
    <option value="az">A-Z</option>
  </select>
  <span class="count" id="count"></span>
</div></div>
<main id="grid"></main>
<footer>Generated from <a href="data.json">data.json</a>.
  Sources: airdroplet, airdropvillage, 99airdrops, airdropstop, airdrops.io.
  Records whose source became unreachable keep their last-checked date.
</footer>
<script>
let DATA=[];
const cls=c=>c>=80?'c80':c>=60?'c60':c>=40?'c40':c>=20?'c20':'c0';
const esc=s=>String(s??'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));
function card(d){
  const c=typeof d.confidence==='number'?d.confidence:0;
  const steps=(d.steps||[]).length;
  return `<article class="card">
    <h2>${esc(d.name)} <span class="badge ${cls(c)}">confidence ${d.confidence??'?'}</span>
      ${d.status?`<span class="badge">${esc(d.status)}</span>`:''}</h2>
    <div class="what">${esc((d.what||'').slice(0,300))||'<i>no description found</i>'}</div>
    <div class="ev">${(d.tags||[]).map(t=>`<span class="badge">${esc(t)}</span>`).join(' ')}</div>
    <div class="meta">
      ${d.official?`<a href="${esc(d.official)}" target="_blank" rel="noopener nofollow">official site</a>`:''}
      ${d.end?`<span>key date: ${esc(d.end)}</span>`:''}
      ${typeof d.days==='number'?`<span>${d.days} days left</span>`:''}
      ${d.pool?`<span>pool: ${esc(d.pool)}</span>`:''}
      ${steps?`<span>${steps} steps</span>`:''}      ${d.forensics&&d.forensics.verdict&&d.forensics.verdict!=='no red flags found'?`<span class="badge ${d.forensics.verdict==='DEAD-LINK'?'c0':'c20'}" title="checked by tools/triage.py">${esc(d.forensics.verdict.toLowerCase())}</span>`:''}
      ${d.friction_label?`<span class="badge ${d.friction<=5?'c80':d.friction<=15?'c40':'c20'}" title="effort: ${d.friction}/100">${esc(d.friction_label)}</span>`:''}
      ${d.domain_age_days?`<span>domain ${d.domain_age_days}d old</span>`:''}
    </div>
    ${d.needs?`<div class="kv"><b>Needs:</b> ${esc(d.needs)}</div>`:''}
    ${steps?`<details><summary>How to do it</summary><ol>${d.steps.map(s=>`<li>${esc(s)}</li>`).join('')}</ol></details>`:''}
    ${d.behind?`<div class="kv"><b>Behind it:</b> ${esc(d.behind.slice(0,220))}</div>`:''}
    ${d.costs?`<div class="kv"><b>Costs:</b> ${esc(d.costs.slice(0,220))}</div>`:''}
    ${d.risks?`<div class="kv"><b>Risks:</b> ${esc(d.risks.slice(0,220))}</div>`:''}
    <div class="ev">${(d.evidence||[]).map(esc).join(' &middot; ')}
      ${d.checked?` &middot; checked ${esc(d.checked)}`:''}</div>
    ${d.source_url?`<div class="ev"><a href="${esc(d.source_url)}" target="_blank" rel="noopener nofollow">source: ${esc(d.source)}</a></div>`:''}
  </article>`;
}
function render(){
  const q=document.getElementById('q').value.toLowerCase();
  const min=+document.getElementById('conf').value;
  const sort=document.getElementById('sort').value;
  const tag=document.getElementById('tag').value;
  let rows=DATA.filter(d=>{
    if((typeof d.confidence!=='number'?0:d.confidence)<min) return false;
    if(tag && !(d.tags||[]).includes(tag)) return false;
    if(!q) return true;
    return [d.name,d.what,d.needs,d.behind,d.status,(d.tags||[]).join(' ')].join(' ').toLowerCase().includes(q);
  });
  if(sort==='conf') rows.sort((a,b)=>(b.confidence??-1)-(a.confidence??-1));
  if(sort==='cheap') rows.sort((a,b)=>(a.friction??99)-(b.friction??99)||(b.confidence??-1)-(a.confidence??-1));
  if(sort==='soon') rows.sort((a,b)=>(a.days??9999)-(b.days??9999));
  if(sort==='az') rows.sort((a,b)=>a.name.localeCompare(b.name));
  document.getElementById('grid').innerHTML=rows.slice(0,400).map(card).join('');
  document.getElementById('count').textContent=rows.length+' shown';
}
fetch('data.json').then(r=>r.json()).then(d=>{DATA=d;fillTags();render();})
  .catch(e=>{document.getElementById('grid').innerHTML='<p>Could not load data.json</p>';});
function fillTags(){
  const tags=[...new Set(DATA.flatMap(d=>d.tags||[]))].sort();
  const sel=document.getElementById('tag');
  tags.forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t+' ('+DATA.filter(d=>(d.tags||[]).includes(t)).length+')';sel.appendChild(o);});
}
['q','conf','tag'].forEach(id=>document.getElementById(id).addEventListener('input',render));
['sort','tag'].forEach(id=>document.getElementById(id).addEventListener('change',render));
</script>
</body></html>
"""


def main():
    data = json.loads((DOCS / "data.json").read_text(encoding="utf-8"))
    verified = sum(1 for d in data if isinstance(d.get("confidence"), int))
    html = (HTML.replace("__COUNT__", str(len(data)))
                .replace("__VERIFIED__", str(verified))
                .replace("__DATE__", date.today().isoformat()))
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"docs/index.html written ({len(html)} bytes, {len(data)} projects, {verified} verified)")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
    sys.exit(main())
