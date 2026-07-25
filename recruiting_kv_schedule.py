#!/usr/bin/env python3
"""SCHEDULE CLOUD (GitHub Action, mattina): seleziona candidati VERI da KV, li riserva e
programma il batch del giorno su ElevenLabs. Gira 24/7 nel cloud, indipendente dal Mac.

Regole: solo mai-contattati; mai Brollo/Karima; SOLO candidati veri (cellulare +393, no aziende
PagineGialle); esclude qualificati/riservati/gia chiamati; concorrenza 2 (trunk condiviso);
slot 11:00 Europe/Rome (fascia poco affollata).

Env (secret GitHub): ELEVENLABS_API_KEY, CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID."""
import os, re, json, requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import recruiting_auto as R

TZ = ZoneInfo("Europe/Rome")
BATCH_SIZE = int(os.environ.get("RUN_SIZE") or 20)
CONCURRENCY = 2
SLOT_HOUR = int(os.environ.get("RUN_SLOT_HOUR") or 11)
SAME_DAY = os.environ.get("RUN_SAME_DAY") == "1"   # consente di schedulare OGGI (anche weekend)
NS = "de8093d84a674862b18e6fda6f3b56fa"
ACCT = os.environ["CLOUDFLARE_ACCOUNT_ID"]
CFH = {"Authorization": f"Bearer {os.environ['CLOUDFLARE_API_TOKEN']}"}
KV = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/storage/kv/namespaces/{NS}/values"

EXCL = re.compile(r"d['’` ]?ignaz|cordeiro|patric", re.I)
BIZ = re.compile(r"paginegialle|call.?center", re.I)
COMPANY = re.compile(r"\b(s\.?r\.?l\.?s?|s\.?p\.?a|srls|s\.?a\.?s|snc|group|media|contact|call|telemarketing|academy|agenzia|servizi|solutions|consulting)\b", re.I)


def kv_get(k):
    r = requests.get(f"{KV}/{k}", headers=CFH, timeout=30); return r.text if r.status_code == 200 else None

def kv_put(k, v):
    requests.put(f"{KV}/{k}", headers=CFH, data=v.encode("utf-8"), timeout=30).raise_for_status()

def e164(p):
    p = re.sub(r"[^\d+]", "", p or "")
    if p.startswith("0039"): p = "+39" + p[4:]
    if p.startswith("39") and len(p) >= 11: p = "+" + p
    if not p.startswith("+") and 9 <= len(p) <= 10: p = "+39" + p
    return p if re.match(r"^\+393\d{8,9}$", p) else None

def is_business(r):
    return bool(BIZ.search(r.get("source_app") or "") or BIZ.search(r.get("role") or "") or COMPANY.search(r.get("name") or ""))


def main():
    R.H = {"xi-api-key": R.key(), "Content-Type": "application/json"}
    raw = kv_get("recruiting_candidates")
    if not raw:
        R.log("KV vuoto, nulla da schedulare."); return
    data = json.loads(raw)
    # slot: oggi 11:00 se futuro, altrimenti prossimo giorno lavorativo
    now = datetime.now(TZ)
    if SAME_DAY:
        when = now.replace(hour=SLOT_HOUR, minute=0, second=0, microsecond=0)
        if when <= now:  # slot gia' passato: metti fra ~15 min
            when = now + timedelta(minutes=15)
    else:
        day = now
        if now.hour >= SLOT_HOUR - 1:
            day = now + timedelta(days=1)
        while day.weekday() >= 5:
            day = day + timedelta(days=1)
        when = day.replace(hour=SLOT_HOUR, minute=0, second=0, microsecond=0)
    # seleziona candidati veri freschi
    fresh = []
    for r in data:
        if R.blocked(r) or r.get("do_not_call") or r.get("has_phone") != "YES": continue
        if (r.get("outreach_canale") or "") or (r.get("outreach_owner") or ""): continue
        if (r.get("status") or "") != "da_contattare" or R.cls(r) == "SCARTATO": continue
        if EXCL.search(r.get("name") or "") or int(r.get("hr_priority") or 0) >= 4: continue
        if is_business(r): continue
        ph = e164(r.get("phone"))
        if not ph: continue
        r["_ph"] = ph; fresh.append(r)
    fresh.sort(key=lambda r: (0 if R.cls(r) == "A" else 1, -(r.get("hr_score") or 0)))
    chosen = fresh[:BATCH_SIZE]
    if not chosen:
        R.log("Nessun candidato vero disponibile: pipeline esaurita, serve nuovo sourcing."); return
    R.log(f"Schedulo {len(chosen)} candidati per {when:%d/%m %H:00}.")
    # riserva su KV
    dl = f"{now:%Y-%m-%d}"
    for r in chosen:
        r["outreach_owner"] = "AI Voice"
        r["phone"] = r["_ph"]
        old = (r.get("notes") or "").strip()
        r["notes"] = f"[schedulato AI {when:%d/%m %H:00}]." + (f" | {old}" if old else "")
    for r in data:
        r.pop("_ph", None)
    kv_put("recruiting_candidates", json.dumps(data, ensure_ascii=False))
    # submit batch Eleven
    recips = [{"phone_number": r["phone"], "conversation_initiation_client_data": {"dynamic_variables": {
        "nome_candidato": R.first_name(r), "fonte": (r.get("source_app") or "database recruiting"),
        "annuncio": R.ANNUNCIO, "note": (r.get("notes") or "")[:180]}}} for r in chosen]
    resp = R.api("POST", "/v1/convai/batch-calling/submit", json={
        "call_name": f"Recruiting AUTO {when:%d/%m %H:00}", "agent_id": R.AGENT,
        "agent_phone_number_id": R.PHONE, "recipients": recips,
        "target_concurrency_limit": CONCURRENCY, "scheduled_time_unix": int(when.timestamp()),
        "telephony_call_config": {"ringing_timeout_secs": 60}})
    R.log(f"Batch schedulato: {resp.get('id')} ({len(chosen)} cand., conc {CONCURRENCY}) status={resp.get('status')}")


if __name__ == "__main__":
    main()
