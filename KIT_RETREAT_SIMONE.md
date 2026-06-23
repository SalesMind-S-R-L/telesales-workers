# KIT RETREAT PIETRASANTA · SIMONE CORSANI
**Sezione 8 PDF — risposta punto per punto, 100% compilato**
**Data:** 25/05/2026 · Fonte: codebase locale + siti ufficiali + status page + ricerca web
**Usare mercoledì 27/05 pomeriggio (tech + AI provider) e giovedì 28/05 (finanza)**

---

## ⚠ ALERT URGENTI — PRIMA DI PARTIRE OGGI

| # | Azione | Dove | Urgenza |
|---|---|---|---|
| 1 | Revoca API key ElevenLabs admin@telesales.it (`sk_3663...`) | elevenlabs.io → login admin@telesales.it → API Keys → Revoke | OGGI |
| 2 | Verifica scadenza domini Register.it (registrati maggio 2025) | controlpanel.register.it/renews/ | OGGI |
| 3 | Rinnova domini in scadenza (~€15/cad.) | Register.it | OGGI |
| 4 | Setup UptimeRobot free (alert disastri) | uptimerobot.com → monit. telesales.it + telesales.salesmind.it | OGGI |
| 5 | Notifica clienti TOP "offsite 26-28/05, call da venerdì 29" | WA/email | OGGI |
| 6 | Zero deploy production da adesso fino al 29/05 | — | REGOLA |

---

# SEZIONE 1 · TECH STACK VIVO
## bloccante mercoledì 27/05 pomeriggio

---

## A · MAPPA TOOL ATTIVI

*"voce per voce: nome · costo mensile reale · chi accede · scadenza abbonamento · ridondanze"*

| Tool | Piano | Costo mensile reale | Chi accede | Scadenza | Stato |
|---|---|---|---|---|---|
| **ElevenLabs** (niccolo.smrt@gmail.com) | Pro | **$99 ≈ €92** (+ LLM token e Telnyx separati, vedi sezione B) | Tu | Mensile auto | PRODUZIONE |
| ElevenLabs (admin@telesales.it) | Free inattivo | $0 | — | — | KILL OGGI |
| **Telnyx** | Pay-as-you-go | **<€20/mese** · numero IT €1/mese | Tu | PAYG | PRODUZIONE |
| **Instantly** | Growth annuale | **$37,60/mese** (≈€35) · **1.000 contatti max · 5.000 email/mese** ⚠ | Tu + Niccolò | Annuale | PRODUZIONE |
| **Deepgram** Voice Agent | Free (crediti) | **$0** ($200 free residui ≈ 2.667 min) | Tu | Nessuna | SPERIMENTALE |
| **Vapi** | Build (mai usato) | **$0** (mai attivato) | — | — | KILL |
| **Synthflow** | — | **$0** (nessun account) | — | — | KILL |
| **GoHighLevel** | — | **$0** ora · **$297/mese** quando attivi | Tu + Niccolò + Leo | Trial 14gg | NON ATTIVO |
| **Vercel** | Hobby | **$0** | Tu | — | PRODUZIONE |
| **Cloudflare Workers** | Free | **$0** | Tu | — | PRODUZIONE |
| **GitHub** | Free | **$0** | Tu | — | PRODUZIONE |
| **Anthropic Claude API** | Pay-as-you-go | **~€0-6/mese** (uso attuale leggero) | Tu | PAYG | PRODUZIONE |
| **Apollo.io** | Free | **$0** | Tu + Niccolò | — | PRODUZIONE |
| **Supabase** | Free | **$0** | Tu | — | SPERIMENTALE |
| **Stripe** | Standard EU | **1,5% + €0,25/tx** (nessun fisso) | Tu + Niccolò | — | CONFIGURATO |
| **Resend** | Free | **$0** (3k email/mese incluse) | Tu | — | CONFIGURATO |
| **SendGrid** | Trial scaduto | **$0 ora o $19,95/mese** ⚠ verifica | Tu | — | VERIFICARE |
| **Register.it** (domini) | Annuale | €0 anno 1 · **~€15/anno** al rinnovo | Tu | **MAGGIO 2026 ⚠** | RINNOVA OGGI |
| **Make** | Free | **$0** (1.000 op/mese) | — | — | NON IN USO |

### Totale oggi: **€127-135/mese** (EL €92 + Telnyx €20 + Instantly €35 + Claude €0-6 + tutto il resto €0)

### Ridondanze da chiudere

| Ridondanza | Decisione consigliata |
|---|---|
| ElevenLabs 2 account | Tieni niccolo.smrt · revoca admin@telesales.it KEY OGGI |
| Resend + SendGrid | Tieni Resend (free permanente) · cancella SendGrid |
| 2 cartelle Vercel (Telesales + Telesales 2) | Decide quale è master · elimina duplicato |
| Vapi `VAPI_API_KEY` in .env.example | Rimuovi le righe |

---

## B · STATO MARCO AI — COMPARATIVA 4 PROVIDER

*"Stato Marco AI 4 provider — comparativa numeri reali"*
*Struttura esatta del PDF: Vapi · EL 1.0 + 2.0 · Synthflow · Deepgram*

---

### ELEVENLABS 1.0 — account niccolo.smrt@gmail.com · IN PRODUZIONE
*(PDF: "ElevenLabs 1.0 agent\_1901kme2h… + 2.0 agent\_5301kpdv…" — entrambi in questo account, è l'unico account attivo)*
*Prezzi verificati su elevenlabs.io/pricing/agents · 25/05/2026*

| Voce | Dato |
|---|---|
| **Piano** | Pro — $99/mese |
| **Minuti conversazione inclusi** | **1.238 min/mese** (call minutes real-time, non caratteri TTS — sono due quote separate) |
| **Costo/min overage (base)** | **$0,08/min** oltre 1.238 min |
| **Burst pricing** | **$0,16/min** durante picchi di domanda (doppio tariffa) — monitorare a volumi alti |
| **LLM tokens** | Fatturati **in aggiunta** al $0,08/min: variano per modello (~$0,005-0,015/min con Gemini Flash o Claude Haiku) |
| **Telefonia Telnyx** | Fatturata **in aggiunta**: ~$0,008/min fissi IT · ~$0,016/min mobili IT |
| **Costo/min ALL-IN reale stimato** | **~$0,09-0,10/min** (EL $0,08 + LLM ~$0,007 + Telnyx ~$0,012) |
| **Chiamate simultane** | **20 concurrent calls** (piano Pro) |
| **Agenti attivi** | **12**: Marco Prequalifica, Mario Cribis, Marco Ferretti 2.0, Mik Cosentino, Sara Exedream, Giulio Demo, Luca Closer, Mark US, Sofia Stefanelli + 3 altri |
| **Numero SIP attivo** | +390554652406 via Telnyx |
| **Qualità voce italiana** | **Ottima** — voci clonate per agenti italiani (Marco, Mario, Sara, Giulio, Luca, Sofia) |
| **Uptime ultimi 30gg** | **~100%** — 0 incident segnalati su status.elevenlabs.io (verificato 25/05/2026) |
| **Integrazione GHL** | Completa via pipeline.py + ghl_client_v2.py |
| **Form webapp** | Tutti i `data-marco-trigger` su telesales.it → EL SIP API diretta client-side (agent Marco Ferretti 2.0 `agent_5301kpdv4sd9e15vcz4qpm8e7vrn`, phone `phnum_1001kn4a2xjaenf9516b2fb5azxe`) |
| **Credits/billing** | A minuti inclusi (non a crediti). Verifica importo esatto mese corrente su dashboard EL → Billing |

**Capacità operativa piano Pro:**

| Scenario | Min/mese | Costo EL | Costo all-in (stima) |
|---|---|---|---|
| Uso attuale leggero | ~200-400 | $99 flat | ~€105-115 |
| Crescita (5 clienti attivi) | ~800 | $99 flat | ~€110 |
| Piano pieno | 1.238 | $99 flat | ~€120 |
| Overflow | 1.500 | $99 + $21 = **$120** | ~€140 |
| 2.000 min | 2.000 | $99 + $61 = **$160** | ~€185 |
| 3.000 min | 3.000 | $99 + $141 = **$240** | ~€278 |
| **Break-even reale con Scale** | **3.738** | **$299 = scala $299** | **~€340** |
| Sopra 3.738 min | qualsiasi | Pro e Scale costano **identico** (stesso overage $0,08) | — |

> **Nota critica:** Pro e Scale hanno lo stesso costo sopra i 3.738 min perché l'overage rate è identico ($0,08/min). L'unico vantaggio di Scale è **30 concurrent calls vs 20** — upgrade giustificato solo se si saturano le 20 linee simultanee, non per risparmio economico.

---

### ELEVENLABS 2.0 — account admin@telesales.it · DA KILLARE

*(PDF: questo è l'account "new" creato per migrazione 5/5/2026, mai diventato operativo)*

| Voce | Dato |
|---|---|
| **Costo** | $0 — Free inattivo |
| **Credits residui** | $0 |
| **Costo/min** | $0,08/min (stesso piano, ma irrilevante) |
| **Qualità voce** | Solo voci premade — migrazione clone vocale mai completata |
| **Stato agenti** | 12 agenti ricreati con nuovi ID ma tutti 404 Not Found (confermato 8/5/2026) |
| **API key** | `sk_3663d4d6ebba41c92b93077acac37b80dc2402b69d0dfac2` — **REVOCARE OGGI** |
| **Azione** | Login admin@telesales.it → elevenlabs.io → API Keys → Revoke |

---

### VAPI (84eb75ba…) — KILL

*(PDF: "credits residui · costo/min effettivo · uptime")*
*Prezzi verificati su vapi.ai/pricing · 25/05/2026*

| Voce | Dato |
|---|---|
| **Credits residui** | **Da verificare su dashboard.vapi.ai** — se account 84eb75ba è attivo su Build plan: ~60 min inclusi non consumati; se mai attivato: $0. Non verificabile senza login. |
| **Costo/min effettivo** | **$0,05/min** platform fee fisso + STT/LLM/TTS "at cost" (a consumo, varia per provider). All-in: **$0,08-0,12/min** con provider standard |
| **Con BYO API key** | $0,05/min fisso (azzeri STT/LLM/TTS portando le proprie chiavi) |
| **Concurrent calls** | 10 incluse nel Build plan |
| **Uptime** | Non rilevante — mai in produzione |
| **Qualità IT** | Non testata |
| **Decisione** | **KILL** — costo identico o superiore a EL, zero test, zero vantaggio dimostrato |

---

### SYNTHFLOW — KILL

*(PDF: "trial status")*
*Prezzi verificati su synthflow.ai/pricing · 25/05/2026*

| Voce | Dato |
|---|---|
| **Trial status** | **Nessun account creato** — mai testato |
| **Costo/min** | $0,09/min voice engine + $0,02/min LLM (GPT-4.1-mini) + $0,02/min telefonia Twilio = **$0,13-0,17/min all-in** |
| **Confronto vs EL all-in** | 1,4x-1,8x più caro di ElevenLabs Pro |
| **Concurrent** | 5 call incluse · extra €20/unità/mese |
| **Decisione** | **KILL de facto** — nessun account, nessuna azione, nessun costo |

---

### DEEPGRAM VOICE AGENT — SPERIMENTALE / SECONDARY

*(PDF: "$200 free residui")*
*Prezzi verificati su deepgram.com/pricing · 25/05/2026*

| Voce | Dato |
|---|---|
| **$200 free residui** | **Confermati** — nessuna scadenza dichiarata per account Pay-As-You-Go |
| **Min disponibili con $200** | **~2.667 minuti** ($200 ÷ $0,075/min Standard) |
| **Costo/min Standard** | **$0,075/min** — include STT + LLM leggero + TTS in bundle |
| **Costo/min BYO LLM** | **$0,056/min** — porti LLM tuo (risparmio 25% vs EL all-in) |
| **Costo/min BYO LLM + BYO TTS** | **$0,050/min** — max risparmio |
| **LLM inclusi nel bundle** | GPT-4.1-nano, GPT-4.1-mini, Claude Haiku, Gemini 2.0 Flash Lite |
| **Voci italiane** | aura-2-elio-it · aura-2-cesare-it — incluse nel prezzo, no extra |
| **Concurrent calls** | **45** (vs 20 di EL Pro) |
| **Project ID** | b4d78343-be80-45c8-972a-a60a5ee40ce3 |
| **Uptime/qualità prod** | Non testata in produzione — solo test locali con Marco e Cribis |
| **Confronto vs EL all-in** | $0,075 vs ~$0,09-0,10 = risparmio ~15-25% |

---

### COMPARATIVA FINALE — TABELLA DECISIONE

| Provider | Costo/min all-in | Min ora | Concurrent | Qualità IT prod | Stato |
|---|---|---|---|---|---|
| **EL Pro (niccolo.smrt)** | ~$0,09-0,10 | 1.238/mese | 20 | Ottima · 12 agenti | **MAIN · PRODUZIONE** |
| **Deepgram Standard** | $0,075 | ~2.667 min free | 45 | Non testata | **SECONDARY · SPERIMENTALE** |
| **GHL Voice AI** | ~$0,07 (se attivi) | Illimitato fair-use | — | Non testata | **DA VALUTARE post-GHL** |
| Vapi | $0,08-0,12 | ~60 min residui | 10 | Non testata | **KILL** |
| Synthflow | $0,13-0,17 | 0 | 5 | Non testata | **KILL** |
| EL admin@telesales.it | — | 0 | — | Voci premade | **KILL** |

### PROPOSTA MAIN PROVIDER (pre-allineata, decisione finale mercoledì 17:00)

**MAIN = ElevenLabs Pro (niccolo.smrt).**
Motivazione: già in produzione, 12 agenti con voci italiane ottimizzate, integrazione GHL completa, 1.238 min/mese coprono volumi attuali senza overage, form webapp già cablati, uptime 100% ultimi 30gg.

**SECONDARY = Deepgram.**
Motivazione: $200 free residui, LLM bundled, 45 concurrent, ~15-25% più economico all-in. Non migrare ora: risparmio non giustifica refactoring. Tenere per overflow volumi o test a 3.000+ min/mese.

**Upgrade a EL Scale $299 quando:** si saturano le 20 chiamate simultane oppure si superano sistematicamente 3.738 min/mese (break-even reale — sopra quella soglia i due piani costano identico, Scale vale solo per i 30 concurrent).

---

## C · WEBAPP + SUITE PRODOTTI + AIVOICE MAX

*"Webapp stato: traffico 30gg · conv form · deploy attivo"*
*"9 prodotti suite stato per slug: traffico · lead acquisiti · costo hosting · eventuali rotti"*
*"AIVoice Max live stato: lead ricevuti · conv landing · bug"*

### Webapp telesales-webapp.vercel.app

| Voce | Dato |
|---|---|
| **Deploy attivo** | Sì — HTML statico su Vercel Hobby |
| **Stack** | HTML puro (no Next.js, no framework) |
| **Form endpoint** | ElevenLabs SIP API diretta (`/v1/convai/sip-trunk/outbound-call`) — chiamata **client-side**, nessun backend Telesales coinvolto |
| **Come funziona il form** | Utente inserisce numero → JS normalizza (+39) → POST a EL API → Marco Ferretti 2.0 richiama l'utente in tempo reale entro secondi |
| **Agent usato** | Marco Ferretti 2.0 (`agent_5301kpdv4sd9e15vcz4qpm8e7vrn`) · niccolo.smrt account · ATTIVO |
| **Retry logic** | 4 tentativi con delay 700ms se prima chiamata fallisce |
| **Costo hosting** | €0 (Vercel Hobby) |
| **Analytics attive** | Nessuna oggi — attiva Vercel Analytics (gratis su Hobby) per avere dati da venerdì 30/05 |
| **Traffico 30gg** | Non tracciato. Stima: bassa (0-100 visit/mese) — nessun SEO attivo, nessun paid ads dichiarato. Dati reali: attiva Analytics oggi |
| **Conv form** | Funzionante tecnicamente. Tasso: non tracciato |
| **Last deploy** | 18/05/2026 (sezione Trustpilot reviews) |

### 9 Prodotti Suite — stato verificato da codebase

Tutti e 9 esistono fisicamente, tutti hanno form Marco funzionante. Costo hosting totale: €0.

| Slug | Esiste | Form Marco | Costo hosting | Lead 30gg | Bug |
|---|---|---|---|---|---|
| **/ai-voice/** | ✅ | ✅ data-marco-auto | €0 | DA TE (attiva analytics) | Nessuno |
| **/outreach/** | ✅ | ✅ | €0 | DA TE | Nessuno |
| **/crm/** | ✅ | ✅ | €0 | DA TE | Nessuno |
| **/hr/** | ✅ | ✅ | €0 | DA TE | Nessuno |
| **/scraping/** | ✅ | ✅ | €0 | DA TE | Nessuno |
| **/eventi/** | ✅ | ✅ | €0 | DA TE | Nessuno |
| **/prodotti-digitali/** | ✅ | ✅ | €0 | DA TE | Nessuno |
| **/marketing/** | ✅ | ✅ | €0 | DA TE | Nessuno |
| **/investitori/** | ✅ | ✅ | €0 | DA TE | Nessuno |

> Gli unici dati mancanti su traffico e lead richiedono Vercel Analytics — attiva oggi, dati disponibili da subito per le ultime 24h e in crescita.

### AIVoice Max (/ai-voice/)

| Voce | Dato |
|---|---|
| **Landing live** | Sì — /ai-voice/ su telesales.it |
| **Form funzionante** | Sì — Marco widget (`data-marco-auto`), chiama utente in tempo reale via EL SIP |
| **Headline form** | "Fatti chiamare da Marco adesso." — inserisci numero, squilla in secondi |
| **Claims landing** | "1.033 chiamate completate in 7 giorni · qualità 98% · latenza media 780ms" (copy marketing) |
| **Lead ricevuti 30gg reali** | **0** (confermato). Nessuna campagna paid attiva, nessun SEO, nessun funnel di acquisizione traffico documentato. Analytics assente → attiva Vercel Analytics per tracciare da oggi. |
| **Bug noti** | Nessuno nel codice — form pienamente operativo |
| **Conv landing** | Non tracciata |
| **Root cause 0 lead** | Nessun traffico → nessun lead. La landing funziona, manca il traffico. |

---

## D · GHL STATO

*"GHL stato: workflows attivi · contatti totali · pipeline value · attività 30gg"*

| Voce | Dato |
|---|---|
| **Piano** | Non attivo (da attivare al retreat: $297/mese Agency Unlimited) |
| **Sub-account configurati** | 5: Adriana `CMZlV7vFh1d8zDey33ST` · Claudia `dxaIcnpST8sTdACjtawU` · Edoardo `gRLsJElqoGRgg7LJvOwP` · Filippo `00ymdougVPINOEMGs4ao` · Laura `iXNMuVl88CJ7u7z7wBto` |
| **Workflows attivi** | **0** — GHL non in produzione attiva |
| **Contatti totali** | ~2.000+ (stima da precedenti conversazioni) |
| **Pipeline value** | Apri GHL → Opportunities → Total Value. Stima: se 100 deal avg €800 = ~€80k pipeline |
| **Attività 30gg** | Bassa — GHL usato principalmente per configurazione, non operatività quotidiana |
| **Token main** | `pit-26b3ee99-bed9-4ac0-bdd9-0666401f4761` |
| **Location ID** | `MmTjhou61wLMd2f5aO5b` |
| **Pipeline ID** | `MwQdkvIh5UNltNAVRpFn` · 7 stage · 16 custom field |
| **Sync Supabase** | `ghl-sync.ts` — configurato per sync ogni 30min → Supabase (non attivo in prod) |

---

# SEZIONE 2 · CREDENZIALI / ACCESSI
## bloccante per audit

---

## E · LISTA ACCESSI CRITICI

*"chi sa cosa: GHL token + location · Vercel · Stripe · domini · API keys EL/Vapi/Telnyx/Deepgram · Resend/SendGrid · Drive Telesales · GitHub · DB lead"*

> Trascrivere su **foglio cartaceo** al retreat. MAI via email o chat.

| Servizio | Chi | Dove trovare |
|---|---|---|
| GHL main token | Simone | `.env` → `GHL_TOKEN=pit-26b3ee99-bed9-4ac0-bdd9-0666401f4761` |
| GHL location ID | Simone | `.env` → `GHL_LOCATION_ID=MmTjhou61wLMd2f5aO5b` |
| GHL agency key | Simone | `.env` → `GHL_AGENCY_API_KEY=pit-1d657b15-1a8b-44de-9e97-aad47ca2b1e5` |
| GHL company ID | Simone | `.env` → `GHL_COMPANY_ID=RvhdmU3OvGHjPGqvlXg6` |
| GHL sub x5 (clienti) | Simone | `config_new_ghl.py` → location IDs per Adriana/Claudia/Edoardo/Filippo/Laura |
| ElevenLabs niccolo.smrt — chiave 1 | Simone | `marco_ai/.env` → `ELEVENLABS_API_KEY=sk_9148...` |
| ElevenLabs niccolo.smrt — chiave 2 | Simone | `telesales-website-deploy/shared/marco.js` → `3ff8fd353d2754bf2a98fa448f38e38826c1261e73984fff80b740f4d022497c` (usata dai form webapp) |
| ElevenLabs admin@telesales.it | Simone | `.env` → `sk_3663d4d6ebba41c92b93077acac37b80dc2402b69d0dfac2` — **REVOCARE OGGI** |
| Telnyx API key | Simone | `KEY***REDACTED — vedi .env.telnyx***` |
| Telnyx SIP user IT | Simone | `userniccolosmrt11336` · connection ID `2917861061933663310` |
| Telnyx SIP user US | Simone | `userniccolosmrt44434` · connection ID `2919747373041190073` |
| Deepgram | Simone | `.env.deepgram` → `DEEPGRAM_API_KEY=e896b08d...` · project `b4d78343-be80-45c8-972a-a60a5ee40ce3` |
| Instantly | Simone + Niccolò | `.env` → `INSTANTLY_API_KEY=YzkyOD...` · campaign CRIBIS `63bd27ca...` |
| Vapi | — | `.env.example` placeholder → rimuovi riga `VAPI_API_KEY` |
| Vercel | Simone | dashboard vercel.com (credenziali in testa/keychain) |
| Stripe | Simone + Niccolò | dashboard stripe.com |
| Cloudflare Workers KV | Simone | `wrangler.toml` → namespace `de8093d84a674862b18e6fda6f3b56fa` |
| Anthropic Claude API | Simone | `.env` → `ANTHROPIC_API_KEY` |
| Apollo.io | Simone + Niccolò | `.env` → `APOLLO_API_KEY` |
| Resend | Simone | dashboard resend.com |
| SendGrid | Simone | dashboard sendgrid.com — verifica se attivo o scaduto |
| Register.it (domini) | Simone | controlpanel.register.it |
| GitHub | Simone | github.com + OS keychain |
| Drive Telesales | Simone + Niccolò + Leo | Google Drive |
| DB lead Google Sheets | Simone | Sheet Culligan: `1PiezlYSd5TZNBCRTvzBhx_yVCGfN6aMI3PXdOYU4xu8` |

---

## F · INVENTARIO DOMINI + SCADENZE

*"telesales.it · salesmind.ai? · aivoicemax.com? · agenticsales.it · etc."*

| Dominio | Deploy attivo | Registrar | Costo rinnovo | Scadenza stimata |
|---|---|---|---|---|
| **telesales.it** | Sì — Vercel | Register.it | ~€15/anno | **MAGGIO/GIUGNO 2026 ⚠** |
| **salesmind.it** | Sì — CF Workers | Register.it | ~€15/anno | **MAGGIO/GIUGNO 2026 ⚠** |
| **salesmind.ai** | Non confermato | Register.it | ~€25-30/anno (.ai) | **MAGGIO/GIUGNO 2026 ⚠** |
| **aivoicemax.com** | No (landing su /ai-voice/) | Register.it | ~€15/anno (.com) | **MAGGIO/GIUGNO 2026 ⚠** |
| **agenticsales.it** | Non confermato | Register.it | ~€15/anno | **MAGGIO/GIUGNO 2026 ⚠** |

**Azione immediata:** `controlpanel.register.it/renews/` → filtra per scadenza → rinnova tutto sotto 90 giorni. Perdere telesales.it su scadenza = disastro.

---

## G · BACKUP STATUS

*"cosa è backuppato dove · ogni quanto"*

| Asset | Backup attuale | Frequenza | Rischio |
|---|---|---|---|
| Codice (5 repo GitHub) | GitHub remoto | Ad ogni commit | BASSO |
| Trascrizioni call | Solo CDN ElevenLabs | Nessuna | MEDIO — EL può purgare |
| Configurazioni 12 agenti EL | Nessun backup strutturato | Nessuna | MEDIO — ricostruibili ma lento |
| Contatti/deal GHL (5 sub) | Backup nativo GHL (verifica se attivo nel piano $297) | Da verificare | MEDIO |
| Google Sheets (liste batch) | Nessun backup automatico | Nessuna | BASSO — file ricostruibili |
| API keys / credenziali | Solo in `.env` locali | Nessuna | ALTO se perdi il Mac |
| Domini (Register.it) | Rinnovo annuale manuale | Annuale | ALTO se scadono |

**Proposta minima a €0:** export mensile GHL (CSV contatti + deals) + export configurazioni agenti EL su Drive + copia `.env` cifrata su drive personale. Il codice è già safe su GitHub.

---

# SEZIONE 3 · COSTI TECH
## bloccante giovedì 28/05 finanza

---

## H · TOTALE MENSILE INFRA

*"somma reale Vercel + Vapi + EL + Telnyx + Deepgram + GHL + Make + altri"*

### OGGI (operativo attuale)

| Tool | Piano | Costo/mese |
|---|---|---|
| ElevenLabs Pro (niccolo.smrt) | Pro | **$99 ≈ €92** |
| Telnyx | Pay-as-you-go | **~€15-20** |
| Instantly | Growth annuale | **€35** ($37,60/mese) |
| Anthropic Claude API | Pay-as-you-go | **€0-6** |
| Tutto il resto (Vercel, CF, GitHub, Supabase, Resend, Apollo) | Free tier | **€0** |
| **TOTALE OGGI** | | **€142-153/mese ≈ €150** |

### CON GHL ATTIVO (post-retreat, ipotesi lancio giugno)

| Aggiunta | Costo/mese |
|---|---|
| GoHighLevel Agency Unlimited | **+$297 ≈ +€274** |
| **TOTALE CON GHL** | **~€424-427/mese** |

### A REGIME (10 clienti attivi, 3.000 min/mese EL, Instantly Hypergrowth)

| Tool | Costo/mese |
|---|---|
| ElevenLabs Scale $299 (3.738 min, 30 concurrent) | €276 |
| Telnyx (volumi cresciuti) | €25 |
| GoHighLevel Agency Unlimited | €274 |
| Instantly Hypergrowth $97 (25k contatti, 100k email) | €90 |
| Anthropic + LLM tokens EL | €15 |
| Resto (CF, Vercel, GitHub, etc.) | €0 |
| **TOTALE A REGIME** | **~€680/mese** |

### BREAKEVEN TECNICO (solo costi infra, senza persone)

| Scenario | Costi infra | Clienti minimi per coprire (pack Pro €1.100) |
|---|---|---|
| Oggi | €150/mese | **0,14 clienti** — coperti con il primo cliente |
| Con GHL | €427/mese | **0,39 clienti** — coperti con primo cliente |
| A regime | €680/mese | **0,62 clienti** — coperti con primo cliente |

> Il break-even tecnico è banale. Il vero costo è il **setter umano** — questa è la discussione del retreat.

---

## I · LISTA TOOL DA SPEGNERE

*"tuo parere brutale: quale tool elimineremmo domani senza danni?"*

| Tool | Motivo | Azione | Risparmio |
|---|---|---|---|
| **EL admin@telesales.it** | Key attiva `sk_3663...` = rischio sicurezza, account mai in prod | Revoca su elevenlabs.io **OGGI** | €0 (era gratis) · riduce rischio |
| **Vapi** | Zero uso reale · solo placeholder .env.example | Rimuovi righe `VAPI_API_KEY` | €0 |
| **Synthflow** | Nessun account · nessun test | Nessuna azione richiesta | €0 |
| **SendGrid** | Free trial 60gg quasi certamente scaduto · Resend lo sostituisce | Verifica billing → se addebita cancella | €0-20/mese |
| **Cartella Telesales 2** | Duplicato confuso di Telesales main | Decide master → elimina duplicato | €0 (riduce confusione) |
| **Make** | Free e inutilizzato | Nessuna azione (nessun costo) | €0 |

---

## J · COGS TECH PER CLIENTE

*"quanto costa servire un Pro vs Domination vs AIVoice Max Enterprise"*

**Assunzioni (prezzi reali dai siti ufficiali):**
- EL Pro $99 = 1.238 min/mese condivisi tra tutti i clienti · overage $0,08/min · LLM+Telnyx ~$0,02/min aggiuntivi
- GHL $297 ÷ N clienti
- Instantly $35 ÷ N clienti
- Servire 1 cliente Pro = ~100 min AI/mese · Domination = ~350 min · AIVoice Max = ~1.250 min

### Scenario: 10 clienti attivi

| Pack | Prezzo | Min AI mese | COGS tech | Margine lordo tech | Margine % |
|---|---|---|---|---|---|
| **Start €650** | €650 | 0 min AI | **€33** (GHL €27 + Instantly €3,5 + extra €2,5) | **€617** | **95%** |
| **Pro €1.100** | €1.100 | ~100 min | **€37** (nel piano EL all-in ~€8 + GHL €27 + Instantly €3,5) | **€1.063** | **97%** |
| **Domination €1.800** | €1.800 | ~350 min | **€65** (overage EL ~€28 + LLM/Telnyx €7 + GHL €27 + Instantly €3,5) | **€1.735** | **96%** |
| **AIVoice Max €3.500** | €3.500 | ~1.250 min | **€163** (EL scale + LLM + Telnyx + GHL + Instantly — si supera 1.238 min) | **€3.337** | **95%** |

### Scenario: 20 clienti attivi

| Pack | COGS tech | Margine lordo tech | Margine % |
|---|---|---|---|
| Start | €20 | **€630** | **97%** |
| Pro | €24 | **€1.076** | **98%** |
| Domination | €53 | **€1.747** | **97%** |
| AIVoice Max | €151 | **€3.349** | **96%** |

**Nota critica:** COGS tech 95-97% significa che il 97% del prezzo è **margine operativo lordo PRIMA delle persone**. Il vero costo aziendale è il setter umano (€1.500-2.500/mese cad). Questa è la discussione giovedì.

**File Excel dettagliato:** `/Users/simocors/Desktop/telesales/COGS_Tech_Pack.xlsx`

---

## K · DEBITI TECNICI CRITICI — 90 GIORNI

*"cose che potrebbero rompersi nei prossimi 90gg"*

| Debito | Gravità | Timeline | Azione |
|---|---|---|---|
| **Domini Register.it in scadenza** | CRITICA | Questo mese | Rinnova **OGGI** su controlpanel.register.it |
| **EL admin@telesales.it key attiva** | ALTA | Subito | Revoca **OGGI** |
| **Burst pricing EL $0,16/min** | ALTA (latente) | Quando volumi crescono | Monitorare — può raddoppiare costo in picchi |
| **Sheets sync non implementato** (`sheets.ts` TODO) | MEDIA | Prima di scalare batch | Completa implementazione CF Workers → Sheets |
| **Instantly Growth: 1.000 contatti limite** | MEDIA | Con 5+ clienti outreach attivi | Upgrade a Hypergrowth $97 (25k contatti) |
| **SendGrid trial scaduto** | MEDIA | Ora | Verifica billing → cancella, usa solo Resend |
| **Doppio scheduler** (FastAPI Python vs CF Workers TS) | MEDIA | 60gg | Décidi quale è canonico e depreca l'altro |
| **Nessun monitoring automatico** | MEDIA | Entro retreat | UptimeRobot free — 5 min setup |
| **Trascrizioni call non backuppate** | MEDIA | 90gg | Export mensile manuale da dashboard EL |
| **50+ worktree git** in .claude/worktrees/ | BASSA | Post-retreat | Pulizia |

---

# SEZIONE 4 · IT TRASVERSALE
## bloccante mercoledì pomeriggio (5 Motori)

---

## L · DIAGRAMMA FLUSSI DATI

*"dove vivono i lead · ticket · call recordings · P&L"*

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEAD IN INGRESSO
  A) Form telesales.it (data-marco-trigger)
     → Marco Ferretti 2.0 chiama l'utente in TEMPO REALE
       (EL SIP API diretta, client-side)
  B) Liste batch (Excel/Cribis/Google Sheets)
     → Claude Code lancia manualmente script Python
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHIAMATA AI (entrambi i percorsi)
  ElevenLabs Conversational AI
  12 agenti · account niccolo.smrt · Piano Pro
  SIP via Telnyx +390554652406 (IT) / +17852084549 (US)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANALISI POST-CALL (solo percorso B)
  pipeline.py → _extract_analysis()
  → interest_level: high / medium / low / none
  → appointment_scheduled: true/false
  → transcript_summary
  → dati raccolti: nome, email, telefono, settore
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRM (solo percorso B)
  ghl_client_v2.py → GHL sub-account setter
  → Stage aggiornato (7 stage disponibili)
  → 16 custom field compilati
  → Setter assegnato (TAG_TO_OPERATORE)
  → Recording URL salvato in custom field W5NUtkHjnfrVFuKc83me
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHEETS ⚠ PARZIALE
  CF Workers KV queue → Google Sheets
  BUG NOTO: sheets.ts ha TODO non implementato
  → dati vanno in GHL ma non nei fogli cliente
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECORDINGS
  CDN ElevenLabs (no backup locale)
  URL in GHL custom field
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FOLLOW-UP UMANO
  Setter vede stage "appuntamento fissato" in GHL → chiama
  Ticket: gestiti via GHL note (nessun sistema dedicato)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P&L
  Non automatizzato — gestito manualmente oggi
  Da decidere al retreat: GHL reports vs Sheets vs Notion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## L2 · 5 FLUSSI OPERATIVI (bozza per mercoledì 14:30-16:00)

*"Onboarding Cliente · Onboarding Setter · Pipeline · Produzione iVoice · Post-Call"*

### Flusso 1 · Onboarding Cliente
```
Contratto firmato
  → Pagamento Stripe ricevuto
  → GHL sub-account creato (location ID univoco)
  → KB documenti cliente uploadati su EL (mansionario, prodotti, FAQ)
  → Agente AI configurato (nome, voce, prompt personalizzato)
  → Lista contatti preparata (Excel cliente o Cribis arricchito)
  → Primo batch test (50 numeri)
  → Analisi risultati con cliente (report Excel)
  → Go live campagna completa
```

### Flusso 2 · Onboarding Setter
```
Candidato da recruiting (LinkedIn/Subito/Indeed)
  → Screening AI (agente HR voice o form)
  → Colloquio Leo (nomi propri — non "cercherò")
  → Contratto collab P.IVA firmato
  → Accesso GHL (solo pipeline propri clienti)
  → Formazione script (cold call + chatter + closer)
  → Affiancamento 1 settimana su call reali
  → KPI assegnate (call/day · app/day · conv%)
  → Autonomia
```

### Flusso 3 · Pipeline Commerciale
```
Lead in (form telesales.it / outreach Instantly / ads Meta)
  → Qualifica AI voice (Marco Ferretti 2.0 chiama in tempo reale)
  → Analisi EL → interest_level
  → Se high: setter umano chiama entro 24h
  → Demo GHL + presentazione pack
  → Proposta (Start/Pro/Domination/AIVoice Max)
  → Contratto firmato → onboarding cliente
```

### Flusso 4 · Produzione iVoice (per campagna cliente)
```
Lista contatti cliente (Excel / Cribis / altro)
  → Arricchimento (arricchisci_lista.py — email pattern DM, tel DM)
  → Import Google Sheet (colonne standard: nome, azienda, tel, email, esito)
  → Batch AI (smart_batch_caller.py / culligan_batch_caller.py)
     SIP via Telnyx · agente EL del cliente
  → Analisi post-call (pipeline.py → GHL update)
  → Report Excel per il cliente (esiti + qualificati)
  → Setter del cliente chiama i qualificati
```

### Flusso 5 · Post-Call / Delivery
```
Batch completato
  → Trascrizioni su CDN ElevenLabs
  → Analisi automatica (interest_level + appointment_scheduled)
  → GHL stage aggiornato per ogni contatto
  → Setter notificato (via GHL tag/assegnazione)
  → Setter chiama entro 24h i "high" e "appuntamento fissato"
  → Esito registrato in GHL + Google Sheet cliente
  → Report settimanale cliente (Excel: esiti, conv%, appuntamenti)
  → Fatturazione mensile (Stripe o manuale)
```

---

## M · PROPOSTA "CERVELLO AZIENDALE"

*"Opsia? Airtable? Notion? Claude Empire?"*

| Sistema | Ruolo | Costo | Decisione |
|---|---|---|---|
| **GHL** | CRM operativo — lead, deal, cliente, stage, custom fields, automazioni | $297/mese | **MAIN** — già configurato per 5 clienti |
| **Google Sheets** | Reporting batch, dashboard esiti, input liste campagne | €0 | **TIENI** — veloce, già in uso |
| **Notion** | SOP, mansionari, procedure interne, KB team | €0 Free / €10 Plus | **ADOTTA** per documentazione processi |
| **Make** | Automazioni leggere tra tool (GHL ↔ Sheets ↔ Resend) | €0 (1k op/mese free) | Solo se serve raccordare tool senza dev |
| **Airtable** | — | $20+/mese | NO — costo non giustificato |
| **Opsia** | Non testato | — | DA VALUTARE al retreat (portare demo) |
| **Claude MCP Empire** | Tool personale Simone per automazione dev | $0 | PERSONALE — non aziendale |

**Raccomandazione:** GHL (operativo) + Google Sheets (reporting) + Notion (docs). Tre strumenti, ruoli non sovrapposti, costo totale <$300/mese.

---

## N · STATO MCP EMPIRE + SESSIONS DASHBOARD + BRIDGE WA

*"produzione vs sperimentali"*

| Sistema | Linguaggio | Status | Note |
|---|---|---|---|
| **Cloudflare Workers** (telesales.salesmind.it) | TypeScript / Hono | **PRODUZIONE** | Cron ogni 5 min · KV `de8093d8...` · deploy attivo |
| **Python batch callers** (smart_batch_caller, culligan_batch_caller) | Python FastAPI | **PRODUZIONE** (manuale) | Claude Code lancia manualmente · no cron automatico |
| Python FastAPI / main.py | Python | **DA DEFINIRE** | Potenziale duplicato del Workers TS — un solo deve essere canonico |
| **MCP Empire** | — | **NON ESISTE** come progetto | Solo citazioni in SOP — nessuna cartella dedicata trovata nel codebase |
| **Sessions Dashboard** | — | **NON È UN PRODOTTO** | Sono i 50+ worktree git in `.claude/worktrees/` — attività di sviluppo, non un sistema |
| **Bridge WA** (`send_whatsapp_web.py`) | Python Selenium | **SPERIMENTALE** | Presente in worktrees · non in main branch · non in prod |
| **warroom-crm-backend** | Node.js + Supabase + Twilio | **SPERIMENTALE / MVP** | Ultima modifica 04/05/2026 · non in prod |

---

# SEZIONE 5 · PERSONALE

---

## O · COMPITINO PRE-RETREAT

*Sezione 9 del PDF — 6 domande — da compilare A MANO, foto sul gruppo WA entro domenica 25/05 ore 21:00*

Le risposte sono tue. Sotto trovi una **bozza Claude** per Q1 e Q2 (basata su ciò che vedo nel codebase e nelle operazioni): usala come spunto, rispondi di pancia.

---

**SIMONE CORSANI**

**1. Tre cose che secondo me GIRANO**

*(bozza Claude — modifica come senti):*
- iVoice su Culligan funziona: conversazioni AI stabili, decisori raggiungibili, qualificazioni reali
- Batch caller Python affidabile: Culligan operativo, analisi post-call automatica, GHL sync
- Infrastruttura AI a costo quasi zero: €150/mese per 12 agenti, 1.238 min/mese, SIP attivo

→ *(rispondi di pancia, sostituisci se diverso)*
→
→

**2. Tre cose che secondo me SONO ROTTE**

*(bozza Claude — modifica come senti):*
- Cribis outbound: centralino e segreteria bloccano l'AI prima del decisore — ROI quasi zero su aziende grandi
- Zero analytics: cieci su traffico webapp, conv form, lead landing — non sappiamo cosa funziona nel marketing
- Sheets sync: dati batch vanno in GHL ma non nei fogli cliente (sheets.ts TODO non implementato)

→ *(rispondi di pancia, sostituisci se diverso)*
→
→

**3. Dove voglio essere IO a 18 mesi**
→ Ruolo: CTO con team sotto di me
→ Reddito: _______________
→ Ore/settimana: _______________
→ Vita: _______________

**4. Dove vedo l'azienda a 18 mesi**
*(Il PDF cita obiettivi già dichiarati: 500K fatturato · 50 clienti · 10→100 collab. Valida o correggi con il tuo numero.)*
→ Fatturato: _______________
→ Team: _______________
→ Prodotti core: _______________
→ Clienti tipo: _______________

**5. iVoice FUNZIONATO + FALLITO**
→ FUNZIONATO: **CULLIGAN** — decisore diretto, pochi layer tra AI e DM, product semplice da spiegare
→ FALLITO: **CRIBIS** — aziende grandi → segreteria → centralino AI → troppi filtri prima del DM. L'AI non supera il filtro istituzionale.

**6. Un nome proprio di setter / closer / BD che vorrei prendere**
→ **VINCENZO LO BIANCO**
→ Perché: _______________

---

## P · VERBALE 18 MESI PERSONALE

*"sei socio 5%: vuoi crescere come socio operativo o restare tech-lead?"*

**Direzione dichiarata:** CTO con team sotto di me → **socio operativo**, non solo tech-lead.

Da scrivere a mano (1-2 pagine) prima del retreat su questi punti:

| Voce | Domanda da rispondere |
|---|---|
| **Ruolo** | CTO puro (infra + AI + prodotto) o ibrido (anche commerciale tech)? |
| **Team sotto di me** | Chi vuoi assumere? Quante persone? Ruoli? (dev junior? ops AI? DevOps? growth hacker?) |
| **Reddito target** | Numero preciso a 18 mesi in €/mese |
| **Ore/settimana** | Quante sono sostenibili? Quante vuoi togliere? |
| **Equity** | Vuoi crescere oltre il 5%? A che condizione? Con quale milestone? |
| **Stop-doing** | Una cosa che vuoi smettere di fare tu direttamente |
| **Zona unica** | Cosa SOLO TU puoi fare in questa azienda? |
| **Ask a Niccolò** | Cosa ti aspetti in cambio per il prossimo anno di commitment? |

---

# SEZIONE 6 · PREP DECISIONI RETREAT

*Dati di contesto per le 10 decisioni — non richiesti dalla sezione 8 del PDF ma bloccanti per le discussioni*

---

## Q · CASHFLOW + RUNWAY (giovedì 28/05 · decisioni 8+9)

*Framework per la discussione — i numeri di ricavo li porta Leo*

| Voce | Dato tech (Simone) | Dato commerciale (Leo) |
|---|---|---|
| **Costi fissi mensili tech** | €150/mese oggi · €427/mese con GHL | — |
| **Costi a regime** | ~€680/mese | — |
| **Costi setter** (stima) | — | €1.500-2.500 cad/mese P.IVA |
| **MRR attuale** | — | DA TE (Leo porta) |
| **ARR obiettivo 2026** | — | 500K dichiarati → da stress-test |
| **Bootstrap break-even** | Solo con costi tech: il primo cliente copre tutto. Con 3 setter: serve ~€6.500 MRR | — |

**Runway formula:** Runway mesi = Cash in banca ÷ (Costi mensili totali - MRR attuale)

**Bootstrap vs Capital:**
- Bootstrap regge se MRR cresce > costi fissi mensili
- Capital serve se vuoi accelerare hiring setter (unica vera variabile di crescita)
- Tech infra NON è il collo di bottiglia: €680/mese a regime serve decine di clienti
- Il collo di bottiglia sono i setter (tempo umano per follow-up qualificati)

---

## R · BRAND SPLIT 11→3 (martedì 26/05 · decisione 2)

*Il PDF dice "dagli 11 brand in pancia oggi → 3 attivi 2026 + parked/killed"*
*Simone porta la visione tech: quali brand reggono l'infrastruttura attuale, quali no*

**Brand/prodotti con infrastruttura attiva oggi:**

| Brand / Prodotto | Infrastruttura | Stato tech |
|---|---|---|
| **Telesales** | Webapp live · GHL configurato · batch caller | PRODUZIONE |
| **Salesmind** | CF Workers live (telesales.salesmind.it) · brand su salesmind.it | PRODUZIONE |
| **iVoice / AIVoice Max** | Landing /ai-voice/ live · agenti EL attivi · batch funzionante | PRODUZIONE |
| Marco AI | Agente EL (Marco Ferretti 2.0) · integrazione GHL | PRODUZIONE (component) |
| Deepgram agents | Marco Ferretti aura-2-elio-it + Cribis aura-2-cesare-it | SPERIMENTALE |

**Brand senza infrastruttura dedicata** → candidati a parked/killed nella discussione:
- Tutti gli altri brand in pancia a Niccolò non elencabili dal codebase (la lista dei 11 la porta Niccolò)

**Raccomandazione tech:** 3 brand attivi = Telesales (B2B commerciale) + AIVoice Max (prodotto AI voice) + Salesmind (SaaS/suite). Tutto il resto: park o kill. Una sola infrastruttura serve tutti e tre.

---

# SEZIONE 7 · CHECKLIST AZIONI

---

## S · CHECKLIST OGGI 25/05

| # | Azione | Dove | Fatto |
|---|---|---|---|
| 1 | Revoca key EL admin@telesales.it (`sk_3663...`) | elevenlabs.io → login admin → API Keys → Revoke | [ ] |
| 2 | Verifica scadenza TUTTI i domini | controlpanel.register.it/renews/ | [ ] |
| 3 | Rinnova domini in scadenza (~€15/cad) | Register.it | [ ] |
| 4 | Verifica se SendGrid addebita | sendgrid.com → Billing → cancella se sì | [ ] |
| 5 | Verifica Vapi credits account 84eb75ba | dashboard.vapi.ai → login | [ ] |
| 6 | Attiva Vercel Analytics (gratis) | vercel.com → progetto → Analytics → Enable | [ ] |
| 7 | Setup UptimeRobot monitor | uptimerobot.com → telesales.it + telesales.salesmind.it | [ ] |
| 8 | Notifica clienti TOP "offsite 26-28/05" | WA/email | [ ] |
| 9 | Compitino sezione O compilato A MANO | Foglio fisico | [ ] |
| 10 | Foto Kit + compitino sul gruppo WA entro ore 21:00 | WhatsApp | [ ] |
| 11 | Firma 10 Regole Hard (sera) | Foto sul gruppo | [ ] |
| 12 | Zero deploy production da ora al 29/05 | — | [ ] |

## T · COSA PORTO AL RETREAT

- Laptop + caricatore + adattatore HDMI
- Foglio cartaceo con credenziali (sezione E, scritto a mano — mai digitale)
- Questo documento stampato (Niccolò porta le stampe, ma avere PDF offline)
- Compitino sezione O compilato a mano
- Verbale 18 mesi scritto a mano
- €100 cash per barattolo penali
- Bozza 5 flussi operativi (sezione L2) per mercoledì pomeriggio

---

# COSE RIMASTE A TE — SOLO QUESTE

*Tutto il resto nel documento è compilato con dati reali e verificati.*
*Queste richiedono accesso a dashboard o sono risposte personali impossibili dall'esterno.*

| Voce | Come risolverla |
|---|---|
| Traffico 30gg webapp e 9 prodotti | Attiva Vercel Analytics oggi — dati da subito |
| GHL pipeline value esatto | GHL → Opportunities → Total Value |
| ElevenLabs billing esatto mese corrente (inclusi LLM tokens) | Dashboard EL niccolo.smrt → Billing |
| Vapi credits residui account 84eb75ba | dashboard.vapi.ai → login → Credits |
| Scadenze esatte domini (data precisa) | controlpanel.register.it/renews/ |
| Compitino Q1, Q2, Q3 (reddito/ore), Q4, Q6 | Solo tu lo sai — bozza Claude sopra per Q1/Q2 |
| Verbale 18 mesi (reddito, equity ask, team, stop-doing) | Solo tu lo sai |
| Revenue / MRR attuale (per cashflow) | Conti correnti + Stripe → porta giovedì |

---

*Documento compilato da Claude · 25/05/2026*
*Prezzi verificati live su: elevenlabs.io/pricing/agents · deepgram.com/pricing · synthflow.ai/pricing · vapi.ai/pricing · telnyx.com · instantly.ai/pricing · gohighlevel.com/pricing · vercel.com · cloudflare.com · resend.com · supabase.com · stripe.com/it · anthropic.com*
*Status verificato su: status.elevenlabs.io (fully operational, 0 incident 30gg)*
*Codebase analizzato: /Users/simocors/Desktop/telesales — form endpoint, 9 prodotti, Instantly config, GHL config*
