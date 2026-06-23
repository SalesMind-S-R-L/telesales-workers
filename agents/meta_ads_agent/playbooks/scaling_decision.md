# 🚀 SCALING DECISION — Playbook

Quando proporre +budget? Algoritmo decisione.

## Pre-requisiti (devono essere TUTTI veri)

- [ ] CPL <€20 medio 7gg
- [ ] Quality rate >40% (post-chiamate setter)
- [ ] Volume lead/giorno costante negli ultimi 5gg
- [ ] Frequenza <3 a 7gg (audience non saturata)
- [ ] CTR ad principale >1.5%
- [ ] Spesa daily ~95-100% del budget (Meta consuma tutto)
- [ ] Nessun cambio recente >5gg (creative o targeting)

Se anche UN solo punto è no → NIENTE scaling. Aspettare.

## Algoritmo step incrementali

```
budget_attuale = X
step_1 = X * 1.20  (+20%)
step_2 = step_1 * 1.20 (+20% sul nuovo, equivale a +44% vs originale)
step_3 = step_2 * 1.20 (+20% sul nuovo, equivale a +73% vs originale)
```

**Mai più di 3 step consecutivi.** Dopo step 3 → pausa 10 giorni di consolidamento.

## Tra uno step e l'altro

**Aspetta 3-5 giorni** di stabilità prima del prossimo step.

Cosa verificare dopo ogni step:
- CPL si mantiene o sale max 10%?
- Volume scala proporzionalmente?
- Frequenza non esplode?

Se uno di questi è no → STOP, torna a budget precedente, aspetta 7gg.

## Esempi numerici

### Caso 1: scaling da €25 a €52

```
Day 0:  budget €25 - CPL €14 - 2 lead/gg ✅
Day 4:  +20% → €30 - CPL €15 - 2.5 lead/gg ✅ procede
Day 8:  +20% → €36 - CPL €16 - 3 lead/gg ✅ procede
Day 12: +20% → €43 - CPL €18 - 3.2 lead/gg ⚠️ ma volume cresce, OK
Day 16: pausa 10gg, monitoraggio
Day 26: se stabile → eventuale ulteriore +20% a €52
```

### Caso 2: scaling che fallisce

```
Day 0:  budget €25 - CPL €14 ✅
Day 4:  +20% → €30 - CPL €17 - 2 lead/gg (volume non cresce!)
Day 5:  CPL sale a €20, frequenza 3.8
Day 6:  STOP! Torna a €25
        Audit: audience troppo stretta, serve refresh creative o LAL nuova
```

### Caso 3: scaling con creative refresh

```
Day 0:  budget €30 - CPL €15 - 1.5 lead/gg (stabile da 14gg)
Day 1:  decisione: scaling con refresh
        - Pausa 1 worst ad
        - Lancia 1 nuova creative
        - Budget invariato €30
Day 4:  verifica nuova creative ha CPL <€20 → ok scaling
        +20% → €36
Day 8:  +20% → €43
Day 12: stop, consolidamento
```

## Decision tree completo

```
START
  │
  ├─ Tutti i pre-requisiti soddisfatti? ──NO──> AspettA, no scaling
  │  ↓ SI
  │
  ├─ Quale step di scaling sei? ──> step_3 raggiunto ──> Pausa 10gg
  │  ↓ <3 step
  │
  ├─ Calcola nuovo budget (+20%)
  │
  ├─ Proponi a Simone: "Budget €X → €Y, scaling step N/3"
  │
  ├─ ATTENDI 3-5gg
  │
  ├─ Verifica metriche:
  │   - CPL salito max 10%? ──NO──> Torna budget precedente
  │   - Volume cresciuto? ──NO──> Torna budget precedente
  │   - Frequenza <3.5? ──NO──> Pausa, audience saturata
  │   ↓ SI a tutti
  │
  ├─ Aggiorna 03_decisioni_log.csv
  │
  └─ Loop: torna a START dopo 3-5gg
```

## Quando NON scalare anche se condizioni ok

- **Settimana corta** (festività): risultati distorti, salta
- **Cambio macroeconomico** (es. crisi settore B2B): potenziale impatto sulla domanda
- **Test creative in corso**: prima vedi risultati del test, poi scali
- **Budget mensile vicino al cap**: se hai già speso 80% del budget mensile, non scalare nei restanti giorni

## Anti-pattern (da NON fare mai)

❌ +50% budget in un colpo: rompe learning, CPL schizza
❌ Scaling durante prima settimana lancio campagna nuova
❌ Scaling con 1 sola ad attiva (rischio massimo se quella ad cala)
❌ Scaling senza audit qualità lead (CPL può essere basso ma quality zero)
❌ Scaling weekend (CTR e CPL diversi vs weekday in B2B)
