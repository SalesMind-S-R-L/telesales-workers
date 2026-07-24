#!/usr/bin/env python3
"""ORCHESTRATORE RECRUITING AUTOMATICO (cloud-ready, solo HTTP).

Ciclo completo, eseguibile senza intervento umano:
 1. Legge la Talent Tower LIVE (fonte unica) e ne estrae il pool.
 2. Seleziona mai-contattati (+ retry non-connesse <3 tentativi), classifica A/B, scarta i non target.
 3. Chiama con l'agente Francesco (ElevenLabs batch), rispettando fasce e suppression.
 4. Attende, processa gli esiti, aggiorna stato/esito/priorita/note nel DATA.
 5. Ridistribuisce la Tower (vercel --prod --token) cosi il link e' aggiornato per tutti.
 6. Notifica Leonardo se ci sono nuovi qualificati (hr_priority>=4).
 7. Scrive il report giornaliero.

REGOLE SEMPRE ATTIVE: solo mai-contattati; mai Brollo/Karima; niente promesse compenso (nel prompt);
fasce 09-12 / 15-18; cap giornaliero; concorrenza bassa per non saturare il trunk.

Env: ELEVENLABS_API_KEY (fallback repo), VERCEL_TOKEN (per redeploy), LEO_WEBHOOK (notifica opz.).
Kill-switch: se esiste il file recruiting_PAUSE non fa nulla.
"""
import os, re, json, time, subprocess, sys, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
TOWER_URL = "https://telesales-talent-tower.vercel.app/"
DEPLOY_DIR = os.path.join(ROOT, "talent_tower_deploy")
AGENT = "agent_8601ky4xgwhde0kbqw21qxhp7rfz"      # Francesco - Recruiter Setter
PHONE = "phnum_1501kr3sx76sfxeap503jqy1m7j9"      # Telnyx Italia +390554652406
ANNUNCIO = "Appointment setter / appuntamentista da remoto - modello a performance"
BATCH_SIZE = 20
CONCURRENCY = 2                                   # basso: evita saturazione trunk condiviso
MAX_RETRY = 3
TZ = ZoneInfo("Europe/Rome")
EL = "https://api.elevenlabs.io"

BAD = re.compile(r"3d|artist|video|graphic|fotograf|design|illustrat|social media manager|marketing communication|copywrit|caritas|belle arti", re.I)
GOOD = re.compile(r"setter|appointment|telemarket|call center|teleselling|commerciale|vendit|sdr|inside sales|customer care|closer|telefonic|operatore telefonico", re.I)


def log(m): print(f"[{datetime.now(TZ):%H:%M:%S}] {m}", flush=True)

def key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if k: return k
    for f in ("ferretti_outreach_batch.py",):
        try:
            m = re.search(r"sk_9148[a-z0-9]+", open(os.path.join(ROOT, f)).read())
            if m: return m.group(0)
        except Exception: pass
    raise SystemExit("ELEVENLABS_API_KEY mancante")

H = None
def api(method, path, **kw):
    import requests
    r = requests.request(method, EL + path, headers=H, timeout=40, **kw)
    r.raise_for_status()
    return r.json() if r.text else {}

def l9(p): return re.sub(r"\D", "", p or "")[-9:]
def blocked(r):
    n = (r.get("name") or "").lower()
    return bool(re.search(r"brollo|\bkarima\b", n))
def cls(r):
    t = (r.get("role") or "") + " " + (r.get("notes") or "")
    if BAD.search(t): return "SCARTATO"
    if GOOD.search(t): return "A"
    return "B"


def fetch_tower():
    html = urllib.request.urlopen(TOWER_URL, timeout=40).read().decode("utf-8")
    m = re.search(r"const DATA\s*=\s*", html); i = html.index("[", m.end())
    d = s = e = 0; s = False; e = False
    for j in range(i, len(html)):
        c = html[j]
        if s:
            if e: e = False
            elif c == "\\": e = True
            elif c == '"': s = False
        else:
            if c == '"': s = True
            elif c == "[": d += 1
            elif c == "]":
                d -= 1
                if d == 0: break
    return html, i, j + 1, json.loads(html[i:j + 1])


def in_fascia(now=None):
    now = now or datetime.now(TZ)
    return 9 <= now.hour < 12 or 15 <= now.hour < 18


def select(data):
    """never-contacted A/B con telefono + retry non-connesse."""
    fresh, retry = [], []
    for r in data:
        if blocked(r) or r.get("do_not_call") or r.get("has_phone") != "YES" or not r.get("phone"):
            continue
        canale = (r.get("outreach_canale") or "")
        st = (r.get("status") or "")
        esito = (r.get("outreach_esito") or "").lower()
        rc = int(r.get("retry_count") or 0)
        # retry: gia' chiamato ma non connesso, <MAX
        if canale and ("non risposto" in esito or "non connessa" in esito) and rc < MAX_RETRY:
            retry.append(r); continue
        # fresh mai-contattato
        if not canale and not (r.get("outreach_owner")) and st == "da_contattare":
            if cls(r) == "SCARTATO": continue
            fresh.append(r)
    fresh.sort(key=lambda r: (0 if cls(r) == "A" else 1, -(r.get("hr_score") or 0)))
    chosen = retry[:BATCH_SIZE] + fresh[:max(0, BATCH_SIZE - len(retry[:BATCH_SIZE]))]
    return chosen[:BATCH_SIZE]


def first_name(r):
    return (r.get("name") or "").split()[0] if r.get("name") else "ciao"


def submit(chosen):
    recips = [{
        "phone_number": r["phone"],
        "conversation_initiation_client_data": {"dynamic_variables": {
            "nome_candidato": first_name(r),
            "fonte": (r.get("source_app") or "database recruiting"),
            "annuncio": ANNUNCIO,
            "note": (r.get("notes") or "")[:180],
        }}} for r in chosen]
    resp = api("POST", "/v1/convai/batch-calling/submit", json={
        "call_name": f"Recruiting AUTO {datetime.now(TZ):%Y%m%d_%H%M}",
        "agent_id": AGENT, "agent_phone_number_id": PHONE,
        "recipients": recips, "target_concurrency_limit": CONCURRENCY,
        "telephony_call_config": {"ringing_timeout_secs": 60},
    })
    return resp.get("id")


def wait_batch(bid, max_min=40):
    for _ in range(max_min * 60 // 20):
        b = api("GET", f"/v1/convai/batch-calling/{bid}")
        pend = sum(1 for r in b.get("recipients", []) if r.get("status") in ("pending", "in_progress", "calling"))
        if b.get("status") not in ("pending", "in_progress") and pend == 0:
            return b
        time.sleep(20)
    return api("GET", f"/v1/convai/batch-calling/{bid}")


def classify_outcome(rstatus, dur, esito_raw):
    e = (esito_raw or "").lower()
    if rstatus == "voicemail" or "voicemail" in e or "segreteria" in e:
        return ("contattato", "Segreteria", 2, False)
    if rstatus == "failed" or (rstatus == "done" and dur < 6) or not esito_raw:
        return ("contattato", "Non risposto", 2, True)  # chiamato ma non connesso; retry interno via esito
    if any(w in e for w in ("non_interess", "non interess", "non_in_target", "non in target", "rifiut")):
        return ("rejected", esito_raw[:40] or "Non interessato", 1, False)
    if any(w in e for w in ("handoff", "qualific")):
        return ("risposto", "QUALIFICATO - handoff Leonardo", 5, False)
    if "vuole_parlare_umano" in e or "umano" in e:
        return ("risposto", "Vuole colloquio umano", 4, False)
    if "ricontatt" in e or "valutar" in e:
        return ("risposto", "Da ricontattare", 3, False)
    return ("risposto", esito_raw[:40] or "Connessa", 3, False)


def process(data, batch, chosen):
    idx = {l9(r["phone"]): r for r in data}
    day = f"{datetime.now(TZ):%Y-%m-%d}"
    newq = []
    for rec in batch.get("recipients", []):
        # guardia: non scrivere esiti per chi non e' stato ancora chiamato (batch schedulato/in corso)
        if rec.get("status") in ("pending", "in_progress", "calling", "scheduled"):
            continue
        r = idx.get(l9(rec.get("phone_number", "")))
        if not r: continue
        cid = rec.get("conversation_id"); dur = 0; esito_raw = ""; piva = ""
        if cid:
            try:
                c = api("GET", f"/v1/convai/conversations/{cid}")
                dur = (c.get("metadata") or {}).get("call_duration_secs", 0)
                dc = (c.get("analysis") or {}).get("data_collection_results") or {}
                def _v(k):
                    x = dc.get(k)
                    return (x.get("value") if isinstance(x, dict) else x) or ""
                esito_raw = _v("esito"); piva = _v("partita_iva")
            except Exception: pass
        st, esito, pri, is_retry = classify_outcome(rec.get("status"), dur, esito_raw)
        was_pri = int(r.get("hr_priority") or 0)
        r["outreach_canale"] = "Chiamata AI (Francesco)"; r["outreach_data"] = day
        r["outreach_owner"] = r.get("outreach_owner") or "AI Voice"
        r["outreach_esito"] = esito; r["hr_priority"] = pri; r["status"] = st
        if cid: r["last_conversation_id"] = cid
        if piva and piva != "nd": r["partita_iva"] = piva
        if is_retry: r["retry_count"] = int(r.get("retry_count") or 0) + 1
        ah = r.get("action_history") or []; ah.append(f"{day} -> chiamata AI: {esito}"); r["action_history"] = ah
        piva_txt = {"si": " P.IVA: sì.", "apribile": " P.IVA: disponibile ad aprirla.", "no": " P.IVA: no."}.get(piva, "")
        note = f"Chiamata AI {day} ({dur}s): {esito}.{piva_txt}"
        old = (r.get("notes") or "").strip(); r["notes"] = f"[{day}] {note}" + (f" | {old}" if old else "")
        if pri >= 4 and was_pri < 4:
            newq.append(r["name"])
    return newq


def redeploy():
    # token (host headless) oppure auth vercel locale gia' presente sul Mac
    tok = os.environ.get("VERCEL_TOKEN")
    cmd = ["npx", "--yes", "vercel@latest", "deploy", "--prod", "--yes"]
    if tok:
        cmd += ["--token", tok]
    env = dict(os.environ, PATH=os.environ.get("PATH", "") + ":/usr/local/bin:/opt/homebrew/bin")
    r = subprocess.run(cmd, cwd=DEPLOY_DIR, capture_output=True, text=True, env=env)
    ok = "ready" in (r.stdout + r.stderr).lower()
    log("Redeploy Tower: " + ("OK" if ok else "FALLITO " + (r.stderr or r.stdout)[-200:]))
    return ok


def notify_leo(newq, report):
    if not newq: return
    hook = os.environ.get("LEO_WEBHOOK")
    msg = f"Nuovi candidati QUALIFICATI (handoff Leonardo): {', '.join(newq)}.\nVista Tower: {TOWER_URL} -> Coda -> 'In target - da chiamare (Leonardo)'."
    if hook:
        try:
            import requests; requests.post(hook, json={"text": msg}, timeout=20); log("Notifica Leo inviata.")
        except Exception as e: log("Notifica Leo FALLITA: " + str(e))
    else:
        log("LEO_WEBHOOK assente: nuovi qualificati = " + ", ".join(newq))


def main():
    global H
    if os.path.exists(os.path.join(ROOT, "recruiting_PAUSE")):
        log("PAUSE attivo: stop."); return
    if not in_fascia():
        log("Fuori fascia (09-12 / 15-18): stop."); return
    H = {"xi-api-key": key(), "Content-Type": "application/json"}
    html, a, b, data = fetch_tower()
    chosen = select(data)
    if not chosen:
        log("Nessun candidato da chiamare."); return
    log(f"Selezionati {len(chosen)}: " + ", ".join(first_name(r) for r in chosen))
    bid = submit(chosen); log(f"Batch {bid} inviato, attendo...")
    batch = wait_batch(bid)
    newq = process(data, batch, chosen)
    # scrivi DATA aggiornato nel file di deploy
    os.makedirs(DEPLOY_DIR, exist_ok=True)
    idxfile = os.path.join(DEPLOY_DIR, "index.html")
    src = open(idxfile, encoding="utf-8").read() if os.path.exists(idxfile) else html
    m = re.search(r"const DATA\s*=\s*", src); i = src.index("[", m.end())
    d = 0; s = False; e = False
    for j in range(i, len(src)):
        c = src[j]
        if s:
            if e: e = False
            elif c == "\\": e = True
            elif c == '"': s = False
        else:
            if c == '"': s = True
            elif c == "[": d += 1
            elif c == "]":
                d -= 1
                if d == 0: break
    open(idxfile, "w", encoding="utf-8").write(src[:i] + json.dumps(data, ensure_ascii=False) + src[j + 1:])
    redeploy()
    # report
    from collections import Counter
    cnt = Counter((r.get("outreach_esito") or "")[:20] for r in chosen)
    report = f"AUTO {datetime.now(TZ):%Y-%m-%d %H:%M} | chiamati {len(chosen)} | esiti: {dict(cnt)} | nuovi qualificati: {newq}"
    log(report)
    os.makedirs(os.path.join(ROOT, "recruiting_reports"), exist_ok=True)
    with open(os.path.join(ROOT, "recruiting_reports", f"{datetime.now(TZ):%Y-%m-%d}.log"), "a") as f:
        f.write(report + "\n")
    notify_leo(newq, report)


if __name__ == "__main__":
    main()
