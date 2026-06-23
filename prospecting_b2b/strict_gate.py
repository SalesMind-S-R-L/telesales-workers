#!/usr/bin/env python3
"""
Gate deterministico finale anti-SIP-404.
Prende l'output del workflow (numeri estratti dagli agenti) e tiene SOLO
quelli con formato italiano matematicamente corretto e completo.
Input:  /tmp/phone_hunt_result.json  (lista di {azienda,numero,tipo,fonte,dialabile})
Output: LEAD_B2B_DIALABILI.csv/.xlsx  (formato Ferretti, merge con dati azienda)
"""
import re, json, sys
import pandas as pd

BASE = '/Users/simocors/Desktop/telesales'
PB = f'{BASE}/prospecting_b2b'

PREFISSI_MOBILE = {'310','311','312','313','314','315','317','319','320','322','323','324','327','328','329','330','331','333','334','335','336','337','338','339','340','342','343','344','345','346','347','348','349','350','351','352','353','360','366','368','370','371','373','377','380','383','388','389','391','392','393','398'}
# prefissi distrettuali fissi italiani: 0 + 1-3 cifre. Set principali noti.
PREFISSI_FISSO_2 = {'02','06','081','011','010','055','051','049','045','041','040','070','075','080','085','090','095','099'}

def gate(numero):
    """Ritorna (e164, tipo) se dialabile, altrimenti None."""
    if not isinstance(numero, str): return None
    d = re.sub(r'\D', '', numero)
    if d.startswith('39'): d = d[2:]
    d = d.lstrip('0') if d.startswith('00') else d
    # mobile
    if d.startswith('3'):
        if len(d) == 10 and d[:3] in PREFISSI_MOBILE:
            return '+39' + d, 'cellulare'
        return None
    # fisso: deve iniziare con 0
    if d.startswith('0'):
        if not (9 <= len(d) <= 11) or d[1] == '0':
            return None
        # prefissi area italiani a 2 cifre (metro) e 3 cifre (capoluoghi)
        AREA2 = {'02','06'}
        AREA3 = {'010','011','013','015','019','030','031','035','039','040','041','045','048','049',
                 '050','051','055','059','070','071','075','079','080','081','085','089','090','091','095','099',
                 '0521','0522'}  # nota: trattati a parte sotto
        pref2 = d[:2]; pref3 = d[:3]
        # numero completo CERTO:
        #  - 10/11 cifre: sempre ok (lunghezza sufficiente per qualsiasi prefisso)
        #  - 9 cifre: ok SOLO se prefisso area 2 cifre (7 abbonato) o 3 cifre (6 abbonato)
        if len(d) >= 10:
            return '+39' + d, 'fisso'
        # len == 9
        if pref2 in AREA2 or pref3 in AREA3:
            return '+39' + d, 'fisso'
        # 9 cifre con prefisso area a 4 cifre -> solo 5 cifre abbonato = probabile troncamento -> SCARTA
        return None
    return None

def main():
    raw = json.load(open('/tmp/phone_hunt_result.json'))
    print(f"Numeri grezzi dagli agenti: {len(raw)}")

    # carica anagrafica aziende per merge (decisore, ruolo, citta, settore, sito)
    comp = {c['a'].lower(): c for c in json.load(open(f'{PB}/companies_input.json')) } if False else {}
    # companies_input.json ha chiavi azienda/decisore/...
    cin = json.load(open(f'{PB}/companies_input.json'))
    by_name = {c['azienda'].strip().lower(): c for c in cin}

    rows = []
    seen = set()
    for r in raw:
        res = gate(r.get('numero', ''))
        if not res:
            continue
        e164, tipo = res
        if e164 in seen:
            continue
        seen.add(e164)
        az = (r.get('azienda') or '').strip()
        meta = by_name.get(az.lower(), {})
        rows.append({
            'nome_azienda': az.title(),
            'nome_decisore': meta.get('decisore', ''),
            'ruolo_decisore': (meta.get('ruolo', '') or '').split(',')[0][:50].capitalize(),
            'email': '',
            'telefono': e164,
            'tipo_numero': tipo,
            'citta': (meta.get('citta', '') or '').title(),
            'settore': meta.get('settore', ''),
            'website': meta.get('website', ''),
            'fonte_numero': r.get('fonte', ''),
        })

    df = pd.DataFrame(rows)
    # dedup vs gia' chiamati (CONTATTI_UNICI)
    called = set()
    try:
        cu = pd.read_excel(f'{BASE}/CONTATTI_UNICI_TELESALES.xlsx', dtype=str)
        for v in cu['Telefono'].dropna():
            dd = re.sub(r'\D','',str(v));  dd = dd[2:] if dd.startswith('39') else dd
            if len(dd)>=9: called.add(dd[-9:])
    except Exception as e:
        print('warn:', e)
    df['_k'] = df['telefono'].apply(lambda p: re.sub(r'\D','',p)[-9:])
    before = len(df)
    df = df[~df['_k'].isin(called)].drop(columns='_k')

    # email pattern
    def dom(w): return re.sub(r'^https?://','',str(w)).split('/')[0].replace('www.','')
    def email(n, w):
        d = dom(w); p = [re.sub(r'[^a-zàèéìòù]','',x) for x in str(n).lower().split() if x]
        return f"{p[0]}.{p[-1]}@{d}" if len(p)>=2 and '.' in d else ''
    df['email'] = [email(n,w) for n,w in zip(df['nome_decisore'], df['website'])]

    csv_p = f'{PB}/LEAD_B2B_DIALABILI.csv'
    xlsx_p = f'{PB}/LEAD_B2B_DIALABILI.xlsx'
    df.to_csv(csv_p, index=False)
    df.to_excel(xlsx_p, index=False)
    print(f"\n=== DIALABILI (gate superato): {len(df)} ===")
    print(f"Cellulari: {(df['tipo_numero']=='cellulare').sum()} | Fissi: {(df['tipo_numero']=='fisso').sum()}")
    print(f"(dedup vs gia' chiamati: rimossi {before-len(df)})")
    print(f"Salvato: {csv_p}")

if __name__ == '__main__':
    main()
