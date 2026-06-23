#!/usr/bin/env python3
"""Riscrive correttamente righe 146-180 sul foglio Sebastiano usando la
struttura colonne reale: A=nome, B=titolare, D=indirizzo, E=tel, F=presente,
I=data chiamata, J=note, K=data appuntamento.
Sovrascrive le righe mappate male precedentemente (no delete)."""
import re, sys
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import get_sheets_service

SRC_ID = "1PiezlYSd5TZNBCRTvzBhx_yVCGfN6aMI3PXdOYU4xu8"
SRC_TAB = "aziende_bolzano_VERIFICATE"
DST_ID = "1KsbFkAhJQDd2edYuKgbVC0yd87jK-Y6egKU254Y1wT0"
DST_TAB = "Foglio1"
START_ROW = 146  # prima riga libera dopo le 145 esistenti

ROW_DATA = {
    2:  ("",                       "non interessati, linea disturbata"),
    3:  ("Nicole (reception)",     "inviare email bolzano@hotellbb.com, Nicole la gira a direzione"),
    4:  ("",                       "audio disturbato, riprovare"),
    5:  ("",                       "non risp"),
    6:  ("",                       "risposto centro Bosen (inoltro?), audio interrotto, verificare numero"),
    7:  ("",                       "inviare email a direzione (indirizzo da verificare)"),
    8:  ("",                       "non risp, solo IVR multilingue"),
    9:  ("",                       "non risp, linee occupate"),
    10: ("",                       "risposto ma chiamata interrotta, riprovare"),
    11: ("",                       "titolare fuori, richiamare domani mattina verso le 9 al fisso"),
    12: ("",                       "richiamare oggi 19/05 alle 9:30 al fisso, dipendente non ha capito proposta visita"),
    13: ("",                       "titolare orari irregolari, ha detto sì generico settimana prossima senza giorno - richiamare per fissare"),
    14: ("",                       "inviare email info@hotelasterixbz.com, titolare non disponibile"),
    15: ("",                       "risposto solo 'potrebbe essere', richiamare per qualificare"),
    16: ("",                       "inviare email info@hotelfiera.it, bassa priorità - non usano acqua/ghiaccio/no bar"),
    17: ("Stefani (gestione)",     "non interessati, hotel senza ristorante"),
    18: ("",                       "solo frasi confuse, chiamata interrotta, riprovare"),
    19: ("",                       "non risp (SIP fail)"),
    20: ("",                       "non risp (SIP fail)"),
    22: ("",                       "inviare email info@lumhotel.com, raggiungibili solo via mail"),
    23: ("",                       "inviare email info@magdalenerhof.it, ristorante chiuso, titolare dall'estero senza orari fissi"),
    24: ("",                       "risposta automatica multilingue, nessuna interazione, riprovare"),
    25: ("",                       "problemi audio, contatto ha chiesto di essere richiamato"),
    26: ("Luca Röhl",              "ok appuntamento martedì 19/05 ore 13 con Luca Röhl, madre lo informa"),
    27: ("Federico (reception)",   "risposto Federico reception, titolare non raggiunto, richiamare"),
    28: ("",                       "conversazione interrotta dopo poche parole, riprovare"),
    29: ("",                       "capo rientra stasera 19:00 o domani 9:30, no cellulare, richiamare al fisso"),
    31: ("",                       "non risp (SIP fail)"),
    32: ("",                       "non risp (SIP fail)"),
    33: ("",                       "non interessati, hanno frainteso pensando fosse prenotazione tavolo"),
    34: ("",                       "titolare assente, richiamare mercoledì"),
    35: ("",                       "non risp (SIP fail)"),
    36: ("",                       "titolare non disponibile, conversazione interrotta, riprovare"),
    37: ("",                       "non risp (SIP fail)"),
    38: ("",                       "non risp (SIP fail)"),
}

DATA_APP_K = {26: "19/05/26 ore 13:00"}
PRESENT_ESITI = {"Appuntamento", "Email", "Da richiamare"}


def clean_phone(s):
    return re.sub(r"[^\d]", "", s or "")


def fmt_date(s):
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
        data_call = fmt_date(r[6])
        data_app = DATA_APP_K.get(row_idx, "")
        # 11 elementi: A=nome B=titolare C=(vuoto) D=indirizzo E=tel F=presente
        # G=(vuoto) H=(vuoto) I=data_chiamata J=nota K=data_appuntamento
        rows_out.append([nome, titolare, "", indir, tel, present, "", "", data_call, nota, data_app])

    end_row = START_ROW + len(rows_out) - 1
    rng = f"'{DST_TAB}'!A{START_ROW}:K{end_row}"
    print(f"Scrittura su {rng} ({len(rows_out)} righe)\n")
    for r in rows_out:
        print(f"  A={r[0]:<35} | E={r[4]:<12} | F={r[5]:<3} | I={r[8]} | J={r[9][:60]}")

    svc.spreadsheets().values().update(
        spreadsheetId=DST_ID, range=rng,
        valueInputOption="USER_ENTERED",
        body={"values": rows_out},
    ).execute()
    print(f"\nSovrascritte righe {START_ROW}-{end_row} sul foglio Sebastiano con colonne corrette.")


if __name__ == "__main__":
    main()
