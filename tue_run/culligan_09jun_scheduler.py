#!/usr/bin/env python3
"""LUNEDI 08/06 — Merano verified-only, 30-35 connesse. Tutte le safeguard (no bug 05/06)."""
import sys, json, time, urllib.request
from datetime import datetime, date
sys.path.insert(0,'/Users/simocors/Desktop/telesales')
from culligan_batch_caller import submit_batch, build_recipient, is_valid_phone
KEY="sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
LOG="/tmp/culligan_09jun.log"
TARGET=date(2026,6,9)  # lunedì
def log(m):
    ts=datetime.now().strftime("%m-%d %H:%M:%S"); print(f"[{ts}] {m}",flush=True); open(LOG,"a").write(f"[{ts}] {m}\n")
def api(p): return json.load(urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io/v1"+p,headers={"xi-api-key":KEY})))
def cat_of(n):
    nl=n.lower()
    if 'pizzer' in nl: return 'pizzeria'
    if 'pasticc' in nl: return 'pasticceria'
    if 'gelat' in nl: return 'gelateria'
    if 'bar' in nl or 'caff' in nl: return 'bar'
    if 'trattor' in nl or 'osteria' in nl or 'ristoran' in nl: return 'ristorante'
    if 'garni' in nl or 'b&b' in nl or 'pension' in nl or 'gasthof' in nl or 'gasthaus' in nl: return 'b&b'
    return 'hotel'
def build(ts):
    out=[]
    for t in ts:
        r=build_recipient(phone=t['tel'],nome_azienda=t['nome'],categoria=t.get('cat') or cat_of(t['nome']),
                          nome_titolare='titolare',indirizzo=t.get('ind',''),note='')
        r['conversation_initiation_client_data']['dynamic_variables']['citta']=t['citta']; out.append(r)
    return out
def wait_done(bid,maxs=1500):
    t0=time.time()
    while time.time()-t0<maxs:
        d=api(f"/convai/batch-calling/{bid}")
        if d.get('status') in ('completed','failed','cancelled'): return d
        time.sleep(20)
    return api(f"/convai/batch-calling/{bid}")
def run_slot(name,ts,rounds=2):
    # PRE-FLIGHT: scarta numeri non E.164 validi (build_recipient normalizza, qui ricontrollo)
    recs=[r for r in build(ts) if is_valid_phone(r['phone_number'])]
    if not recs: log(f"{name}: 0 numeri validi, skip"); return
    log(f"=== {name}: {len(recs)} submit (validati E.164) ===")
    res=submit_batch(f"09jun-{name}",recs); bid=res.get('id','?'); log(f"  batch {bid}")
    by={r['phone_number']:r for r in recs}
    for rnd in range(1,rounds+1):
        d=wait_done(bid); rr=d.get('recipients',[])
        failed=[r['phone_number'] for r in rr if r.get('status')=='failed']
        ok=sum(1 for r in rr if r.get('status') in ('completed','voicemail'))
        log(f"  round {rnd}: connesse={ok} fail={len(failed)}")
        if not failed or rnd==rounds: log(f"  {name} FINE: ~{ok} connesse"); break
        time.sleep(60)
        rt=[by[p] for p in failed if p in by]
        res=submit_batch(f"09jun-{name}-r{rnd}",rt); bid=res.get('id','?'); log(f"  retry {rnd}: {len(rt)} -> {bid}")
plan=json.load(open('/Users/simocors/Desktop/telesales/tue_run/plan_09jun.json'))
SCHED=[('10:00','slot_1000'),('11:30','slot_1130'),('15:00','slot_1500'),('17:30','slot_1730')]
log(f"=== SCHEDULER MARTEDI 09/06 armato (target {TARGET}) ===")
for hhmm,key in SCHED:
    h,m=map(int,hhmm.split(':'))
    tgt=datetime.combine(TARGET,datetime.min.time()).replace(hour=h,minute=m)
    while datetime.now()<tgt:
        s=(tgt-datetime.now()).total_seconds()
        log(f"Attendo {int(s//3600)}h{int((s%3600)//60)}m per {hhmm} ({key})"); time.sleep(min(s,1800))
    if plan.get(key): run_slot(hhmm.replace(':',''),plan[key])
log("=== MARTEDI COMPLETO ===")
