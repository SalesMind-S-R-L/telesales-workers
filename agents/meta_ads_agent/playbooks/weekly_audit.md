# 📋 WEEKLY AUDIT — Playbook

Lunedì 09:00. Durata: 15 minuti.

## Step 1 — Aggregazione 7gg

Dati da estrarre:
- Spesa totale 7gg
- Lead totali 7gg
- CPL medio
- Volume medio giorno
- Distribuzione lead per ad
- Distribuzione lead per ad set (se multi)
- CTR medio per ad
- Frequenza media a 7gg
- CPM medio

## Step 2 — Quality audit (richiede sync setter)

Per i lead della settimana, sync con:
- **Karima** → quanti dei suoi lead caldi (Q1=sì + Q4=subito) ha contattato? Quanti in target?
- **Rebecca** → quanti tiepidi (Q1=sì + Q4=valutando) ha gestito?
- **Barbara** → quanti fuori target ha smistato a nurturing?

**Quality rate settimanale**:
```
qualified_real = chiusure + appuntamenti fissati + interessati reali
total_lead = totale lead settimana
quality_rate = qualified_real / total_lead * 100
```

## Step 3 — Creative fatigue check

Per ogni ad attiva:
- CTR settimanale vs settimana precedente
- Se -20% → segnale fatigue iniziale
- Se -30% → fatigue confermata

Identifica ad con CTR worst → candidata per pausa.

## Step 4 — Audience health

- Frequenza per ad set:
  - <2 = audience fresh
  - 2-3 = audience matura, performance peak
  - >3.5 = audience saturated, scaling difficile
- Reach plateau? (reach cumulativo non cresce più)
- Overlap audience tra ad set (se >2)

## Step 5 — Compara con benchmark Telesales storico

Riferimento dataset `02_ads_performance.csv`:
- Cos'è telesales: CPL benchmark €14
- Leonardo: CPL benchmark €12

Se ad attuali sotto benchmark → buon trend
Se sopra → audit cause

## Step 6 — Decisione settimanale

Matrice decisionale:

| Status | Volume | Quality | Decisione |
|---|---|---|---|
| 🟢 verde | Stabile | >40% | Mantieni, micro tweak (+10% budget se possibile) |
| 🟢 verde | Crescita | >40% | SCALING step (+20% budget se prerequisiti ok) |
| 🟡 giallo | Stabile | 30-40% | Refresh 1 creative, mantieni budget |
| 🟡 giallo | Calo | 30-40% | Pausa worst ad + 1 nuova creative |
| 🔴 rosso | Calo | <30% | Audit profondo, crisi response |
| 🔴 rosso | 0 lead | N/A | Crisi 1 (vedi crisis_response.md) |

## Step 7 — Output report

Format settimanale:

```
📋 WEEKLY AUDIT — settimana {dal-al}

EXECUTIVE SUMMARY:
- Spesa: €X / €Y budget (X% utilizzo)
- Lead: N totali, N qualified (X% quality)
- CPL medio: €X | CPL qualified: €Y
- Volume medio: X lead/gg
- Status: 🟢/🟡/🔴

TOP/WORST AD:
- Top: {ad_name} - N lead - €X CPL
- Worst: {ad_name} - N lead - €X CPL  

CREATIVE FATIGUE WATCH:
- {ad_name}: CTR -X% vs settimana scorsa (warning)

AUDIENCE HEALTH:
- AS_main: freq X.X (status)
- AS_other: freq X.X (status)

QUALITY DEEP-DIVE:
- Lead in target (P.IVA reale + decisore + >50k): N
- Pensionati passati filtro: N (X% sul totale)
- Modulo submission rate: X%

DECISIONE PROPOSTA:
{Una sola azione concreta con razionale}

PROSSIMA AUDIT: prossimo lunedì
```
