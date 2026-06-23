# Dataset Analisi Campagne Meta Telesales (feb-mag 2026)

**Generato:** 11 maggio 2026
**Obiettivo:** dataset analitico per agente Claude — non per uso operativo setter.
**Periodo:** 25 febbraio 2026 → 11 maggio 2026 (76 giorni totali)

---

## Struttura file

| File | Granularità | Righe | Uso |
|---|---|---|---|
| `01_campagne_overview.csv` | Per campagna | 9 | Overview KPI cumulativi, setup, esito |
| `02_ads_performance.csv` | Per inserzione | 9 | Performance singole creative + verdict |
| `03_decisioni_log.csv` | Per evento | 13 | Diario decisionale: cosa, perché, esito, lezione |

---

## Convenzioni di compilazione

- **TBD** = dato da raccogliere (es. quality rate post-chiamate)
- **sconosciuto** = dato non disponibile (campagne pre-tracking strutturato, feb-apr)
- **N/A** = dato non applicabile
- **id_campagna** = chiave primaria, formato `v{n}_{mese}_{slug}`
- Date in formato ISO 8601 (`YYYY-MM-DD`)
- Importi in EUR, decimali con punto
- Boolean: `si` / `no`

---

## Domande analizzabili dal dataset

### Performance & ROI
1. Qual è il CPL medio per quality_rate vs altre campagne? → `01_campagne_overview.csv`
2. Quali ad sono "WINNER" vs "LOSER" cumulativo? → `02_ads_performance.csv`
3. Esiste correlazione tra `form_questions_count` e `quality_rate`? → cross 01
4. La switch da modulo "Volume maggiore" a "Intenzione elevata" ha migliorato quality? → cross 01

### Pattern strategici
5. Quali decisioni hanno avuto outcome positivo (`validata=si`)? → `03_decisioni_log.csv`
6. Quali ipotesi hanno fallito ripetutamente (lezione strutturale)? → 03
7. Qual è la lifespan media di un'ad prima del kill? → 02 (`data_attivazione` → `data_pausa`)
8. Quali categorie di decisione ricorrono di più (`launch`, `kill`, `creative_rotation`)? → 03

### Vincoli tecnici Meta scoperti
9. Cosa NON funziona (e perché) in account Telesales? → 03 (filtri `outcome_reale` contiene "hardcoded" o "non disattivabile")
10. Quali workaround sono stati trovati? → 03 (filtra `validata=si_workaround`)

### Audience & creative
11. Hook educativo (`cos_e_telesales`) vs brand (`telesales_v4`) vs AI (`AI_voice`): chi vince? → 02
12. Performance "Biliardo" cambia tra v2 e v4 — perché? Modulo o audience? → 02 + 01

---

## Glossario campi chiave

- **modulo_type**: `Volume_maggiore` (modulo standard) | `Intenzione_elevata` (con review screen pre-submit)
- **Advantage_plus_*: si_hardcoded** = non disattivabile in account Telesales (regola Meta scoperta 02/05)
- **conv_rate_pct**: lead / impressions × 100 (non click-rate, è impression-to-lead)
- **quality_score_inferito**: dedotto dai dati Meta + interpretazione esperta, non è metrica ufficiale
- **outcome_reale** in 03: cosa è successo davvero (vs ipotesi)
- **validata**: `si` = ipotesi corretta | `no` = ipotesi smentita | `parziale` = mixed | `si_workaround` = bug confermato, soluzione esiste

---

## Lezioni strutturali (per consultazione rapida agente)

### Vincoli tecnici Meta (account Telesales)
1. **Advantage+ leads campaign è HARDCODED** per objective "Contatti" — non disattivabile (Manual mode mostra l'opzione ma duplica eredita Advantage+)
2. **Età massima sempre infinita** — non si può fissare max age 50 → pensionati entrano comunque
3. **Età minima max 25** — non si può alzare a 30+
4. **Moduli NON modificabili post-pubblicazione** — per cambiare anche un titolo serve duplicare il modulo + swappare nelle ad
5. **Form custom fields (Q1-Q4 P.IVA ruolo) NON esportati** dall'integrazione CRM nativa Meta → Google Sheet — serve Make.com webhook per averli

### Pattern strategici ricorrenti
6. **Filtro pensionati funziona SOLO via modulo hard** (P.IVA obbligatoria + ruolo binary + intenzione elevata + phone obbligatorio)
7. **Bandit algorithm Meta sceglie volume su efficienza** — ad con CPL migliore ma audience più stretta riceve €0 budget
8. **Audience stretta + Lookalike + new creative = audience overlap** che alza CPM
9. **Max 3-5 ad per ad set** con budget €25/giorno (sotto soglia learning = €5/ad)
10. **Aumento budget >30% rompe learning phase** — sempre +20-30% max ogni 3-5 giorni

### Anti-pattern da NON ripetere
11. **Hook AI-generated** (AI_voice) non funziona per audience B2B italiana
12. **Lancio multiple ad insieme con budget piccolo** = nessuna riceve abbastanza signal
13. **Cambio creative durante learning phase** = reset signal, CPL spike temporaneo

---

## Stato corrente snapshot (11/05/2026)

- **Campagna attiva:** v8 = TS_LEADS_v4_Manual_2026-05-04
- **Lead totali storici:** 51 totali (42 reali + 9 dummy/test)
- **Lead qualificati confermati:** 3 (Antonio Bellei, Vince Vita, Piergiorgio Gabrielli — tutti feb 2026, modulo senza titolo 25/02)
- **Pensionati confermati:** 8 (4 da Hormozi + 4 da v5)
- **Quality rate storica:** ~7% (3 qualified / 42 reali)
- **CPL medio storico:** €16.38 (v8 cumulativo)
- **Setup v4 (attuale):** 2 ad attive (cos_e_telesales + Leonardo), 5 pausate, budget €25/giorno

---

## Note per agente futuro

- Aggiorna `03_decisioni_log.csv` ad ogni decisione strategica (launch/kill/budget/creative)
- Quando una nuova campagna parte, aggiungi riga in `01_campagne_overview.csv` con stato `IN_LEARNING`
- Per ogni ad nuova, aggiungi riga in `02_ads_performance.csv` con `verdict=PENDING` finché non hai 50+ impression
- Tutti i lead vanno nel foglio Google `LEADS Telesales e pipeline` (gid=1222400733) — NON in questo dataset
- Per analisi cross-campagna usa `id_campagna` come join key
