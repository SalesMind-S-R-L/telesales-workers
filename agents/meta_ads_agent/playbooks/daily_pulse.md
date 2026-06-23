# 📊 DAILY PULSE — Playbook

Esegui ogni mattina 08:00. Durata: 3-5 minuti.

## Step 1 — Estrai dati IERI

Apri Ads Manager con filtro data "Ieri":
```
https://adsmanager.facebook.com/adsmanager/manage/ads?act=40219042
```

Raccogli per OGNI ad attiva:
- Spesa
- Risultati (lead)
- CPL (costo per risultato)
- Impressions
- Frequenza
- CTR

## Step 2 — Confronta con media 7gg

Filtro "Ultimi 7 giorni" → media giornaliera:
- CPL medio settimanale
- Volume lead/giorno medio
- Spesa media

**Calcola delta**:
- CPL ieri vs media 7gg: `+/-€X`
- Volume ieri vs media: `+/-X lead`

## Step 3 — Quality check rapido (foglio Google)

URL foglio (export CSV):
```bash
curl -sL "https://docs.google.com/spreadsheets/d/1wFYXFDFo6W2GT6HT3HKHLYx8eN-C4VUGnxlU_dIiNyk/export?format=csv&gid=GID_v4b_tab" -o /tmp/leads_today.csv
```

Filtra `data_creazione = ieri` → conta:
- Totale lead
- Quanti con Q1 = "Sì decisore"
- Quanti con Q2 = ">50k fatturato"  
- Quanti con P.IVA formato valido (IT + 11 cifre)
- Quanti con timing = "Subito"

**Quality score stimato ieri**:
```
qualità = (lead_in_target / lead_totali) * 100
in_target = Q1=sì AND Q2=>50k AND P.IVA_valida
```

## Step 4 — Anomaly detection

Trigger ALERT se:
- CPL ieri >€25 (rosso)
- 0 lead ieri (rosso)
- Spesa <80% del budget (delivery lenta)
- Frequenza >4 (audience exhaustion)
- Top performer ad cambiato (Meta sta esplorando?)

## Step 5 — Output report

Format risposta a Simone:

```
📊 PULSE IERI ({data})

NUMBERS:
- Spesa: €X (budget €Y)
- Lead: N (vs media 7gg: ±X)
- CPL: €X (vs media 7gg: ±€X)
- Quality stimata: X%

TOP AD: {ad_name} - N lead - CPL €X

STATUS: 🟢 verde / 🟡 giallo / 🔴 rosso

[Solo se rosso o azione necessaria:]
ALERT: {description}
RACCOMANDAZIONE: {action} perché {razionale}

PROSSIMO CHECK: domani 08:00 (auto)
```

## Esempio output verde

```
📊 PULSE IERI (2026-06-15)

NUMBERS:
- Spesa: €27 (budget €30)
- Lead: 3 (vs media 7gg: +0.5)
- CPL: €9 (vs media 7gg: -€2)
- Quality stimata: 60%

TOP AD: cos'è telesales - 2 lead - CPL €7

STATUS: 🟢 verde

Tutto in linea. Niente da toccare.
```

## Esempio output rosso

```
📊 PULSE IERI (2026-06-22)

NUMBERS:
- Spesa: €30 (budget €30)
- Lead: 0 (vs media 7gg: -2)
- CPL: N/A (vs media €15)
- Quality stimata: N/A

TOP AD: nessuna conversione

STATUS: 🔴 ROSSO

ALERT: Zero lead 24h consecutive con spesa completa.
Possibili cause: ad fatigue (frequenza 4.2), modulo bloccato, audience saturata.

RACCOMANDAZIONE 1 (impatto alto): pausare ad worst CTR e lanciare 1 nuova creative.
RACCOMANDAZIONE 2 (low risk): test pubblico modulo via link condivisione per escludere bug.

AZIONE RICHIESTA: ok/no?
```
