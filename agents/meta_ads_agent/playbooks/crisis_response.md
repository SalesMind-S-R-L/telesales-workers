# 🚨 CRISIS RESPONSE — Playbook

Cosa fare in scenari critici (CPL>€30, 0 lead, ad rifiutate, audience exhausted).

## CRISI 1: 0 lead in 24-48h con spesa attiva

### Diagnosi immediata (5 min)

1. **Status ad**: tutte "Attiva" o qualcuna in "In esame" / "Rifiutata"?
2. **Spesa**: sta consumando o ferma a €0?
3. **Impressions**: ne arrivano o 0?

### Scenari + azioni

**A) Spesa €0 + impression 0** → ad in revisione Meta o rifiutate
- Azione: aspetta 24h se in esame. Se rifiutate, leggi motivo → fix.

**B) Spesa normale + impression normali + 0 lead** → problema modulo/tracking
- Azione 1: testa modulo pubblicamente via link condivisione
- Azione 2: verifica integrazione CRM (lead arrivano nel foglio Google)
- Azione 3: scarica CSV lead da Ads Manager → se ci sono → problema integrazione CRM. Se non ci sono → problema modulo.

**C) Spesa normale + impression alte + 0 click** → creative non risuona
- Azione: refresh creative o pausa worst ad

### Escalation a Simone se persiste >48h

Subject: `[CRITICAL] Meta Ads — 0 lead da 48h`

Body:
```
Diagnosi: {scenario A/B/C}
Cause probabili: {lista ordinata}
Azione consigliata: {1 sola, alto impatto}
Decisione richiesta: ok/no
```

---

## CRISI 2: CPL salita >€40 da €15

### Diagnosi (10 min)

1. **Quando è iniziata la salita?** (audit ultimi 7gg per identificare giorno di cambio)
2. **Cosa è cambiato quel giorno?** (budget? creative? targeting? — controlla 03_decisioni_log.csv)
3. **Quale ad ha guidato la salita?** (top spender ha CPL salito?)
4. **Frequenza?** (se >4 → audience exhausted)
5. **CPM?** (se >€40 → competizione alta o quality score dropped)

### Cause + azioni

**Creative fatigue** (CTR sceso del >30% in 7gg)
- Azione: pausa ad worst, lancia 1 nuova creative

**Audience exhaustion** (freq >4, reach plateau)
- Azione: allarga lookalike (1% → 2-3%), aggiungi custom audience nuova

**Competizione/CPM esploso**
- Azione: nessuna azione operativa, aspettare 7gg. Se persiste, considerare cambio orario delivery o placement

**Quality score scaduto**
- Azione: refresh totale creative, allinea body+headline+CTA

### Azione di emergenza

Se CPL >€40 per 5gg → **riduci budget del 30%** per stabilizzare, fai audit + riparte gradualmente.

---

## CRISI 3: Pensionati >40% nei lead (filtro modulo bucato)

### Audit (15 min)

1. Esporta lead ultimi 14gg
2. Per ognuno verifica:
   - Q1 ruolo: chi ha risposto "Sì decisore" ma è pensionato?
   - Q3 P.IVA: numero valido? (test su visura.it)
   - Età stimata dal nome/social
3. Identifica pattern: i pensionati passano grazie a... quale Q?

### Cause probabili

- Q1 troppo permissivo: "Sì decisore" include freelance/pensionati che hanno P.IVA
- Q3 P.IVA: alcuni pensionati hanno P.IVA → filtro inefficace
- Modulo troppo lasso: serve domanda più hard

### Azione

**Proponi a Simone** (duplicazione modulo):
- Mantieni Q1, Q2, Q3 P.IVA, Q4
- **AGGIUNGI nuova Q5**: "Hai dipendenti nella tua azienda?" → Sì / No
- "No" = filtro pensionati/freelance solo

⚠️ Duplicazione modulo = reset learning. Valutare costo/benefit.

---

## CRISI 4: Ad rifiutate da Meta

### Diagnosi

1. Vai su ad rifiutata → click "Vedi motivo"
2. Categorie comuni:
   - Personal attributes (es. età, salute, religione)
   - Misleading claims
   - Restricted content (es. crypto, salute, prestiti)
   - Trademark issues
   - Low quality

### Azione per categoria

**Personal attributes** (es. "Sei un imprenditore?")
- Riformula: da "Sei imprenditore?" a "Aziende B2B con team commerciale"
- Resubmit

**Misleading claims** (es. "Garantito 50 appuntamenti")
- Riformula evitando garanzie numeriche
- Resubmit

**Restricted** (raro per Telesales B2B)
- Cambia angolo, evita parole trigger

### Se la richiesta è ingiustificata

- Click "Richiedi revisione" → spiega contesto
- Tempo di risposta Meta: 24-72h

---

## CRISI 5: Budget bruciato senza risultati

### Quando è "budget bruciato"

- Spesa cumulata >€500 in 30gg con CPL medio >€40 e quality <20%

### Audit completo prima di pivotare (30 min)

1. Quale ad ha consumato di più? Performance individuale
2. Audience: troppo stretta/larga? Quale ad set ha performato meglio?
3. Creative: hook che ha funzionato in passato?
4. Modulo: submission rate? Drop-off?
5. Targeting: città giuste? Audience anziana?

### Azioni di pivot

**Opzione 1 — Pivot creative**
- Identifica creative best storico
- Crea variante moderna stesso angle
- Test 7gg con budget basso

**Opzione 2 — Pivot audience**
- Audience più ampia (no LAL, no custom)
- O più stretta (solo retargeting warm)

**Opzione 3 — Pivot modulo**
- Modulo più corto (3 domande max)
- O modulo più hard (escludere pensionati definitivamente)

**Opzione 4 — Pause + sit-down**
- Pausa campagna 1 settimana
- Sit-down con Simone, ripartire da zero

### Decisione finale

Mai prendere unilateralmente decisione "stop campagna". Sempre escalation a Simone con:
- Dati cumulativi 30gg
- 3 opzioni di pivot
- Tua raccomandazione + razionale
- Budget richiesto per il test del pivot
