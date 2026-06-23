#!/usr/bin/env python3
"""VENERDI 12/06 — Sebastiano a Bolzano alle 15:00 (Il Vascello). Leverage presenza fisica:
appuntamenti SAME-DAY 13:00 o 17:00 a Bolzano. 153 submit, target 60 connesse.
Slot: 10:00 / 11:30 / 14:30 / 16:30 (no 17:30 — venerdi sera ristoranti pieni di servizio)."""
import sys, json, time, urllib.request
from datetime import datetime, date
sys.path.insert(0,'/Users/simocors/Desktop/telesales')
from culligan_batch_caller import submit_batch, build_recipient, is_valid_phone
KEY="sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
LOG="/tmp/culligan_12jun.log"
TARGET=date(2026,6,12)
PREFIX="12jun"
def log(m):
    ts=datetime.now().strftime("%m-%d %H:%M:%S"); print(f"[{ts}] {m}",flush=True); open(LOG,"a").write(f"[{ts}] {m}\n")
def api(p):
    for att in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io/v1"+p,headers={"xi-api-key":KEY}),timeout=60))
        except Exception as e:
            log(f"  api retry {att+1}: {e}"); time.sleep(10)
    raise RuntimeError("api: 3 tentativi falliti")
def submit_retry(name,recs):
    for att in range(3):
        try:
            return submit_batch(name,recs)
        except Exception as e:
            log(f"  submit retry {att+1}/3: {e}"); time.sleep(20)
            try:
                names={b.get('name',''):b.get('id') for b in api("/convai/batch-calling/workspace?limit=30").get('batch_calls',[])}
                if name in names:
                    log(f"  submit era passato server-side: {names[name]}"); return {"id":names[name]}
            except Exception: pass
    raise RuntimeError(f"submit {name}: 3 tentativi falliti")
def cat_of(n):
    nl=n.lower()
    if 'pizzer' in nl: return 'pizzeria'
    if 'pasticc' in nl or 'konditorei' in nl or 'panific' in nl: return 'pasticceria'
    if 'gelat' in nl: return 'gelateria'
    if 'bar' in nl or 'caf' in nl or 'bistro' in nl or 'pub' in nl: return 'bar'
    if 'trattor' in nl or 'osteria' in nl or 'ristoran' in nl or 'restaurant' in nl: return 'ristorante'
    if 'garni' in nl or 'b&b' in nl or 'pension' in nl or 'gasthof' in nl or 'gasthaus' in nl: return 'b&b'
    return 'hotel'
def build(ts):
    out=[]
    for t in ts:
        k=t.get('kind','')
        cat=k if k else cat_of(t['nome'])
        r=build_recipient(phone=t['tel'],nome_azienda=t['nome'],categoria=cat,
                          nome_titolare=t.get('titolare') or 'titolare',indirizzo=t.get('ind',''),note='')
        r['conversation_initiation_client_data']['dynamic_variables']['citta']=t.get('citta','Bolzano')
        if is_valid_phone(r['phone_number']): out.append(r)
    return out
def wait_done(bid,maxs=1500):
    t0=time.time()
    while time.time()-t0<maxs:
        d=api(f"/convai/batch-calling/{bid}")
        if d.get('status') in ('completed','failed','cancelled'): return d
        time.sleep(20)
    return api(f"/convai/batch-calling/{bid}")
def already_fired(name):
    try:
        names=[b.get('name','') for b in api("/convai/batch-calling/workspace?limit=40").get('batch_calls',[])]
        return name in names
    except Exception: return False
def run_slot(name,ts,rounds=3):
    bname=f"{PREFIX}-{name}"
    if already_fired(bname):
        log(f"{name}: gia' lanciata, skip"); return
    recs=build(ts)
    if not recs: log(f"{name}: 0 numeri validi, skip"); return
    log(f"=== {bname}: {len(recs)} submit ===")
    res=submit_retry(bname,recs); bid=res.get('id','?'); log(f"  batch {bid}")
    by={r['phone_number']:r for r in recs}
    for rnd in range(1,rounds+1):
        d=wait_done(bid); rr=d.get('recipients',[])
        failed=[r['phone_number'] for r in rr if r.get('status')=='failed']
        ok=sum(1 for r in rr if r.get('status') in ('completed','voicemail'))
        log(f"  round {rnd}: connesse={ok} fail={len(failed)}")
        if not failed or rnd==rounds: log(f"  {name} FINE: ~{ok} connesse"); break
        time.sleep(60)
        rt=[by[p] for p in failed if p in by]
        res=submit_retry(f"{bname}-r{rnd}",rt); bid=res.get('id','?'); log(f"  retry {rnd}: {len(rt)} -> {bid}")
plan=json.load(open('/Users/simocors/Desktop/telesales/fri_run/plan_12jun.json'))
SCHED=[('10:00','slot_1000'),('11:30','slot_1130'),('14:30','slot_1430'),('16:30','slot_1630')]
log(f"=== SCHEDULER VENERDI 12/06 armato (target {TARGET}) ===")
for hhmm,key in SCHED:
    h,m=map(int,hhmm.split(':'))
    tgt=datetime.combine(TARGET,datetime.min.time()).replace(hour=h,minute=m)
    if datetime.now()>tgt and (datetime.now()-tgt).total_seconds()>3600:
        log(f"{hhmm}: passata da >1h, skip"); continue
    while datetime.now()<tgt:
        s=(tgt-datetime.now()).total_seconds()
        log(f"Attendo {int(s//3600)}h{int((s%3600)//60)}m per {hhmm} ({key})"); time.sleep(min(s,1800))
    if plan.get(key): run_slot(hhmm.replace(':',''),plan[key])
log("=== VENERDI COMPLETO ===")
