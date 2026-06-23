#!/usr/bin/env python3
"""Batch caller per Marco Ferretti — Outreach Telesales.

Legge un CSV o un foglio Google con le colonne:
  nome_azienda, telefono, tipo_numero, nome_decisore, ruolo_decisore, note

E lancia un batch ElevenLabs concurrency=2 con dynamic_variables popolate.
L'agent (agent_5301kpdv4sd9e15vcz4qpm8e7vrn) usa tipo_numero per scegliere il flow:
  - diretto    → va dritto al pitch (cell del decisore)
  - aziendale  → chiede del decisore al centralino

Uso:
  python3 ferretti_outreach_batch.py --csv /path/to/list.csv --dry-run
  python3 ferretti_outreach_batch.py --csv /path/to/list.csv --limit 30 --send
  python3 ferretti_outreach_batch.py --sheet "<sheet_id>" --tab "Foglio1" --limit 30 --send
"""
import argparse, csv, json, re, sys, time
from datetime import datetime
import requests

ELEVENLABS_API_KEY = "sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io"
FERRETTI_AGENT_ID = "agent_5301kpdv4sd9e15vcz4qpm8e7vrn"
FERRETTI_PHONE_ID = "phnum_1501kr3sx76sfxeap503jqy1m7j9"  # +39 055 465 2406
CONCURRENCY = 1
RINGING_TIMEOUT = 45

REQUIRED_COLS = ["nome_azienda", "telefono"]
OPTIONAL_COLS = ["tipo_numero", "nome_decisore", "ruolo_decisore", "angolo_pitch", "note"]

# Mapping header CSV originale → header normalizzato
HEADER_MAP = {
    "nome azienda": "nome_azienda",
    "telefono": "telefono",
    "decisore target": "ruolo_decisore",
    "angolo pitch": "angolo_pitch",
    "settore": "settore",
    "citta": "citta",
    "città": "citta",
    "fatturato": "fatturato",
    "sito": "sito",
    "linkedin": "linkedin",
}


def normalize_phone(raw: str) -> str:
    if not raw: return ""
    cleaned = re.sub(r"[^\d+]", "", raw.strip())
    if not cleaned: return ""
    if cleaned.startswith("+"): return cleaned
    if cleaned.startswith("00"): return "+" + cleaned[2:]
    if cleaned.startswith("39") and len(cleaned) >= 11: return "+" + cleaned
    return "+39" + cleaned


def is_valid_phone(ph: str) -> bool:
    return ph.startswith("+39") and 10 <= len(ph) <= 16


def load_csv(path: str) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            norm = {}
            for k, v in r.items():
                if not k: continue
                key_norm = k.strip().lower()
                key_final = HEADER_MAP.get(key_norm, key_norm.replace(" ", "_"))
                norm[key_final] = (v.strip() if v else "")
            rows.append(norm)
    return rows


def infer_tipo_numero(ph: str) -> str:
    """+393xx = cellulare (probabile diretto); altrimenti fisso (aziendale)."""
    if ph.startswith("+393"):
        return "diretto"
    return "aziendale"


def build_pitch_default(angolo: str, settore: str) -> str:
    if angolo: return angolo
    return "i nostri agenti AI fanno le chiamate, la prequalifica e il follow-up al posto dei tuoi commerciali, in scala"


def load_sheet(sheet_id: str, tab: str) -> list[dict]:
    """Legge da Google Sheet — prima riga = header."""
    sys.path.insert(0, "/Users/simocors/Desktop/telesales")
    from culligan_batch_caller import get_sheets_service
    svc = get_sheets_service()
    data = svc.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=f"'{tab}'!A:Z"
    ).execute().get("values", [])
    if not data: return []
    header = [c.strip().lower() for c in data[0]]
    out = []
    for row in data[1:]:
        row = row + [""] * (len(header) - len(row))
        out.append(dict(zip(header, [c.strip() for c in row])))
    return out


def validate_rows(rows: list[dict]) -> tuple[list[dict], list[str]]:
    ok, issues = [], []
    for i, r in enumerate(rows, 2):
        nome = r.get("nome_azienda", "").strip()
        tel = r.get("telefono", "").strip()
        if not nome:
            issues.append(f"r{i}: nome_azienda vuoto"); continue
        if not tel:
            issues.append(f"r{i}: telefono vuoto ({nome})"); continue
        ph = normalize_phone(tel)
        if not is_valid_phone(ph):
            issues.append(f"r{i}: telefono non valido '{tel}' → '{ph}' ({nome})"); continue
        tipo_raw = r.get("tipo_numero", "").strip().lower()
        if tipo_raw in ("diretto", "aziendale"):
            tipo = tipo_raw
        else:
            tipo = infer_tipo_numero(ph)  # auto-detect
        r["_phone"] = ph
        r["_tipo"] = tipo
        ok.append(r)
    return ok, issues




def ruolo_ita(raw: str) -> str:
    """Traduce ruoli LinkedIn inglesi in italiano breve e pronunciabile."""
    r = (raw or "").lower()
    if any(k in r for k in ("owner", "founder", "fondatore", "titolare")):
        return "titolare"
    if "amministratore" in r:
        return "amministratore delegato" if "delegat" in r else "amministratore"
    if any(k in r for k in ("chief executive", "ceo", "managing director", "general manager", "direttore generale")):
        return "amministratore delegato"
    if any(k in r for k in ("chief operating", "coo", "operations")):
        return "direttore operativo"
    if any(k in r for k in ("chief technology", "cto", "chief information")):
        return "responsabile tecnico"
    if any(k in r for k in ("chief financial", "cfo")):
        return "responsabile amministrativo"
    if any(k in r for k in ("chief marketing", "cmo", "marketing")):
        return "responsabile marketing"
    if any(k in r for k in ("chief commercial", "sales", "commerciale", "revenue")):
        return "responsabile commerciale"
    if "president" in r or "presidente" in r:
        return "presidente"
    if "partner" in r or "socio" in r:
        return "socio"
    if "direttore" in r:
        return "direttore"
    return "titolare"

def build_recipient(r: dict) -> dict:
    angolo = r.get("angolo_pitch", "").strip()
    settore = r.get("settore", "").strip()
    return {
        "phone_number": r["_phone"],
        "conversation_initiation_client_data": {
            "dynamic_variables": {
                "nome_azienda": r.get("nome_azienda", ""),
                "tipo_numero": r["_tipo"],
                "nome_decisore": r.get("nome_decisore", ""),
                "ruolo_decisore": ruolo_ita(r.get("ruolo_decisore", "")),
                "angolo_pitch": build_pitch_default(angolo, settore),
                "settore": settore,
                "citta": r.get("citta", ""),
            }
        }
    }


def submit_batch(name: str, recipients: list) -> dict:
    payload = {
        "call_name": name,
        "agent_id": FERRETTI_AGENT_ID,
        "agent_phone_number_id": FERRETTI_PHONE_ID,
        "recipients": recipients,
        "target_concurrency_limit": CONCURRENCY,
        "telephony_call_config": {"ringing_timeout_secs": RINGING_TIMEOUT},
    }
    resp = requests.post(
        f"{ELEVENLABS_BASE_URL}/v1/convai/batch-calling/submit",
        headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"},
        json=payload, timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--csv", help="path CSV con header: nome_azienda,telefono,tipo_numero,nome_decisore,ruolo_decisore,note")
    src.add_argument("--sheet", help="Google Sheet ID")
    ap.add_argument("--tab", default="Foglio1", help="tab name (con --sheet)")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--send", action="store_true", help="invio reale (altrimenti dry-run)")
    args = ap.parse_args()

    rows = load_csv(args.csv) if args.csv else load_sheet(args.sheet, args.tab)
    print(f"Letti {len(rows)} righe dalla sorgente.")
    if not rows: return

    ok, issues = validate_rows(rows)
    print(f"Valide: {len(ok)} · Scartate: {len(issues)}")
    for issue in issues[:20]:
        print(f"  ⚠ {issue}")
    if len(issues) > 20:
        print(f"  ... e altri {len(issues)-20}")

    selected = ok[: args.limit]
    print(f"\nAnteprima {len(selected)} candidati (limit={args.limit}):")
    for r in selected:
        print(f"  [{r['_tipo']:<9}] {r['nome_azienda'][:34]:<34} | {r['_phone']:<14} | decisore: {r.get('nome_decisore','-')[:20]:<20} | ruolo: {r.get('ruolo_decisore','-')}")

    if not args.send:
        print("\nDry-run. Lancia con --send per inviare il batch.")
        return

    name = f"Ferretti-Outreach-{datetime.now().strftime('%Y%m%d-%H%M')}"
    recipients = [build_recipient(r) for r in selected]
    print(f"\nSubmit batch '{name}' (concurrency={CONCURRENCY}, ringing_timeout={RINGING_TIMEOUT}s)")
    res = submit_batch(name, recipients)
    batch_id = res.get("batch_call_id", res.get("id", "?"))
    print(f"Batch ID: {batch_id}")
    print(f"Monitora: https://elevenlabs.io/app/conversational-ai/batch-calling")


if __name__ == "__main__":
    main()
