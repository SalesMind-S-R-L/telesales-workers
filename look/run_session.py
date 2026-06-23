#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sessione di chiamate Look TUTTO-IN-UNO (automazione completa):
 1. lancia il batch AI dal Master
 2. mentre le chiamate vanno, ogni ~8 min aggiorna esiti + scheda SETTER - DA CHIUDERE + Drive
 3. a batch finito fa l'aggiornamento finale
Cosi il foglio setter si compila DA SOLO, senza nessun passaggio manuale.

USO:
    python3 look/run_session.py --limit 40
    LOOK_GIORNI="lunedi e mercoledi" python3 look/run_session.py --limit 40
"""
import os, re, sys, json, time, argparse, subprocess, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOK = os.path.join(ROOT, "look")
KEY = re.search(r'"(sk_[a-z0-9]{40,})"', open(os.path.join(ROOT, "culligan_batch_caller.py")).read()).group(1)

def batch_status(bid):
    r = urllib.request.Request(f"https://api.elevenlabs.io/v1/convai/batch-calling/{bid}", headers={"xi-api-key": KEY})
    b = json.loads(urllib.request.urlopen(r, timeout=30).read())
    st = {}
    for x in b.get("recipients", []):
        st[x.get("status")] = st.get(x.get("status"), 0) + 1
    return b.get("status"), st

def run_analyzer():
    p = subprocess.run([sys.executable, os.path.join(LOOK, "look_post_batch_analyze.py"), "--hours", "6"],
                       capture_output=True, text=True, cwd=ROOT)
    out = [l for l in p.stdout.splitlines() if "SETTER" in l or "Scritte" in l or "Conversazioni" in l]
    print("   " + " | ".join(out[-2:]) if out else "   (analyzer ok)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--poll", type=int, default=60, help="secondi tra i controlli")
    ap.add_argument("--analyze-every", type=int, default=8, help="minuti tra gli aggiornamenti del foglio")
    a = ap.parse_args()

    # 1) lancia il batch
    print(f"[{datetime.datetime.now():%H:%M}] Lancio batch da {a.limit} chiamate...")
    p = subprocess.run([sys.executable, os.path.join(LOOK, "look_batch_caller.py"), "--limit", str(a.limit)],
                       capture_output=True, text=True, cwd=ROOT, env={**os.environ})
    m = re.search(r'"id":\s*"(btcal_[a-z0-9]+)"', p.stdout)
    if not m:
        print("Errore: batch non avviato.\n", p.stdout[-500:], p.stderr[-300:])
        return
    bid = m.group(1)
    print(f"   batch {bid} avviato.")

    # 2) monitora + aggiorna periodicamente
    t0 = time.time()
    last_an = 0
    MAXSEC = 3 * 3600
    while time.time() - t0 < MAXSEC:
        time.sleep(a.poll)
        try:
            status, st = batch_status(bid)
        except Exception:
            continue
        done = st.get("completed", 0) + st.get("voicemail", 0) + st.get("failed", 0)
        print(f"[{datetime.datetime.now():%H:%M}] {status} | {st}")
        if time.time() - last_an >= a.analyze_every * 60:
            print("   aggiorno foglio setter...")
            run_analyzer()
            last_an = time.time()
        if status in ("completed", "cancelled", "failed"):
            break

    # 3) aggiornamento finale
    print(f"[{datetime.datetime.now():%H:%M}] Batch concluso. Aggiornamento finale del foglio setter...")
    run_analyzer()
    print("Fatto. Foglio SETTER - DA CHIUDERE aggiornato su Drive.")

if __name__ == "__main__":
    main()
