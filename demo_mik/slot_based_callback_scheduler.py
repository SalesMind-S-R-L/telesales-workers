#!/usr/bin/env python3
"""Slot-Based Callback Scheduler — Marco Culligan.

Workflow:
1. Legge tutte le righe Da richiamare / Non risposto / Segreteria con col M (DATA_CHIAMATA_2) vuota
2. Parser hint orario su col J → assegna slot orario (mattina 10:30, pranzo 14:30,
   pomeriggio 16:00, sera 18:00, specifico se ora specifica nel range 8-22)
3. Scrive col W (SLOT RICHIAMO) sul foglio per tracciamento
4. Schedula un `at` job per slot orario → `run_callback_slot.py <slot_name>`
5. Ogni job esegue batch concurrency=1 per quel slot, analyzer scrive M-Q

Esecuzione:
    python3 demo_mik/slot_based_callback_scheduler.py            # dry-run
    python3 demo_mik/slot_based_callback_scheduler.py --schedule # crea at jobs
    python3 demo_mik/slot_based_callback_scheduler.py --schedule --now-test  # esegue ora il primo slot non vuoto
"""
import os, re, sys, subprocess
from datetime import datetime, timedelta
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import (
    get_sheets_service, normalize_phone, is_valid_phone, safe_get,
    SHEET_ID, TAB_NAME,
    COL_TELEFONO, COL_NOTE,
)

RICHIAMA_ESITI = {"Da richiamare", "Non risposto", "Segreteria"}
SKIP_KEYWORDS = [
    'non interessat', 'non ci serve', 'non vogliamo',
    'abbiamo già fornit', 'abbiamo già un depurat',
    'abbiamo già il depurat', 'già installato un depurat',
]

# Slot orari standard
SLOTS = {
    "mattina_10_30": {"hour": 10, "minute": 30, "label": "Mattina 10:30"},
    "pranzo_14_30":  {"hour": 14, "minute": 30, "label": "Pranzo 14:30"},
    "pomeriggio_16_00": {"hour": 16, "minute": 0,  "label": "Pomeriggio 16:00"},
    "sera_18_00":    {"hour": 18, "minute": 0,  "label": "Sera 18:00"},
}

GIORNI_MAP = {"lunedì":0,"lunedi":0,"martedì":1,"martedi":1,"mercoledì":2,"mercoledi":2,
              "giovedì":3,"giovedi":3,"venerdì":4,"venerdi":4,"sabato":5,"domenica":6}


def parse_slot(note: str, now: datetime):
    """Restituisce (slot_key, hour, minute) deciso dall'analisi della nota."""
    n = (note or '').lower()

    # Ora specifica
    m = re.search(r'\b(?:alle|verso le|ore)\s+(\d{1,2})(?:[:.](\d{2}))?\b', n)
    if m:
        h = int(m.group(1))
        mm = int(m.group(2) or 0)
        if 6 <= h <= 22:
            # Mappa al slot più vicino
            if h < 12: return "mattina_10_30", 10, 30
            if h < 15: return "pranzo_14_30", 14, 30
            if h < 17: return "pomeriggio_16_00", 16, 0
            return "sera_18_00", 18, 0

    # "tra X ore" / "tra un'ora"
    if re.search(r"\btra\s+(?:circa\s+)?(?:un['\s]*ora|\d+\s*ore?)\b", n):
        h = now.hour + 1
        return ("mattina_10_30",10,30) if h<12 else ("pranzo_14_30",14,30) if h<15 else ("pomeriggio_16_00",16,0) if h<17 else ("sera_18_00",18,0)

    # 'stasera' / 'sera'
    if re.search(r'\b(stasera|sera)\b', n):
        return "sera_18_00", 18, 0

    # 'mattina'
    if re.search(r'\bmattina\b', n):
        return "mattina_10_30", 10, 30

    # 'pomeriggio'
    if re.search(r'\bpomeriggio\b', n):
        return "pomeriggio_16_00", 16, 0

    # giorno settimana → mattina default
    for nome in GIORNI_MAP:
        if re.search(rf'\b{nome}\b', n):
            return "mattina_10_30", 10, 30

    # nessun hint → mattina default (default safer slot per HoReCa)
    return "mattina_10_30", 10, 30


def main():
    now = datetime.now()
    schedule = "--schedule" in sys.argv
    now_test = "--now-test" in sys.argv

    svc = get_sheets_service()
    rows = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"'{TAB_NAME}'!A:W").execute().get('values',[])

    candidati_per_slot = {k:[] for k in SLOTS}
    skipped = 0
    for i,r in enumerate(rows[1:], start=2):
        r = r + ['']*(23-len(r))
        esito = r[8].strip()
        if esito not in RICHIAMA_ESITI: continue
        if r[12].strip(): continue  # M già compilato → già richiamato
        ph = normalize_phone(safe_get(r, COL_TELEFONO))
        if not is_valid_phone(ph): continue
        note_lower = r[9].strip().lower()
        if any(k in note_lower for k in SKIP_KEYWORDS):
            skipped += 1; continue

        slot_key, hh, mm = parse_slot(r[9], now)
        candidati_per_slot[slot_key].append({"row": i, "nome": r[0], "tel": ph, "prev_note": r[9]})

    print(f"=== Slot-Based Callback Scheduler ===")
    print(f"Now: {now.strftime('%H:%M')}  | Skipped (anti-non-interessati): {skipped}\n")
    for slot_key, info in SLOTS.items():
        cands = candidati_per_slot[slot_key]
        target_dt = now.replace(hour=info['hour'], minute=info['minute'], second=0, microsecond=0)
        if target_dt < now: target_dt += timedelta(days=1)
        # se è già passato oggi, sposta domani
        print(f"[{info['label']:<20}] {len(cands)} candidati  → target {target_dt.strftime('%d/%m %H:%M')}")
        for c in cands[:5]:
            print(f"    r{c['row']:3d} {c['nome'][:38]}")
        if len(cands)>5: print(f"    ... e altri {len(cands)-5}")

    # Aggiorna col W (SLOT) sul foglio
    updates = []
    for slot_key, cands in candidati_per_slot.items():
        for c in cands:
            updates.append({"range":f"'{TAB_NAME}'!W{c['row']}","values":[[slot_key]]})
    if updates:
        svc.spreadsheets().values().batchUpdate(spreadsheetId=SHEET_ID,
            body={"valueInputOption":"USER_ENTERED","data":updates}).execute()
        print(f"\nCol W aggiornata su {len(updates)} righe (slot assegnato).")

    if not schedule and not now_test:
        print("\nDry-run completato. Lancia con --schedule per creare at jobs.")
        return

    # Crea at jobs per ogni slot non vuoto
    script = "/Users/simocors/Desktop/telesales/demo_mik/run_callback_slot.py"
    for slot_key, cands in candidati_per_slot.items():
        if not cands: continue
        info = SLOTS[slot_key]
        target_dt = now.replace(hour=info['hour'], minute=info['minute'], second=0, microsecond=0)
        if target_dt < now: target_dt += timedelta(days=1)
        if now_test:
            print(f"\n[NOW-TEST] Eseguo subito slot '{slot_key}' ({len(cands)} chiamate)")
            subprocess.run(["python3", script, slot_key], cwd="/Users/simocors/Desktop/telesales")
            break  # solo primo slot in modalità test
        else:
            at_time = target_dt.strftime("%H:%M %m/%d/%Y").replace(" 0", " ")
            cmd = f"cd /Users/simocors/Desktop/telesales && /usr/bin/python3 demo_mik/run_callback_slot.py {slot_key} > /tmp/callback_slot_{slot_key}.out 2>&1"
            print(f"\nScheduled '{slot_key}' at {target_dt.strftime('%d/%m %H:%M')} ({len(cands)} calls)")
            subprocess.run(f'echo "{cmd}" | at {target_dt.strftime("%H:%M")}', shell=True)


if __name__ == "__main__":
    main()
