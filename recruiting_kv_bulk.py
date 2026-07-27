#!/usr/bin/env python3
"""BULK (GitHub Action): programma TUTTI i candidati veri liberi su piu' slot di oggi+domani,
concorrenza 2, fasce 09-12/15-18, evitando il 18:00 affollato. Riserva su KV, submit su Eleven.

Env: ELEVENLABS_API_KEY, CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID."""
import os, re, json, requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import recruiting_auto as R

TZ = ZoneInfo("Europe/Rome")
CONCURRENCY = 2
PER_SLOT = 25
# slot per OGGI (ore) e DOMANI (ore) - fasce 09-12 / 15-18, no 18:00, distanziati
SLOTS_TODAY = [15, 17]
SLOTS_TMRW = [9, 10, 15, 17]

NS = "de8093d84a674862b18e6fda6f3b56fa"
ACCT = os.environ["CLOUDFLARE_ACCOUNT_ID"]
CFH = {"Authorization": f"Bearer {os.environ['CLOUDFLARE_API_TOKEN']}"}
KV = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/storage/kv/namespaces/{NS}/values"

EXCL = re.compile(r"d['’` ]?ignaz|cordeiro|patric", re.I)
SOC = re.compile(r"\b(s\.?r\.?l\.?s?|s\.?p\.?a|s\.?n\.?c|s\.?a\.?s|societa|cooperativa|sagl)\b", re.I)
ANON = re.compile(r"operatore|call.?center|centro assistenza|^\(", re.I)


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

def is_company(r):
    n = r.get("name") or ""
    return bool(SOC.search(n) or ANON.search(n))


def build_slots(now):
    slots = []
    for h in SLOTS_TODAY:
        t = now.replace(hour=h, minute=0, second=0, microsecond=0)
        if t > now + timedelta(minutes=10):
            slots.append(t)
    tmrw = now + timedelta(days=1)
    for h in SLOTS_TMRW:
        slots.append(tmrw.replace(hour=h, minute=0, second=0, microsecond=0))
    return slots


def main():
    R.H = {"xi-api-key": R.key(), "Content-Type": "application/json"}
    data = json.loads(kv_get("recruiting_candidates") or "[]")
    # candidati VERI liberi (cellulare, nome persona, mai chiamati, non riservati)
    fresh = []
    for r in data:
        if R.blocked(r) or r.get("do_not_call") or r.get("has_phone") != "YES": continue
        if (r.get("outreach_canale") or "") or (r.get("outreach_owner") or ""): continue
        if (r.get("status") or "") != "da_contattare": continue
        if EXCL.search(r.get("name") or "") or int(r.get("hr_priority") or 0) >= 4: continue
        if is_company(r): continue
        ph = e164(r.get("phone"))
        if not ph: continue
        r["_ph"] = ph; fresh.append(r)
    fresh.sort(key=lambda r: (0 if R.cls(r) == "A" else 1, -(r.get("hr_score") or 0)))
    R.log(f"Candidati veri liberi: {len(fresh)}")
    if not fresh:
        R.log("Nessuno da schedulare."); return

    now = datetime.now(TZ)
    slots = build_slots(now)
    R.log(f"Slot disponibili: {[s.strftime('%d/%m %H:00') for s in slots]}")
    i = 0; scheduled = []
    for slot in slots:
        chunk = fresh[i:i + PER_SLOT]
        if not chunk: break
        i += len(chunk)
        for r in chunk:
            r["outreach_owner"] = "AI Voice"; r["phone"] = r["_ph"]
            old = (r.get("notes") or "").strip()
            r["notes"] = f"[schedulato AI {slot:%d/%m %H:00}]." + (f" | {old}" if old else "")
        recips = [{"phone_number": r["phone"], "conversation_initiation_client_data": {"dynamic_variables": {
            "nome_candidato": R.first_name(r), "fonte": (r.get("source_app") or "database recruiting"),
            "annuncio": R.ANNUNCIO, "note": (r.get("notes") or "")[:180]}}} for r in chunk]
        resp = R.api("POST", "/v1/convai/batch-calling/submit", json={
            "call_name": f"Recruiting BULK {slot:%d/%m %H:00}", "agent_id": R.AGENT,
            "agent_phone_number_id": R.PHONE, "recipients": recips,
            "target_concurrency_limit": CONCURRENCY, "scheduled_time_unix": int(slot.timestamp()),
            "telephony_call_config": {"ringing_timeout_secs": 60}})
        scheduled.append((slot.strftime("%d/%m %H:00"), len(chunk), resp.get("id")))
        R.log(f"  {slot:%d/%m %H:00}: {len(chunk)} candidati -> {resp.get('id')}")
    for r in data:
        r.pop("_ph", None)
    kv_put("recruiting_candidates", json.dumps(data, ensure_ascii=False))
    tot = sum(n for _, n, _ in scheduled)
    R.log(f"BULK FATTO: {tot} candidati su {len(scheduled)} slot. Rimasti non schedulati: {len(fresh) - i}")


if __name__ == "__main__":
    main()
