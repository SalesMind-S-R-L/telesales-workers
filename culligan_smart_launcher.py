#!/usr/bin/env python3
"""Smart launcher batch Culligan — triggered da cron, slot-aware.

Usage:
    python3 culligan_smart_launcher.py morning    # 09:30 → Hotel/Garni/B&B
    python3 culligan_smart_launcher.py afternoon  # 15:00 → Pizzerie/Ristoranti
    python3 culligan_smart_launcher.py late       # 16:30 → Mixed HoReCa

Cron entries (Lun-Ven):
    30 9  * * 1-5 /usr/bin/python3 /tmp/culligan_smart_launcher.py morning
    0  15 * * 1-5 /usr/bin/python3 /tmp/culligan_smart_launcher.py afternoon
    30 16 * * 1-5 /usr/bin/python3 /tmp/culligan_smart_launcher.py late
"""
import sys, json
from datetime import datetime, date, timedelta
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import (submit_batch, build_recipient, get_sheets_service,
                                    SHEET_ID, normalize_phone, is_valid_phone)

LOG = "/tmp/culligan_smart_launcher.log"
def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")

SLOT = sys.argv[1] if len(sys.argv) > 1 else 'afternoon'
TARGET_N = 10
CITIES = [
    ('Caldaro', 'aziende_caldaro_VERIFICATE'),
    ('Appiano', 'aziende_appiano_VERIFICATE'),
    ('Laives',  'aziende_laives_VERIFICATE'),
    ('Egna',    'aziende_egna_VERIFICATE'),
    ('Salorno', 'aziende_salorno_VERIFICATE'),
]

# Slot definisce le categorie preferite
SLOT_CATEGORIES = {
    'morning':   ['garni','b&b','bed','pensione','gasthof','gasthaus','hotel garni'],
    'afternoon': ['pizzeria','ristorante','trattoria','osteria','braceria'],
    'late':      ['bar','café','caffè','pub','pasticceria','gelateria','ristorante','trattoria'],
}
if SLOT not in SLOT_CATEGORIES:
    log(f"ERRORE: slot '{SLOT}' invalido. Usa morning/afternoon/late.")
    sys.exit(1)

log(f"=== SMART LAUNCHER slot={SLOT} target_n={TARGET_N} ===")

def good(raw):
    if not raw: return None
    n = normalize_phone(raw)
    return n if is_valid_phone(n) else None

def cat_match(nome, slot):
    nl = (nome or '').lower()
    cats = SLOT_CATEGORIES[slot]
    if any(c in nl for c in cats):
        return True
    return False

def slot_score(nome, note, slot):
    """Score easy-close + slot match."""
    n = (nome + ' ' + (note or '')).lower()
    s = 0
    if cat_match(nome, slot): s += 20
    # Family-run bonus
    if any(x in n for x in ['b&b','bed','garni','pensione','gasthof','gasthaus','trattoria','osteria','pizzeria','panificio','pasticceria','gelateria']): s += 10
    if any(x in n for x in ['ristorante','bar','café','caffè']): s += 5
    # Penalizza hotel grandi
    if any(x in n for x in ['parc hotel','wellviva','schloss','resort','5 stell','5*','superior','spa','wellness']): s -= 25
    if 'hotel' in n and not any(x in n for x in ['garni','pensione','b&b']): s -= 5
    return s

svc = get_sheets_service()

def parse_date_it(s):
    if not s: return None
    s = str(s).strip()
    for fmt in ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'):
        try: return datetime.strptime(s.split()[0], fmt).date()
        except: pass
    return None

# Filter: non chiamate negli ultimi 14 giorni
cutoff = date.today() - timedelta(days=14)
candidates = []

for citta, tab in CITIES:
    res = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID,
        range=f'{tab}!A2:W500', valueRenderOption='FORMATTED_VALUE').execute()
    for i, r in enumerate(res.get('values',[]), start=2):
        while len(r) < 23: r.append('')
        p = good(r[4])
        if not p: continue
        # Già chiamato di recente?
        dg = parse_date_it(r[6])
        dm = parse_date_it(r[12])
        if dg and dg >= cutoff: continue
        if dm and dm >= cutoff: continue
        # Note flags
        cn = (r[2] or '').lower()
        if any(x in cn for x in ['verificare','chiusa','duplicato','rimuovere']): continue
        # Skip VoIP problematici
        if p.startswith('+390471 1') or '+39047118' in p or '+39047119' in p: continue
        # Categoria deve matchare slot
        if not cat_match(r[0], SLOT): continue
        s = slot_score(r[0], r[2], SLOT)
        if s < 20: continue
        candidates.append({'row':i,'nome':r[0],'tel':p,'ind':r[3],
                          'tab':tab,'citta':citta,'score':s})

candidates.sort(key=lambda x: -x['score'])
targets = candidates[:TARGET_N]
log(f"Candidati totali: {len(candidates)} → selezionati top {len(targets)}")
if not targets:
    log("Nessun target disponibile. Skip batch.")
    sys.exit(0)

from collections import Counter
log(f"Distribuzione: {dict(Counter(t['citta'] for t in targets))}")
for t in targets:
    log(f"  [{t['score']:>2}] {t['citta']:9} R{t['row']:>3} {t['nome'][:38]}")

# Build recipients
recipients = []
mark_per_tab = {}
for t in targets:
    nl = t['nome'].lower()
    if 'pizzer' in nl: cat='pizzeria'
    elif 'pastic' in nl: cat='pasticceria'
    elif 'gelat' in nl: cat='gelateria'
    elif 'bar' in nl or 'café' in nl or 'caffè' in nl: cat='bar'
    elif 'trattor' in nl or 'osteria' in nl or 'ristoran' in nl: cat='ristorante'
    elif 'gasthof' in nl or 'pensione' in nl: cat='b&b'
    elif 'garni' in nl or 'b&b' in nl: cat='b&b'
    else: cat='ristorante'
    r = build_recipient(phone=t['tel'], nome_azienda=t['nome'], categoria=cat,
                        nome_titolare='titolare', indirizzo=t.get('ind',''), note='')
    r['conversation_initiation_client_data']['dynamic_variables']['citta'] = t['citta']
    recipients.append(r)
    mark_per_tab.setdefault(t['tab'], []).append(t['row'])

# Submit
batch_name = f"Auto-{SLOT}-{date.today().strftime('%Y%m%d')}"
res = submit_batch(batch_name, recipients)
bid = res.get('id','?')
log(f"Batch ID: {bid}")
open(f'/tmp/auto_batch_id_{SLOT}_{date.today()}.txt','w').write(bid)

# Mark data_chiamata
today_str = date.today().strftime('%d/%m/%Y')
for tab, rows in mark_per_tab.items():
    body = {'valueInputOption':'RAW','data':[{'range':f'{tab}!G{r}','values':[[today_str]]} for r in rows]}
    svc.spreadsheets().values().batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()
    log(f"  {tab}: {len(rows)} marcate G={today_str}")

log(f"=== {SLOT.upper()} BATCH LANCIATO ({len(recipients)} chiamate) ===")
