# PIANO OUTREACH TELESALES — 5 CANALI (definitivo, 15/06/2026)

Obiettivo: riempire il calendario di Niccolò e Leonardo di appuntamenti
qualificati con PMI italiane B2B. Regola fondante: **ogni azienda in UN solo
canale** (coordinati nel metodo, separati nei pool). CTA unica = Cal.com.
Hub di coordinamento: tab **00_COORDINAMENTO** del foglio pipeline_opportunita.

---

## 1. I 5 CANALI E I VOLUMI

| # | Canale | Pool / dove | Pronte | Owner | Volume/gg |
|---|---|---|---|---|---|
| 1 | LinkedIn+Email | tab MASTER OUTREACH B2B (consulenza) | 136 | Niccolò + Leonardo | 15-20 conn/profilo |
| 2 | Email cold | tab EMAIL COLD | 228 | casella personale | 10-20 |
| 3 | AI Voice | tab AI VOICE CODA → foglio OUTREACH AI VOICE | 215 (197 dialabili, CSV) | Marco AI / Simone | 50+ (concurrency 1) |
| 4 | Instagram | tab IG CODA B2B | 173 handle | @telesalesita | 15-66 (ramp-up) |
| 5 | Setter (umano) | Drive "Liste per Telesales": TARGET_1000 | 1000 (252 oggi) | setter + closer | pod per area |

Totale prospect coordinati: **~1.750 aziende**, 0 collisioni cross-pool.
Volumi cresciuti ~2x rispetto al primo set (12/06); processo ripetibile per il
3x pieno su email/voice/IG (vedi §6).

## 2. IL 5° CANALE — SETTER (anchor)

Pacchetto già pronto di Niccolò (Drive, letto via service account):
- **TARGET_1000**: 1000 aziende, 973 con email, 936 con DM. 4 parti da 250.
- **CHIAMATE_OGGI**: 252 numeri chiamabili oggi (245 centralino, 69 cellulare).
- **SCRIPT SETTER per macro-area**: gatekeeper + 4 pod (Immobiliare 89,
  Industria/Medicale/Food/Auto 50, Agenzie Mkt-Web/Software 52,
  Consulenza/Finance/Studi/HR 61). Obiettivo: call 15 min con Niccolò/closer.
- Riserva citata: POOL_COMPLETO_2948_fresh per scalare oltre i 1000.
- **È il canale anchor**: gli altri 4 sono deduplicati contro queste 1000
  (chiamate umane = priorità). Le ~13 collisioni emerse sono marcate
  "su lista setter — non contattare nel digitale" nei tab.

## 3. DIVISIONE LINKEDIN PER SOCIO

- **Niccolò** (CEO SalesMind, brand AI): consulenze innovazione, marketing/
  martech, data, HR moderno, eventi, brand. Founder→founder.
- **Leonardo** (consulente CRIBIS/CRIF): finanza agevolata, fiscale, patrimonio,
  compliance, sicurezza, executive search, consulenza tradizionale.
- File: `outreach/settimana1/batch_linkedin_{niccolo,leonardo}.md`.
- TODO: aggiungere ruolo Telesales nell'headline LinkedIn di Leonardo.

## 4. SEQUENZE

1. **LinkedIn+Email**: visita profilo → connessione (nota iper-personalizzata)
   → msg1 → +2gg msg2 → +2gg email bridge. Max 15-20 conn/gg/profilo.
2. **Email cold**: email 1 (<80 parole, 1 CTA, variante B Sales Six) → +3gg bump
   → +7gg ultima. Email = pattern non verificati, monitorare bounce.
3. **AI Voice**: pipeline zero-SIP-404 (agenti leggono il sito + strict_gate),
   agente `agent_5301kpdv4sd9e15vcz4qpm8e7vrn`, batch ore 10-11, Culligan
   priorità, push automatico al foglio dedicato, follow-up email per esito.
4. **Instagram**: DM1 leva Sales Six → +3gg DM2 Cal.com. Partire 15-20/gg.
5. **Setter**: script gatekeeper → DM → gancio 30s → doppia scelta slot.

## 5. KPI (tab KPI OUTREACH, review lunedì)

| Canale | Metrica | Target / baseline |
|---|---|---|
| LinkedIn+Email | accept + reply | accept ~30%, reply ~10%, +72% con nota person. |
| Email cold | reply rate | ≥10% su lista studiata (mercato 3,4%) |
| AI Voice | appunt./chiamate | baseline interno 0,5% (2/394); connect 73% |
| Instagram | consegna/risposta/blocchi | da stabilire nel ramp-up |
| Setter | call fissate/chiamate | dal foglio CHIAMATE_OGGI |

## 6. SOURCING RIPETIBILE (per 3x pieno)

Lead hunt a subagenti su verticali distinti, dedup vs
`outreach/esclusioni_outreach.txt` (4138 domini + 5061 nomi, include setter
1000 + già contattati). Per crescere ancora: rigenerare le esclusioni, poi
nuova ondata di subagenti su verticali non ancora usati. AI Voice consuma di
più (~250/sett a regime); il suo valore è alimentare "Da richiamare" +
follow-up, non il closing diretto a freddo.

## 7. BLOCCHI APERTI (dipendono da Simone)

1. **Cal.com** ai calendari (blocca tutte le CTA) — setup browser
2. **Firma email** → rigenero bozze risolte
3. **Deploy landing Sales Six** → sblocca variante B + leva IG
4. **Ok disclosure AI** + agente dedicato → sblocca AI Voice
5. **Headline LinkedIn Leonardo**
6. **Parere legale** chiamate automatizzate B2B

## 8. CARTELLA UNICA — `outreach/`

- **Piani/ricerca**: PIANO_5_CANALI.md (questo), RICERCA_OUTREACH_4CANALI.md,
  RICERCA_MERCATO_2026.md, ICP_TARGETING.md
- **Canali**: TEMPLATES_COPY.md, PLAYBOOK_AI_VOICE_OUTREACH.md
- **Script**: enrich_context.py, genera_bozze.py, check_collisioni.py,
  followup_aivoice.py, inject_disclosure.py, setup_master_sheet.py
- **Dati**: schede/, bozze/, settimana1/, setter/TARGET_1000.csv,
  esclusioni_outreach.txt, TRACKING_OUTREACH.xlsx (snapshot)
- **AI Voice ops**: prospecting_b2b/ferretti_aivoice_pronti.csv +
  ferretti_lancia_e_push.py + strict_gate.py
- **Landing**: telesales-website-deploy/sales-six.html + apps_script_sales_six.gs
- **Foglio pipeline** (tab): 00_COORDINAMENTO (dashboard), MASTER OUTREACH B2B,
  EMAIL COLD, AI VOICE CODA, IG CODA B2B, KPI OUTREACH, SALES SIX
- **Drive setter**: cartella "Liste per Telesales" (TARGET_1000, CHIAMATE_OGGI,
  SCRIPT SETTER) — di Niccolò, condivisa col service account
