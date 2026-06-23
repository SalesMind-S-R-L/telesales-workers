# SOP — Analisi post-batch ElevenLabs

Procedura per: dopo che un batch ElevenLabs ha finito, analizzare ogni conversazione e popolare il foglio interno con esiti + note ITALIANE DI SENSO COMPIUTO, basate sui fatti reali della trascrizione (non riassunto generico, non note tecniche).

## Principi non negoziabili

1. **Fonte primaria** = trascrizione turn-by-turn (`/v1/convai/conversations/{cid}` → `transcript`)
2. **Fonte secondaria** = `analysis.data_collection_results` (campo `note_chiamata` scritto dall'agente live) + `analysis.transcript_summary`. Servono per CONFERMARE, non per generare la nota
3. **Mai citare AI/agente/bot/prompt/sistema** nelle note
4. **Mai gonfiare esiti**: un "sì" generico ≠ Appuntamento; appuntamento_preso=True senza giorno+ora concreti ≠ Appuntamento
5. **Match conversazione → riga foglio**: via `dynamic_variables.nome_azienda` (preferenziale) o telefono dell'`external_number`

## Step concreti

### 1. Recupera elenco conversazioni del batch
```python
import requests
H = {"xi-api-key": API_KEY}
batch = requests.get(f"https://api.elevenlabs.io/v1/convai/batch-calling/{BATCH_ID}",
                     headers=H, timeout=30).json()
# Ogni recipient ha: conversation_id, status, phone_number,
# conversation_initiation_client_data.dynamic_variables.nome_azienda
```

In alternativa, lista per agent + finestra temporale:
```python
requests.get("https://api.elevenlabs.io/v1/convai/conversations",
             params={"agent_id": AID, "page_size": 100}, headers=H)
# Poi filtra per start_time_unix_secs >= TODAY_START
```

### 2. Per ogni conversazione, fetch dettagli completi
```python
conv = requests.get(f"https://api.elevenlabs.io/v1/convai/conversations/{cid}",
                    headers=H, timeout=30).json()
turns = conv.get("transcript", [])
dc = conv.get("analysis",{}).get("data_collection_results",{})
summary = conv.get("analysis",{}).get("transcript_summary","")
start_ts = (conv.get("metadata") or {}).get("start_time_unix_secs")
```

### 3. Estrai fatti grezzi dalla trascrizione (turn-by-turn)

Per ogni user turn cerca:
- **nome decisore**: pattern "signor X", "il signor X", "sono X", "parla con X"
- **ruolo**: "titolare", "responsabile", "gestore", "figlio", "moglie", "reception"
- **numero diretto**: regex `\b3\d{2}[\s.-]?\d{2,4}[\s.-]?\d{3,4}\b`
- **giorno richiamo/appuntamento**: `lunedì|martedì|...|domani|oggi|dopodomani`
- **ora**: `\d{1,2}[:.]\d{2}` o `alle <numero>`
- **email**: regex standard
- **motivo no**: "non mi interessa", "abbiamo già un fornitore"
- **fraintendimento**: "tavolo", "prenotazione", "quante persone"

### 4. Classifica esito (priorità top-down)

| Trigger | Esito |
|---|---|
| user dice "tavolo"/"prenotazione" + appuntamento prosegue | Non interessato (fraintendimento) |
| user dice esplicitamente "non interessa", "abbiamo già..." | Non interessato |
| `appuntamento_preso=True` E giorno+ora concreti in trascrizione | Appuntamento |
| numero diretto fornito o giorno+ora di richiamo | Da richiamare |
| email data + "mandi una mail" | Email |
| solo IVR/segreteria nei turni iniziali | Non risposto |
| `status == "failed"` (SIP fail) | Non risposto (SIP) |
| nessuno dei sopra | Da richiamare |

**Caso trappola**: se `appuntamento_preso=True` ma il `data_appuntamento` è vuoto o vago ("settimana prossima") e l'utente ha solo detto "sì" senza pinnare giorno → **NON è Appuntamento, è Da richiamare**.

### 5. Scrivi nota italiana di senso compiuto

Stile: come un setter umano che riferisce al collega. Frasi complete, lowercase iniziale opzionale, max 200 caratteri.

Template:
- **Appuntamento**: `Sebastiano passa di persona <giorno> <ora> a <indirizzo> con <nome titolare>. <Dettaglio chi ha preso l'app, se utile>.`
- **Da richiamare**: `<Chi ha risposto> ha detto che <situazione>. <Quando/come richiamare>.`
- **Email**: `<Chi ha risposto> ha chiesto di mandare email a <indirizzo>. <Dettaglio>.`
- **Non interessato**: `<Chi> ha detto chiaramente <citazione breve>. <Motivo se rilevante>.`
- **Non risposto** (sul foglio interno): `Non risposto.` (su foglio condiviso: `non risp`)

Esempi reali (Culligan batch 18/05/2026):
- r26 Pension Röllhof → `Risposto la madre. Il figlio Luca Röhl è il titolare. Sebastiano passa di persona martedì 19/05 alle 13:00 a Campegno 27. La madre informerà Luca.`
- r12 Gasthof Kohlern → `Titolare assente, dipendente ha annotato il richiamo per domani 19/05 alle 9:30 al fisso 0471 329978. Cellulare diretto non disponibile.`
- r17 Hotel Hanny → `Stefani (gestione) ha risposto. Hotel senza ristorante, ha detto chiaramente "non ci serve tanta acqua, mi dispiace". Non interessati.`

### 6. Scrivi su foglio interno

Colonne (Culligan-style):
- F (PRESENTE): `Sì` se esito ∈ {Appuntamento, Email, Da richiamare}, `No` altrimenti
- G (DATA CHIAMATA): timestamp reale `start_time_unix_secs` formattato `DD/MM/YYYY HH:MM` (Europe/Rome = UTC+2 maggio)
- H (DATA APPUNTAMENTO): popolato SOLO per Appuntamento fisico con data esplicita (es. `19/05/2026 09:30`)
- I (ESITO): dropdown
- J (NOTE_AI): la nota italiana
- K (EMAIL): se raccolta
- L (TRANSCRIPT_LINK): `https://elevenlabs.io/app/conversational-ai/history/{cid}`

### 7. Sanity check

Prima di chiudere:
- [ ] Tutti gli "Appuntamento" hanno H popolata con `DD/MM/YYYY HH:MM`
- [ ] Tutti i "Non risposto" hanno nota = `Non risposto.` (foglio interno) o `non risp` (foglio condiviso)
- [ ] Nessuna nota cita "agente", "AI", "bot", "Marco AI", "SIP fail" (sul foglio condiviso)
- [ ] Match nome_azienda corretto per ogni riga (no scambi)
- [ ] DATA_CHIAMATA è oggi (data reale), non data trigger

## Reference implementativo

Vedi `/Users/simocors/Desktop/telesales/demo_mik/post_batch_culligan_analyze.py` — analyzer completo che:
1. Recupera batch + lista conversazioni
2. Fetcha trascrizione completa per ogni conv
3. Classifica esito + estrae fatti
4. Scrive su foglio interno via `values.batchUpdate`
