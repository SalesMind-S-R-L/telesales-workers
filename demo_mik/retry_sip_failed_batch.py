#!/usr/bin/env python3
"""Retry batch sui SIP fail di un batch precedente.
Legge i recipients failed, rilancia un nuovo batch con concurrency=1 con i loro dynamic_variables originali."""
import os, sys, time, re
from datetime import datetime
import requests
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import (
    submit_batch, get_sheets_service, mark_called,
    SHEET_ID, TAB_NAME, COL_DATA_CHIAMATA,
)

H = {"xi-api-key": "sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"}
PREV_BATCH = "btcal_1901ks0dk9bce0498rg3g5bhfe82"


def main():
    r = requests.get(f"https://api.elevenlabs.io/v1/convai/batch-calling/{PREV_BATCH}",
                     headers=H, timeout=20).json()
    failed = [x for x in r.get("recipients", []) if x.get("status") == "failed"]
    print(f"SIP fail da rilanciare: {len(failed)}")

    recipients = []
    for x in failed:
        recipients.append({
            "phone_number": x["phone_number"],
            "conversation_initiation_client_data": x.get("conversation_initiation_client_data") or {},
        })

    name = f"Culligan-RETRY-SIP-{datetime.now().strftime('%Y%m%d-%H%M')}"
    print(f"Submit batch '{name}' concurrency=1 ringing_timeout=60s")
    res = submit_batch(name, recipients)
    batch_id = res.get("batch_call_id", res.get("id", "?"))
    print(f"Retry Batch ID: {batch_id}")

    # mark data_chiamata aggiornata sulle righe corrispondenti
    svc = get_sheets_service()
    oggi = datetime.now().strftime("%d/%m/%Y %H:%M")
    for x in failed:
        dv = (x.get("conversation_initiation_client_data") or {}).get("dynamic_variables") or {}
        row_idx = dv.get("row_index")
        if not row_idx: continue
        try:
            mark_called(svc, int(row_idx) - 1, oggi)
            time.sleep(0.2)
        except Exception as e:
            print(f"  warn row {row_idx}: {e}")
    print(f"Mark data_chiamata={oggi} aggiornata.")
    print(f"\nMonitor: tail -f, oppure poll API con batch_id sopra")


if __name__ == "__main__":
    main()
