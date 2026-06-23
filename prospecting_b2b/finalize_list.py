#!/usr/bin/env python3
"""
Finalizza la lista chiamabile:
- filtra numeri fake (cifre ripetute/sequenziali)
- dedup per telefono (tiene il DM piu' senior)
- dedup vs numeri gia' chiamati (CONTATTI_UNICI + log)
- aggiunge angolo_pitch per settore
- esporta XLSX formato Ferretti pronto per batch ElevenLabs
"""
import re
import pandas as pd

BASE = '/Users/simocors/Desktop/telesales'
PB = f'{BASE}/prospecting_b2b'

# --- angolo pitch per settore (frase di senso compiuto, senza trattini) ---
ANGOLO = {
    'IT / Software': "noi vi portiamo aziende gia' interessate al vostro software cosi' i vostri commerciali parlano solo con chi vuole comprare",
    'Consulenza gestionale': "noi riempiamo l'agenda dei vostri consulenti di appuntamenti con imprenditori che cercano gia' una consulenza",
    'Energia / Fotovoltaico': "noi vi portiamo contatti di aziende e privati pronti a installare il fotovoltaico cosi' chiudete piu' impianti",
    'Formazione': "noi vi riempiamo le aule di persone realmente interessate ai vostri corsi senza che dobbiate rincorrere nessuno",
    'Marketing / Agenzia': "noi vi portiamo clienti gia' pronti a investire in marketing cosi' la vostra agenzia cresce senza fare cold call",
    'Immobiliare': "noi vi portiamo proprietari e acquirenti gia' interessati cosi' i vostri agenti chiudono piu' trattative",
}
ANGOLO_DEFAULT = "noi vi portiamo clienti gia' interessati cosi' i vostri commerciali si concentrano solo sul chiudere"

def is_fake(phone):
    d = re.sub(r'\D', '', phone)
    if d.startswith('39'):
        d = d[2:]
    # tutte uguali o run di 7+ cifre identiche
    if re.search(r'(\d)\1{6,}', d):
        return True
    # sequenze ovvie
    if d in ('1234567890', '0123456789'):
        return True
    # troppo poche cifre distinte
    if len(set(d)) <= 2:
        return True
    return False

SENIORITY = [
    ('owner', 100), ('founder', 95), ('fondatore', 95), ('titolare', 95),
    ('amministratore', 90), ('ceo', 88), ('chief executive', 88),
    ('president', 80), ('presidente', 80), ('managing', 78),
    ('general manager', 70), ('direttore generale', 70),
    ('chief', 60), ('director', 50), ('direttore', 50),
    ('manager', 30), ('head', 25),
]
def seniority_score(ruolo):
    r = str(ruolo).lower()
    for kw, sc in SENIORITY:
        if kw in r:
            return sc
    return 10

def load_called_numbers():
    called = set()
    try:
        df = pd.read_excel(f'{BASE}/CONTATTI_UNICI_TELESALES.xlsx', dtype=str)
        for v in df['Telefono'].dropna():
            d = re.sub(r'\D', '', str(v))
            if d.startswith('39'):
                d = d[2:]
            if len(d) >= 9:
                called.add(d[-10:])
    except Exception as e:
        print('warn CONTATTI_UNICI:', e)
    return called

def main():
    df = pd.read_csv(f'{PB}/lead_b2b_telesales_CHIAMABILI.csv', dtype=str).fillna('')
    print(f"Partenza: {len(df)}")

    # 1. filtro fake
    df = df[~df['telefono'].apply(is_fake)]
    print(f"Dopo filtro fake: {len(df)}")

    # 2. seniority score
    df['_sen'] = df['ruolo_decisore'].apply(seniority_score)
    df['_key'] = df['telefono'].apply(lambda p: re.sub(r'\D','',p)[-10:])

    # 3. dedup per telefono: tieni il piu' senior
    df = df.sort_values('_sen', ascending=False).drop_duplicates('_key', keep='first')
    print(f"Dopo dedup per telefono (DM piu' senior): {len(df)}")

    # 4. dedup vs gia' chiamati
    called = load_called_numbers()
    before = len(df)
    df = df[~df['_key'].isin(called)]
    print(f"Dopo dedup vs gia' chiamati ({len(called)} numeri noti): {len(df)} (rimossi {before-len(df)})")

    # 5. angolo pitch
    df['angolo_pitch'] = df['settore'].map(ANGOLO).fillna(ANGOLO_DEFAULT)

    # 6. pulizia ruolo (italiano leggibile, no maiuscole strane)
    def clean_role(r):
        r = str(r).split(',')[0].split('|')[0].strip()
        return r[:60].capitalize()
    df['ruolo_decisore'] = df['ruolo_decisore'].apply(clean_role)
    df['citta'] = df['citta'].replace('Nan', '').replace('nan', '')

    # 7. formato finale Ferretti
    out = pd.DataFrame({
        'nome_azienda': df['nome_azienda'],
        'nome_decisore': df['nome_decisore'],
        'ruolo_decisore': df['ruolo_decisore'],
        'email': '',
        'telefono': df['telefono'],
        'tipo_numero': df['tipo_numero'],
        'citta': df['citta'],
        'regione': df['regione'].replace('Nan','').replace('nan',''),
        'settore': df['settore'],
        'website': df['website'],
        'angolo_pitch': df['angolo_pitch'],
    })

    csv_path = f'{PB}/LEAD_B2B_TELESALES_FINALE.csv'
    xlsx_path = f'{PB}/LEAD_B2B_TELESALES_FINALE.xlsx'
    out.to_csv(csv_path, index=False)
    out.to_excel(xlsx_path, index=False)
    print(f"\n=== LISTA FINALE: {len(out)} contatti chiamabili ===")
    print(f"Cellulari: {(out['tipo_numero']=='cellulare').sum()} | Fissi: {(out['tipo_numero']=='fisso').sum()}")
    print('Per settore:', out['settore'].value_counts().to_dict())
    print(f"\nSalvato:\n  {csv_path}\n  {xlsx_path}")

if __name__ == '__main__':
    main()
