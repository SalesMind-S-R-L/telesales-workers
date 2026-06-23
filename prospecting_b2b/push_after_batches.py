#!/usr/bin/env python3
"""Aspetta la fine delle due finestre e pusha gli esiti sul foglio.
Anche se il Mac dorme, al risveglio pusha (i risultati sono statici)."""
import time, subprocess, sys, json
from datetime import datetime
ROOT="/Users/simocors/Desktop/telesales"
ids=json.load(open(f"{ROOT}/prospecting_b2b/sched_ids_20260623.json"))
plan=[("Ferretti-Mattina-20260623","prospecting_b2b/ferretti_mattina.csv",12,40),
      ("Ferretti-Pomeriggio-20260623","prospecting_b2b/ferretti_pomeriggio.csv",17,5)]
for name,csv_p,h,m in plan:
    bid=ids.get(name)
    target=datetime.now().replace(hour=h,minute=m,second=0,microsecond=0)
    while datetime.now()<target: time.sleep(60)
    if bid:
        subprocess.run([sys.executable,f"{ROOT}/ferretti_push_to_sheet.py",bid,"--csv",f"{ROOT}/{csv_p}"],
                       cwd=ROOT,capture_output=True,text=True,timeout=300)
        print(f"[{datetime.now():%H:%M}] push {name} fatto",flush=True)
