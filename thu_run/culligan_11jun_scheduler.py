#!/usr/bin/env python3
"""GIOVEDI 11/06 — cluster Bolzano core, 125 submit, target 50 connesse.
Safeguard: E.164, idempotenza per fascia, SUBMIT CON RETRY (fix timeout 10/06 che ha perso la 17:30)."""
import sys, json, time, urllib.request
from datetime import datetime, date
sys.path.insert(0,'/Users/simocors/Desktop/telesales')
from culligan_batch_caller import submit_batch, build_recipient, is_valid_phone
KEY="sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
LOG="/tmp/culligan_11jun.log"
TARGET=date(2026,6,11)
PREFIX="11jun"
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
    """FIX 10/06: il submit della 17:30 e' morto su ReadTimeout. 3 tentativi con pausa,
    e prima di ogni retry verifica se il batch e' in realta' gia' stato creato server-side."""
    for att in range(3):
        try:
            return submit_batch(name,recs)
        except Exception as e:
            log(f"  submit retry {att+1}/3: {e}")
            time.sleep(20)
            try:
                names={b.get('name',''):b.get('id') for b in api("/convai/batch-calling/workspace?limit=30").get('batch_calls',[])}
                if name in names:
                    log(f"  submit era passato server-side: {names[name]}")
                    return {"id":names[name]}
            except Exception:
                pass
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
        cat=k if k and k!='fam' else cat_of(t['nome'])
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
    except Exception:
        return False
def run_slot(name,ts,rounds=3):
    bname=f"{PREFIX}-{name}"
    if already_fired(bname):
        log(f"{name}: gia' lanciata (anti-doppione), skip"); return
    recs=build(ts)
    if not recs: log(f"{name}: 0 numeri validi, skip"); return
    log(f"=== {bname}: {len(recs)} submit (E.164 ok) ===")
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
plan=json.load(open('/Users/simocors/Desktop/telesales/thu_run/plan_11jun.json'))
SCHED=[('10:00','slot_1000'),('11:30','slot_1130'),('15:00','slot_1500'),('17:30','slot_1730')]
log(f"=== SCHEDULER GIOVEDI 11/06 armato (target {TARGET}) ===")
now=datetime.now()
for hhmm,key in SCHED:
    h,m=map(int,hhmm.split(':'))
    tgt=datetime.combine(TARGET,datetime.min.time()).replace(hour=h,minute=m)
    if now>tgt and (now-tgt).total_seconds()>3600:
        log(f"{hhmm} ({key}): fascia passata da >1h, skip (solo fasce future)"); continue
    while datetime.now()<tgt:
        s=(tgt-datetime.now()).total_seconds()
        log(f"Attendo {int(s//3600)}h{int((s%3600)//60)}m per {hhmm} ({key})"); time.sleep(min(s,1800))
    if plan.get(key): run_slot(hhmm.replace(':',''),plan[key])
log("=== GIOVEDI COMPLETO ===")
