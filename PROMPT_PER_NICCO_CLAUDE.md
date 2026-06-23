# Prompt per nuova chat Claude Code di Nicco

Copia-incolla TUTTO il blocco sotto in una chat Claude Code nuova:

---

Ciao Claude. Sto riprendendo un progetto complesso da un'altra sessione Claude. Sono Niccolò Pratesi di Telesales Italia — agenzia di outbound B2B / lead-gen per PMI italiane. Tu non hai memoria di quanto fatto prima, te lo passo io qua sotto.

**Obiettivo finale**: trasformare la nostra campagna Instantly "My Campaign" da target PMI piccole (terminata) a target aziende grandi italiane. Devi prepararmi un CSV pronto per import Instantly con 542 aziende, decisore identificato, email verificata, personalizzazione profonda.

---

## 0. HOOK · OFFER · CTA · VALUE (la cosa più importante)

Per aziende grandi (mid-market €1-50M) il vecchio gancio "ti mando la lista gratuita di decision maker" NON funziona — loro un database ce l'hanno già. Serve un altro bene tangibile da scambiare per l'attenzione.

### Variante V0 — "Benchmark di settore"

| Elemento | Cosa è |
|---|---|
| **HOOK** | "Ho un'analisi sul vostro settore e su come 30 aziende come la vostra fanno outbound nel 2026" |
| **OFFER** | Report 1 pagina concreto in PDF/email: open rate medio settore, reply rate, sequenze che convertono, errori frequenti, copy che funziona |
| **CTA** | "Glielo mando? Anche solo per vederlo, senza altri impegni" |
| **VALUE** | Intel competitiva utilizzabile anche senza parlarci. Dimostra data-driven, non chiacchiere |

### Variante V1 — "Reverse pitch decisionale"

| Elemento | Cosa è |
|---|---|
| **HOOK** | "Una domanda diretta, così non le faccio perdere tempo" |
| **OFFER** | 15 minuti di videocall SOLO SE in fase decisionale |
| **CTA** | Binaria: "State assumendo SDR internamente o c'è apertura ad esternalizzare?" |
| **VALUE** | Decisional clarity. Se è "assumiamo internamente" non lo disturbo più. Se "esternalizzare" o "non so" arriva un confronto utile |

### Principio strategico (mai violare)

Per executive di aziende €1-50M l'offerta deve essere:
1. **Concreta** (non "ne parliamo", ma "le mando X")
2. **Time-bounded** (15 min, 1 pagina, 1 frase)
3. **Reciprocata** (do qualcosa prima di chiedere)
4. **No-risk** ("anche se non lavoriamo insieme")

### Cosa NON è il valore (da non scrivere mai)

- ❌ "Aumentiamo il vostro fatturato" → tutti lo dicono
- ❌ "Migliore qualità leads del mercato" → claim non verificabile
- ❌ "Esperienza decennale" → noioso
- ❌ "Posso mandarvi la nostra brochure" → kill
- ❌ Lista contatti gratis → loro un database ce l'hanno già

---

## 1. ASSET E CREDENZIALI A TUA DISPOSIZIONE

### File locali
- **Lista aziende grandi da Margò Cribis**: `/Users/simocors/Downloads/AZIENDE GRANDI X TELESALES_20260518021338.xlsx`
  - 542 aziende, 107 colonne. Tab unica: "Mio portafoglio"
  - Tutte hanno: email aziendale, sito web, esponenti (fino a 8) con nome+cognome+carica, fatturato, dipendenti, ATECO, sede
- **Service account Google Sheets**: `/Users/simocors/Desktop/telesales/service-account.json`
  - Email service account: `claude-sheets@claude-telesales.iam.gserviceaccount.com`
  - Scopes da usare: `https://www.googleapis.com/auth/spreadsheets` + `/auth/drive`

### Google Sheet centrale
- **Sheet ID**: `1fMzEkw8garXGJBan_yX6gUlsnc8CRL6ASgXZFymxu9w`
- **URL**: https://docs.google.com/spreadsheets/d/1fMzEkw8garXGJBan_yX6gUlsnc8CRL6ASgXZFymxu9w/edit
- **Tab esistenti**:
  - `INSTANTLY` — 7 righe (lead caldi già trasferiti, NON toccare)
  - `retargeting instantly` — 527 righe (lead ghosted già trasferiti, NON toccare)
  - `ADV META`, `NUOVA CAMPAGNA META b`, `NUOVO MODULO META`, `vecchie campagne` — non rilevanti
- **NUOVA tab da creare**: `aziende_grandi_v1` — qui finisce il CSV finale prima di uploadarlo su Instantly

### Instantly API
- **API key**: `YzkyODNiOTAtNWRmNi00OTc1LWExODktZTY5MjAyMmQxNjRhOlhlZXVXRUxBS0xqRw==`
- **Base URL**: `https://api.instantly.ai/api/v2/`
- **Header**: `Authorization: Bearer <APIKEY>` + `Content-Type: application/json`
- ⚠️ **ATTENZIONE**: il workspace al momento risponde `402 Payment Required` perché il piano è scaduto. Simone sta per rinnovare. Fai tutto il pre-lavoro offline (parse Excel, scraping, build CSV) — non serve toccare l'API finché il piano non è attivo.

### Campagne Instantly esistenti
- **"My Campaign"** ID: `b41294c8-f0dd-4601-bfc3-c7dbafec24d5` — campagna PMI piccole, da svuotare e riusare (oppure crearne una nuova)
- **"CRIBIS Email Outreach"** ID: `63bd27ca-963a-4187-aa00-dea9ea25cd69` — campagna Cribis pausata, da svuotare

### Sender mailbox (già configurate e warmed, score 100)
1. `l.stefanelli@telesalesconsulting.com`
2. `n.pratesi@telesalesconsulting.com` (la mia)
3. `s.corsani@telesalesconsulting.com`

### Script utili già esistenti
- `/Users/simocors/Desktop/telesales/scripts/daily_update_instantly_sheet.py` — sincronizza la tab INSTANTLY con i nuovi reply caldi (gira ogni giorno alle 18:00 via scheduled task `aggiorna-instantly-sheet-daily`)

---

## 2. STORICO E APPRENDIMENTI DALLA CAMPAGNA PRECEDENTE

Cose che funzionano, da preservare nel nuovo setup:

### Settings campagna (best practice testata su 2500+ email inviate)
- `first_email_text_only`: **TRUE** (no logo image step 0)
- `insert_unsubscribe_header`: **TRUE** (richiesto da Gmail/Yahoo 2024)
- `match_lead_esp`: **TRUE** (Gmail→Gmail, M365→M365)
- `stop_on_reply`: TRUE
- `stop_on_auto_reply`: **TRUE** (OOO non blocca pipeline)
- `link_tracking`: **FALSE** (impatta deliverability)
- `open_tracking`: TRUE
- `daily_limit`: 90 (= 30 email/sender × 3 sender)

### Subject che ha funzionato
- V1 winner: `{{firstName}}, una domanda rapida` → 58,5% open rate
- V0 disaster: `Ho notato una cosa su {{companyName}}, {{firstName}}` → 4,9% open rate (formula triggera SpamAssassin)

### Sequenza 3 step (totale ~9 giorni)
- Step 0: primo contatto (2 varianti A/B)
- Step 1: follow-up dopo 4 giorni
- Step 2: chiusura/breakup dopo 5 giorni

### Errori da NON ripetere
- Mai email generiche come `info@`, `contatti@`, `staff@`, `support@` — bounce alti + reply automatica ticket
- Solo nominativa o fallback (`amministrazione@`, `commerciale@`, `direzione@`) se proprio non c'è altro
- Mai bugie del tipo "ci siamo già sentiti" (la CRIBIS campaign aveva questo e bruciava reputation)
- Mai mismatch sender/firma (es. mittente @telesalesconsulting.com che firma "CRIBIS")

---

## 3. DECISIONI GIÀ PRESE PER QUESTO NUOVO PROGETTO

| Aspetto | Scelta |
|---|---|
| **Hook A/B test** | V0 = **Benchmark di settore** · V1 = **Reverse pitch** (no "elenco gratuito") |
| **Decisore target** | Priority: **AD** (Amministratore Delegato) → fallback Consigliere Delegato → Presidente CdA → Amministratore Unico |
| **Email finding** | Cross-reference multi-fonte (sito + LinkedIn pubblico + Google + Camera Commercio + pattern + MX). NON solo pattern cieco. |
| **Personalization** | Deep multi-fonte. Spider sito + LinkedIn azienda + Google news. 1 fatto specifico per lead. |

---

## 4. LE 6 FASI CHE DEVI ESEGUIRE

### FASE 1 — Identificazione decisore (30 min, algoritmica)

Parse l'Excel `AZIENDE GRANDI X TELESALES_20260518021338.xlsx` (tab "Mio portafoglio"). Per ognuna delle 542 aziende:

1. Scorri gli 8 esponenti (`Nome esponente 1` → `Carica esponente 1`, idem per 2-8)
2. Trova l'esponente con la carica per priority più alta:
   - Priority 1: `Amministratore delegato`
   - Priority 2: `Consigliere delegato`
   - Priority 3: `Presidente consiglio amministrazione`
   - Priority 4: `Amministratore unico`
   - **SKIP**: `Sindaco effettivo`, `Sindaco supplente`, `Revisore`, `Società di revisione`, `Procuratore`, `Consigliere` puro (senza "delegato")
3. Estrai: `firstName`, `lastName`, `role`, `companyName`, `partita_iva`, `website`, `email_aziendale` (dal Margò), `città`, `provincia`, `regione`, `fatturato`, `dipendenti`, `ATECO`, `descrizione_ateco`

### FASE 2 — Email finding cross-referenced (6-10 ore parallel)

Per ogni decisore identificato, pipeline a 5 step (fermati appena trovi):

1. **Spider sito aziendale** (homepage + `/contatti` + `/contact` + `/about` + `/chi-siamo` + `/team` + `/staff` + `/press`):
   - Estrai TUTTI gli email con regex
   - Filtra solo email del dominio aziendale (matching del netloc del sito)
   - Cerca se l'AD identificato compare già come `mailto:` → confidence 95
2. **Google search via DuckDuckGo HTML** (`https://html.duckduckgo.com/html/?q=...`):
   - Query: `"Nome Cognome" "Azienda" email`
   - Parse snippet HTML per pattern email
3. **LinkedIn pubblico via Google**:
   - Query: `"Nome Cognome" "Azienda" site:linkedin.com`
   - Estrai URL profilo (le info contatto sono protette ma il URL conferma identità)
4. **Camera di Commercio / PEC**:
   - Cerca PEC nominativa via Registro Imprese
5. **Pattern guess + MX validate**:
   - Domain dal sito web
   - Pattern: `nome.cognome@dominio` (default Italian B2B)
   - Fallback: `n.cognome@dominio`, `nome@dominio`
   - Validate MX record del dominio via `socket.getaddrinfo(domain, 25)` o `dnspython`

**Confidence score**:
- 95: mailto: nominativa visibile sul sito
- 85: LinkedIn match + pattern coerente
- 70: pattern + altri email simili visibili sul dominio
- 60: pattern guess + MX OK
- **< 60 = SCARTA il lead**

### FASE 3 — Personalization deep multi-fonte (8-12 ore parallel)

Per OGNI azienda, in parallelo all'email finding:

1. **Spider profondo del sito** (homepage + news + press + blog + chi-siamo):
   - Title pagina, meta description, h1, primo paragrafo "about"
   - Eventuali press release / annunci
2. **Google News search**: `"[Azienda]" 2025 OR 2026` (ultimi 6-12 mesi)
3. **LinkedIn pagina azienda** via Google cache (`site:linkedin.com/company [nome azienda]`):
   - Ultimi 3-5 post recenti / annunci
4. **Bilanci Camera Commercio** (già hai trend fatturato da Margò):
   - In salita = fase espansiva → "sto vedendo la vostra crescita"
   - In calo = ristrutturazione → "in fase di repositioning come la vostra"
5. **Estrai 1 fatto specifico** tra:
   - Apertura nuova sede / espansione geografica
   - Acquisizione / M&A
   - Nomina executive recente
   - Award / certificazione / IPO
   - Nuovo prodotto / linea / brand
   - Investimento dichiarato
6. **Costruisci 3 campi di personalizzazione** per ogni lead:
   - `gancio_specifico`: 1-2 frasi che citano un fatto specifico dell'azienda + bridge al pitch
   - `contesto_settore`: 1 frase con un data point/trend del loro settore (per V0 benchmark) o 1 osservazione che apre il binario decisionale (per V1 reverse pitch)
   - `proof_point`: NON usato in V0 (l'offer è il report). Usato solo se serve in step 1 follow-up

### FASE 4 — Build CSV finale (30 min)

**Colonne del CSV** (15 colonne, in quest'ordine):

```
firstName, lastName, email, role_decisor, companyName, website, city, region, sector_short, size_label, gancio_specifico, contesto_settore, proof_point, confidence_score, fonti
```

**File output**: `/Users/simocors/Desktop/telesales/lead_generation_v3/aziende_grandi_v1.csv` (UTF-8, header)

E parallelamente push nel Google Sheet → tab `aziende_grandi_v1` (creala con gspread)

### FASE 5 — Setup nuova campagna Instantly (1 ora, post-pagamento)

Quando l'API è di nuovo accessibile (Simone paga il piano):

**Crea nuova campagna**:
- Nome: `Telesales — Aziende Grandi Mag 2026`
- Sender: tutte e 3 le mailbox esistenti
- Settings (POST `/api/v2/campaigns` con questi field):

```json
{
  "name": "Telesales — Aziende Grandi Mag 2026",
  "email_list": ["l.stefanelli@telesalesconsulting.com", "n.pratesi@telesalesconsulting.com", "s.corsani@telesalesconsulting.com"],
  "daily_limit": 90,
  "first_email_text_only": true,
  "insert_unsubscribe_header": true,
  "match_lead_esp": true,
  "stop_on_reply": true,
  "stop_on_auto_reply": true,
  "link_tracking": false,
  "open_tracking": true
}
```

**Sequenza 3 step**:

#### Step 0 — A/B test (50/50)

**V0 Benchmark di settore**:
- Subject: `{{firstName}}, dati outbound nel {{sector_short}} 2026`
- Body:
```
Buongiorno {{firstName}},

{{gancio_specifico}}

Ho chiuso un'analisi sui principali player del {{sector_short}} in Italia: open rate outbound, sequenze che convertono, errori frequenti, copy che apre conversazioni con i decisori.

{{contesto_settore}}

Le mando il report in 1 pagina? Vede come {{companyName}} si posiziona rispetto ai pari, senza altri impegni.

Cordiali saluti,
Simone Corsani
Telesales Italia
```

**V1 Reverse pitch**:
- Subject: `{{firstName}}, domanda secca`
- Body:
```
Buongiorno {{firstName}},

una domanda diretta, così non le faccio perdere tempo:

per {{companyName}}, l'acquisizione di nuovi clienti oggi sta seguendo principalmente passaparola e network di settore, oppure c'è una funzione dedicata che fa outbound strutturato sui decisori target?

Se è la prima, ne parliamo in 15 minuti — c'è un modo di strutturare il primo contatto che evita di bruciare relazioni storiche.

Se è la seconda, non la disturbo più.

Cordiali saluti,
Simone Corsani
Telesales Italia
```

#### Step 1 — Follow-up dopo 4 giorni
- Subject: `Re: {{firstName}}, le riprendo`
- Body breve (max 80 parole) che richiama la prima email e rilancia l'offer

#### Step 2 — Breakup dopo 5 giorni
- Subject: `{{firstName}}, chiudo il thread`
- Educato breakup ("se cambia idea sa dove trovarmi")

### FASE 6 — Upload CSV + start campagna (30 min)

Upload via UI Instantly (più affidabile dell'API per CSV grandi):
1. Apri https://app.instantly.ai/app/campaigns
2. Seleziona la nuova campagna
3. Leads → Import CSV → carica `aziende_grandi_v1.csv`
4. Mappa le colonne: firstName, lastName, email, companyName, website come standard. Le altre (gancio_specifico, contesto_settore, role_decisor, city, region, sector_short, size_label) come **Custom variables**.
5. Avvia campagna

### FASE 0 (per ultima, post-pagamento) — Pulizia
- Sincronizza tab `INSTANTLY` + `retargeting instantly` con eventuali nuovi reply/ghosted
- Elimina tutti i 755 lead da "My Campaign" e 91 da "CRIBIS" via `DELETE /api/v2/leads/{id}` (i dati sono già nel foglio Google = nessuna perdita)

---

## 5. ESEMPIO CONCRETO — V0 Benchmark renderizzato

Lead reale dalla lista 542: **TAMPIERI FINANCIAL GROUP SPA** (Faenza, RA, holding finanziaria agro-industriale, 59 dip, €10M).

### Custom variables compilate

| Var | Valore |
|---|---|
| firstName | Fabrizio |
| lastName | Donega' |
| email | fabrizio.donega@tampieri.com (pattern + MX OK) |
| role_decisor | Amministratore Delegato |
| companyName | Tampieri Financial Group |
| sector_short | finance specialistico per agri-food |
| size_label | 59 dip · €10M fatturato |
| gancio_specifico | "ho dato un'occhiata al posizionamento di Tampieri come holding finanziaria a servizio del comparto agro-alimentare romagnolo — un mercato dove le aziende clienti decidono via fiducia e tempistiche rapide, non via brochure" |
| contesto_settore | "Un dato che ne è uscito: chi struttura outbound diretto verso i CFO di PMI agro-industriali chiude il 40% più in fretta del solo passaparola di settore" |

### Email finale renderizzata

**Subject:** `Fabrizio, dati outbound nel finance specialistico per agri-food 2026`

```
Buongiorno Fabrizio,

ho dato un'occhiata al posizionamento di Tampieri come holding finanziaria a servizio del comparto agro-alimentare romagnolo — un mercato dove le aziende clienti decidono via fiducia e tempistiche rapide, non via brochure.

Ho chiuso un'analisi sui principali player del finance specialistico per agri-food in Italia: open rate outbound, sequenze che convertono, errori frequenti, copy che apre conversazioni con i decisori.

Un dato che ne è uscito: chi struttura outbound diretto verso i CFO di PMI agro-industriali chiude il 40% più in fretta del solo passaparola di settore.

Le mando il report in 1 pagina? Vede come Tampieri Financial Group si posiziona rispetto ai pari, senza altri impegni.

Cordiali saluti,
Simone Corsani
Telesales Italia
```

### Perché funziona
- Subject specifico settore (no nome azienda → no spam trigger)
- Apertura mostra ricerca specifica (no template)
- Hook locale (Romagna + agri = chirurgico)
- Data point concreto (40%, credibile)
- CTA friction zero ("le mando il report? sì/no")
- No P.S., no logo, no link tracking

---

## 6. REGOLE OPERATIVE NON NEGOZIABILI

1. **Zero allucinazioni**: ogni decisore, ogni email, ogni fatto deve essere VERIFICABILE da fonte pubblica. Mai inventare.
2. **No emoji** nelle email, custom field, subject (Simone è chiaro su questo).
3. **Italian B2B "Lei" form**: le email parlano in "Lei", non in "tu". Eccezione: se il prospect ha già risposto in "tu" si rispecchia.
4. **No email generiche**: mai `info@`. Solo nominative o fallback (`amministrazione@`, `commerciale@`, `direzione@`) se davvero non c'è altro.
5. **Bounce target <5%** (best effort, senza paid tool 5-10% è il realistico).
6. **Cross-reference minimo 2 fonti** per ogni email prima di darle confidence ≥80.
7. **Personalization specifica all'azienda**, mai template generico tipo "ho visto che operate nel settore X".
8. **Risposte ultra-concise** a Simone: zero filler, no ripetizioni.
9. **Output a chunks** con report intermedi: primi 50 lead → quality check con Simone → poi continua a 200 → 500 → 542 totali.
10. **Non toccare** le tab `INSTANTLY` e `retargeting instantly` del foglio Google.

---

## 7. STATS ATTESI

| KPI | Stima realistica |
|---|---|
| Lead caricati | 480-510 (dopo drop confidence <60) |
| Email VERIFIED score ≥85 | 8-12% |
| Email pattern score 60-84 | 75-80% |
| Bounce rate atteso | 5-10% |
| Open rate atteso | 35-50% |
| Reply rate atteso | 2-4% |
| Reply caldi attesi 30gg | 10-20 |

---

## 8. WORKFLOW CHE TI PROPONGO

1. **Setup TodoWrite** con le 6 fasi
2. **Fase 1** completa (30 min) → controlla che le 542 abbiano tutte un decisore identificato
3. **Fase 2 + 3 in parallelo** su un primo batch di 50 lead → genera CSV intermedio → mostralo a Simone per quality check
4. **Aspetta OK** da Simone sul primo batch
5. **Continua su tutti i 542** con il pattern validato
6. **Fase 4** CSV finale
7. **Fase 5** quando Simone conferma che ha pagato Instantly
8. **Fase 6** upload + go

---

## 9. POSSIBILI BLOCCHI E COME GESTIRLI

- **API Instantly 402**: aspetta che Simone paghi, NON serve per Fasi 1-4
- **Google Sheets rate limit**: usa `batch_update` invece di update riga per riga
- **Sito aziendale Cloudflare-blocked**: salta quello, prosegui col next. Non scartare il lead, usa solo pattern
- **MX record fail**: drop il lead dal CSV finale
- **DuckDuckGo rate limit**: usa user-agent vario + sleep 1-2s tra query
- **LinkedIn blocked**: cerca via Google cache invece (`site:linkedin.com/in [nome]`)

---

## 10. Come pormi le domande

Se hai dubbi, blocker, o serve una decisione mia su qualcosa, fammele **a risposta chiusa** — opzioni multiple tra cui scegliere (A / B / C), MAI domande aperte.

Esempi del formato che voglio:

> **Q: Su quale batch test iniziale parto?**
> A) Top 50 aziende per fatturato → quality check
> B) Random 50 aziende → quality check
> C) Tutti 542 in una passata

> **Q: Per email finding, partiamo con quale fonte primaria?**
> A) Spider sito + pattern guess + MX validate (più veloce)
> B) DuckDuckGo + LinkedIn cache (più preciso ma più lento)
> C) Entrambi in parallelo

Così rispondo veloce con A/B/C senza dover scrivere troppo. Se proprio nessuna delle opzioni funziona, aggiungi sempre una **D) Altro (specifica)**.

## INIZIO

Comincia creando TodoWrite con le 6 fasi e mostrami il piano in linea. Dimmi se ci sono blocker prima di partire con Fase 1.

— Simone
