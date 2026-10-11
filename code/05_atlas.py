"""Step 5: build the atlas web page (report/atlas/index.html).

Plain-language note: turns the processed tables into one self-contained web
page with a map and a college lookup. Numbers come only from data/processed/.
The page shows a DRAFT banner until run with --final.

Run:  python code/05_atlas.py   (or --final after verification)
"""
import json
import math
import sys

import build_lib as b

FINAL = "--final" in sys.argv
W, H = 520, 470
PAD = 18


def project(state_rings, pts):
    """Simple equal-scale projection per state: x = lon*cos(mid lat), y = -lat, fit to the box."""
    lats = [p[1] for r in state_rings for p in r]
    lons = [p[0] for r in state_rings for p in r]
    k = math.cos(math.radians((min(lats) + max(lats)) / 2))
    xs = [x * k for x in lons]
    minx, maxx, miny, maxy = min(xs), max(xs), min(lats), max(lats)
    s = min((W - 2 * PAD) / (maxx - minx), (H - 2 * PAD) / (maxy - miny))
    ox = (W - s * (maxx - minx)) / 2
    oy = (H - s * (maxy - miny)) / 2
    f = lambda lon, lat: (round(ox + (lon * k - minx) * s, 1), round(oy + (maxy - lat) * s, 1))
    path = " ".join("M" + "L".join(f"{x},{y}" for x, y in (f(*p) for p in r)) + "Z" for r in state_rings)
    return path, [f(lon, lat) for lon, lat in pts]


def main():
    cols = b.read_csv(b.OUT / "atlas_v1_colleges.csv")
    long = b.read_csv(b.OUT / "atlas_v1_long.csv")
    stats = json.load(open(b.ROOT / "report" / "stats.json"))
    geo = json.load(open(b.RAW / "geo" / "gma_outlines_ca_tx.json"))
    data = {}
    for s, gname in [("CA", "California"), ("TX", "Texas")]:
        cs = [c for c in cols if c["state"] == s]
        path, xy = project(geo[gname], [(float(c["longitude"]), float(c["latitude"])) for c in cs])
        colleges = []
        for c, (x, y) in zip(cs, xy):
            hist = [r for r in long if r["state"] == s and r["unitid"] == c["unitid"]]
            hist.sort(key=lambda r: r["cohort"])
            colleges.append({
                "id": c["unitid"], "name": c["ipeds_name"], "src": c["state_source_name"], "lvl": c["match_level"],
                "city": c["city"], "x": x, "y": y, "loc": c["locale_group"], "sector": c["sector_label"],
                "enr": int(c["ug_enroll_fall2023"]) if c["ug_enroll_fall2023"] else None,
                "pt": float(c["pct_parttime_fall2023"]) if c["pct_parttime_fall2023"] else None,
                "pell": float(c["pct_pell_2021_22"]) if c["pct_pell_2021_22"] else None,
                "rate": float(c["pooled_rate"]) if c["pooled_rate"] else None, "pn": int(c["pooled_n"]),
                "pc": c["pooled_cohorts"], "small": c["small_cohort"] == "1",
                "hist": [{"c": r["cohort"], "n": int(r["cohort_n"]),
                          "k": int(r["completed_n"]) if r["completed_n"] else None,
                          "pn": r["prepared_n"], "pk": r["prepared_completed_n"],
                          "un": r["underprepared_n"], "uk": r["underprepared_completed_n"]} for r in hist],
            })
        rates = sorted(c["rate"] for c in colleges if c["rate"] is not None and not c["small"])
        q = [rates[int(len(rates) * i / 5)] for i in range(1, 5)] if len(rates) >= 5 else []
        data[s] = {"path": path, "colleges": colleges, "breaks": q, "stats": stats.get(s, {})}
    page = TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":"))) \
                   .replace("__DRAFT__", "" if FINAL else DRAFT_BANNER)
    out = b.ROOT / "report" / "atlas"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print("wrote", out / "index.html", f"{len(page)/1024:.0f} KB")


DRAFT_BANNER = """<div class="draft" role="note"><strong>Draft for checking.</strong> These numbers have not yet been verified by the author. Do not cite until version 1.0 is released.</div>"""

TEMPLATE = r"""<title>Gateway Math Atlas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: masthead, state switch, then map (graph-paper panel) beside a college lookup; detail and methods below. */
:root{
  --paper:#f6f7f4; --panel:#ffffff; --ink:#18222d; --ink-2:#4b5560; --ink-3:#6c7681; --rule:#d9ddd6; --grid:#e8ebe5;
  --accent:#1c5cab; --accent-soft:#e3edf9; --land:#eef0eb; --warn-bg:#fff4d6; --warn-ink:#6b4a00;
  --q1:#cde2fb; --q2:#86b6ef; --q3:#3987e5; --q4:#1c5cab; --q5:#0d366b; --dot-ring:#ffffff;
  --f-display:"Archivo Narrow","Arial Narrow",Arial,sans-serif; --f-body:"Source Sans 3","Segoe UI",system-ui,sans-serif; --f-data:"IBM Plex Mono",ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#12171d; --panel:#1a2129; --ink:#e9ecef; --ink-2:#b9c0c7; --ink-3:#8d96a0; --rule:#2c353f; --grid:#222a33;
  --accent:#7fb2f0; --accent-soft:#1e2c3d; --land:#1f272f; --warn-bg:#3a2f12; --warn-ink:#f3d58a;
  --q1:#184f95; --q2:#256abf; --q3:#3987e5; --q4:#6da7ec; --q5:#b7d3f6; --dot-ring:#1a2129; color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#12171d; --panel:#1a2129; --ink:#e9ecef; --ink-2:#b9c0c7; --ink-3:#8d96a0; --rule:#2c353f; --grid:#222a33;
  --accent:#7fb2f0; --accent-soft:#1e2c3d; --land:#1f272f; --warn-bg:#3a2f12; --warn-ink:#f3d58a;
  --q1:#184f95; --q2:#256abf; --q3:#3987e5; --q4:#6da7ec; --q5:#b7d3f6; --dot-ring:#1a2129; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding-inline:clamp(16px,3vw,32px);padding-block:24px 48px;display:grid;gap:20px}
header{display:grid;gap:6px}
.eyebrow{font-family:var(--f-data);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
h1{font-family:var(--f-display);font-weight:700;font-size:clamp(28px,4.4vw,44px);line-height:1.05;margin:0;text-wrap:balance;letter-spacing:-.01em}
.lede{max-width:68ch;color:var(--ink-2);margin:0}
.draft{background:var(--warn-bg);color:var(--warn-ink);padding:10px 14px;border-radius:6px;font-size:15px}
.switch{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:8px;overflow:hidden;background:var(--panel)}
.seg button{font:600 15px var(--f-body);color:var(--ink-2);background:none;border:0;padding:8px 18px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.seg button:focus-visible,.row:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.measure{font-size:15px;color:var(--ink-2);max-width:70ch;min-width:0}
.measure code{font-family:var(--f-data);font-size:13px;background:var(--accent-soft);color:var(--ink);padding:1px 6px;border-radius:4px}
.main{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:20px}
@media (max-width:860px){.main{grid-template-columns:1fr}}
.mapbox{background:var(--panel);border:1px solid var(--rule);border-radius:8px;padding:12px;display:grid;gap:10px;min-width:0}
.mapbox svg{width:100%;height:auto;display:block;background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:20px 20px;border-radius:4px}
.land{fill:var(--land);stroke:var(--ink-3);stroke-width:1}
.dot{stroke:var(--dot-ring);stroke-width:1.5;cursor:pointer}
.dot.small{fill:none!important;stroke:var(--ink-3);stroke-dasharray:2 2}
.dot.sel{stroke:var(--ink);stroke-width:2.5}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;color:var(--ink-2);align-items:center}
.legend span{display:inline-flex;align-items:center;gap:6px;font-family:var(--f-data);font-size:12px}
.sw{width:12px;height:12px;border-radius:50%;display:inline-block}
.tip{position:absolute;pointer-events:none;background:var(--ink);color:var(--paper);font-size:13px;padding:6px 9px;border-radius:5px;max-width:240px}
.list{background:var(--panel);border:1px solid var(--rule);border-radius:8px;display:grid;grid-template-rows:auto 1fr;min-width:0;max-height:620px}
.tools{display:flex;flex-wrap:wrap;gap:8px;padding:12px;border-bottom:1px solid var(--rule)}
.tools input{flex:1 1 180px;min-width:0;font:15px var(--f-body);padding:8px 10px;border:1px solid var(--rule);border-radius:6px;background:var(--paper);color:var(--ink)}
.tools select{font:15px var(--f-body);padding:8px;border:1px solid var(--rule);border-radius:6px;background:var(--paper);color:var(--ink)}
.rows{overflow-y:auto}
.row{display:grid;grid-template-columns:minmax(0,1fr) 120px 52px;gap:10px;align-items:center;padding:9px 12px;border-bottom:1px solid var(--grid);cursor:pointer;font-size:15px}
.row:hover{background:var(--accent-soft)}
.row.sel{background:var(--accent-soft);box-shadow:inset 3px 0 0 var(--accent)}
.row .nm{min-width:0}.row .nm b{font-weight:600;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.row .nm small{color:var(--ink-3);font-size:13px}
.bar{height:8px;background:var(--grid);border-radius:4px;overflow:hidden}.bar i{display:block;height:100%;background:var(--q3);border-radius:4px}
.pct{font-family:var(--f-data);font-size:13px;text-align:right;font-variant-numeric:tabular-nums}
.detail{background:var(--panel);border:1px solid var(--rule);border-radius:8px;padding:16px 18px;display:grid;gap:12px}
.detail h2{font-family:var(--f-display);font-size:26px;margin:0;line-height:1.1}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px 18px;margin:0}
.facts div{display:grid;gap:2px}.facts dt{font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-3)}
.facts dd{margin:0;font-family:var(--f-data);font-size:15px;font-variant-numeric:tabular-nums}
.tbl{overflow-x:auto}
table{border-collapse:collapse;font-size:14px;width:100%;font-variant-numeric:tabular-nums}
th,td{text-align:right;padding:6px 10px;border-bottom:1px solid var(--grid);white-space:nowrap}
th:first-child,td:first-child{text-align:left}th{font-weight:600;color:var(--ink-2);font-size:13px}
td{font-family:var(--f-data);font-size:13px}
.note{font-size:14px;color:var(--ink-3);max-width:75ch;margin:0}
.methods{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;border-top:1px solid var(--rule);padding-top:18px}
.methods h3{font-family:var(--f-display);font-size:19px;margin:0 0 6px}
.methods p,.methods li{font-size:15px;color:var(--ink-2);max-width:65ch}
.methods ul{padding-left:18px;margin:0}
a{color:var(--accent)}
@media (prefers-reduced-motion:no-preference){.dot{transition:r .15s}}
</style>
<div class="wrap">
<header>
  <div class="eyebrow">Version 1.0 · California and Texas · public two-year colleges</div>
  <h1>US Gateway Mathematics Outcomes Atlas</h1>
  <p class="lede">How many new students at each community college pass their first college-level math course, from state reporting, matched to federal facts about the college.</p>
</header>
__DRAFT__
<div class="switch">
  <div class="seg" role="group" aria-label="State">
    <button type="button" id="b-CA" aria-pressed="true">California</button>
    <button type="button" id="b-TX" aria-pressed="false">Texas</button>
  </div>
  <p class="measure" id="measure"></p>
</div>
<div class="main">
  <section class="mapbox" aria-label="Map">
    <div style="position:relative"><svg id="map" viewBox="0 0 520 470" role="img" aria-label="Map of colleges"></svg><div class="tip" id="tip" hidden></div></div>
    <div class="legend" id="legend"></div>
    <p class="note" id="mapnote"></p>
  </section>
  <section class="list" aria-label="College lookup">
    <div class="tools">
      <label class="eyebrow" for="q" style="flex-basis:100%">Find a college</label>
      <input id="q" type="search" placeholder="Name or city" autocomplete="off">
      <select id="sort" aria-label="Sort"><option value="name">A to Z</option><option value="rate">Highest rate</option><option value="low">Lowest rate</option><option value="n">Largest cohort</option></select>
    </div>
    <div class="rows" id="rows"></div>
  </section>
</div>
<section class="detail" id="detail" aria-live="polite"></section>
<section class="methods">
  <div><h3>What the numbers mean</h3>
    <p><b>California</b> uses Chancellor's Office metric 502C: of the students in a fall cohort, the share who completed transfer-level math in their first academic year, anywhere in the college's district.</p>
    <p><b>Texas</b> uses Coordinating Board measure C18UC: of first-time degree-seeking students, the share who passed a college-level math course with an A, B or C within two years. Texas reports students who arrived college-ready and not ready separately; the atlas adds them together and shows both parts.</p>
    <p>Because the windows and cohorts differ, compare colleges within a state only. Map colors are fifths of each state's own colleges.</p></div>
  <div><h3>Sources</h3><ul>
    <li>California Community Colleges Chancellor's Office, <a href="https://datavista.cccco.edu/" target="_blank" rel="noopener">Data Vista</a>, General Admit Cohort, school years 2019-20 to 2023-24, downloaded 10 October 2026.</li>
    <li>Texas Higher Education Coordinating Board, <a href="https://www.txhigheredaccountability.org/AcctPublic/" target="_blank" rel="noopener">Accountability System</a>, measure C18UC, cohorts 2020 to 2022, downloaded 10 October 2026.</li>
    <li>IPEDS directory (2023), fall enrollment (2023) and student financial aid (2021-22), via <a href="https://educationdata.urban.org/documentation/" target="_blank" rel="noopener">Education Data Portal</a> v0.27.0, Urban Institute, under the ODC Attribution License.</li>
    <li>State outlines: us-atlas 3.0.1, from US Census Bureau boundaries.</li></ul></div>
  <div><h3>Read before using</h3><ul>
    <li>Rates describe who enrolls as much as what a college does. They are not quality rankings.</li>
    <li>Dallas, Lone Star, San Jacinto and Tarrant report as whole districts.</li>
    <li>Dashed circles mark colleges with fewer than 30 students across the pooled cohorts.</li>
    <li>Full list in the project's LIMITATIONS file. Maintained by Faith Oluwafunmitan Esan (ORCID <span style="font-family:var(--f-data)">0009-0001-3694-157X</span>).</li></ul></div>
</section>
</div>
<script>
const D=__DATA__;
const MEAS={CA:'Share of each fall cohort who passed <b>transfer-level math in their first year</b>. California metric <code>502C</code>, pooled over the last three cohorts.',
            TX:'Share of first-time students who passed <b>a college-level math course within two years</b>. Texas measure <code>C18UC</code>, pooled over cohorts 2020 to 2022.'};
const pct=v=>v==null?'n/a':(v*100).toFixed(1)+'%';
const fmt=v=>v==null?'n/a':v.toLocaleString('en-US');
let st='CA', sel=null;
try{const s=localStorage.getItem('gma-state'); if(s==='CA'||s==='TX') st=s;}catch(e){}
const qcls=(s,r)=>{const b=D[s].breaks; let i=0; while(i<b.length&&r>=b[i]) i++; return 'var(--q'+(i+1)+')';};
function draw(){
  const d=D[st], svg=document.getElementById('map');
  const maxn=Math.max(...d.colleges.map(c=>c.pn));
  let h='<path class="land" d="'+d.path+'"/>';
  const cs=[...d.colleges].sort((a,b)=>b.pn-a.pn);
  for(const c of cs){ const r=(3+9*Math.sqrt(c.pn/maxn)).toFixed(1);
    h+='<circle class="dot'+(c.small?' small':'')+(sel===c.id?' sel':'')+'" data-id="'+c.id+'" cx="'+c.x+'" cy="'+c.y+'" r="'+r+'" fill="'+(c.rate==null?'var(--ink-3)':qcls(st,c.rate))+'"><title>'+c.name+'</title></circle>'; }
  svg.innerHTML=h;
  const b=d.breaks, lab=['under '+pct(b[0])]; for(let i=0;i<b.length-1;i++) lab.push(pct(b[i])+' to '+pct(b[i+1])); lab.push(pct(b[b.length-1])+' and over');
  document.getElementById('legend').innerHTML='<b style="font-size:13px">Passed (pooled rate)</b>'+lab.map((l,i)=>'<span><i class="sw" style="background:var(--q'+(i+1)+')"></i>'+l+'</span>').join('')+'<span><i class="sw" style="border:1.5px dashed var(--ink-3)"></i>fewer than 30 students</span>';
  document.getElementById('mapnote').textContent='Each circle is one college or district, sized by students in the pooled cohorts. '+d.colleges.length+' shown.';
  document.getElementById('measure').innerHTML=MEAS[st];
  ['CA','TX'].forEach(s=>document.getElementById('b-'+s).setAttribute('aria-pressed',s===st));
  list();
}
function list(){
  const q=document.getElementById('q').value.trim().toLowerCase(), so=document.getElementById('sort').value;
  let cs=D[st].colleges.filter(c=>!q||(c.name+' '+c.city+' '+c.src).toLowerCase().includes(q));
  const k={name:(a,b)=>a.name.localeCompare(b.name),rate:(a,b)=>(b.rate??-1)-(a.rate??-1),low:(a,b)=>(a.rate??9)-(b.rate??9),n:(a,b)=>b.pn-a.pn}[so];
  cs.sort(k);
  document.getElementById('rows').innerHTML=cs.length?cs.map(c=>'<div class="row'+(sel===c.id?' sel':'')+'" tabindex="0" role="button" data-id="'+c.id+'"><div class="nm"><b>'+c.name+'</b><small>'+c.city+(c.lvl==='district'?' · whole district':'')+(c.small?' · small cohort':'')+'</small></div><div class="bar" aria-hidden="true"><i style="width:'+((c.rate||0)*100).toFixed(1)+'%"></i></div><div class="pct">'+pct(c.rate)+'</div></div>').join(''):'<p class="note" style="padding:12px">No college matches that search in this state.</p>';
}
function show(id){
  sel=id; const c=D[st].colleges.find(x=>x.id===id); if(!c) return;
  const tx=st==='TX';
  let t='<div class="tbl"><table><thead><tr><th>Cohort</th><th>Students</th><th>Passed</th><th>Rate</th>'+(tx?'<th>Ready: passed</th><th>Not ready: passed</th>':'')+'</tr></thead><tbody>';
  for(const h of c.hist){ t+='<tr><td>'+(st==='CA'?h.c+'-'+String(+h.c+1).slice(2):h.c)+'</td><td>'+fmt(h.n)+'</td><td>'+fmt(h.k)+'</td><td>'+(h.k==null?'n/a':pct(h.k/h.n))+'</td>'+(tx?'<td>'+(h.pn?fmt(+h.pk)+' of '+fmt(+h.pn):'n/a')+'</td><td>'+(h.un?fmt(+h.uk)+' of '+fmt(+h.un):'n/a')+'</td>':'')+'</tr>'; }
  t+='</tbody></table></div>';
  document.getElementById('detail').innerHTML='<div class="eyebrow">'+(st==='CA'?'California':'Texas')+' · IPEDS UNITID '+c.id+(c.lvl==='district'?' · reported as one district':'')+'</div><h2>'+c.name+'</h2>'+
   '<dl class="facts"><div><dt>Pooled rate '+c.pc+'</dt><dd>'+pct(c.rate)+'</dd></div><div><dt>Students pooled</dt><dd>'+fmt(c.pn)+'</dd></div><div><dt>Undergraduates, fall 2023</dt><dd>'+fmt(c.enr)+'</dd></div><div><dt>Part-time</dt><dd>'+pct(c.pt)+'</dd></div><div><dt>Pell recipients, 2021-22</dt><dd>'+pct(c.pell)+'</dd></div><div><dt>Setting</dt><dd>'+(c.loc||'n/a')+'</dd></div></dl>'+t+
   '<p class="note">State source name: '+c.src+'. Federal facts describe the whole college, not only the students in these cohorts.</p>';
  draw();
}
document.getElementById('detail').innerHTML='<p class="note">Select a college on the map or in the list to see each cohort and its federal facts.</p>';
['CA','TX'].forEach(s=>document.getElementById('b-'+s).addEventListener('click',()=>{st=s;sel=null;try{localStorage.setItem('gma-state',s)}catch(e){};document.getElementById('detail').innerHTML='<p class="note">Select a college on the map or in the list to see each cohort and its federal facts.</p>';draw();}));
document.getElementById('q').addEventListener('input',list);
document.getElementById('sort').addEventListener('change',list);
document.getElementById('rows').addEventListener('click',e=>{const r=e.target.closest('.row'); if(r) show(r.dataset.id);});
document.getElementById('rows').addEventListener('keydown',e=>{const r=e.target.closest('.row'); if(r&&(e.key==='Enter'||e.key===' ')){e.preventDefault();show(r.dataset.id);}});
const svg=document.getElementById('map'), tip=document.getElementById('tip');
svg.addEventListener('click',e=>{const t=e.target.closest('circle'); if(t) show(t.dataset.id);});
svg.addEventListener('mousemove',e=>{const t=e.target.closest('circle'); if(!t){tip.hidden=true;return;} const c=D[st].colleges.find(x=>x.id===t.dataset.id); const box=svg.getBoundingClientRect();
  tip.innerHTML='<b>'+c.name+'</b><br>'+pct(c.rate)+' passed · '+fmt(c.pn)+' students'; tip.hidden=false;
  tip.style.left=Math.min(e.clientX-box.left+12,box.width-200)+'px'; tip.style.top=(e.clientY-box.top+12)+'px';});
svg.addEventListener('mouseleave',()=>tip.hidden=true);
draw();
</script>
"""

if __name__ == "__main__":
    main()
