#!/usr/bin/env python3
"""
Controller: diala a ondate (concurrency 1, coesiste con Culligan) finche' raggiunge
TARGET chiamate CONNESSE (completed+voicemail). Push automatico per ogni ondata.
Si ferma a TARGET o quando il pool finisce.

Uso: python3 ferretti_target_connesse.py --pool <pool.csv> --target 50 [--wave 30]
"""
import argparse, csv, time, sys, subprocess, tempfile, os
from datetime import datetime
import requests
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
import ferretti_outreach_batch as fb

PUSH = '/Users/simocors/Desktop/telesales/ferretti_push_to_sheet.py'

def log(m):
    print(f"[{datetime.now():%H:%M}] {m}", flush=True)

def wait_lunch_break():
    """Pausa pranzo: niente chiamate tra le 12:15 e le 14:30. Riprende alle 14:30."""
    notified = False
    while True:
        now = datetime.now()
        hm = (now.hour, now.minute)
        if (12, 15) <= hm < (14, 30):
            if not notified:
                log("PAUSA PRANZO: stop chiamate fino alle 14:30")
                notified = True
            time.sleep(60)
        else:
            if notified:
                log("Ripresa chiamate (14:30)")
            return

def wait_done(bid, key):
    while True:
        # stop netto alle 12:15: annulla l'ondata in corso
        hm = (datetime.now().hour, datetime.now().minute)
        if (12, 15) <= hm < (14, 30):
            requests.post(f'{fb.ELEVENLABS_BASE_URL}/v1/convai/batch-calling/{bid}/cancel',
                          headers={'xi-api-key': key}, timeout=20)
            log("Stop 12:15 — ondata in corso annullata per la pausa")
            time.sleep(8)
        d = requests.get(f'{fb.ELEVENLABS_BASE_URL}/v1/convai/batch-calling/{bid}',
                         headers={'xi-api-key': key}, timeout=30).json()
        if d.get('status') in ('completed', 'cancelled', 'failed'):
            return d
        time.sleep(45)

def field_active(key):
    """Ritorna la lista di batch attivi (in_progress o pending) sul numero condiviso.
    Qualsiasi batch attivo = Ferretti deve cedere (stesso numero in uscita = no overlap)."""
    try:
        w = requests.get(f'{fb.ELEVENLABS_BASE_URL}/v1/convai/batch-calling/workspace',
                         headers={'xi-api-key': key}, timeout=30).json()
        return [b for b in (w.get('batch_calls') or []) if b.get('status') in ('in_progress', 'pending')]
    except Exception:
        return ['__errore_rete__']  # in dubbio, cede

def wait_field_clear(key):
    """CULLIGAN HA PRIORITA' SUL NUMERO CONDIVISO: non lancia finche' c'e' QUALSIASI batch
    attivo o pending. Conferma due letture consecutive a campo libero prima di partire,
    cosi' evita la finestra in cui Culligan sta per partire."""
    while True:
        active = field_active(key)
        if not active:
            time.sleep(8)
            if not field_active(key):  # doppia conferma campo libero
                return
            continue
        log(f"ATTENDO (Culligan priorita, numero condiviso): attivo {[b.get('name') if isinstance(b,dict) else b for b in active]}")
        time.sleep(45)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pool', required=True)
    ap.add_argument('--target', type=int, default=50)
    ap.add_argument('--dial-target', type=int, default=0, help='se >0, ferma a N chiamate LANCIATE invece che a N connesse')
    ap.add_argument('--wave', type=int, default=30)
    args = ap.parse_args()
    key = fb.ELEVENLABS_API_KEY

    pool = list(csv.DictReader(open(args.pool, encoding='utf-8')))
    fields = pool[0].keys()
    log(f"AVVIO — target {args.target} connesse | pool {len(pool)} numeri | wave {args.wave} | concurrency 1")

    idx = 0
    connected = 0
    dialed = 0
    wave_n = 0
    def reached():
        if args.dial_target > 0:
            return dialed >= args.dial_target
        return connected >= args.target
    while not reached() and idx < len(pool):
        wave_n += 1
        # PAUSA PRANZO 12:15-14:30
        wait_lunch_break()
        # CULLIGAN PRIORITA': aspetta che il campo sia libero prima di lanciare
        wait_field_clear(key)
        wave = pool[idx: idx + args.wave]
        idx += len(wave)
        # csv temporaneo dell'ondata
        tf = tempfile.NamedTemporaryFile('w', delete=False, suffix='.csv', newline='')
        w = csv.DictWriter(tf, fieldnames=fields); w.writeheader(); w.writerows(wave); tf.close()
        ok, _ = fb.validate_rows(fb.load_csv(tf.name))
        name = f"Ferretti-Target-{datetime.now():%Y%m%d-%H%M}"
        res = fb.submit_batch(name, [fb.build_recipient(r) for r in ok])
        bid = res.get('batch_call_id', res.get('id'))
        dialed += len(ok)
        log(f"ONDATA {wave_n}: lanciati {len(ok)} (batch {bid}) — attendo fine...")

        d = wait_done(bid, key)
        from collections import Counter
        c = Counter(x.get('status') for x in d.get('recipients', []))
        wave_conn = c.get('completed', 0) + c.get('voicemail', 0)
        connected += wave_conn
        # push automatico ondata
        time.sleep(10)
        subprocess.run([sys.executable, PUSH, bid, '--csv', args.pool],
                       capture_output=True, text=True)
        os.unlink(tf.name)
        log(f"ONDATA {wave_n} chiusa: +{wave_conn} connesse | TOTALE {connected}/{args.target} | dialed {dialed}")

    log(f"FINE — {connected} connesse su target {args.target} | dialed totali {dialed} | ondate {wave_n}")
    if connected < args.target:
        log(f"Pool esaurito prima del target (mancano {args.target - connected}). Servono nuovi numeri.")

if __name__ == '__main__':
    main()
