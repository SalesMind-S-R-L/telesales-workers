# Push generico giorno -> Sebastiano. Uso: python3 push_seb_day.py DD/MM realphones.json [--send]
import sys, json, re; sys.path.insert(0,'.')
from culligan_batch_caller import get_sheets_service, normalize_phone
svc=get_sheets_service()
SRC="1PiezlYSd5TZNBCRTvzBhx_yVCGfN6aMI3PXdOYU4xu8"
DST="1KsbFkAhJQDd2edYuKgbVC0yd87jK-Y6egKU254Y1wT0"; DST_TAB="Foglio1"
tabs=['aziende_bolzano_VERIFICATE','aziende_laives_VERIFICATE','aziende_caldaro_VERIFICATE','aziende_appiano_VERIFICATE','aziende_egna_VERIFICATE','aziende_salorno_VERIFICATE','aziende_mezzolombardo_VERIFICATE','aziende_mezzocorona_VERIFICATE']
DAY=sys.argv[1]; REAL=set(json.load(open(sys.argv[2])))
DIRTY=re.compile(r'(calligan|operatore|il chiamante|un contatto|contatto ha|è stato rilevato|è stato fornito|intelligenza artificial|presentandosi|ha presentato|ha contattato|ha offerto|ha avuto difficolt|non ha risposto dopo|messaggio di segreteria|conversazione è iniziata|saluto iniziale|verifica della connession)', re.I)
NOANS=re.compile(r'(segreteria|non ha risposto|nessuna risposta|messaggio|non risposto|non è disponibile)', re.I)
def digits(s): return re.sub(r'\D','',s or '')
def yy(dd):
    m=re.match(r'(\d{2}/\d{2})/(\d{4})',dd or ''); return f"{m.group(1)}/{m.group(2)[-2:]}" if m else ''
def cap(s,n=120):
    s=s.strip()
    if len(s)<=n: return s
    c=s[:n]; return (c[:c.rfind(' ')] if ' ' in c else c).rstrip(' ,.;')
def tit_clean(b):
    b=(b or '').strip()
    if not b or b.lower() in ('titolare','famiglia','-'): return ''
    return b
def seb_note(esito,nota):
    e=(esito or '').strip(); n=(nota or '').strip()
    if e=='Appuntamento': return cap(n.lower()) if n else 'appuntamento fissato'
    if e=='Non risposto' or n=='Non risposto.': return 'non risposto'
    if e=='Non interessato':
        return cap('non interessato - '+n.lower()) if (n and not n.lower().startswith('non interess')) else 'non interessato'
    if DIRTY.search(n) or len(n)>150:
        return 'non risposto' if NOANS.search(n) else 'da richiamare'
    return cap(n.lower())
def present(esito,nota):
    nn=seb_note(esito,nota)
    return 'no' if (nn=='non risposto' or nn.startswith('non interessato')) else 'sì'
def appt_HK(appt_raw, nota):
    # H = giorno/ora, K = conferma
    if not appt_raw: return '',''
    return yy(appt_raw) if re.match(r'\d',appt_raw) else appt_raw, 'confermato col titolare'
slotc=[(6,8,9,7),(12,13,14,7),(17,18,19,7)]  # data,esito,nota,H(appt=col7)
out=[]
for tab in tabs:
    vals=svc.spreadsheets().values().get(spreadsheetId=SRC, range=f'{tab}!A2:W600').execute().get('values',[])
    for r in vals:
        r=r+['']*23; nome=r[0].strip()
        if not nome: continue
        for di,ei,ni,hi in slotc:
            dval=r[di] or ''; esito=(r[ei] or '').strip()
            if 'outreach' in dval.lower() or not esito: continue
            if DAY in dval and normalize_phone(r[4]) in REAL:
                H,K = appt_HK(r[hi].strip() if esito=='Appuntamento' else '', r[ni])
                # A,B,C,D,E,F,G,H,I,J,K
                out.append([nome, tit_clean(r[1]), '', r[3].strip(), digits(r[4]),
                            present(esito,r[ni]), '', H, yy(dval), seb_note(esito,r[ni]), K])
seen={}
for row in out:
    k=row[4] or row[0]
    if k not in seen or (row[5]=='sì' and seen[k][5]!='sì'): seen[k]=row
out=list(seen.values())
ev=svc.spreadsheets().values().get(spreadsheetId=DST, range=f"'{DST_TAB}'!A1:K3000").execute().get('values',[])
existing=set()
for r in ev:
    r=r+['']*11; t=re.sub(r'\D','',r[4] or ''); dd=(r[8] or '').strip()
    if t and dd: existing.add((t,dd))
out=[x for x in out if (x[4],x[8]) not in existing]
START=len(ev)+1; END=START+len(out)-1
p=sum(1 for x in out if x[5]=='sì')
print(f"{DAY} -> {len(out)} righe (sì={p}, no={len(out)-p}). Append {START}-{END}")
for x in out:
    extra=f" | B={x[1]}" if x[1] else ""
    extra+=f" | APP H={x[7]} K={x[10]}" if x[10] else ""
    print(f"  {x[0][:26]:<26} F={x[5]:<3} I={x[8]} | {x[9][:50]}{extra}")
if '--send' in sys.argv and out:
    svc.spreadsheets().values().update(spreadsheetId=DST, range=f"'{DST_TAB}'!A{START}:K{END}", valueInputOption='USER_ENTERED', body={'values':out}).execute()
    print(f"INVIATO {len(out)} righe")
