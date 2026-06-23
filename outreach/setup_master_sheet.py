#!/usr/bin/env python3
"""
Crea (o aggiorna) il tab MASTER OUTREACH B2B nel foglio pipeline_opportunita.

Una riga per azienda della lista LEAD_B2B_TELESALES_FINALE.csv, colonne di
stato per canale (Email, LinkedIn, AI Voice, Instagram) con dropdown chiusi.
Le colonne Hook e Variante vengono riempite da schede_contesto.csv se presente.

Riesegubile: aggiunge solo le aziende non ancora presenti (match per email).
"""

from __future__ import annotations

import csv
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
SA_PATH = ROOT / "service-account.json"
SHEET_ID = "1nLvvZ98RLp-ic81Wa8NBNGI0Ig_t8Sl4XIzx7GBnuww"  # pipeline_opportunita
TAB = "MASTER OUTREACH B2B"
LISTA = ROOT / "prospecting_b2b" / "LEAD_B2B_TELESALES_FINALE.csv"
SCHEDE = ROOT / "outreach" / "schede_contesto.csv"

HEADER = [
    "Azienda", "Decisore", "Ruolo", "Email", "Telefono", "Citta", "Settore",
    "Sito", "Hook", "Variante Email", "Stato Email", "Data Email",
    "Stato LinkedIn", "Data LinkedIn", "Esito AI Voice", "Data AI Voice",
    "Stato IG", "Data IG", "Note",
    "Canale Primario", "Verticale", "Prossima Azione", "Data Prossima Azione",
]

DROPDOWNS = {
    9:  ["A", "B"],                                                        # J Variante Email
    10: ["Da inviare", "Inviata", "Risposta", "Call fissata", "Non interessato"],   # K Stato Email
    12: ["Da contattare", "Richiesta inviata", "Msg 1", "Msg 2", "Risposta",
         "Email follow-up", "Non interessato"],                            # M Stato LinkedIn
    14: ["Da chiamare", "Non risposto", "Da richiamare", "Interessato",
         "Appuntamento", "Non interessato"],                               # O Esito AI Voice
    16: ["Da contattare", "DM inviato", "Risposta", "Non interessato"],    # Q Stato IG
    19: ["LinkedIn", "Email", "AI Voice", "IG"],                           # T Canale Primario
    20: ["Consulenza", "IT", "Altro"],                                     # U Verticale
}

KPI_TAB = "KPI OUTREACH"
KPI_HEADER = [
    "Settimana", "Canale", "Invii", "Risposte", "Reply %",
    "Call fissate", "Show", "Note",
]


def svc():
    creds = Credentials.from_service_account_file(
        str(SA_PATH), scopes=["https://www.googleapis.com/auth/spreadsheets"])
    return build("sheets", "v4", credentials=creds)


def estendi_coordinamento(s, tab_id):
    """Aggiunge/aggiorna le colonne T-W (Canale Primario, Verticale,
    Prossima Azione, Data Prossima Azione) e i relativi dropdown."""
    meta = s.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    ncols = next(sh["properties"]["gridProperties"]["columnCount"]
                 for sh in meta["sheets"] if sh["properties"]["sheetId"] == tab_id)
    if ncols < len(HEADER):
        s.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={"requests": [
            {"appendDimension": {"sheetId": tab_id, "dimension": "COLUMNS",
                                 "length": len(HEADER) - ncols}}]}).execute()

    intest = s.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{TAB}'!T1:W1").execute().get("values", [[]])
    if not intest or intest[0][:1] != ["Canale Primario"]:
        s.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f"'{TAB}'!T1",
            valueInputOption="RAW",
            body={"values": [HEADER[19:]]}).execute()
        s.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={"requests": [
            {"repeatCell": {
                "range": {"sheetId": tab_id, "startRowIndex": 0, "endRowIndex": 1,
                          "startColumnIndex": 19, "endColumnIndex": 23},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True},
                    "backgroundColor": {"red": 0.85, "green": 0.88, "blue": 0.95}}},
                "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
        ] + [
            {"setDataValidation": {
                "range": {"sheetId": tab_id, "startRowIndex": 1, "endRowIndex": 300,
                          "startColumnIndex": col, "endColumnIndex": col + 1},
                "rule": {"condition": {"type": "ONE_OF_LIST",
                                       "values": [{"userEnteredValue": v} for v in vals]},
                         "strict": True, "showCustomUi": True}}}
            for col, vals in DROPDOWNS.items() if col >= 19
        ]}).execute()
        print("Colonne coordinamento T-W aggiunte.")

    # Compila Canale Primario e Verticale dove vuoti
    dati = s.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{TAB}'!A2:U").execute().get("values", [])
    aggiornamenti = []
    for i, r in enumerate(dati, start=2):
        if not r or not r[0]:
            continue
        settore = r[6] if len(r) > 6 else ""
        canale = r[19] if len(r) > 19 else ""
        vertic = r[20] if len(r) > 20 else ""
        if not canale or not vertic:
            v = "Consulenza" if "onsulenza" in settore else ("IT" if "IT" in settore else "Altro")
            aggiornamenti.append({
                "range": f"'{TAB}'!T{i}:U{i}",
                "values": [[canale or "LinkedIn", vertic or v]],
            })
    if aggiornamenti:
        s.spreadsheets().values().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={"valueInputOption": "RAW", "data": aggiornamenti}).execute()
        print(f"Canale Primario/Verticale compilati su {len(aggiornamenti)} righe.")


def crea_tab_kpi(s, tabs):
    if KPI_TAB in tabs:
        return
    resp = s.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={
        "requests": [{"addSheet": {"properties": {
            "title": KPI_TAB,
            "gridProperties": {"rowCount": 200, "columnCount": len(KPI_HEADER),
                               "frozenRowCount": 1}}}}]
    }).execute()
    kpi_id = resp["replies"][0]["addSheet"]["properties"]["sheetId"]
    s.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=f"'{KPI_TAB}'!A1",
        valueInputOption="RAW", body={"values": [KPI_HEADER]}).execute()
    s.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={"requests": [
        {"repeatCell": {
            "range": {"sheetId": kpi_id, "startRowIndex": 0, "endRowIndex": 1},
            "cell": {"userEnteredFormat": {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.85, "green": 0.95, "blue": 0.85}}},
            "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
        {"setDataValidation": {
            "range": {"sheetId": kpi_id, "startRowIndex": 1, "endRowIndex": 200,
                      "startColumnIndex": 1, "endColumnIndex": 2},
            "rule": {"condition": {"type": "ONE_OF_LIST",
                                   "values": [{"userEnteredValue": v} for v in
                                              ["Email", "LinkedIn", "AI Voice", "IG", "Instantly"]]},
                     "strict": True, "showCustomUi": True}}},
    ]}).execute()
    print(f"Tab '{KPI_TAB}' creato.")


def main():
    s = svc()
    meta = s.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    tabs = {sh["properties"]["title"]: sh["properties"]["sheetId"] for sh in meta["sheets"]}

    if TAB not in tabs:
        resp = s.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={
            "requests": [{"addSheet": {"properties": {
                "title": TAB, "gridProperties": {"rowCount": 300, "columnCount": len(HEADER), "frozenRowCount": 1}}}}]
        }).execute()
        tab_id = resp["replies"][0]["addSheet"]["properties"]["sheetId"]
        s.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f"'{TAB}'!A1",
            valueInputOption="RAW", body={"values": [HEADER]}).execute()
        # header bold + sfondo
        s.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={"requests": [
            {"repeatCell": {
                "range": {"sheetId": tab_id, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {"userEnteredFormat": {
                    "textFormat": {"bold": True},
                    "backgroundColor": {"red": 0.85, "green": 0.88, "blue": 0.95}}},
                "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
        ] + [
            {"setDataValidation": {
                "range": {"sheetId": tab_id, "startRowIndex": 1, "endRowIndex": 300,
                          "startColumnIndex": col, "endColumnIndex": col + 1},
                "rule": {"condition": {"type": "ONE_OF_LIST",
                                       "values": [{"userEnteredValue": v} for v in vals]},
                         "strict": True, "showCustomUi": True}}}
            for col, vals in DROPDOWNS.items()
        ]}).execute()
        print(f"Tab '{TAB}' creato.")
    else:
        tab_id = tabs[TAB]
        print(f"Tab '{TAB}' gia' esistente, aggiungo solo righe nuove.")

    estendi_coordinamento(s, tab_id)
    crea_tab_kpi(s, tabs)

    esistenti = s.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{TAB}'!D2:D").execute().get("values", [])
    email_presenti = {r[0].strip().lower() for r in esistenti if r}

    schede = {}
    if SCHEDE.exists():
        with open(SCHEDE, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                schede[r["email"].strip().lower()] = r

    righe = []
    with open(LISTA, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            em = r["email"].strip().lower()
            if em in email_presenti:
                continue
            email_presenti.add(em)  # dedup anche dentro la lista stessa
            sc = schede.get(em, {})
            righe.append([
                r["nome_azienda"], r["nome_decisore"], r["ruolo_decisore"],
                r["email"], r["telefono"], r.get("citta", ""), r["settore"],
                r["website"], sc.get("hook", ""), sc.get("variante_email", ""),
                "Da inviare", "", "Da contattare", "", "Da chiamare", "",
                "Da contattare", "", "",
            ])

    if righe:
        s.spreadsheets().values().append(
            spreadsheetId=SHEET_ID, range=f"'{TAB}'!A1",
            valueInputOption="RAW", insertDataOption="INSERT_ROWS",
            body={"values": righe}).execute()
    print(f"Aggiunte {len(righe)} aziende. Totale nel tab: {len(email_presenti)}.")


if __name__ == "__main__":
    main()
