#!/usr/bin/env python3
"""Recall daemon 04/06 — richiama LIVE oggi i 'da richiamare' con orario in giornata."""
import sys, json, time, re, urllib.request
from datetime import datetime, date, timedelta
sys.path.insert(0,'/Users/simocors/Desktop/telesales')
from culligan_batch_caller import submit_batch, build_recipient, get_sheets_service, SHEET_ID, normalize_phone
KEY="sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
LOG="/tmp/culligan_recall_10.log"; STATE="/tmp/recall_state_10.json"
def log(m):
    ts=datetime.now().strftime("%H:%M:%S"); print(f"[{ts}] {m}",flush=True); open(LOG,"a").write(f"[{ts}] {m}\n")
def api(p): return json.load(urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io/v1"+p, headers={"xi-api-key":KEY})))

def load_state():
    try: return json.load(open(STATE))
    except: return {"processed":[], "recalled":{}, "queue":{}}
def save_state(s): json.dump(s, open(STATE,"w"))

# indice foglio per telefono -> info
def sheet_index():
    svc=get_sheets_service()
    tabs=['aziende_bolzano_VERIFICATE','aziende_laives_VERIFICATE','aziende_caldaro_VERIFICATE','aziende_appiano_VERIFICATE','aziende_egna_VERIFICATE','aziende_salorno_VERIFICATE','aziende_mezzolombardo_VERIFICATE','aziende_mezzocorona_VERIFICATE']
    idx={}
    for tab in tabs:
        rows=svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f'{tab}!A2:E600').execute().get('values',[])
        for r in rows:
            r=r+['']*5; ph=normalize_phone(r[4])
            if ph: idx[ph]={'nome':r[0],'titolare':r[1].strip(),'ind':r[3],'citta':tab.split('_')[1].capitalize()}
    return idx

NEG=re.compile(r'non (siamo |sono |mi )?interess|gia un (sistema|impianto|depuratore)|fontana (in casa|nostra)|sorgente|non ci serve|gia a posto|abbiamo gia')
def detect_recall_time(text, call_dt):
    t=text.lower()
    if NEG.search(t): return None  # non interessato -> no recall
    # relativi
    if re.search(r"mezz[' ]?or", t): return call_dt+timedelta(minutes=35)
    if re.search(r"(un paio d|due or|2 or)", t): return call_dt+timedelta(hours=2)
    if re.search(r"(tra|fra) un['? ]?or", t): return call_dt+timedelta(hours=1)
    # assoluti oggi
    m=re.search(r"(?:dopo le|verso le|alle|dalle|le)\s*(\d{1,2})(?:[:.,]?(\d{2}))?", t)
    if m:
        h=int(m.group(1)); mi=int(m.group(2)) if m.group(2) else 0
        if 9<=h<=18:
            return datetime.now().replace(hour=h,minute=mi,second=0,microsecond=0)
    if 'pomeriggio' in t: return datetime.now().replace(hour=15,minute=0,second=0,microsecond=0)
    if 'più tardi' in t or 'piu tardi' in t: return call_dt+timedelta(hours=2)
    if 'mattin' in t and datetime.now().hour<12: return datetime.now().replace(hour=11,minute=0,second=0,microsecond=0)
    return None

def todays_batches():
    d=api("/convai/batch-calling/workspace?limit=60")
    bs=d.get("batch_calls",d if isinstance(d,list) else [])
    out=[]
    for b in bs:
        nm=b.get("name","")
        if nm.startswith("15jun-") and not nm.startswith("recall-"):
            out.append(b.get("id"))
    return out

def main():
    st=load_state(); idx=sheet_index()
    log(f"recall daemon avviato. foglio: {len(idx)} numeri")
    end=datetime.now().replace(hour=18,minute=30,second=0,microsecond=0)
    while datetime.now()<end:
        # 1) scopri nuovi 'da richiamare' con orario
        for bid in todays_batches():
            try: d=api(f"/convai/batch-calling/{bid}")
            except: continue
            for r in d.get("recipients",[]):
                cid=r.get("conversation_id")
                if r.get("status")!="completed" or not cid or cid in st["processed"]: continue
                st["processed"].append(cid)
                try: c=api(f"/convai/conversations/{cid}")
                except: continue
                txt=" ".join(t.get("message","") for t in c.get("transcript",[]) if t.get("message"))
                if len(txt)<20: continue
                ph=normalize_phone(r.get("phone_number",""))
                if st["recalled"].get(ph,0)>=2: continue  # max 2 recall
                ct=c.get("metadata",{}).get("start_time_unix_secs")
                call_dt=datetime.fromtimestamp(ct) if ct else datetime.now()
                rt=detect_recall_time(txt, call_dt)
                if rt and rt>datetime.now() and rt<end:
                    st["queue"][ph]=rt.strftime("%Y-%m-%d %H:%M")
                    log(f"  QUEUE recall {ph} ({idx.get(ph,{}).get('nome','?')[:28]}) -> {rt.strftime('%H:%M')}")
        save_state(st)
        # 2) esegui recall maturi
        due=[ph for ph,ts in st["queue"].items() if datetime.strptime(ts,"%Y-%m-%d %H:%M")<=datetime.now()]
        for ph in due:
            info=idx.get(ph)
            del st["queue"][ph]
            if not info: continue
            tit=info['titolare'] or 'titolare'
            rec=build_recipient(phone=ph,nome_azienda=info['nome'],categoria='ristorante',
                                nome_titolare=tit, indirizzo=info['ind'], note='')
            rec['conversation_initiation_client_data']['dynamic_variables']['citta']=info['citta']
            res=submit_batch(f"15jun-recall-{ph[-4:]}", [rec])
            st["recalled"][ph]=st["recalled"].get(ph,0)+1
            log(f"  >>> RECALL LIVE {ph} {info['nome'][:28]} -> {res.get('id','?')}")
            save_state(st)
        time.sleep(180)
    log("recall daemon: fine giornata")

if __name__=="__main__": main()
