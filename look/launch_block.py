#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lancia un blocco di chiamate Look SOLO se non c'e gia un batch Look attivo
(pending o in_progress). Evita doppioni quando i batch sono gia schedulati
lato-server. Usato dai task ricorrenti mattina/pomeriggio.

USO: python3 look/launch_block.py --limit 30
"""
import sys, os, re, json, subprocess, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = re.search(r'"(sk_[a-z0-9]{40,})"', open(os.path.join(ROOT, "culligan_batch_caller.py")).read()).group(1)

def active_look_batches():
    d = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://api.elevenlabs.io/v1/convai/batch-calling/workspace?limit=15",
        headers={"xi-api-key": KEY}), timeout=30).read())
    rows = d.get("batch_calls", d if isinstance(d, list) else [])
    return [b for b in rows if b.get("name", "").startswith("Look") and b.get("status") in ("pending", "in_progress")]

def main():
    limit = "30"
    if "--limit" in sys.argv:
        limit = sys.argv[sys.argv.index("--limit") + 1]
    act = active_look_batches()
    if act:
        print(f"SKIP: gia attivo/schedulato un batch Look ({act[0].get('name')} - {act[0].get('status')}). Non lancio.")
        return
    print(f"Nessun batch Look attivo -> lancio {limit} chiamate.")
    subprocess.run([sys.executable, os.path.join(ROOT, "look", "look_batch_caller.py"), "--limit", str(limit)], cwd=ROOT)

if __name__ == "__main__":
    main()
