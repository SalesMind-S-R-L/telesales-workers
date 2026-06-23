#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Riversa la lista Look (prospects.json) nel NOSTRO foglio Google, tab "CHIAMATE",
nel layout che il caller (look_batch_caller.py) legge.

PREREQUISITO: crea un Google Sheet (anche una copia del Master) e condividilo in
MODIFICA con il service account:  claude-sheets@claude-telesales.iam.gserviceaccount.com
Poi:
    LOOK_SHEET_ID=<id_del_foglio> python3 look/look_push_to_sheet.py
oppure:
    python3 look/look_push_to_sheet.py <id_del_foglio>

Telefoni scritti in formato nazionale (testo), niente +39 (lo normalizza il caller).
"""
import os, re, sys, json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SA_PATH = os.path.join(ROOT, "service-account.json")
PROSPECTS = os.path.join(ROOT, "look", "prospects.json")
TAB = "CHIAMATE"

SHEET_ID = (sys.argv[1] if len(sys.argv) > 1 else os.getenv("LOOK_SHEET_ID", "")).strip()
if not SHEET_ID:
    raise SystemExit("Passa l'ID del foglio (arg o LOOK_SHEET_ID). Il foglio va condiviso col SA "
                     "claude-sheets@claude-telesales.iam.gserviceaccount.com")

def verde_of(r):
    d = re.sub(r"[^0-9]", "", str(r.get("numero_verde", "")))
    if len(d) >= 8:
        return r.get("numero_verde", "")
    m = re.search(r"800[\s\.]?\d[\d\s\.]{4,}", r.get("evidenza", "") or "")
    return m.group(0).strip() if m else ""

def prio_key(r):
    inv = r.get("investimento", "Medio")
    nuovo = bool((r.get("nuovo_investimento") or "").strip())
    return 0 if (inv == "Alto" and nuovo) else (1 if (inv == "Alto" or nuovo) else 2)

m = json.load(open(PROSPECTS, encoding="utf-8"))
m.sort(key=lambda r: (prio_key(r), r.get("settore", ""), r.get("azienda", "")))

header = ["Azienda", "Settore", "Citta", "Numero verde", "Ruolo decisore",
          "Titolare (nome)", "Resp. acquisti (nome)", "Telefono centralino", "Telefono diretto",
          "Esito", "Note", "Appuntamento (data/ora)", "Data chiamata", "Conversation ID"]
rows = [header]
for r in m:
    rows.append([
        r.get("azienda", ""), r.get("settore", ""), r.get("sede", ""), verde_of(r),
        r.get("decision_maker", ""), r.get("titolare_nome", ""), r.get("acquisti_nome", ""),
        r.get("telefono_centralino", ""), r.get("telefono_diretto", ""),
        "Da contattare", "", "", "", "",
    ])

creds = Credentials.from_service_account_file(SA_PATH, scopes=["https://www.googleapis.com/auth/spreadsheets"])
svc = build("sheets", "v4", credentials=creds)

# assicura il tab CHIAMATE
meta = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
tabs = [s["properties"]["title"] for s in meta["sheets"]]
if TAB not in tabs:
    svc.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID,
        body={"requests": [{"addSheet": {"properties": {"title": TAB}}}]}).execute()

svc.spreadsheets().values().clear(spreadsheetId=SHEET_ID, range=f"'{TAB}'!A:N").execute()
svc.spreadsheets().values().update(
    spreadsheetId=SHEET_ID, range=f"'{TAB}'!A1",
    valueInputOption="RAW", body={"values": rows}).execute()
# header grassetto
sid = next(s["properties"]["sheetId"] for s in svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()["sheets"] if s["properties"]["title"] == TAB)
svc.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={"requests": [
    {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1},
     "cell": {"userEnteredFormat": {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.12, "green": 0.22, "blue": 0.39}, "horizontalAlignment": "CENTER"}},
     "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"}},
    {"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 1}}, "fields": "gridProperties.frozenRowCount"}},
]}).execute()

print(f"OK: scritte {len(rows)-1} aziende nel tab '{TAB}' del foglio {SHEET_ID}")
print(f"URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
