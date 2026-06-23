#!/usr/bin/env python3
"""
Orchestratore Ferretti: lancia batch -> attende fine -> push automatico su foglio.
Uso: python3 ferretti_lancia_e_push.py --csv <lista.csv> --limit 30
"""
import argparse, time, sys, subprocess, re
import requests
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
import ferretti_outreach_batch as fb

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', default='/Users/simocors/Desktop/telesales/prospecting_b2b/ferretti_aivoice_pronti.csv')
    ap.add_argument('--limit', type=int, default=30)
    args = ap.parse_args()

    # 1. submit
    rows = fb.load_csv(args.csv)
    ok, _ = fb.validate_rows(rows)
    selected = ok[:args.limit]
    from datetime import datetime
    name = f"Ferretti-Outreach-{datetime.now().strftime('%Y%m%d-%H%M')}"
    recipients = [fb.build_recipient(r) for r in selected]
    res = fb.submit_batch(name, recipients)
    bid = res.get('batch_call_id', res.get('id'))
    print(f"[LANCIO] batch {bid} ({len(selected)} numeri)", flush=True)

    # 2. attendi fine
    key = fb.ELEVENLABS_API_KEY
    while True:
        d = requests.get(f'{fb.ELEVENLABS_BASE_URL}/v1/convai/batch-calling/{bid}',
                         headers={'xi-api-key': key}, timeout=20).json()
        st = d.get('status')
        if st in ('completed', 'cancelled', 'failed'):
            print(f"[FINE] batch {st}", flush=True)
            break
        time.sleep(60)

    # 3. push automatico
    time.sleep(15)
    out = subprocess.run([sys.executable, '/Users/simocors/Desktop/telesales/ferretti_push_to_sheet.py',
                          bid, '--csv', args.csv], capture_output=True, text=True)
    print('[PUSH]', out.stdout.strip().splitlines()[-1] if out.stdout.strip() else out.stderr[-200:], flush=True)

if __name__ == '__main__':
    main()
