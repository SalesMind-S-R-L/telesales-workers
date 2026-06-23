#!/usr/bin/env python3
"""
Push automatico esiti batch Marco Ferretti -> foglio OUTREACH AI VOICE.
Classifica esito + nota professionale (regole esiti/note) da trascrizione.
Inserisce le nuove righe in cima (sotto l'header), newest-on-top.

Uso: python3 ferretti_push_to_sheet.py <batch_id> [--csv path_lista]
"""
import sys, re, argparse
from datetime import datetime, timezone, timedelta
import requests
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import get_sheets_service

ELEVENLABS_API_KEY = "sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
BASE = "https://api.elevenlabs.io"
SID = '1wFYXFDFo6W2GT6HT3HKHLYx8eN-C4VUGnxlU_dIiNyk'
TAB = 'OUTREACH AI VOICE'
GID = 431195392

def h(): return {'xi-api-key': ELEVENLABS_API_KEY}

IVR = ['premere', 'premi ', 'digiti', 'digita', 'tasto', 'benvenut', 'in attesa',
       'operatore disponibile', 'la sua chiamata', 'press one', 'press two',
       'segreteria telefonica', 'lasciate un messaggio', 'al momento non',
       'i nostri uffici', 'orari di apertura', 'casella vocale']
ABSENT = ['non c’è', 'non c\'è', 'non e\' in ufficio', 'non è in ufficio',
          'in riunione', 'occupat', 'non disponibile', 'richiam', 'non risponde',
          'al momento non', 'fuori ufficio', 'non in sede']
DECLINE = ['non ci interessa', 'non interessa', 'no grazie', 'non fa per noi',
           'non siamo interessati', 'già a posto', 'non mi interessa']
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
GENERIC = ('info@', 'amministrazione@', 'segreteria@', 'commerciale@', 'contatti@', 'support@', 'customerservice@')

def classify(status, transcript):
    """Ritorna (esito, nota)."""
    if status in ('failed', 'no_answer') and not transcript:
        return 'Non risposto', 'Non risposto.'
    user_txt = ' '.join((t.get('message') or '').lower() for t in transcript if t.get('role') == 'user')
    if not user_txt.strip() or len(user_txt.replace('.', '').strip()) < 3:
        if status == 'voicemail':
            return 'Segreteria', 'Segreteria telefonica.'
        return 'Non risposto', 'Non risposto.'

    emails = [e for e in EMAIL_RE.findall(user_txt) if not e.endswith('.it.')]
    real_email = next((e for e in emails if not e.lower().startswith(GENERIC)), '')
    is_ivr = any(k in user_txt for k in IVR)
    has_human = any(w in user_txt for w in ['buongiorno', 'pronto', 'chi lo cerca', 'chi parla',
                    'collega', 'sono ', 'mi dica', 'di cosa', 'cosa', 'momento', 'attimo'])
    declined = any(k in user_txt for k in DECLINE)
    absent = any(k in user_txt for k in ABSENT)
    # lead caldo: il DECISORE (non lo staff/IVR) mostra interesse esplicito
    INTEREST = ['mi interessa', 'ci interessa', 'molto interessante', 'interessante',
                'come funziona', 'quanto costa', 'che prezzi', 'mandami', 'mi mandi qualcosa',
                'voglio saperne', 'dimmi di più', 'mi piacerebbe', 'potrebbe interessarci',
                'fammi sapere', 'sì, mi interessa', 'volentieri sentire', 'sentire niccolò',
                'sentire nicolò', 'mi puoi spiegare', 'approfondire']
    interested = any(k in user_txt for k in INTEREST) and not is_ivr

    # appuntamento: solo con conferma esplicita di slot (giorno) + accordo
    weekdays = ['luned', 'marted', 'mercoled', 'gioved', 'venerd']
    appt = ('appuntamento' in user_txt or any(d in user_txt for d in weekdays)) and \
           any(w in user_txt for w in ['va bene', 'sì', 'd\'accordo', 'perfetto', 'ok'])
    # ma serve che il chiamato confermi, non solo l'agente -> richiede slot concreto giorno
    has_slot = any(d in user_txt for d in weekdays)

    if declined:
        return 'Non interessato', 'Il contatto ascolta la proposta e declina.'
    if appt and has_slot:
        return 'Appuntamento', 'Mostra disponibilità; concordare giorno e ora.'
    if real_email:
        return 'Email raccolta', f'Lo staff chiede una mail per inoltrare al referente. Email: {real_email}.'
    if interested:
        return 'Interessato', 'Il contatto mostra interesse e vuole approfondire; ricontattare per fissare la call.'
    if absent or (has_human and not is_ivr):
        return 'Da richiamare', 'Risponde lo staff, il titolare non è disponibile al momento.'
    if is_ivr:
        return 'Da richiamare', 'Centralino con risponditore automatico, non navigabile fino al decisore.'
    return 'Da richiamare', 'Contatto stabilito, da riprovare per parlare con il decisore.'

def fetch_conv(cid):
    try:
        d = requests.get(f'{BASE}/v1/convai/conversations/{cid}', headers=h(), timeout=20).json()
        md = d.get('metadata', {})
        return d.get('transcript', []), md.get('call_duration_secs', 0) or 0
    except Exception:
        return [], 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('batch_id')
    ap.add_argument('--csv', default='/Users/simocors/Desktop/telesales/prospecting_b2b/LEAD_B2B_DIALABILI.csv')
    args = ap.parse_args()

    # mappa telefono -> anagrafica
    import csv as csvmod
    meta = {}
    with open(args.csv, encoding='utf-8') as f:
        for r in csvmod.DictReader(f):
            ph = re.sub(r'\D', '', r.get('telefono', ''))
            meta[ph[-9:]] = r

    d = requests.get(f'{BASE}/v1/convai/batch-calling/{args.batch_id}', headers=h(), timeout=30).json()
    recs = d.get('recipients', [])
    batch_name = d.get('name', args.batch_id)
    today = datetime.now(timezone(timedelta(hours=2))).strftime('%d/%m/%Y')
    print(f"Batch {batch_name}: {len(recs)} destinatari")

    rows = []
    for x in recs:
        ph = x.get('phone_number', '')
        phk = re.sub(r'\D', '', ph)[-9:]
        m = meta.get(phk, {})
        cid = x.get('conversation_id', '')
        transcript, dur = fetch_conv(cid) if cid else ([], 0)
        esito, nota = classify(x.get('status'), transcript)
        # email: se raccolta nella nota usala, altrimenti quella anagrafica (pattern)
        em = ''
        mm = re.search(r'Email: (\S+@\S+)\.', nota)
        if mm: em = mm.group(1)
        link = f'=HYPERLINK("https://elevenlabs.io/app/conversational-ai/history/{cid}";"{cid[:12]}")' if cid else ''
        rows.append([
            today, batch_name, m.get('nome_azienda', ''), m.get('nome_decisore', ''),
            m.get('ruolo_decisore', ''), ph, em, m.get('citta', ''), m.get('settore', ''),
            esito, nota, m.get('angolo_pitch', ''), str(dur), link,
        ])

    svc = get_sheets_service()
    # SOLO opportunita' sul foglio principale; richiamate/normali nel LOG
    POSITIVE = {'Appuntamento', 'Email raccolta', 'Interessato', 'Da richiamare'}
    LOG_TAB = 'LOG AI VOICE'
    pos = [r for r in rows if r[9] in POSITIVE]
    rest = [r for r in rows if r[9] not in POSITIVE]

    # 1. positive -> OUTREACH AI VOICE in cima
    if pos:
        svc.spreadsheets().batchUpdate(spreadsheetId=SID, body={'requests': [{
            'insertDimension': {'range': {'sheetId': GID, 'dimension': 'ROWS',
                                          'startIndex': 3, 'endIndex': 3 + len(pos)},
                                'inheritFromBefore': False}}]}).execute()
        svc.spreadsheets().values().update(
            spreadsheetId=SID, range=f"'{TAB}'!A4",
            valueInputOption='USER_ENTERED', body={'values': pos}).execute()

    # 2. resto -> LOG AI VOICE in fondo (crea il tab se manca)
    if rest:
        meta = svc.spreadsheets().get(spreadsheetId=SID, fields='sheets.properties.title').execute()
        if LOG_TAB not in [s['properties']['title'] for s in meta['sheets']]:
            svc.spreadsheets().batchUpdate(spreadsheetId=SID, body={'requests': [
                {'addSheet': {'properties': {'title': LOG_TAB}}}]}).execute()
        col = svc.spreadsheets().values().get(spreadsheetId=SID, range=f"'{LOG_TAB}'!A:A").execute().get('values', [])
        start = len(col) + 1 if col else 1
        svc.spreadsheets().values().update(
            spreadsheetId=SID, range=f"'{LOG_TAB}'!A{start}",
            valueInputOption='USER_ENTERED', body={'values': rest}).execute()

    from collections import Counter
    c = Counter(r[9] for r in rows)
    print(f"Push: {len(pos)} opportunita' su OUTREACH AI VOICE, {len(rest)} nel LOG. Esiti: {dict(c)}")

if __name__ == '__main__':
    main()
