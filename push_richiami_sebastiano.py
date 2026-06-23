#!/usr/bin/env python3
"""
Push richiami (seconda chiamata) dal foglio interno → foglio Sebastiano col S/T.
Logica: match per telefono, scrive DATA RICHIAMO (S) e NOTE (T) solo se:
  - azienda già presente in Sebastiano (col I ha prima chiamata)
  - ha una seconda chiamata nel foglio interno (col M = DATA CHIAMATA 2)
  - esito seconda chiamata non è vuoto e non è "Numero errato"
  - col S di Sebastiano è ancora vuota (no sovrascrittura)
"""
import sys, re
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import get_sheets_service, SHEET_ID, TAB_NAME, normalize_phone

SHEET_SEB = "1KsbFkAhJQDd2edYuKgbVC0yd87jK-Y6egKU254Y1wT0"

def fmt_phone(raw):
    return re.sub(r"\D", "", raw.strip().lstrip("+").lstrip("39") if raw.strip().startswith("+39") else raw.strip())

def fmt_date(d):
    d = d.strip()[:10]
    parts = d.split("/")
    return f"{parts[0]}/{parts[1]}/{parts[2][2:]}" if len(parts) == 3 else d

def fmt_note(esito, note_ai):
    note = (note_ai or "").strip().rstrip(".")
    esito = (esito or "").strip()
    if esito == "Non interessato": return "non interessato"
    if esito == "Segreteria" or "segreteria" in note.lower(): return "segreteria"
    if esito == "Appuntamento": return note.lower() if note else "appuntamento fissato"
    if esito == "Email": return note.lower() if note else "email raccolta"
    if note and note.lower() not in ("non risposto", ""):
        return note.lower()
    return "da richiamare"

def main():
    svc = get_sheets_service()

    # Leggi foglio interno
    rows_int = svc.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{TAB_NAME}'!A:P"
    ).execute().get("values", [])

    # Leggi Sebastiano — tutti i dati A:T
    rows_seb = svc.spreadsheets().values().get(
        spreadsheetId=SHEET_SEB, range="'Foglio1'!A:T"
    ).execute().get("values", [])

    # Mappa telefono → row index in Sebastiano (1-based per API)
    seb_phone_map = {}
    for i, row in enumerate(rows_seb[1:], 2):
        tel = fmt_phone(row[4].strip()) if len(row) > 4 else ""
        if tel:
            seb_phone_map[tel] = {"row": i, "col_s": row[18].strip() if len(row) > 18 else ""}

    updates = []
    pushed = []

    for row in rows_int[1:]:
        if not row or not row[0].strip(): continue
        name = row[0].strip()
        phone_raw = row[4].strip() if len(row) > 4 else ""
        if not phone_raw: continue

        # Seconda chiamata: col M (idx 12) = data, N (idx 13) = esito2, O (idx 14) = note2
        date2 = row[12].strip() if len(row) > 12 else ""
        esito2 = row[13].strip() if len(row) > 13 else ""
        note2 = row[14].strip() if len(row) > 14 else ""

        if not date2 or not esito2: continue
        if esito2 in ("Numero errato", ""): continue

        tel_clean = fmt_phone(normalize_phone(phone_raw))
        # Try both with/without leading zero
        match = seb_phone_map.get(tel_clean) or seb_phone_map.get(tel_clean.lstrip("0"))
        if not match: continue
        if match["col_s"]:  # già compilata
            continue

        date_fmt = fmt_date(date2)
        note_fmt = fmt_note(esito2, note2)

        updates.append({
            "range_s": f"'Foglio1'!S{match['row']}",
            "range_t": f"'Foglio1'!T{match['row']}",
            "date": date_fmt,
            "note": note_fmt,
            "name": name
        })
        pushed.append(f"  r{match['row']}: {name:<45} {date_fmt}  {note_fmt[:60]}")

    if not updates:
        print("Nessun richiamo da pushare (nessuna seconda chiamata nel foglio interno ancora).")
        return

    print(f"Richiami da pushare su Sebastiano: {len(updates)}")
    for p in pushed:
        print(p)

    batch_data = []
    for u in updates:
        batch_data.append({"range": u["range_s"], "values": [[u["date"]]]})
        batch_data.append({"range": u["range_t"], "values": [[u["note"]]]})

    svc.spreadsheets().values().batchUpdate(
        spreadsheetId=SHEET_SEB,
        body={"valueInputOption": "USER_ENTERED", "data": batch_data}
    ).execute()
    print(f"\nPush completato: {len(updates)} richiami scritti in col S/T.")

if __name__ == "__main__":
    main()
