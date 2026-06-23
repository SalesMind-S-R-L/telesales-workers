#!/usr/bin/env python3
"""
culligan_city_batch.py — Batch caller multi-città per territorio Sebastiano.

Uso:
    python3 culligan_city_batch.py --city laives
    python3 culligan_city_batch.py --city caldaro --limit 30
    python3 culligan_city_batch.py --city appiano --rows 5,6,7,8
    python3 culligan_city_batch.py --list  # mostra città disponibili

Ogni città ha un tab dedicato nel foglio Claude:
    aziende_{city}_VERIFICATE  →  stesso SHEET_ID del foglio Bolzano
"""

import sys, os, argparse, logging, time
sys.path.insert(0, os.path.dirname(__file__))

from culligan_batch_caller import (
    get_sheets_service, SHEET_ID, CULLIGAN_AGENT_ID, PHONE_NUMBER_ID,
    normalize_phone, is_valid_phone, extract_categoria, build_recipient,
    submit_batch, mark_called, ELEVENLABS_API_KEY
)

# -------------------------------------------------------------------
# Config città
# -------------------------------------------------------------------
CITIES = {
    'bolzano':      {'tab': 'aziende_bolzano_VERIFICATE',       'prefix': '0471', 'nome': 'Bolzano'},
    'laives':       {'tab': 'aziende_laives_VERIFICATE',         'prefix': '0471', 'nome': 'Laives'},
    'caldaro':      {'tab': 'aziende_caldaro_VERIFICATE',        'prefix': '0471', 'nome': 'Caldaro'},
    'appiano':      {'tab': 'aziende_appiano_VERIFICATE',        'prefix': '0471', 'nome': 'Appiano'},
    'egna':         {'tab': 'aziende_egna_VERIFICATE',           'prefix': '0471', 'nome': 'Egna'},
    'salorno':      {'tab': 'aziende_salorno_VERIFICATE',        'prefix': '0471', 'nome': 'Salorno'},
    'mezzolombardo':{'tab': 'aziende_mezzolombardo_VERIFICATE',  'prefix': '0461', 'nome': 'Mezzolombardo'},
    'mezzocorona':  {'tab': 'aziende_mezzocorona_VERIFICATE',    'prefix': '0461', 'nome': 'Mezzocorona'},
}

TARGET_CONCURRENCY = 1
RINGING_TIMEOUT   = 60

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/culligan_city_batch.log'),
    ]
)
log = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def read_sheet_rows(svc, tab, limit=None, target_rows=None):
    """Legge righe dal tab specificato. Restituisce lista di (row_idx, row_data)."""
    res = svc.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f'{tab}!A:W'
    ).execute()
    all_rows = res.get('values', [])
    if len(all_rows) < 2:
        return []

    out = []
    for i, row in enumerate(all_rows[1:], start=2):  # row 2+ (1-indexed, skip header)
        if target_rows and i not in target_rows:
            continue
        while len(row) < 23:
            row.append('')
        nome     = row[0].strip()
        telefono = row[4].strip()
        data_ch  = row[6].strip()   # col G = DATA DELLA CHIAMATA

        if not nome or not telefono:
            continue
        if data_ch:
            continue  # già chiamata
        if not is_valid_phone(telefono):
            log.warning(f'R{i} {nome}: telefono non valido ({telefono}), skip')
            continue

        out.append((i, row))
        if limit and len(out) >= limit:
            break

    return out


def build_recipients_from_rows(rows_data, city_nome):
    """Costruisce lista recipient ElevenLabs da righe foglio."""
    recipients = []
    for row_idx, row in rows_data:
        nome_az   = row[0].strip()
        contatto  = row[1].strip() or 'titolare'
        note      = row[2].strip()
        indirizzo = row[3].strip()
        telefono  = row[4].strip()
        categoria = extract_categoria(nome_az, note)

        r = build_recipient(
            phone=telefono,
            nome_azienda=nome_az,
            nome_titolare=contatto,
            categoria=categoria,
            citta=city_nome,
            indirizzo=indirizzo,
            note_extra=note,
        )
        r['_row_idx'] = row_idx
        recipients.append(r)
        log.info(f'  R{row_idx} {nome_az} ({telefono})')

    return recipients


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Culligan batch caller multi-città')
    parser.add_argument('--city',  required=False, help='Nome città (es: laives, caldaro)')
    parser.add_argument('--limit', type=int, default=30, help='Max chiamate (default 30)')
    parser.add_argument('--rows',  help='Righe specifiche separate da virgola (es: 5,6,7)')
    parser.add_argument('--list',  action='store_true', help='Elenca città disponibili')
    args = parser.parse_args()

    if args.list:
        print('\nCittà disponibili:')
        for k, v in CITIES.items():
            print(f'  {k:15} → tab: {v["tab"]}  prefisso: {v["prefix"]}')
        return

    if not args.city:
        parser.error('Specifica --city oppure --list')

    city_key = args.city.lower()
    if city_key not in CITIES:
        print(f'Città non trovata. Disponibili: {list(CITIES.keys())}')
        sys.exit(1)

    cfg      = CITIES[city_key]
    tab      = cfg['tab']
    city_nome = cfg['nome']
    target_rows = [int(r) for r in args.rows.split(',')] if args.rows else None

    log.info(f'=== BATCH {city_nome.upper()} — tab: {tab} ===')

    svc = get_sheets_service()

    # 1. Leggi righe
    log.info(f'Lettura righe da {tab}...')
    rows = read_sheet_rows(svc, tab, limit=args.limit, target_rows=target_rows)
    if not rows:
        log.error('Nessuna riga valida trovata. Popola il foglio prima di lanciare il batch.')
        sys.exit(1)

    log.info(f'{len(rows)} righe selezionate per {city_nome}')

    # 2. Build recipients
    recipients = build_recipients_from_rows(rows, city_nome)
    if not recipients:
        log.error('Nessun recipient valido.')
        sys.exit(1)

    # 3. Submit batch
    log.info(f'Submit batch ElevenLabs ({len(recipients)} chiamate)...')
    batch_id = submit_batch(
        recipients=[{k: v for k, v in r.items() if not k.startswith('_')} for r in recipients],
        concurrency=TARGET_CONCURRENCY,
        ringing_timeout_secs=RINGING_TIMEOUT,
    )
    log.info(f'Batch ID: {batch_id}')

    # Save batch_id
    bid_file = f'/tmp/culligan_{city_key}_batch_id.txt'
    with open(bid_file, 'w') as f:
        f.write(batch_id)
    log.info(f'Batch ID salvato in {bid_file}')

    # 4. Mark called (DATA DELLA CHIAMATA = oggi)
    from datetime import date
    today = date.today().strftime('%d/%m/%Y')
    row_indices = [r['_row_idx'] for r in recipients]

    mark_called(svc, tab, row_indices, today)
    log.info(f'Marcate {len(row_indices)} righe con data {today}')

    log.info(f'=== FINE STEP 1 — batch {city_key} in progress ===')
    print(f'\nBatch ID: {batch_id}')
    print(f'Chiamate inviate: {len(recipients)}')
    print(f'Città: {city_nome}')
    print(f'Log: /tmp/culligan_city_batch.log')


if __name__ == '__main__':
    main()
