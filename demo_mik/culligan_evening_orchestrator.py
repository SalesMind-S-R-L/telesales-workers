#!/usr/bin/env python3
"""Orchestratore serale Culligan:
1. Lancia batch di 30 chiamate (NOT in Sebastiano)
2. Polla stato batch fino a completed (o 75 min timeout)
3. Analizza trascrizioni → scrive esiti/note sul foglio interno
4. NON pusha al foglio Sebastiano (richiede via libera manuale).
"""
import os, re, sys, time, json, subprocess
from datetime import datetime, timezone
import requests

sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import (
    get_sheets_service, read_all_rows, mark_called, normalize_phone,
    is_valid_phone, is_already_called, safe_get, extract_categoria,
    build_recipient, submit_batch,
    SHEET_ID, TAB_NAME,
    COL_NOME_AZIENDA, COL_NOME_TITOLARE, COL_NOTE, COL_INDIRIZZO, COL_TELEFONO,
)
from demo_mik.launch_culligan_30_not_in_sebastiano import read_sebastiano_phones

API = "sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
AGENT_ID = "agent_5101kreejrz1e98rfzjrf3brhd50"
BASE = "https://api.elevenlabs.io"
H = {"xi-api-key": API}
LIMIT = 30
LOG = "/tmp/culligan_evening_run.log"
BATCH_ID_FILE = "/tmp/culligan_last_batch_id.txt"


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def step1_launch_batch():
    log("STEP 1 — lancio batch")
    svc = get_sheets_service()
    rows = read_all_rows(svc)
    seb = read_sebastiano_phones(svc)
    log(f"  Internal: {len(rows)-1} righe | Sebastiano: {len(seb)} numeri")

    to_call = []
    for i, row in enumerate(rows[1:]):
        if is_already_called(row): continue
        ph = normalize_phone(safe_get(row, COL_TELEFONO))
        if not is_valid_phone(ph): continue
        if ph in seb: continue
        note = safe_get(row, COL_NOTE)
        to_call.append({
            "row_num": i + 2, "row_index": i + 1, "phone": ph,
            "nome_azienda": safe_get(row, COL_NOME_AZIENDA),
            "nome_titolare": safe_get(row, COL_NOME_TITOLARE),
            "categoria": extract_categoria(note),
            "indirizzo": safe_get(row, COL_INDIRIZZO),
            "note": note,
        })
        if len(to_call) >= LIMIT: break

    log(f"  Selezionate {len(to_call)} aziende:")
    for it in to_call:
        log(f"    r{it['row_num']:3d} {it['nome_azienda']:<40} [{it['categoria']}] {it['phone']}")

    recipients = [build_recipient(
        phone=it["phone"], nome_azienda=it["nome_azienda"],
        categoria=it["categoria"], nome_titolare=it["nome_titolare"],
        indirizzo=it["indirizzo"], note=it["note"],
    ) for it in to_call]

    name = f"Culligan-30-NotInSeb-{datetime.now().strftime('%Y%m%d-%H%M')}"
    log(f"  Submit batch '{name}' concurrency=1")
    res = submit_batch(name, recipients)
    batch_id = res.get("batch_call_id", res.get("id", "?"))
    log(f"  Batch ID: {batch_id}")

    with open(BATCH_ID_FILE, "w") as f:
        f.write(batch_id)

    oggi = datetime.now().strftime("%d/%m/%Y %H:%M")
    log(f"  Mark data_chiamata={oggi} sulle righe interne...")
    for it in to_call:
        try:
            mark_called(svc, it["row_index"], oggi)
            time.sleep(0.25)
        except Exception as e:
            log(f"    warn row {it['row_num']}: {e}")
    return batch_id


def step2_wait_batch(batch_id, max_minutes=75):
    log(f"STEP 2 — polling batch {batch_id} (max {max_minutes} min)")
    start = time.time()
    while True:
        elapsed = (time.time() - start) / 60
        if elapsed > max_minutes:
            log(f"  TIMEOUT dopo {max_minutes} min, procedo comunque all'analisi")
            return
        try:
            r = requests.get(f"{BASE}/v1/convai/batch-calling/{batch_id}",
                             headers=H, timeout=30).json()
            status = r.get("status")
            from collections import Counter
            counts = Counter(x.get("status") for x in r.get("recipients", []))
            log(f"  t+{elapsed:.0f}min status={status} {dict(counts)}")
            if status in ("completed", "failed", "cancelled"):
                log(f"  Batch finito: {status}")
                return
        except Exception as e:
            log(f"  err polling: {e}")
        time.sleep(60)


def step3_analyze():
    log("STEP 3 — analisi trascrizioni + scrittura foglio interno")
    # Forza TODAY_START sul giorno corrente
    env = os.environ.copy()
    res = subprocess.run(
        ["python3", "/Users/simocors/Desktop/telesales/demo_mik/post_batch_culligan_analyze.py"],
        capture_output=True, text=True, env=env, cwd="/Users/simocors/Desktop/telesales"
    )
    log("  stdout:\n" + res.stdout)
    if res.stderr:
        log("  stderr:\n" + res.stderr[:1000])
    log("STEP 3 — done")


def main():
    open(LOG, "w").close()  # reset log
    log(f"START orchestrator — oggi {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    batch_id = step1_launch_batch()
    step2_wait_batch(batch_id, max_minutes=75)
    step3_analyze()
    log("FINE — foglio interno popolato. ATTENDERE VIA LIBERA per push su foglio Sebastiano.")
    log(f"Log completo: {LOG}")


if __name__ == "__main__":
    main()
