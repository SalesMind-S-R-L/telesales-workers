#!/usr/bin/env python3
"""
Check giornaliero dei pool outreach (sola lettura).

MODELLO: pool ESCLUSIVI per canale (deciso 12/06) — ogni azienda sta in UN
solo pool: MASTER (LinkedIn+Email, consulenza) / AI Voice (IT del master +
AI VOICE CODA) / EMAIL COLD / IG CODA B2B.

Segnala:
1. VIOLAZIONI POOL: stessa azienda o stesso dominio presente in piu' pool
2. SEQUENZE DA FERMARE: aziende del pool LinkedIn che hanno risposto ma
   hanno ancora sequenze attive
3. AZIONI DI OGGI: righe master con Data Prossima Azione <= oggi

Uso: python3 outreach/check_collisioni.py
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
SHEET_ID = "1nLvvZ98RLp-ic81Wa8NBNGI0Ig_t8Sl4XIzx7GBnuww"
TAB = "MASTER OUTREACH B2B"

COL = {  # indice 0-based colonne del master
    "azienda": 0, "decisore": 1, "email": 3,
    "stato_email": 10, "data_email": 11,
    "stato_li": 12, "data_li": 13,
    "esito_voice": 14, "data_voice": 15,
    "stato_ig": 16, "data_ig": 17,
    "prossima_azione": 21, "data_prossima": 22,
}

RISPOSTE = {"Risposta", "Call fissata", "Interessato", "Appuntamento"}
ATTIVI_EMAIL = {"Inviata"}
ATTIVI_LI = {"Richiesta inviata", "Msg 1", "Msg 2"}


def get(riga, chiave):
    i = COL[chiave]
    return riga[i].strip() if len(riga) > i and riga[i] else ""


def parse_data(s):
    for fmt in ("%d/%m/%Y", "%d/%m/%Y %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def main():
    creds = Credentials.from_service_account_file(
        str(ROOT / "service-account.json"),
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    s = build("sheets", "v4", credentials=creds)
    righe = s.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{TAB}'!A2:W").execute().get("values", [])

    oggi = datetime.now().date()
    da_fermare, azioni_oggi = [], []

    def dominio(sito):
        return sito.strip().lower().removeprefix("https://").removeprefix(
            "http://").removeprefix("www.").split("/")[0]

    # mappa pool -> {dominio o nome azienda}
    # il canale e' la chiave di confronto: la stessa azienda puo' comparire in
    # piu' tab dello STESSO canale (es. riga master IT + riga AI VOICE CODA)
    NOME_CANALE = {"EMAIL COLD": "Email cold", "AI VOICE CODA": "AI Voice",
                   "IG CODA B2B": "IG"}
    pool = {}
    for r in righe:
        if not r or not get(r, "azienda"):
            continue
        canale = r[19].strip() if len(r) > 19 and r[19] else "LinkedIn"
        chiave = dominio(r[7]) if len(r) > 7 and r[7] else get(r, "azienda").lower()
        pool.setdefault(chiave, set()).add(canale)
    for tab, col_az, col_sito in (("EMAIL COLD", 0, 6), ("AI VOICE CODA", 0, 7), ("IG CODA B2B", 3, 2)):
        try:
            vals = s.spreadsheets().values().get(
                spreadsheetId=SHEET_ID, range=f"'{tab}'!A2:L").execute().get("values", [])
        except Exception:
            continue
        for r in vals:
            if not r or len(r) <= col_az or not r[col_az]:
                continue
            sito = r[col_sito] if len(r) > col_sito else ""
            chiave = dominio(sito) if sito else r[col_az].strip().lower()
            pool.setdefault(chiave, set()).add(NOME_CANALE[tab])
    violazioni = [f"{k}: {', '.join(sorted(v))}" for k, v in pool.items()
                  if len(v) > 1]

    for r in righe:
        if not r or not get(r, "azienda"):
            continue
        nome = get(r, "azienda")
        ha_risposto = (get(r, "stato_email") in RISPOSTE
                       or get(r, "stato_li") in RISPOSTE
                       or get(r, "esito_voice") in RISPOSTE)
        sequenze_attive = (get(r, "stato_email") in ATTIVI_EMAIL
                           or get(r, "stato_li") in ATTIVI_LI)
        if ha_risposto and sequenze_attive:
            da_fermare.append(nome)

        dp = parse_data(get(r, "data_prossima"))
        if dp and dp <= oggi:
            azioni_oggi.append(f"{nome}: {get(r, 'prossima_azione') or 'azione non specificata'}")

    print(f"Master: {len(righe)} righe — check del {oggi.strftime('%d/%m/%Y')}\n")
    sezioni = [
        ("VIOLAZIONI POOL (stessa azienda in piu' canali)", violazioni),
        ("SEQUENZE DA FERMARE (hanno risposto)", da_fermare),
        ("AZIONI DI OGGI", azioni_oggi),
    ]
    for titolo, lista in sezioni:
        print(f"{titolo}: {len(lista)}")
        for x in lista[:30]:
            print(f"  - {x}")
        if len(lista) > 30:
            print(f"  ... e altre {len(lista) - 30}")
        print()


if __name__ == "__main__":
    main()
