#!/usr/bin/env python3
"""Lancia 30 chiamate Culligan sequenziali (concurrency=1) sulle aziende
del foglio interno NON presenti nel foglio condiviso con Sebastiano."""
import os, re, sys, time, json, subprocess
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from culligan_batch_caller import (
    get_sheets_service, read_all_rows, mark_called, normalize_phone,
    is_valid_phone, is_already_called, safe_get, extract_categoria,
    build_recipient, submit_batch,
    COL_NOME_AZIENDA, COL_NOME_TITOLARE, COL_NOTE, COL_INDIRIZZO,
    COL_TELEFONO,
)

SEBASTIANO_SHEET_ID = "1KsbFkAhJQDd2edYuKgbVC0yd87jK-Y6egKU254Y1wT0"
SEBASTIANO_TAB = "Foglio1"
SEBASTIANO_PHONE_COL = 4  # E (0-based)

LIMIT = 30


def read_sebastiano_phones(service):
    res = service.spreadsheets().values().get(
        spreadsheetId=SEBASTIANO_SHEET_ID,
        range=f"'{SEBASTIANO_TAB}'!A:E",
    ).execute()
    rows = res.get("values", [])
    phones = set()
    for r in rows[1:]:
        ph = normalize_phone(safe_get(r, SEBASTIANO_PHONE_COL))
        if ph:
            phones.add(ph)
    return phones


def main():
    print("Lettura foglio interno + foglio Sebastiano...")
    svc = get_sheets_service()
    rows = read_all_rows(svc)
    sebastiano_phones = read_sebastiano_phones(svc)
    print(f"  Internal rows: {len(rows)-1} | Sebastiano phones: {len(sebastiano_phones)}")

    to_call = []
    for i, row in enumerate(rows[1:]):
        if is_already_called(row):
            continue
        ph = normalize_phone(safe_get(row, COL_TELEFONO))
        if not is_valid_phone(ph):
            continue
        if ph in sebastiano_phones:
            continue
        note = safe_get(row, COL_NOTE)
        to_call.append({
            "row_num": i + 2,
            "row_index": i + 1,
            "phone": ph,
            "nome_azienda": safe_get(row, COL_NOME_AZIENDA),
            "nome_titolare": safe_get(row, COL_NOME_TITOLARE),
            "categoria": extract_categoria(note),
            "indirizzo": safe_get(row, COL_INDIRIZZO),
            "note": note,
        })
        if len(to_call) >= LIMIT:
            break

    print(f"\n{len(to_call)} aziende selezionate (non in Sebastiano, telefono valido, mai chiamate):")
    for it in to_call:
        print(f"  {it['row_num']:3d}. {it['nome_azienda']:<38} [{it['categoria']}]  {it['phone']}")

    if len(to_call) == 0:
        print("Niente da chiamare.")
        return

    recipients = [build_recipient(
        phone=it["phone"], nome_azienda=it["nome_azienda"],
        categoria=it["categoria"], nome_titolare=it["nome_titolare"],
        indirizzo=it["indirizzo"], note=it["note"],
    ) for it in to_call]

    name = f"Culligan-30-NotInSeb-{datetime.now().strftime('%Y%m%d-%H%M')}"
    print(f"\nInvio batch '{name}' con concurrency=1 (sequenziale, no overlap)...")
    res = submit_batch(name, recipients)
    batch_id = res.get("batch_call_id", res.get("id", "?"))
    print(f"Batch ID: {batch_id} | status: {res.get('status','?')}")

    oggi = datetime.now().strftime("%d/%m/%Y %H:%M")
    print(f"\nMark data_chiamata={oggi} su righe interne...")
    for it in to_call:
        try:
            mark_called(svc, it["row_index"], oggi)
            time.sleep(0.25)
        except Exception as e:
            print(f"  warn row {it['row_num']}: {e}")
    print("\nFatto. Le chiamate partono sequenzialmente lato ElevenLabs (concurrency=1).")


if __name__ == "__main__":
    main()
