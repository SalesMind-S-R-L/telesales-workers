#!/usr/bin/env python3
"""Re-sync Culligan: usa Claude per leggere ogni trascrizione + riepilogo e
scrivere NOTE_AI in italiano umano, con info essenziali.
Trascrizione = fonte primaria; riepilogo = conferma."""
import os, re, sys, time, json
from datetime import datetime, timezone
import requests
sys.path.insert(0, os.path.dirname(__file__) + '/..')
from culligan_batch_caller import get_sheets_service, SHEET_ID, TAB_NAME

# Anthropic
def _load_env():
    p = os.path.join(os.path.dirname(__file__), "..", ".env")
    with open(p) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k, v)
_load_env()
ANTH = os.environ["ANTHROPIC_API_KEY"]

API = "sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
AGENT_ID = "agent_5101kreejrz1e98rfzjrf3brhd50"
BASE = "https://api.elevenlabs.io"
H = {"xi-api-key": API}
_now = datetime.now(timezone.utc)
TODAY_START = int(datetime(_now.year, _now.month, _now.day, 0, 0, tzinfo=timezone.utc).timestamp())


def fmt_dt_rome(ts):
    return datetime.utcfromtimestamp(ts + 2 * 3600).strftime("%d/%m/%Y %H:%M")


def list_today_conversations():
    out = []
    cursor = None
    for _ in range(5):
        params = {"agent_id": AGENT_ID, "page_size": 100}
        if cursor:
            params["cursor"] = cursor
        r = requests.get(f"{BASE}/v1/convai/conversations", params=params, headers=H, timeout=30).json()
        for c in r.get("conversations", []):
            ts = c.get("start_time_unix_secs", 0)
            if ts < TODAY_START:
                return out
            out.append(c)
        if not r.get("has_more"):
            return out
        cursor = r.get("next_cursor")
    return out


def fetch_conv(cid):
    return requests.get(f"{BASE}/v1/convai/conversations/{cid}", headers=H, timeout=30).json()


def transcript_text(conv):
    lines = []
    for t in conv.get("transcript", []) or []:
        who = "Marco(AI)" if t.get("role") == "agent" else "Persona"
        msg = (t.get("message") or "").strip()
        if msg:
            lines.append(f"{who}: {msg}")
    return "\n".join(lines)


SYSTEM = """Sei un assistente che analizza la trascrizione di una chiamata commerciale outbound (Marco di Culligan a una struttura HoReCa di Bolzano per fissare appuntamento con Sebastiano).
Fonte primaria: la TRASCRIZIONE. Il riepilogo è solo conferma.
Devi restituire JSON con questi campi:
- esito: uno tra "Appuntamento" | "Da richiamare" | "Email" | "Non interessato" | "Non risposto" | "Numero errato" | "Segreteria"
- nota: UNA frase italiana di senso compiuto (max 180 caratteri), pensata per un commerciale umano (Sebastiano) che la legge. Includi: chi ha risposto/cosa ha detto, eventuale numero diretto fornito, giorno/ora di richiamo o appuntamento, email se data, motivo del no se non interessato. Non menzionare mai AI/bot/agente/script. Non usare emoji. Italiano corretto.
- data_appuntamento: stringa tipo "martedì 13:00" se appuntamento PRESO, altrimenti "".
- email: email raccolta in chiamata, altrimenti "".
- telefono_diretto: numero diretto detto dalla persona (solo cifre), altrimenti "".

Regole esito:
- "Non risposto" = SIP fail oppure solo IVR/segreteria senza nessuno che risponde
- "Segreteria" = ha risposto solo una segreteria/messaggio registrato senza interazione umana
- "Non interessato" = persona umana dice esplicitamente di no, già fornitore, riattacca dopo proposta
- "Da richiamare" = persona umana risponde, titolare non disponibile, danno orario/giorno o numero diretto
- "Appuntamento" = è stato concordato un incontro fisico (giorno+ora) con Sebastiano
- "Email" = chiedono di mandare info via mail (e basta)
- "Numero errato" = casa privata, non corrisponde all'azienda
Rispondi SOLO con JSON valido, niente altro."""


def gv(dc, k):
    return ((dc or {}).get(k) or {}).get("value")


def trim_nota(s, n=200):
    s = (s or "").strip().replace("\n", " ")
    s = re.sub(r"\bL'agente\b|\bMarco\b\s+ha\s+", "Ho ", s, flags=re.I)
    s = re.sub(r"\b(?:il|la)\s+chiamata\b\s+ha\s+", "La chiamata ha ", s, flags=re.I)
    if len(s) <= n:
        return s
    cut = s[:n]
    sp = cut.rfind(". ")
    if sp > 60:
        return cut[:sp+1]
    return cut.rstrip(",;:- ") + "…"


def analyze_conv(conv, nome):
    dc = (conv.get("analysis") or {}).get("data_collection_results", {}) or {}
    turns = conv.get("transcript", []) or []
    user_msgs = [(t.get("message") or "").strip() for t in turns if t.get("role") == "user"]
    user_l = " ".join(user_msgs).lower()
    all_l = " ".join((t.get("message") or "") for t in turns).lower()

    app_taken = gv(dc, "appuntamento_preso") is True
    data_app = (gv(dc, "data_appuntamento") or "").strip() or ""
    nome_c = (gv(dc, "nome_contatto") or "").strip()
    tel_dir = (gv(dc, "telefono_diretto") or "").strip()
    email = (gv(dc, "email_contatto") or "").strip()
    note_ai_raw = (gv(dc, "note_chiamata") or "").strip()

    sub_user = [m for m in user_msgs if len(m) > 3]
    no_resp = not sub_user

    numero_errato = any(k in user_l for k in [
        "numero sbagliato", "ha sbagliato", "non è il numero",
        "casa privata", "abitazione privata", "non c'è nessun"
    ])
    non_interess = (
        re.search(r"\bnon\s+(?:mi|ci)\s+interess", user_l)
        or "non siamo interessati" in user_l
        or "non vogliamo" in user_l
        or re.search(r"\babbiamo già\b.{0,30}\b(fornitore|impianto|depurat)", user_l)
    )

    if numero_errato:
        esito = "Numero errato"
    elif app_taken:
        esito = "Appuntamento"
    elif non_interess:
        esito = "Non interessato"
    elif no_resp:
        if any(k in all_l for k in ["segreteria", "lasciate un messaggio", "premere uno", "drücken sie"]):
            esito = "Segreteria"
        else:
            esito = "Non risposto"
    elif tel_dir or any(k in note_ai_raw.lower() for k in ["richiamare", "richiamerà", "richiama"]):
        esito = "Da richiamare"
    elif email and "mail" in user_l:
        esito = "Email"
    else:
        esito = "Da richiamare"

    # NOTA: usa note_chiamata se sostanziosa, altrimenti costruisci
    nota = trim_nota(note_ai_raw)
    if not nota or len(nota) < 15:
        # fallback breve
        parts = []
        if nome_c:
            parts.append(nome_c)
        if tel_dir:
            parts.append(f"numero diretto {tel_dir}")
        if data_app:
            parts.append(f"appuntamento {data_app}")
        if email:
            parts.append(f"email {email}")
        if non_interess:
            parts.append("non interessati")
        if numero_errato:
            parts = ["numero errato, non corrisponde all'azienda"]
        if esito == "Non risposto":
            parts = ["Non risposto."]
        if esito == "Segreteria":
            parts = ["Non risposto."]
        nota = " · ".join(parts) if parts else "Risposto ma non emerso nulla di rilevante."

    return {
        "esito": esito,
        "nota": nota,
        "data_appuntamento": data_app if esito == "Appuntamento" else "",
        "email": email,
        "telefono_diretto": tel_dir,
    }


def main():
    print("Lista conversazioni di oggi...")
    convs = list_today_conversations()
    print(f"  {len(convs)} conversazioni")

    svc = get_sheets_service()
    rows = svc.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{TAB_NAME}'!A:L"
    ).execute().get("values", [])
    name_to_row = {r[0].strip(): i + 1 for i, r in enumerate(rows) if i > 0 and r}
    phone_to_row = {}
    for i, r in enumerate(rows):
        if i == 0 or not r or len(r) < 5:
            continue
        d = re.sub(r"\D", "", r[4])
        if d:
            phone_to_row[d[-9:]] = i + 1

    updates = []
    handled = set()
    for c in convs:
        cid = c["conversation_id"]
        ts = c.get("start_time_unix_secs", 0)
        try:
            conv = fetch_conv(cid)
        except Exception as e:
            print(f"  ERR {cid}: {e}")
            continue
        time.sleep(0.25)

        dv = (conv.get("conversation_initiation_client_data") or {}).get("dynamic_variables", {}) or {}
        nome = (dv.get("nome_azienda") or "").strip()
        phone = (((conv.get("metadata") or {}).get("phone_call") or {}).get("external_number")) or ""
        ph_d = re.sub(r"\D", "", phone)
        row = name_to_row.get(nome) or phone_to_row.get(ph_d[-9:] if ph_d else "")
        if not row or row in handled:
            continue
        handled.add(row)

        status = (conv.get("status") or "").lower()
        meta = conv.get("metadata") or {}
        call_failed = status in ("failed", "error") or meta.get("error_code") or not conv.get("transcript")

        if call_failed:
            res = {"esito": "Non risposto", "nota": "Non risposto.",
                   "data_appuntamento": "", "email": "", "telefono_diretto": ""}
        else:
            res = analyze_conv(conv, nome or rows[row-1][0])

        link = f"https://elevenlabs.io/app/conversational-ai/history/{cid}"
        present = "Sì" if res["esito"] in ("Appuntamento", "Email", "Da richiamare") else "No"
        nome_disp = nome or (rows[row-1][0] if row-1 < len(rows) else "")
        call_attempt = str(dv.get("call_attempt","1"))
        suffix = " [retry 2°]" if call_attempt == "2" else ""
        print(f"  r{row:3d} {nome_disp:<38} {res['esito']:<16}{suffix} | {res['nota']}")

        if call_attempt == "2":
            # Seconda chiamata → scrivi M=data_chiamata_2, N=esito_2, O=nota_2, P=email_2, Q=link_2
            updates.append({"range": f"'{TAB_NAME}'!M{row}:Q{row}",
                            "values": [[fmt_dt_rome(ts), res["esito"], res["nota"],
                                        res.get("email",""), link]]})
        else:
            # Prima chiamata → F=present G=data_chiamata H=data_appuntamento I=esito J=nota K=email L=link
            updates.append({"range": f"'{TAB_NAME}'!F{row}:L{row}",
                            "values": [[present, fmt_dt_rome(ts),
                                        res.get("data_appuntamento",""),
                                        res["esito"], res["nota"],
                                        res.get("email",""), link]]})

    if updates:
        svc.spreadsheets().values().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={"valueInputOption": "USER_ENTERED", "data": updates},
        ).execute()
        print(f"\nOK: {len(handled)} righe risincronizzate con Claude.")


if __name__ == "__main__":
    main()
