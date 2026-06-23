#!/usr/bin/env python3
"""Push 30 righe del batch 19/05 dal foglio Claude Bolzano al foglio Sebastiano.
Mapping colonne: A=nome, B=titolare, D=indirizzo, E=tel, F=presente,
                  I=data chiamata (DD/MM/YY), J=nota lowercase, K=data app."""
import re, sys
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import get_sheets_service

SRC_ID = "1PiezlYSd5TZNBCRTvzBhx_yVCGfN6aMI3PXdOYU4xu8"
SRC_TAB = "aziende_bolzano_VERIFICATE"
DST_ID = "1KsbFkAhJQDd2edYuKgbVC0yd87jK-Y6egKU254Y1wT0"
DST_TAB = "Foglio1"
START_ROW = 181  # prima riga libera dopo ieri (180)

# row_interno → (titolare, nota_breve_stile_sebastiano)
ROW_DATA = {
    39: ("", "non risp"),
    41: ("", "non risp"),
    42: ("", "cameriera da sola in struttura, ha chiesto di richiamare tra 15 minuti col titolare"),
    43: ("", "non risp"),
    44: ("", "non risp"),
    45: ("", "reception Da Libero, comunicazione difficile e chiamata interrotta, riprovare"),
    46: ("", "non risp"),
    47: ("", "disponibile a dare diretto del titolare ma chiamata interrotta prima del passaggio"),
    49: ("", "non risp"),
    50: ("", "non risp"),
    51: ("", "non risp"),
    52: ("Belen Barbara", "risposto Belen Barbara, da qualificare se è la titolare, riprovare"),
    53: ("", "non risp"),
    55: ("", "non risp"),
    56: ("", "titolare ha detto 'usiamo solo acqua plastica', riprovare per approfondire"),
    57: ("", "non risp"),
    58: ("", "non risp"),
    60: ("", "risposto Tatiana di Goldenstein Townhouse (probabile inoltro), verificare numero"),
    61: ("", "non risp"),
    62: ("", "titolare ha detto 'non sono interessato, grazie', non interessati"),
    63: ("", "non risp"),
    64: ("", "audio molto disturbato, ha chiesto di essere richiamato"),
    65: ("", "risposto ma conversazione corta, riprovare"),
    66: ("", "non risp"),
    68: ("", "non risp"),
    69: ("", "titolare disponibile martedì in generale ma no a martedì 14 e 16, riconfermare orario"),
    70: ("", "non risp"),
    71: ("", "titolare di Pizzeria La Grolla ha detto chiaramente no, non interessati"),
    72: ("", "non risp"),
    73: ("", "risposto ma conversazione interrotta dopo saluto, riprovare"),
}

PRESENT_ESITI = {"Appuntamento", "Email", "Da richiamare"}


def clean_phone(s):
    return re.sub(r"[^\d]", "", s or "")


def fmt_date_short(s):
    m = re.match(r"(\d{2}/\d{2})/(\d{4})", s or "")
    return f"{m.group(1)}/{m.group(2)[-2:]}" if m else ""


def main():
    svc = get_sheets_service()
    src = svc.spreadsheets().values().get(
        spreadsheetId=SRC_ID, range=f"'{SRC_TAB}'!A:L"
    ).execute().get("values", [])

    rows_out = []
    for row_idx, (titolare, nota) in sorted(ROW_DATA.items()):
        r = src[row_idx - 1] + [""] * 12
        nome = r[0].strip()
        indir = r[3].strip()
        tel = clean_phone(r[4])
        esito = r[8].strip()
        present = "sì" if esito in PRESENT_ESITI else ""
        data_call = fmt_date_short(r[6])
        # 11 elementi: A nome, B titolare, C vuoto, D indir, E tel, F presente,
        # G vuoto, H vuoto, I data chiamata, J nota, K vuoto (no appt fissati)
        rows_out.append([nome, titolare, "", indir, tel, present, "", "", data_call, nota, ""])

    end_row = START_ROW + len(rows_out) - 1
    rng = f"'{DST_TAB}'!A{START_ROW}:K{end_row}"
    print(f"DRY-RUN — anteprima {len(rows_out)} righe su {rng}\n")
    for r in rows_out:
        print(f"  A={r[0]:<38} | E={r[4]:<12} | F={r[5]:<3} | I={r[8]} | J={r[9][:70]}")

    # check pre-flight
    issues = []
    for r in rows_out:
        if not r[0]: issues.append(f"nome vuoto: {r}")
        if not r[4]: issues.append(f"telefono vuoto: {r[0]}")
        if not r[8]: issues.append(f"data chiamata vuota: {r[0]}")
        if not r[9]: issues.append(f"nota vuota: {r[0]}")
    if issues:
        print("\nERRORI rilevati:")
        for i in issues:
            print(f"  - {i}")
        return
    print("\nNessun errore. Procedere con --send per scrivere su Sebastiano.")

    if "--send" in sys.argv:
        svc.spreadsheets().values().update(
            spreadsheetId=DST_ID, range=rng,
            valueInputOption="USER_ENTERED",
            body={"values": rows_out},
        ).execute()
        print(f"\nOK: scritte righe {START_ROW}-{end_row} sul foglio Sebastiano.")


if __name__ == "__main__":
    main()
