# Cliente — Marco Culligan (Bolzano HoReCa)

## Tipo campagna
B2B outbound. Marco è l'agente AI di Culligan che chiama strutture HoReCa di Bolzano (hotel, bar, ristoranti) per fissare appuntamenti col rappresentante umano **Sebastiano**.

## Asset ElevenLabs

- **Agent ID**: `agent_5101kreejrz1e98rfzjrf3brhd50`
- **Phone Number ID**: `phnum_1501kr3sx76sfxeap503jqy1m7j9` (Telnyx Italia, +39 055 4652406)
- **API key**: `sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726`

### Settings agente
- max_duration_seconds: **180** (HoReCa, conversazioni brevi)
- LLM: gemini-2.5-flash-lite, temp 0.7
- TTS: eleven_v3_conversational, stability 0.2, similarity 0.8, speed 1.1, expressive_mode TRUE
- Tools attivi: `end_call`, `voicemail_detection`
- Prompt: ~24 KB con sezione ANTI-LOOP completa

## Fogli Google

### Foglio interno "claude bolzano"
- ID: `1PiezlYSd5TZNBCRTvzBhx_yVCGfN6aMI3PXdOYU4xu8`
- Tab: `aziende_bolzano_VERIFICATE`
- Colonne: A=NOME, B=TITOLARE, C=NOTE_FONTE, D=INDIRIZZO, E=TELEFONO, F=PRESENTE, G=DATA_CHIAMATA, H=DATA_APP, I=ESITO, J=NOTE_AI, K=EMAIL, L=TRANSCRIPT_LINK

### Foglio condiviso con Sebastiano (cliente)
- ID: `1KsbFkAhJQDd2edYuKgbVC0yd87jK-Y6egKU254Y1wT0`
- Tab: `Foglio1`
- Colonne reali: A=nome, B=titolare, D=indirizzo, E=telefono, F=presente, **I=data chiamata, J=note, K=data appuntamento** (NB: C/G/H inutilizzate)

⚠️ Importante: Sebastiano usa I/J/K, non C/G/H come dice l'header. Verifica sempre prima di scrivere (vedi `sop_push_to_shared_sheet.md`).

## Bridge Apps Script

- File: `/Users/simocors/Desktop/telesales/demo_mik/apps_script_culligan.gs` (27 KB)
- Container-bound al foglio interno
- Menu custom "☎ Marco AI Culligan" con: setup, chiamata singola, batch sequenziale 30, trasferimento al foglio Sebastiano
- doPost gestisce post-call webhook ElevenLabs → match per `row_index` o `nome_azienda` → scrive F-L

### Webhook ElevenLabs
- Workspace webhook ID: `48fdc617e82b4b8e846f8a9c0a6699c4` ("Culligan — Post Call to Sheet")
- URL Apps Script: `https://script.google.com/macros/s/AKfycbwGPV2Wjb5lL_1-QH2xQoyZGX2jAjjaEH0pymC8aLNs7_OuxFv41OhmkBeyLazsVTh7lA/exec`
- Eventi: `transcript`, formato JSON

## Identità agente

```
Sei Marco, consulente Culligan per la zona di Bolzano. Chiami strutture 
HoReCa (hotel, bar, ristoranti) per fissare un appuntamento di 20 minuti 
con Sebastiano, il rappresentante senior che passa di persona.

NON spieghi tecnologie. Vendi BENEFICI:
- Qualità acqua e ghiaccio
- Taglio costi bottiglie (numeri precisi li porta Sebastiano)
- Zero plastica → immagine ambientale

OBIETTIVO: fissare appuntamento fisico con Sebastiano in struttura.
```

## Dynamic variables

- `nome_azienda` (obbligatoria)
- `nome_titolare` (può essere vuota)
- `categoria` (hotel/bar/ristorante) — estratta dalle note fonte
- `citta` = "Bolzano" sempre
- `indirizzo`
- `note_extra` (note dalla sorgente lead — sito, email pubblica, ecc.)
- `row_index` (per match webhook → foglio)

## STEP del flow (priorità)

- **STEP A**: apertura, riconoscimento chi risponde
- **STEP A.1**: se NON è il titolare:
  1. Quando trovarlo? (giorno+ora)
  2. Numero diretto? (se può darlo)
  3. Sebastiano passa di persona con valore (se rifiutano numero)
- **STEP B**: hook col decisore (3 benefici)
- **STEP C**: proposta appuntamento "Sebastiano passa martedì o mercoledì la settimana prossima?"
- **STEP D**: raccolta dati appuntamento
- **STEP E**: chiusura email se no appuntamento

## Pipeline operativa

```
1. Lista verificata → foglio interno (filtro: NOT in foglio Sebastiano per tel)
2. Batch sequenziale 30 chiamate, concurrency=1
3. Post-call webhook → riga interna popolata (F, H, I, J, K, L)
4. Post-batch analyzer Python (fetch transcript turn-by-turn) → corregge esiti+note
5. Verifica manuale appuntamenti (specie casi limite tipo "sì" generico)
6. Via libera utente → push verso foglio Sebastiano (mapping I/J/K)
```

## Risultati batch tipico (30 chiamate Bolzano HoReCa)

Distribuzione attesa:
- 1-2 Appuntamento fisico confermato
- 4-6 Email da inviare
- 12-15 Da richiamare
- 2-4 Non interessati
- 6-10 Non risposto (di cui SIP fail variabile)

Costo medio batch: ~5-7 € (LLM + TTS + SIP Telnyx).

## Script Python rilevanti

- `/Users/simocors/Desktop/telesales/culligan_batch_caller.py` — launcher batch
- `/Users/simocors/Desktop/telesales/demo_mik/launch_culligan_30_not_in_sebastiano.py` — wrapper con filtro NOT-in-Sebastiano
- `/Users/simocors/Desktop/telesales/demo_mik/post_batch_culligan_analyze.py` — analyzer trascrizioni
- `/Users/simocors/Desktop/telesales/demo_mik/push_culligan_to_sebastiano.py` — push controllato

## Note operative

- **Sebastiano è il rep umano**, non un agente AI — nelle note menziona "Sebastiano passa di persona"
- **Mai compilare** il foglio Sebastiano senza via libera esplicito utente
- **DATA_APPUNTAMENTO** popola SOLO se trascrizione conferma giorno + ora concreti
- **Lingua**: italiano. Alcune persone di Bolzano rispondono in tedesco → l'agente può rispondere in italiano comunque, ma se l'IVR è automatico bilingue → end_call
