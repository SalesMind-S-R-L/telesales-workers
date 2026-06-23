# AI Voice Telesales — Workspace

## Scopo
Team di skill + sub-agent Claude Code per automatizzare le operazioni voice AI:
- Creazione/manutenzione agenti ElevenLabs (Marco Culligan, Mario Cribis, Marco Ferretti, Mik Cosentino, ecc.)
- Filtro liste contro fogli condivisi clienti (no duplicati)
- Esecuzione batch SIP outbound sequenziali (concurrency=1, no overlap, no SIP overload)
- Post-batch transcript analysis → esiti reali + note umane
- Push controllato verso fogli condivisi clienti (solo dopo via libera)
- Reportistica xlsx settimanale

## Stack
- **Voice AI**: ElevenLabs (account `admin@telesales.it`, key in `.env`), Deepgram (test)
- **CRM**: GoHighLevel (sub-account per cliente)
- **Sheets**: Google Sheets via `service-account.json` (vedi `context/04_sheets_rules.md`)
- **Apps Script**: bridge post-call webhook (`demo_mik/apps_script_culligan.gs`, `apps_script_marco_ferretti.gs`)
- **Scripting**: Python in `/Users/simocors/Desktop/telesales/`

## Organizzazione cartelle

```
ai_voice_workspace/
├── CLAUDE.md                ← questo file (regole + routing)
├── SETUP_GUIDE.md           ← step-by-step da seguire ORA
├── context/                 ← regole brand, prompt rules, esiti, sheets, team
├── sop/                     ← procedure operative
│   ├── sop_antiloop_elevenlabs.md      ← REGOLE ANTI-LOOP da incollare in ogni prompt
│   ├── sop_post_batch_analysis.md      ← come analizzare chiamate dopo batch
│   ├── sop_push_to_shared_sheet.md     ← mapping colonne foglio interno → cliente
│   ├── sop_sip_retry.md
│   ├── sop_enrichment.md
│   └── sop_report_settimanale.md
├── catalogo_clienti/        ← scheda per cliente (asset, agent_id, sheet ID)
├── templates/               ← template prompt agenti
├── liste/                   ← liste CSV input
├── reports/                 ← output report .xlsx
├── output/                  ← output intermedi
├── skills/                  ← creata da Claude
└── agents/                  ← creata da Claude
```

## Regole chiave (universali, non negoziabili)

### Output e linguaggio
1. **Mai emoji** in nessun output destinato al cliente o ai fogli
2. **Note**: mai menzionare AI/bot/agente/prompt/variabili — scrivi come un commerciale umano
3. **Note foglio cliente**: lowercase, telegrafico, stile setter (es. "non risp", "inviare email info@...", "ok appuntamento martedì 13 con Luca")
4. **Risposte all'utente**: ultra-concise, zero filler, no ripetizioni in sessione
5. **Non ripetere domande già risposte**

### Classificazione esiti
6. **"Non risposto"** SOLO se nessuno risponde (squilli a vuoto)
7. **Segreteria / IVR / centralino** = "Da richiamare" sul foglio interno; sul foglio condiviso → nota "non risp" (senza dettagli tecnici)
8. **"Non interessato"** → solo se ha parlato un decisore o assimilabile, mai una reception generica
9. **"Appuntamento"** → SOLO se in trascrizione c'è giorno + ora concreti concordati; un "sì" generico a "settimana prossima" senza data = "Da richiamare"
10. **SIP fail**: MAI marcare come "Non risposto", sempre retry (max 5, pausa 60s); sul foglio condiviso scrivi solo "non risp" senza menzionare SIP

### Sheets
11. **Report**: sempre `.xlsx`, mai Word/PDF/Pages
12. **Date foglio interno**: `DD/MM/YYYY HH:MM` (timestamp reale chiamata)
13. **Date foglio cliente**: `DD/MM/YY` (compatibile con stile setter)
14. **Match contatti**: prima per telefono, poi per nome
15. **Pre-filtro**: prima di lanciare un batch, escludi aziende già presenti nel foglio condiviso cliente (match per telefono)
16. **Push verso foglio cliente**: SOLO dopo via libera esplicito; mai automatico

### ElevenLabs agenti
17. **Ogni prompt** deve includere il blocco `sop_antiloop_elevenlabs.md` integralmente
18. **Tool obbligatori**: `end_call` + `voicemail_detection` attivi su ogni agente outbound
19. **max_duration_seconds**: 180 per outbound HoReCa, 300 per demo
20. **Batch**: `target_concurrency_limit=1` sempre, `ringing_timeout_secs=60`
21. **Pubblicazione**: prima di pubblicare verifica che TUTTE le dynamic variables (`nome_contatto`, `nome_azienda`, `categoria`, `citta`, `note`) siano nel prompt come `{{var}}`

### Analisi post-batch
22. **Fonte primaria**: trascrizione turn-by-turn della conversazione (`/v1/convai/conversations/{cid}`)
23. **Fonte secondaria di conferma**: `analysis.transcript_summary` e `analysis.data_collection_results`
24. **Match conversazione → riga foglio**: via `dynamic_variables.nome_azienda` (preferenziale) o telefono
25. **Verifica appuntamenti**: `appuntamento_preso=True` da solo NON basta — verifica giorno e ora concreti in trascrizione
26. **DATA_CHIAMATA**: timestamp reale `start_time_unix_secs` della conv, non il momento del trigger

Dettagli completi in `context/` e `sop/`.

---

## Routing agenti

| Task | Agente | Note |
|---|---|---|
| Crea/modifica prompt ElevenLabs | `@voice-prompt-engineer` | Inserisce sempre `sop_antiloop_elevenlabs` |
| Pubblica agente ElevenLabs | `@voice-prompt-engineer` | Checklist tools + dynamic vars |
| Estrai pezzi prompt da altri agenti | `@voice-prompt-engineer` | Best-of su agenti workspace |
| Filtra lista contro foglio cliente | `@list-ops` | Match per telefono, no duplicati |
| Arricchimento lista Cribis | `@list-ops` | Usa `arricchisci_lista.py` |
| Validazione cellulari DM | `@list-ops` | Anti-allucinazione (3xx) |
| Lancio batch SIP outbound | `@batch-runner` | concurrency=1, mark data_chiamata |
| Sorveglianza batch + SIP retry | `@batch-runner` | Mai "Non risposto" su fail |
| Analisi post-batch (transcript + esiti) | `@call-analyst` | Fonte: trascrizione, conferma: summary |
| Aggiorna foglio interno | `@call-analyst` | Note italiane di senso compiuto |
| Push verso foglio condiviso cliente | `@sheet-push` | SOLO dopo via libera utente |
| Report settimanale .xlsx | `@call-analyst` | Classificazione realistica |
| Strategia campagna nuovo cliente | `@campaign-strategist` | Solo ragionamento |
| Task semplice (1 file) | nessun agente | Direttamente |

## Modello mentale

- **Skill** = procedura ripetibile (script + regole verificabili)
- **Agente** = ruolo specializzato che orchestra più skill seguendo le regole di CLAUDE.md
- Le skill vivono in `skills/`, gli agenti in `agents/`

## Stato attuale

Workspace in setup iniziale. Vedi `SETUP_GUIDE.md` per gli step ordinati.

Asset esistenti pronti all'uso:
- `/Users/simocors/Desktop/telesales/culligan_batch_caller.py` — batch sequenziale ElevenLabs
- `/Users/simocors/Desktop/telesales/demo_mik/apps_script_culligan.gs` — bridge post-call → foglio interno
- `/Users/simocors/Desktop/telesales/demo_mik/post_batch_culligan_analyze.py` — analyzer trascrizione → esiti+note
- `/Users/simocors/Desktop/telesales/demo_mik/push_culligan_to_sebastiano.py` — push controllato foglio cliente
