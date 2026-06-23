#!/usr/bin/env python3
"""
Scheduler: alle 14:30 (Europe/Rome) lancia il batch Ferretti (50 chiamate) sul
numero Telnyx +39 055 4652406, MA solo se la linea e' libera (nessun altro
batch attivo su quel numero, es. Look). Se occupata, riprova ogni 5 min fino
alle 17:30. Detached: gira anche a sessione chiusa (nohup).

Lancio: nohup python3 prospecting_b2b/schedule_ferretti_1430.py > /tmp/ferretti_sched.log 2>&1 &
"""
import re, time, subprocess, sys
from datetime import datetime, timedelta
import requests

ROOT = "/Users/simocors/Desktop/telesales"
TELNYX = "phnum_1501kr3sx76sfxeap503jqy1m7j9"   # +39 055 4652406, numero nostro
CSV = f"{ROOT}/prospecting_b2b/ferretti_aivoice_pronti.csv"
KEY = re.search(r'"(sk_[a-f0-9]{40,})"', open(f"{ROOT}/ferretti_outreach_batch.py").read()).group(1)
H = {"xi-api-key": KEY}
B = "https://api.elevenlabs.io"

def log(m):
    print(f"[{datetime.now():%H:%M:%S}] {m}", flush=True)

def line_busy():
    """True se c'e' un batch attivo (non nostro) sul numero Telnyx."""
    try:
        r = requests.get(f"{B}/v1/convai/batch-calling/workspace", headers=H, timeout=20).json()
        items = r.get("batch_calls", r.get("workspace_batch_calls", []))
        for b in items:
            if b.get("phone_number_id") == TELNYX and str(b.get("status", "")).lower() in ("pending", "in_progress", "processing"):
                if not str(b.get("name", "")).startswith("Ferretti"):
                    return b.get("name")
    except Exception as e:
        log(f"check linea err: {e}")
    return None

def main():
    now = datetime.now()
    target = now.replace(hour=14, minute=30, second=0, microsecond=0)
    if target < now:
        target += timedelta(days=1)
    wait = (target - now).total_seconds()
    log(f"Scheduler avviato. Lancio previsto {target:%d/%m %H:%M} (tra {wait/3600:.1f}h).")
    time.sleep(max(0, wait))

    deadline = target.replace(hour=17, minute=30)
    while datetime.now() < deadline:
        busy = line_busy()
        if busy:
            log(f"Linea Telnyx occupata da '{busy}'. Riprovo tra 5 min.")
            time.sleep(300)
            continue
        log("Linea libera. Lancio batch Ferretti 50.")
        r = subprocess.run([sys.executable, f"{ROOT}/ferretti_lancia_e_push.py",
                            "--csv", CSV, "--limit", "50"],
                           capture_output=True, text=True, cwd=ROOT)
        log("STDOUT:\n" + r.stdout[-2000:])
        if r.stderr:
            log("STDERR:\n" + r.stderr[-1000:])
        log("Batch Ferretti lanciato (push automatico a fine batch).")
        return
    log("Deadline 17:30 raggiunta con linea sempre occupata: NON lanciato. Rilanciare a mano.")

if __name__ == "__main__":
    main()
