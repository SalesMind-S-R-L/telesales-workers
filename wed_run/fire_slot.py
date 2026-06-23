#!/usr/bin/env python3
"""Lancia UNA fascia del piano: submit + retry SIP 1x. Robusto allo sleep, idempotente."""
import sys, json, time, urllib.request
from datetime import datetime
sys.path.insert(0,'/Users/simocors/Desktop/telesales')
from culligan_batch_caller import submit_batch, build_recipient, is_valid_phone
KEY="sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
PLAN=sys.argv[1]; SLOT=sys.argv[2]; PREFIX=sys.argv[3]
LOG="/Users/simocors/Desktop/telesales/wed_run/fire.log"
def log(m):
    open(LOG,"a").write(f"[{datetime.now():%m-%d %H:%M:%S}] {m}\n"); print(m,flush=True)
def api(p): return json.load(urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io/v1"+p,headers={"xi-api-key":KEY})))
def cat_of(n):
    nl=n.lower()
    if 'pizzer' in nl: return 'pizzeria'
    if 'gelat' in nl: return 'gelateria'
    if 'pasticc' in nl: return 'pasticceria'
    if 'bar' in nl or 'caff' in nl: return 'bar'
    if 'trattor' in nl or 'osteria' in nl or 'ristoran' in nl: return 'ristorante'
    if 'garni' in nl or 'b&b' in nl or 'gasthof' in nl or 'pension' in nl: return 'b&b'
    return 'ristorante'
def build(ts):
    out=[]
    for t in ts:
        r=build_recipient(phone=t['tel'],nome_azienda=t['nome'],categoria=cat_of(t['nome']),nome_titolare=t.get('titolare') or 'titolare',indirizzo=t.get('ind',''),note='')
        r['conversation_initiation_client_data']['dynamic_variables']['citta']=t['citta']
        if is_valid_phone(r['phone_number']): out.append(r)
    return out
def wait_done(bid,maxs=1500):
    t0=time.time()
    while time.time()-t0<maxs:
        d=api(f"/convai/batch-calling/{bid}")
        if d.get('status') in ('completed','failed','cancelled'): return d
        time.sleep(20)
    return api(f"/convai/batch-calling/{bid}")
# IDEMPOTENZA: salta se la fascia è già stata lanciata (scheduler "PREFIX-1130" o task "PREFIX-slot_1130")
alt=f"{PREFIX}-"+SLOT.replace("slot_","")
try:
    names=[b.get('name','') for b in api("/convai/batch-calling/workspace?limit=40").get('batch_calls',[])]
    if f"{PREFIX}-{SLOT}" in names or alt in names:
        log(f"{SLOT}: già lanciata oggi, skip (anti-doppione)"); sys.exit(0)
except Exception:
    pass
ts=json.load(open(PLAN)).get(SLOT,[])
recs=build(ts)
if not recs:
    log(f"{SLOT}: 0 numeri validi, skip"); sys.exit(0)
log(f"=== {PREFIX}-{SLOT}: {len(recs)} submit ===")
res=submit_batch(f"{PREFIX}-{SLOT}", recs); bid=res.get('id','?'); log(f"  batch {bid}")
by={r['phone_number']:r for r in recs}
for rnd in (1,2):
    d=wait_done(bid); rr=d.get('recipients',[])
    failed=[r['phone_number'] for r in rr if r.get('status')=='failed']
    ok=sum(1 for r in rr if r.get('status') in ('completed','voicemail'))
    log(f"  round {rnd}: connesse={ok} fail={len(failed)}")
    if not failed or rnd==2: break
    time.sleep(60)
    res=submit_batch(f"{PREFIX}-{SLOT}-r{rnd}", [by[p] for p in failed if p in by]); bid=res.get('id','?')
log(f"  {SLOT} FATTO")
