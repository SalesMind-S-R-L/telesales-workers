# SOP — Batch SIP outbound sequenziale (zero overlap, zero SIP overload)

## Principi

1. **`target_concurrency_limit=1`** sul batch ElevenLabs → una chiamata alla volta
2. **`ringing_timeout_secs=60`** → squilla 60s prima di marcare timeout
3. Mai usare `Utilities.sleep()` in Apps Script per >5 minuti (limite 6 min esecuzione)
4. Marca `data_chiamata` al trigger della chiamata sul foglio interno, NON aspettare il webhook
5. Pre-filtra liste contro foglio cliente (no duplicati — vedi `sop_enrichment.md`)
6. Conferma dynamic variables nel payload prima del lancio

## Architettura raccomandata

```
[Foglio interno]                    [ElevenLabs]               [SIP/Telnyx]
       │                                 │                          │
       │  Python launcher                │                          │
       │  (legge righe pending)          │                          │
       ▼                                 ▼                          ▼
   filter pre-batch ──► submit batch ──► dispatch 1-at-a-time ──► outbound
       │                                 │                          │
   mark data_chiamata             ringing_timeout=60s          recipient phone
       │                                 │                          │
       │                                 ▼                          ▼
       │                          completed/failed              picks up / no
       │                                 │
       │                                 ▼
       │                       post_call_webhook → Apps Script doPost
       │                                                       │
       └──────────────────────── update F, H, I, J, K, L ◄─────┘
```

## Launcher Python (reference: `culligan_batch_caller.py`)

```python
from culligan_batch_caller import (
    get_sheets_service, read_all_rows, mark_called, normalize_phone,
    is_valid_phone, is_already_called, safe_get, extract_categoria,
    build_recipient, submit_batch,
)

SEBASTIANO_PHONES = read_sebastiano_phones(svc)  # pre-filtro

to_call = []
for i, row in enumerate(rows[1:]):
    if is_already_called(row): continue
    ph = normalize_phone(safe_get(row, COL_TELEFONO))
    if not is_valid_phone(ph): continue
    if ph in SEBASTIANO_PHONES: continue  # già nel foglio cliente
    to_call.append({...})
    if len(to_call) >= LIMIT: break  # es. 30

recipients = [build_recipient(...) for it in to_call]
result = submit_batch(name, recipients)
# submit_batch DEVE usare target_concurrency_limit=1

# Mark data_chiamata sulle righe interne
for it in to_call:
    mark_called(svc, it["row_index"], oggi)
```

## Configurazione submit_batch (regole d'oro)

```python
payload = {
    "call_name": "<Cliente>-<Citta>-<YYYYMMDD-HHMM>",
    "agent_id": CULLIGAN_AGENT_ID,
    "agent_phone_number_id": PHONE_NUMBER_ID,
    "recipients": recipients,
    "target_concurrency_limit": 1,    # SEMPRE 1 per outbound HoReCa
    "telephony_call_config": {
        "ringing_timeout_secs": 60
    }
}
```

## Verifica dynamic variables PRE-batch

Prima di lanciare, fai un test con 1 sola riga e verifica nella conversazione su ElevenLabs UI che le dynamic variables siano lette. Le var minime per HoReCa Culligan:
- `nome_azienda` (obbligatoria)
- `nome_titolare` (può essere vuota)
- `categoria` (hotel/bar/ristorante — estratta da `[Categoria]` nelle note fonte)
- `citta`
- `indirizzo`
- `note_extra`
- `row_index` (per match webhook)

## Monitoraggio live batch

```python
r = requests.get(f"https://api.elevenlabs.io/v1/convai/batch-calling/{BATCH_ID}",
                 headers=H, timeout=20).json()
from collections import Counter
counts = Counter(x.get("status") for x in r.get("recipients",[]))
# {pending: 29, in_progress: 1, completed: 0, failed: 0}
```

Stato:
- `pending` — in coda
- `in_progress` — in chiamata adesso
- `completed` — finita normalmente
- `failed` — SIP fail (vedi `sop_sip_retry.md`)

## Dopo il batch

1. Lascia che il post-call webhook scriva sul foglio interno (vedi `sop_postcall_webhook.md`)
2. Lancia `sop_post_batch_analysis.md` per rifinire esiti + note basandoti sulle trascrizioni reali
3. Aspetta via libera utente
4. `sop_push_to_shared_sheet.md`

## Stima costi e tempi

Per 30 chiamate HoReCa medie (60-180s ciascuna):
- Durata totale: ~45-60 min (concurrency=1)
- Costi: ~5-7 € totali
- Output atteso: 1-3 appuntamenti veri + 4-6 email + 8-12 da richiamare + 8-12 non risposto

## SIP fail policy

Se >20% del batch fa SIP fail, è probabile un problema di rete/throttle Telnyx. Pause 5-10 min e riprova con un batch più piccolo (10 invece di 30).

Mai marcare SIP fail come "Non risposto" sul foglio interno o cliente — sempre `Da richiamare` interno e `non risp` cliente (senza menzione SIP).
