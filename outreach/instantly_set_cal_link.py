#!/usr/bin/env python3
"""
Inserisce il link Cal.com nella campagna A (Proposta) di Instantly, sostituendo
il placeholder [INSERIRE_LINK_CALCOM] in tutti gli step della sequenza.

Uso:
    INSTKEY="<chiave instantly>" python3 outreach/instantly_set_cal_link.py "https://cal.com/telesales/15min"
"""
import os, sys, json, requests

if len(sys.argv) < 2:
    sys.exit("Uso: instantly_set_cal_link.py <url_cal_com>")
CAL = sys.argv[1]
KEY = os.environ.get("INSTKEY", "")
if not KEY:
    sys.exit("INSTKEY mancante in ambiente")

H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
B = "https://api.instantly.ai/api/v2"
CAMP_A = "7bbbf91e-d6dc-4941-8147-9f24a72d9b3c"  # Proposta (A)

c = requests.get(f"{B}/campaigns/{CAMP_A}", headers=H, timeout=20).json()
seq = c["sequences"]
n = 0
for step in seq[0]["steps"]:
    for v in step["variants"]:
        if "[INSERIRE_LINK_CALCOM]" in v["body"]:
            v["body"] = v["body"].replace("[INSERIRE_LINK_CALCOM]", CAL)
            n += 1
r = requests.patch(f"{B}/campaigns/{CAMP_A}", headers=H, json={"sequences": seq}, timeout=25)
print(f"Sostituzioni: {n} | PATCH: {r.status_code}")
print("Fatto. La campagna A ora ha il link Cal.com. Resta in DRAFT finche' non la attivi.")
