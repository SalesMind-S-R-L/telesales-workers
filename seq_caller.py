#!/usr/bin/env python3
"""
Chiamatore 1-ALLA-VOLTA anti-SIP-503, salva-lista.
- Una chiamata per volta. Aspetta che finisca.
- SIP 503 (trunk giu'): NON avanza, pausa 60s e RIPROVA lo stesso numero
  (cosi' appena Telnyx torna su riparte da solo, senza bruciare numeri buoni).
- SIP 404 (numero morto): salta al prossimo.
- Connessa / no-answer / altro: avanza al prossimo (pausa breve).
- Si ferma alla deadline. A fine: push esiti sul foglio.
Uso: python3 seq_caller.py --until 17:50
"""
import argparse, time, subprocess, sys
from datetime import datetime
import requests
import ferretti_outreach_batch as fb

H = {"xi-api-key": fb.ELEVENLABS_API_KEY}
B = fb.ELEVENLABS_BASE_URL
CSV = "/Users/simocors/Desktop/telesales/prospecting_b2b/ferretti_cellulari.csv"

def log(m): print(f"[{datetime.now():%H:%M:%S}] {m}", flush=True)

def conv_error(cid):
    try:
        d = requests.get(f"{B}/v1/convai/conversations/{cid}", headers=H, timeout=15).json()
        e = d.get("error") or d.get("metadata", {}).get("error") or {}
        return e.get("code")
    except Exception:
        return None

def call_one(row):
    """Manda 1 chiamata, aspetta, ritorna (codice_errore|None, batch_id)."""
    res = fb.submit_batch(f"Ferretti-1x-{datetime.now():%H%M%S}", [fb.build_recipient(row)])
    bid = res.get("id") or res.get("batch_id")
    for _ in range(20):
        time.sleep(7)
        d = requests.get(f"{B}/v1/convai/batch-calling/{bid}", headers=H, timeout=20).json()
        recs = d.get("recipients", [])
        if d.get("status") in ("completed", "failed", "cancelled") or (
           recs and all(str(x.get("status")) not in ("pending", "in_progress", "calling") for x in recs)):
            break
    recs = requests.get(f"{B}/v1/convai/batch-calling/{bid}", headers=H, timeout=20).json().get("recipients", [])
    for x in recs:
        if str(x.get("status")) == "failed" and x.get("conversation_id"):
            return conv_error(x["conversation_id"]), bid
    return None, bid

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--until", default="17:50")
    args = ap.parse_args()
    hh, mm = map(int, args.until.split(":"))
    deadline = datetime.now().replace(hour=hh, minute=mm, second=0, microsecond=0)

    rows, _ = fb.validate_rows(fb.load_csv(CSV))
    rows = [r for r in rows if r.get("_phone")]
    log(f"Pool {len(rows)} numeri. 1-alla-volta fino alle {args.until}.")

    i, connesse, err503, err404, batch_ids = 0, 0, 0, 0, []
    while i < len(rows) and datetime.now() < deadline:
        r = rows[i]
        log(f"Chiamo: {r['_phone']} ({r.get('nome_azienda','')[:30]})")
        code, bid = call_one(r)
        batch_ids.append(bid)
        if code == 503:
            err503 += 1
            log(f"  SIP 503 (trunk giu'). Riprovo STESSO numero tra 60s. [503 totali: {err503}]")
            time.sleep(60)
            continue            # non avanza
        elif code == 404:
            err404 += 1; i += 1
            log(f"  SIP 404 numero morto, salto. [{i}/{len(rows)}]")
            time.sleep(4)
        else:
            connesse += 1; i += 1
            log(f"  OK chiamata partita (err={code}). [{i}/{len(rows)}]")
            time.sleep(5)

    log(f"FINE alle {datetime.now():%H:%M}. Partite ok: {connesse} | 404 saltati: {err404} | 503: {err503}")
    log("Push esiti sul foglio...")
    for bid in dict.fromkeys(batch_ids):
        try:
            subprocess.run([sys.executable, "/Users/simocors/Desktop/telesales/ferretti_push_to_sheet.py",
                            bid, "--csv", CSV], capture_output=True, text=True, timeout=150)
        except Exception:
            pass
    log("Esiti compilati: LOG AI VOICE (tutto) + OUTREACH AI VOICE (caldi).")

if __name__ == "__main__":
    main()
