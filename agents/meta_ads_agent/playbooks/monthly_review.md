# 📊 MONTHLY REVIEW — Playbook

Primo giorno del mese. Durata: 45 minuti.

## Step 1 — Aggregazione mensile completa

Apri Ads Manager → filtro "Mese precedente":

Estrai:
- Spesa totale mese
- Lead totali mese
- CPL medio mese
- CPC medio
- CPM medio
- Impressions totali
- Reach unica totale
- Frequenza media a 30gg
- CTR medio
- Conversion rate (lead/impression)

Per ogni ad attiva nel mese:
- Spesa individuale
- Lead individuali
- CPL individuale

Per ogni ad set attivo nel mese:
- Stessa break-down

## Step 2 — Sync con setter per quality finale

Email/messaggio a Karima/Rebecca/Barbara:

```
Ciao,
Bilancio mensile Meta Ads. Mi serve:
1. Quanti lead della campagna hai chiamato a {mese}?
2. Quanti in target (decisore B2B con P.IVA reale + fatturato OK)?
3. Quanti appuntamenti fissati?
4. Quanti chiusi (contratto firmato)?

Grazie.
```

Calcola:
- **Quality rate**: lead_in_target / lead_totali
- **Appointment rate**: appuntamenti / lead_in_target
- **Close rate**: chiusi / appuntamenti
- **CAC blended**: spesa_mese / chiusi_mese

## Step 3 — ROI calcolato

Se Simone fornisce valore medio cliente Telesales (es. €X primo mese):

```
ROI = (chiusi_mese × valore_cliente - spesa_mese) / spesa_mese × 100
```

Esempio:
- 100 lead, 30 qualified, 10 appuntamenti, 3 chiusi
- Valore cliente: €2.000
- Spesa: €2.000
- ROI: (3 × 2000 - 2000) / 2000 × 100 = 200%

## Step 4 — Confronto month-over-month

Compara mese corrente vs mese precedente:
- Lead volume: ±X%
- CPL: ±€X
- Quality rate: ±X%
- ROI: ±X%

Identifica trend:
- 🟢 In crescita su tutti i fronti → mantieni strategia
- 🟡 Mixed (volume su, quality giù?) → audit profondo
- 🔴 In calo su tutti i fronti → pivot

## Step 5 — Aggiorna dataset

Riga in `01_campagne_overview.csv`:
```csv
v8_mag_v4_LIVE,TS_LEADS_v4_Manual_2026-05-04,...,SPESA_MESE,LEAD_MESE,...,quality_mese,...
```

Riga in `03_decisioni_log.csv` per ogni decisione presa nel mese:
```csv
DATA,id_campagna,categoria,decisione,razionale,...
```

## Step 6 — Roadmap mese prossimo

Basato su trend mensile:

**Se 🟢**:
- Budget mensile +10-15%
- 1 nuova creative test
- 1 nuovo ad set test (audience nuova)

**Se 🟡**:
- Budget mensile invariato
- Refresh creative (1 nuova sostituisce worst)
- Audit qualità modulo

**Se 🔴**:
- Budget mensile -10%
- Audit completo strategia
- Sit-down con Simone per pivot

## Step 7 — Output report mensile

Format report a Simone (max 1 pagina):

```
📊 MONTHLY REVIEW — {mese} 2026

EXECUTIVE NUMBERS:
- Spesa: €X
- Lead: N (vs {mese-1}: ±X%)
- CPL: €X (vs {mese-1}: ±€X)
- Quality rate: X% (vs {mese-1}: ±X%)
- Chiusi: N → CAC: €X
- ROI stimato: X%

STATUS COMPLESSIVO: 🟢/🟡/🔴

TOP 3 WIN:
1. {win1}
2. {win2}
3. {win3}

TOP 3 LESSON:
1. {lesson1}
2. {lesson2}
3. {lesson3}

PROSSIMO MESE — ROADMAP:
- Budget proposto: €X (±X% vs mese corrente)
- Azione 1: {action1}
- Azione 2: {action2}
- Azione 3: {action3}

DECISIONE RICHIESTA: ok/modifiche?

PROSSIMA REVIEW: 1/{mese+1}
```

## Anti-pattern (da NON fare)

❌ Cambi drastici basati su 1 mese di dati (servono almeno 3 mesi per trend)
❌ Pivot strategia per 1 settimana brutta dentro un mese complessivamente buono
❌ Scaling aggressivo dopo 1 mese di crescita (aspetta 2 mesi confermati)
❌ Tagliare creative top performer per "novità" (mai disturbare il winner stabile)
