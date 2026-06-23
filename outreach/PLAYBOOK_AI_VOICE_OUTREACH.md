# Playbook AI Voice Outreach — Telesales (canale 3)

Obiettivo: 50+ chiamate/giorno con l'agente "Marco — Outreach Telesales"
(`agent_5301kpdv4sd9e15vcz4qpm8e7vrn`) per fissare call conoscitive col
fondatore Niccolò. Questo canale ha gia' una pipeline collaudata: questo
documento la allinea alla strategia 4 canali (pool esclusivi).

## REGOLA NUMERO UNO: zero SIP 404

Il problema storico = numeri morti. Un batch di 50 con numeri presi a regex
dai siti ha dato 46 SIP 404. Mai scraping a regex puro come fonte finale.
Metodo che funziona (0 SIP 404 su 100+ chiamate) = DUE BARRIERE:
1. Agenti coordinati che LEGGONO il sito reale e scelgono il numero giusto
2. Gate deterministico (`prospecting_b2b/strict_gate.py`) che valida
   matematicamente prefisso AGCOM e numero di cifre.

## Pool del canale (pool esclusivo, mai sovrapposto a LinkedIn/Email)

- Tab **AI VOICE CODA** (foglio pipeline) = bacino candidati: 68 aziende
  IT/Software ex-master. Validate il 12/06:
  - **50 dialabili + nuove** → CSV pronto: `prospecting_b2b/ferretti_aivoice_pronti.csv`
  - 11 numeri da riverificare (gate fail = rischio troncamento/SIP 404)
  - 7 gia' chiamate (dedup vs foglio OUTREACH AI VOICE) → escluse
- **Foglio operativo dedicato** (NON il pipeline): esiti e log chiamate vanno
  su `1wFYXFDFo6W2GT6HT3HKHLYx8eN-C4VUGnxlU_dIiNyk`, tab "OUTREACH AI VOICE"
  (gid 431195392). I push sono automatici (vedi sotto).

## Sourcing nuovi numeri (gap ~250/settimana)

Vibe Prospecting da' i decision maker (azienda+sito+citta+ruolo) MA **non da'
telefoni italiani affidabili** (enrichment phone = numeri esteri/sbagliati):
i numeri li cacciamo NOI dai siti. Sorgenti aziende:
1. Vibe `fetch-entities` (entity_type prospects), filtri `{"values":[...]}`,
   `has_website:true` — consuma crediti (oggi esauriti)
2. `CONTATTI_UNICI_TELESALES.xlsx` (14k righe): tieni solo aziende con dominio
   email proprio (scarta gmail/libero/yahoo/hotmail/pec), il dominio = sito
3. Lead hunt via subagenti su fonti pubbliche (come fatto per LinkedIn+Email)

Poi: phone hunt con agenti coordinati (template `prospecting_b2b/phone_hunter.py`)
→ output `/tmp/phone_hunt_result.json` → `strict_gate.py` →
`prospecting_b2b/ferretti_*.csv` formato Ferretti.

## Lancio batch + push automatico

```
./prospecting_b2b/LANCIA_BATCH.sh <N>
# oppure
python3 ferretti_lancia_e_push.py --csv prospecting_b2b/ferretti_aivoice_pronti.csv --limit 50
```
Lancia il batch (concurrency 1, una alla volta), aspetta la fine e PUSHA da
solo gli esiti sul foglio OUTREACH AI VOICE.

### CULLIGAN HA PRIORITA' MASSIMA
Prima di lanciare, controllare i batch attivi su ElevenLabs
(`/v1/convai/batch-calling/workspace`). Ferretti gira solo a concurrency 1 e
non deve sovrapporsi a batch Culligan attivi. OK: 1 Culligan + 1 Ferretti
contemporanei. Di piu' no.

## Regole esiti e note (foglio OUTREACH AI VOICE)

- MAI menzionare AI/bot/agente nelle note. Come un commerciale umano, corte.
- "Non risposto" solo se nessuno risponde davvero; IVR/centralino/segreteria
  = "Da richiamare"; email generica (info@) NON e' un lead; "Appuntamento"
  solo con giorno+ora confermati. Zero emoji.
- Mai inventare numeri, mai dedurre per somiglianza: solo cifre lette dal sito.

## Adattamento alla strategia 4 canali

- **Disclosure AI a inizio chiamata** (AI Act): "sono l'assistente virtuale di
  Telesales". Per noi e' anche DEMO: il prospect vive il prodotto che vendiamo.
  L'agente puo' dirlo ("quello che sto facendo con lei e' quello che facciamo
  per i nostri clienti"). Applicare con `outreach/inject_disclosure.py --apply`
  (solo con ok di Simone).
- CTA = call di 15 min col fondatore su Cal.com (slot reali, mai inventati).
- Post-batch: `outreach/followup_aivoice.py` genera email per esito
  (interessato/da richiamare/non interessato). "Non risposto" = niente email.
- Pool esclusivo: le aziende in AI VOICE CODA non stanno in LinkedIn/Email
  (verificato da check_collisioni.py: 0 violazioni).

## File chiave

`prospecting_b2b/strict_gate.py` (gate) · `ferretti_outreach_batch.py` (submit,
`ruolo_ita()` traduce i ruoli) · `ferretti_lancia_e_push.py` (orchestra) ·
`ferretti_push_to_sheet.py` (push) · `prospecting_b2b/phone_hunter.py` (regole
hunt) · `prospecting_b2b/LANCIA_BATCH.sh`. Credenziali ElevenLabs e phone_id
dentro `ferretti_outreach_batch.py`.

## Prerequisiti primo batch (settimana 1)

1. Ok disclosure AI (inject_disclosure.py --apply)
2. Cal.com live (l'agente propone slot reali)
3. Check batch Culligan attivi (priorita')
4. CSV `ferretti_aivoice_pronti.csv` (50 numeri) gia' pronto al lancio

Obiettivo: liste 100% dialabili (zero SIP 404). Meglio meno numeri ma che
partano davvero.
