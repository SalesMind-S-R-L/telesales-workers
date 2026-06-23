#!/usr/bin/env python3
"""Callback Scheduler Marco Culligan.
Legge righe foglio Claude Bolzano dove ESITO='Da richiamare' e colonna M
(DATA CHIAMATA 2) è vuota. Parse delle note (col J) per estrarre orario/giorno
richiamo concordato. Mappa al miglior slot di OGGI:
- Se l'orario indicato è passato: chiama oggi alla stessa ora
- Se diceva 'tra X ore' contato dalla prima chiamata: chiama oggi adesso o nello slot
- Se indicava giorno della settimana (es. martedì) e oggi è dopo: chiama oggi
Submit batch ElevenLabs concurrency=1 con {{call_attempt}}=2 + {{prev_note}}.

Default: dry-run. Lancia con --send per submit reale."""
import os, re, sys, time
from datetime import datetime
import requests

sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import (
    get_sheets_service, normalize_phone, is_valid_phone, safe_get, extract_categoria,
    submit_batch, mark_called,
    SHEET_ID, TAB_NAME, CULLIGAN_AGENT_ID, PHONE_NUMBER_ID,
    COL_NOME_AZIENDA, COL_NOME_TITOLARE, COL_NOTE, COL_INDIRIZZO, COL_TELEFONO,
)

H = {"xi-api-key": "sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"}
COL_DATA_CHIAMATA_1 = 6   # G
COL_ESITO_1 = 8           # I
COL_NOTE_AI_1 = 9         # J
COL_DATA_CHIAMATA_2 = 12  # M (0-based)
COL_NOTE_AI_2 = 14        # O

GIORNI_MAP = {"lunedì":0,"lunedi":0, "martedì":1,"martedi":1, "mercoledì":2,"mercoledi":2,
              "giovedì":3,"giovedi":3, "venerdì":4,"venerdi":4, "sabato":5, "domenica":6}


def parse_callback_time(note: str, prev_call_dt: datetime, now: datetime):
    """Restituisce un dict con info su quando richiamare:
       {hint_type, hour_target, can_call_now}
       Logica:
       - se nota dice 'verso le 15' / 'alle 9' → hour_target=15/9 oggi
       - 'tra X ore/un'ora' → prev_call_dt + X
       - 'stasera' → oggi 18:00
       - 'domani mattina' → oggi 9:00 (se la prima chiamata era ieri/passato)
       - 'lunedì'/'martedì'... → oggi a 10:30 default (se giorno passato)
       - nessun hint → oggi adesso slot generico
    """
    n = (note or '').lower()

    # hh:mm o "alle HH" o "verso le HH"
    m = re.search(r'\b(?:alle|verso le|ore)\s+(\d{1,2})(?:[:.](\d{2}))?\b', n)
    if m:
        h = int(m.group(1))
        mm = m.group(2) or "00"
        if 6 <= h <= 22:
            return {"hint_type":"specific_hour","hour_target":h,"min_target":int(mm)}

    # "tra X ore" / "tra un'ora"
    if re.search(r"\btra\s+(?:circa\s+)?(?:un['\s]*ora|\d+\s*ore?)\b", n):
        return {"hint_type":"hours_offset","hour_target":(now.hour + 1)}

    # 'stasera' / 'sera'
    if re.search(r'\b(stasera|sera)\b', n):
        return {"hint_type":"evening","hour_target":18,"min_target":0}

    # 'domani mattina' / 'mattina'
    if re.search(r'\bdomani mattina\b|\bmattina\b', n):
        return {"hint_type":"morning","hour_target":10,"min_target":0}

    # 'domani'
    if re.search(r'\bdomani\b', n):
        return {"hint_type":"tomorrow_generic","hour_target":11,"min_target":0}

    # giorno settimana
    for nome,wd in GIORNI_MAP.items():
        if re.search(rf'\b{nome}\b', n):
            return {"hint_type":"weekday","hour_target":10,"min_target":30}

    # nessun hint
    return {"hint_type":"none","hour_target":now.hour,"min_target":0}


def main():
    send = "--send" in sys.argv
    print(f"Modalità: {'INVIO REALE' if send else 'DRY-RUN'}")
    now = datetime.now()

    svc = get_sheets_service()
    rows = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"'{TAB_NAME}'!A:Q").execute().get('values',[])

    # Keywords che indicano in realtà NON interessato anche se classificato "Da richiamare"
    SKIP_KEYWORDS = [
        'non interessat', 'non ci serve', 'non vogliamo',
        'abbiamo già fornit', 'abbiamo già un depurat',
        'abbiamo già il depurat', 'già installato un depurat',
    ]

    # Esiti da richiamare: "Da richiamare" + "Non risposto" (SIP fail / nessuna risposta)
    RICHIAMA_ESITI = {"Da richiamare", "Non risposto", "Segreteria"}

    candidati = []
    for i,r in enumerate(rows[1:], start=2):
        r = r + ['']*(17-len(r))
        esito = r[COL_ESITO_1].strip()
        if esito not in RICHIAMA_ESITI: continue
        if r[COL_DATA_CHIAMATA_2].strip(): continue  # già richiamato

        note_lower = r[COL_NOTE_AI_1].strip().lower()
        skip_match = next((k for k in SKIP_KEYWORDS if k in note_lower), None)
        if skip_match:
            print(f"  SKIP r{i:3d} {r[0]:<35} [match '{skip_match}']")
            continue

        ph = normalize_phone(safe_get(r, COL_TELEFONO))
        if not is_valid_phone(ph): continue

        # Parse data prima chiamata
        prev_dt = None
        try:
            prev_dt = datetime.strptime(r[COL_DATA_CHIAMATA_1].split()[0], "%d/%m/%Y")
        except Exception:
            prev_dt = now
        prev_note = r[COL_NOTE_AI_1].strip()
        hint = parse_callback_time(prev_note, prev_dt, now)

        candidati.append({
            "row": i,
            "nome": r[0].strip(),
            "tel": ph,
            "categoria": extract_categoria(r[2]),
            "indirizzo": r[3].strip(),
            "nome_titolare": r[1].strip(),
            "note_fonte": r[2].strip(),
            "prev_note": prev_note,
            "prev_date": r[COL_DATA_CHIAMATA_1],
            "hint": hint,
        })

    print(f"\nCandidati richiamo: {len(candidati)}\n")
    for c in candidati:
        print(f"  r{c['row']:3d} {c['nome']:<38} {c['hint']['hint_type']:<15} ora→{c['hint']['hour_target']:02d}:{c['hint'].get('min_target',0):02d}")
        print(f"        prev_note: {c['prev_note'][:90]}")

    if not candidati:
        print("Nessun candidato — niente da fare.")
        return

    # Ordina per ora target crescente
    candidati.sort(key=lambda c: (c['hint']['hour_target'], c['hint'].get('min_target',0)))

    if not send:
        print(f"\nDry-run: con --send invio batch di {len(candidati)} richiami concurrency=1.")
        return

    # Costruisci recipients
    recipients = []
    for c in candidati:
        recipients.append({
            "phone_number": c['tel'],
            "conversation_initiation_client_data": {
                "dynamic_variables": {
                    "nome_azienda": c['nome'],
                    "nome_titolare": c['nome_titolare'],
                    "categoria": c['categoria'].lower(),
                    "citta": "Bolzano",
                    "indirizzo": c['indirizzo'],
                    "note_extra": c['note_fonte'],
                    "row_index": str(c['row']),
                    "call_attempt": "2",
                    "prev_note": c['prev_note'],
                    "prev_data_chiamata": c['prev_date'],
                }
            }
        })

    name = f"Culligan-Callback-{now.strftime('%Y%m%d-%H%M')}"
    print(f"\nSubmit batch '{name}' concurrency=1 ringing 60s...")
    res = submit_batch(name, recipients)
    batch_id = res.get("batch_call_id", res.get("id", "?"))
    print(f"Batch ID: {batch_id}")

    # Mark col M (DATA CHIAMATA 2) per ogni riga
    oggi = now.strftime("%d/%m/%Y %H:%M")
    updates = [{"range": f"'{TAB_NAME}'!M{c['row']}", "values":[[oggi]]} for c in candidati]
    svc.spreadsheets().values().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"valueInputOption":"USER_ENTERED","data":updates}
    ).execute()
    print(f"Marcate {len(updates)} righe con DATA CHIAMATA 2 = {oggi}")


if __name__ == "__main__":
    main()
