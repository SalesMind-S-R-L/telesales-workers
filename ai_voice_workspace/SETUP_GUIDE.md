# SETUP GUIDE — AI Voice Workspace

Esegui questi step **nell'ordine**. Tempo stimato: ~90 minuti.

---

## STEP 1 — Apri il workspace in VS Code

```bash
code /Users/simocors/Desktop/telesales/ai_voice_workspace
```

In VS Code:
- Installa estensione **Claude Code** (publisher: Anthropic) se non l'hai
- Clicca icona Claude Code nella sidebar → login col tuo account Claude
- Apri terminale integrato (`Ctrl+\``)

---

## STEP 2 — Conferma CLAUDE.md aggiornato

Apri `CLAUDE.md` e leggi le 26 regole chiave. Verifica che siano allineate al tuo workflow attuale.

Verifica anche che i file in `context/` e `sop/` corrispondano (sono 5 context + 6 sop). Prompt utile:
> "Leggi tutti i file in context/ e sop/, dimmi se ci sono regole nei file che NON sono richiamate in CLAUDE.md, o se ci sono contraddizioni."

---

## STEP 3 — Installa skill ufficiali Anthropic

In chat Claude Code:
```
/plugin
```
- Aggiungi marketplace GitHub Anthropic
- Installa **document-skills** (contiene xlsx, docx, pdf)

Verifica con `/` — devono apparire `xlsx`, `docx`, `pdf`.

---

## STEP 4 — Crea le SKILL custom

Per ogni skill, lancia il prompt completo (uno per uno, non in batch). I prompt sono molto dettagliati perché contengono regole specifiche.

### Skill 1 — `elevenlabs_prompt_builder`
> "Crea skill `elevenlabs_prompt_builder`. Compito: generare/modificare prompt di agenti ElevenLabs. Input: nome cliente, obiettivo agente (outbound HoReCa / demo / qualifica / etc.), dynamic variables previste. Output: prompt completo da PATCH-are sull'agente. Regole obbligatorie:
> 1. Includere INTEGRALMENTE il blocco anti-loop da `sop/sop_antiloop_elevenlabs.md`
> 2. Rispettare tone of voice da `context/02_prompt_rules_elevenlabs.md` (anti-esclamativo, energia, audio tags `[warm]` solo T1)
> 3. Inserire le dynamic variables con sintassi `{{var}}` esattamente come previste
> 4. Aggiungere checklist tools obbligatori (`end_call` + `voicemail_detection`)
> 5. Default `max_duration_seconds` = 180 (outbound HoReCa) o 300 (demo)
> 6. Output salvato in `templates/<cliente>_<obiettivo>_v<N>.md`"

### Skill 2 — `elevenlabs_agent_publisher`
> "Crea skill `elevenlabs_agent_publisher`. Compito: applicare un prompt template a un agente ElevenLabs via PATCH API, attivare i built_in_tools end_call + voicemail_detection, settare max_duration. Checklist pre-publish:
> - Tutte le dynamic variables del payload outbound combaciano con `{{var}}` del prompt
> - Voce confermata (premade italiana o custom)
> - Webhook post-call collegato (vedi `sop/sop_postcall_webhook.md`)
> - Test su 3 numeri reali prima del batch
> Reference API: `context/07_elevenlabs_api.md`. Output: log delle modifiche + agent_id + URL ElevenLabs UI."

### Skill 3 — `prompt_snippet_extractor`
> "Crea skill `prompt_snippet_extractor`. Compito: dato un problema (es. 'agente continua a parlare dopo riaggancio'), analizzare gli altri agenti del workspace ElevenLabs e estrarre i pezzi di prompt più efficaci che risolvono quel problema. Output: lista di snippet con citazione dell'agente d'origine + proposta di integrazione nel prompt target. Reference: la sessione che ha generato `sop_antiloop_elevenlabs.md`."

### Skill 4 — `batch_sequential_launcher`
> "Crea skill `batch_sequential_launcher`. Compito: lanciare batch outbound ElevenLabs con `target_concurrency_limit=1` (no overlap). Input: cliente, lista CSV, agent_id, phone_number_id, limite chiamate (default 30). Workflow:
> 1. Pre-filtro contro foglio cliente (no duplicati per telefono)
> 2. Validazione dynamic variables per ogni riga
> 3. Submit batch ElevenLabs
> 4. Mark `data_chiamata` sul foglio interno per ogni riga
> 5. Monitora stato batch ogni 30s, stampa progress
> Reference: `sop/sop_batch_sequential.md` + script `culligan_batch_caller.py`."

### Skill 5 — `post_batch_analyzer`
> "Crea skill `post_batch_analyzer`. Compito: dopo che un batch ha finito, leggere la trascrizione turn-by-turn di ogni conversazione e riscrivere ESITO + NOTE sul foglio interno con frasi italiane di senso compiuto. Input: batch_id o range temporale. Workflow:
> 1. Lista conversazioni del batch o del giorno
> 2. Per ognuna fetch dettaglio (`/v1/convai/conversations/{id}`)
> 3. Estrai fatti dalla trascrizione (nome, ruolo, num diretto, giorno+ora, email, motivo no)
> 4. Verifica `appuntamento_preso=True` con giorno+ora concreti in transcript (no falsi positivi)
> 5. Scrivi F, G (timestamp reale), H (solo appt fisici), I, J, K, L sul foglio interno
> Regole non negoziabili in `sop/sop_post_batch_analysis.md`. Reference: `post_batch_culligan_analyze.py`."

### Skill 6 — `shared_sheet_push`
> "Crea skill `shared_sheet_push`. Compito: dopo via libera utente, copiare righe dal foglio interno al foglio condiviso cliente. Workflow:
> 1. Leggi headers riga 1 del foglio cliente
> 2. Leggi 2-3 righe esistenti per capire DOVE il cliente scrive davvero (può essere I/J/K invece di C/G/H)
> 3. Mappa per ogni esito → nota in stile cliente (lowercase, telegrafico)
> 4. Append in fondo (`values.update` su range esplicito, non `append` che può shiftare)
> Regole + esempi reali in `sop/sop_push_to_shared_sheet.md`. NESSUN push senza via libera utente esplicito."

### Skill 7 — `lista_enricher`
> "Crea skill `lista_enricher`. Compito: arricchire CSV liste contatti Cribis seguendo `sop/sop_enrichment.md`. Wrappa lo script Python `/Users/simocors/Desktop/telesales/arricchisci_lista.py`. Valida cellulari come da phone_hunting_rules (solo prefissi italiani mobili 3xx). Output: CSV `_VERIFICATE.csv` in `liste/`."

### Skill 8 — `phone_validator`
> "Crea skill `phone_validator`. Compito: validare cellulari DM anti-allucinazione. Solo prefissi italiani mobili (3xx). Gold standard: file `Filippo_Mobili_34.csv` se presente. Output: report con falsi positivi flaggati."

### Skill 9 — `sip_retry_manager`
> "Crea skill `sip_retry_manager`. Compito: gestire policy retry SIP fail (`sop/sop_sip_retry.md`). Max 5 tentativi/numero, pausa 60s tra round. MAI marcare SIP fail come 'Non risposto' né sul foglio interno né su quello cliente. Wrappa `tools/retry_until_success.py`."

### Skill 10 — `weekly_report_xlsx`
> "Crea skill `weekly_report_xlsx`. Compito: generare report settimanale `.xlsx` per cliente seguendo `sop/sop_report_settimanale.md`. Usa la skill `xlsx` già installata. Output in `reports/<cliente>/<YYYY-WW>_report.xlsx` con i 4 sheet richiesti. Classificazione realistica, mai gonfiare numeri."

### Skill 11 — `apps_script_bridge_setup`
> "Crea skill `apps_script_bridge_setup`. Compito: scaffoldare un nuovo bridge Apps Script per un cliente nuovo. Output: codice `.gs` completo basato sul template `context/08_apps_script_bridge.md` + istruzioni di deploy (web app, scope OAuth, webhook ElevenLabs)."

### Skill 12 — `landing_call_setup`
> "Crea skill `landing_call_setup`. Compito: configurare il flusso landing → outbound ElevenLabs come `chiamami.html`. Output: HTML landing + endpoint server (Cloudflare Worker o Apps Script) + configurazione webhook post-call con email recap. Reference: `sop/sop_landing_integration.md`."

Dopo ogni skill, verifica che Claude abbia creato il file in `skills/`.

---

## STEP 5 — Crea i SUB-AGENT

Comando: `/agents` → **Crea nuovo agente** → **Solo per questo progetto**

### Agente 1 — `voice-prompt-engineer`
Skill: `elevenlabs_prompt_builder`, `elevenlabs_agent_publisher`, `prompt_snippet_extractor`
Ruolo: "Crea, modifica e pubblica agenti ElevenLabs. Estrae snippet dai migliori agenti del workspace per risolvere problemi specifici. Non agisce mai senza dynamic variables compilate."

### Agente 2 — `list-ops`
Skill: `lista_enricher`, `phone_validator`
Ruolo: "Arricchisce e valida liste contatti da Cribis. Pre-filtra contro fogli clienti. Produce CSV pronti per upload."

### Agente 3 — `batch-runner`
Skill: `batch_sequential_launcher`, `sip_retry_manager`
Ruolo: "Lancia e sorveglia batch outbound ElevenLabs sequenziali (concurrency=1). Gestisce SIP fail con retry policy. MAI marca SIP fail come 'Non risposto'."

### Agente 4 — `call-analyst`
Skill: `post_batch_analyzer`, `weekly_report_xlsx`
Ruolo: "Analizza chiamate basandosi sulle trascrizioni reali, rifina esiti+note sul foglio interno, genera report settimanali xlsx. Verifica `appuntamento_preso=True` con giorno+ora concreti. Classificazione realistica, mai gonfiare numeri."

### Agente 5 — `sheet-push`
Skill: `shared_sheet_push`
Ruolo: "Dopo via libera utente esplicito, pusha righe dal foglio interno al foglio condiviso cliente. Verifica mapping colonne reali del cliente prima di scrivere. Note in stile cliente (lowercase, telegrafico, no riferimenti tecnici)."

### Agente 6 — `bridge-setup`
Skill: `apps_script_bridge_setup`, `landing_call_setup`
Ruolo: "Scaffolda bridge Apps Script e flussi landing → outbound per nuovi clienti. Una tantum per cliente."

### Agente 7 — `campaign-strategist`
Skill: (nessuna — solo ragionamento)
Ruolo: "Pianifica campagne per cliente nuovo. Decide: agent tipo, dynamic vars necessarie, foglio interno setup, mapping verso foglio cliente. Output: brief + lista skill/agenti da attivare in sequenza."

---

## STEP 6 — Aggiorna CLAUDE.md (se serve)

Dopo aver creato skill e agenti, prompt:
> "Leggi `skills/` e `agents/`, aggiorna la tabella 'Routing agenti' di `CLAUDE.md` coi nomi esatti generati. Aggiungi anche una sezione 'Skill disponibili' con elenco di tutte le skill custom + ufficiali (xlsx/docx/pdf)."

---

## STEP 7 — Test end-to-end

### Test 1 — Marco Culligan (cliente già attivo)
> "Cliente Marco Culligan (vedi `catalogo_clienti/marco_culligan.md`). Voglio:
> 1. Patchare il prompt agente con la versione anti-loop più recente
> 2. Verificare che tools end_call + voicemail_detection siano attivi
> 3. Lanciare batch test di 5 chiamate sulle prossime aziende non-in-Sebastiano
> 4. Dopo batch, analizzare trascrizioni e popolare foglio interno
> 5. Mostrarmi proposta push verso foglio Sebastiano (NON pushare, aspetto via libera)"

Claude deve orchestrare: `voice-prompt-engineer` → `batch-runner` → `call-analyst` → `sheet-push` (in dry-run).

### Test 2 — Setup cliente nuovo
> "Onboard nuovo cliente fittizio 'Acme Solar'. Settore: B2B fotovoltaico. Foglio interno da creare, foglio cliente da chiedermi. Voglio agent ElevenLabs scaffold + bridge Apps Script + landing call setup."

Claude deve attivare: `campaign-strategist` → `bridge-setup` → `voice-prompt-engineer`.

---

## STEP 8 (opzionale) — Remote control da mobile

In chat:
```
/remote-control
```
Apri link sul telefono. **Non condividere il link**.

---

## Quando hai finito

Salva memory:
> "Salva memory: workspace AI Voice operativo in `Desktop/telesales/ai_voice_workspace/`. 7 agenti attivi (voice-prompt-engineer, list-ops, batch-runner, call-analyst, sheet-push, bridge-setup, campaign-strategist). 12 skill custom + xlsx/docx/pdf ufficiali. Clienti attivi: Marco Culligan, Mario Cribis, Marco Ferretti, Mik Cosentino."

## Riferimenti rapidi

- Regole base: `CLAUDE.md`
- Tone agenti: `context/02_prompt_rules_elevenlabs.md`
- Anti-loop (CRITICO): `sop/sop_antiloop_elevenlabs.md`
- API ElevenLabs: `context/07_elevenlabs_api.md`
- Bridge pattern: `context/08_apps_script_bridge.md`
- Post-batch analysis: `sop/sop_post_batch_analysis.md`
- Push foglio cliente: `sop/sop_push_to_shared_sheet.md`
- Batch sequenziale: `sop/sop_batch_sequential.md`
- Webhook setup: `sop/sop_postcall_webhook.md`
- Landing integration: `sop/sop_landing_integration.md`
- TTS settings: `context/06_tts_voice_settings.md`
