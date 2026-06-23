#!/usr/bin/env python3
"""Run callback batch for a specific slot.
Usage: python3 run_callback_slot.py <slot_key>
Lanciato da scheduler `at` job o manualmente.

1. Legge righe con col W = slot_key e M vuota (non ancora richiamate)
2. Submit batch ElevenLabs concurrency=1 con {{call_attempt}}=2 + {{prev_note}}
3. Marca M con timestamp
4. Polling status fino completed
5. Lancia analyzer post_batch (che scrive su M-Q per call_attempt=2)
"""
import os, sys, time, subprocess
from datetime import datetime
import requests
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import (
    submit_batch, get_sheets_service, mark_called,
    normalize_phone, is_valid_phone, safe_get, extract_categoria,
    SHEET_ID, TAB_NAME,
    COL_NOME_AZIENDA, COL_NOME_TITOLARE, COL_NOTE, COL_INDIRIZZO, COL_TELEFONO,
)

H = {"xi-api-key": "sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"}
BASE = "https://api.elevenlabs.io"

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 run_callback_slot.py <slot_key>"); return
    slot_key = sys.argv[1]
    log_prefix = f"[{datetime.now().strftime('%H:%M:%S')}] [{slot_key}]"
    print(f"{log_prefix} START")

    svc = get_sheets_service()
    rows = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"'{TAB_NAME}'!A:W").execute().get('values',[])

    candidati = []
    for i,r in enumerate(rows[1:], start=2):
        r = r + ['']*(23-len(r))
        if r[22].strip() != slot_key: continue  # W diversa
        if r[12].strip(): continue  # M già compilato
        ph = normalize_phone(safe_get(r, COL_TELEFONO))
        if not is_valid_phone(ph): continue
        candidati.append({
            "row": i, "nome": r[0].strip(), "tel": ph,
            "categoria": extract_categoria(r[2]).lower(),
            "indirizzo": r[3].strip(),
            "nome_titolare": r[1].strip(),
            "note_fonte": r[2].strip(),
            "prev_note": r[9].strip(),
            "prev_date": r[6],
        })

    print(f"{log_prefix} {len(candidati)} candidati nel slot")
    if not candidati: return

    recipients = [{
        "phone_number": c['tel'],
        "conversation_initiation_client_data": {
            "dynamic_variables": {
                "nome_azienda": c['nome'],
                "nome_titolare": c['nome_titolare'],
                "categoria": c['categoria'],
                "citta": "Bolzano",
                "indirizzo": c['indirizzo'],
                "note_extra": c['note_fonte'],
                "row_index": str(c['row']),
                "call_attempt": "2",
                "prev_note": c['prev_note'],
                "prev_data_chiamata": c['prev_date'],
            }
        }
    } for c in candidati]

    name = f"Culligan-Callback-{slot_key}-{datetime.now().strftime('%Y%m%d-%H%M')}"
    res = submit_batch(name, recipients)
    batch_id = res.get("batch_call_id", res.get("id", "?"))
    print(f"{log_prefix} Batch ID: {batch_id}")

    # Mark M
    oggi = datetime.now().strftime("%d/%m/%Y %H:%M")
    updates = [{"range":f"'{TAB_NAME}'!M{c['row']}", "values":[[oggi]]} for c in candidati]
    svc.spreadsheets().values().batchUpdate(spreadsheetId=SHEET_ID,
        body={"valueInputOption":"USER_ENTERED","data":updates}).execute()
    print(f"{log_prefix} Mark M = {oggi} su {len(candidati)} righe")

    # Polling
    print(f"{log_prefix} Polling batch...")
    start = time.time()
    while time.time() - start < 75*60:
        r = requests.get(f"{BASE}/v1/convai/batch-calling/{batch_id}", headers=H, timeout=30).json()
        status = r.get('status')
        from collections import Counter
        c = Counter(x.get('status') for x in r.get('recipients',[]))
        print(f"{log_prefix} t+{int((time.time()-start)/60)}min status={status} {dict(c)}")
        if status in ('completed','failed','cancelled'): break
        time.sleep(60)

    # Analyzer
    print(f"{log_prefix} Lancio analyzer...")
    subprocess.run(["python3","/Users/simocors/Desktop/telesales/demo_mik/post_batch_culligan_analyze.py"],
                   cwd="/Users/simocors/Desktop/telesales")
    print(f"{log_prefix} DONE")


if __name__ == "__main__":
    main()
