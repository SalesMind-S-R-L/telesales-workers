# 06 — Pricing Strategy

**Telesales — Maggio 2026**
*Fortune 500 pricing consultant analysis: competitive audit + value-based + cost-plus + 3 tier + revenue scenarios.*

---

## TL;DR

**3 pricing tier raccomandati**:

| Tier | Prezzo target | Target persona | ARPU annuo |
|---|---|---|---|
| **Starter AI-only** | €1.490/mese | Agenzie piccole / coach singoli / PMI test | €17.880 |
| **Pro Hybrid** *(recommended)* | €3.290/mese | Persona 1, 2, 4 (cuore del mercato) | €39.480 |
| **Premium Performance** | €5.990/mese + €/appuntamento variabile | Persona 3 (cliente flagship B2C) / Persona 2 enterprise | €72k - 200k+ |

Floor cost-plus: €1.100/mese (margine 25% min). Ceiling value-based: €15-20k/mese per progetti riattivazione B2C (basato su revenue generata).

---

## 1. Competitive pricing audit

### 1.1 Italia — boutique B2B (comparable diretti)

| Player | Modello | Range prezzo | Trasparenza |
|---|---|---|---|
| **TeleLead.it** | Pay-per-appointment | €20-35/app a volume; €700+IVA per 20 app (€35/app); €4.000+IVA per 200 app (€20/app) | **Listino pubblico** |
| **L'Ippogrifo Group** | Retainer + performance | €2.000-8.000/mese stimato | Su richiesta |
| **Telemarketingb2b.it** | Pay-per-call + pay-per-appointment | €750+IVA per 1.000 chiamate | Listino parziale |
| **Web Leaders / Media Servizi** | Misto | €1.500-5.000/mese stimato | Su richiesta |

Fonti: [TeleLead](https://telelead.it/appuntamenti-b2b/), [Ippogrifo Group](https://www.ippogrifogroup.com/marketingevenditeb2b/quanto-costa-un-appuntamento-nel-b2b-numeri/), [leadhunt](https://www.leadhunt.it/blog/telemarketing-b2b-2024).

### 1.2 USA / Global benchmarks (per posizionamento alto)

| Tipo offerta | Range |
|---|---|
| Pay-per-meeting USA | $100-1.700 per appuntamento qualificato |
| Retainer mensile USA | $3.000-10.000+ |
| In-house SDR fully-loaded USA | $9.800-14.200/mese |

Fonti: [Leads at Scale](https://leadsatscale.com/insights/b2b-appointment-setting-pricing-guide-complete-2025-breakdown/).

### 1.3 AI Voice platforms self-serve (substitute pricing)

| Piattaforma | $/min platform fee | Note |
|---|---|---|
| ElevenLabs Agents | $0,08-0,12 | Top quality italiano |
| OpenAI Realtime | $0,18-0,46 | Premium pricing |
| Deepgram Voice Agent | $0,075 ($4,50/h) | Best value |
| Vapi | $0,05 + infra | Developer-grade |
| Synthflow | $0,12-0,13 over-usage | No-code, target SMB |
| Bland AI | $0,11-0,14 | SMB/Enterprise |

Per costo orario equivalente all-in (TTS + STT + LLM + telephony + supervisor): **stima propria $7-12/h** (vs setter umano IT $25-39/h fully loaded).

### 1.4 In-house build-vs-buy benchmark per cliente

- Setter junior IT: €25-39k/anno costo aziendale + 3-6 mesi onboarding
- Setter senior IT: €40-55k/anno + manageriality founder
- Outsourcing Telesales Pro Hybrid: €30-39k/anno chiavi in mano, attivo in 2-4 settimane

**Conclusione**: Telesales può posizionarsi competitivo vs in-house anche a €3.000-3.500/mese se messaggio "speed + risk-free + tech edge" è chiaro.

---

## 2. Cost-plus floor analysis (analisi del costo)

### 2.1 Costo unitario all-in per cliente Pro Hybrid (stima propria)

Ipotesi: cliente medio Pro Hybrid riceve 25-30 appuntamenti qualificati al mese, generati da ~600-900 chiamate AI + ~80-100 follow-up umani.

| Voce di costo | €/mese |
|---|---|
| **AI infra**: 600 call × 5 min media × $0,10/min × €0,93/$ | €280 |
| **Telefonia Telnyx**: 600 call × 5 min × $0,005/min | €14 |
| **Setter umano dedicato** (frazione di tempo: 30%): 0,3 × €3.500 costo aziendale mensile | €1.050 |
| **CRM / GoHighLevel / dashboard**: $497/mese / 30 clienti distribuito | €15 |
| **Software outbound (Cribis, Apollo, altre subscriptions)**: distribuito | €40 |
| **Compliance / DPA / monitoring**: distribuito | €20 |
| **Manageriality / supervisor / training**: 5% retainer | €165 |
| **Costo diretto totale (gross cost)** | **~€1.585** |
| Allocazione overhead aziendale (15%) | €240 |
| **Costo all-in** | **~€1.825** |

Floor cost-plus 25% margin = **€2.430/mese**. Floor 40% margin = €3.040/mese.

### 2.2 Costo Starter AI-only (cliente più leggero)

Ipotesi: 200 chiamate AI/mese, setter umano supervisore 10%.

| Voce | €/mese |
|---|---|
| AI infra: 200 × 4 min × $0,10/min | €75 |
| Telefonia: 200 × 4 min × $0,005 | €4 |
| Setter supervisor 10%: 0,1 × €3.500 | €350 |
| CRM/software distribuito | €40 |
| Compliance/overhead | €40 |
| **Gross cost** | **~€510** |
| Overhead aziendale 15% | €77 |
| **Costo all-in** | **~€590** |

Floor cost-plus 40% margin = **€825/mese**. Floor 60% margin = €1.180/mese.

### 2.3 Premium Performance (cliente flagship B2C / infomarketer)

Cliente flagship B2C (infomarketing)-type: 80-100k lead, riattivazione su 12 mesi.

| Voce | €/mese (su campagna 12 mesi) |
|---|---|
| AI infra: 8.000 call/mese × 4 min × $0,10/min | €2.980 |
| Telefonia: 8.000 × 4 min × $0,005 | €150 |
| Setter umano dedicato (full-time): 1,0 × €3.500 | €3.500 |
| Strategist / supervisor (frazionale 25%): 0,25 × €5.500 (senior) | €1.375 |
| CRM/integrazione/dashboard custom | €200 |
| Compliance/audit lead provenance | €100 |
| **Gross cost** | **~€8.305** |
| Overhead aziendale 20% (per progetti enterprise) | €1.660 |
| **Costo all-in** | **~€10.000** |

Floor cost-plus 40% margin = **€14.000/mese**. Floor 50% margin = €16.700/mese.

---

## 3. Value-based pricing ceiling

### 3.1 Valore generato per cliente Pro Hybrid

Ipotesi (Persona 1 — agenzia €500k fatturato):
- 25 appuntamenti/mese × 30% close rate (clienti agency vendono €5-15k/contratto medio) × €8.000 deal medio = **€60.000 revenue mensile attribuibile**
- LTV cliente agenzia: ~€20-40k/anno (retainer recurring) × 18 mesi avg retention = **€30-60k LTV cliente acquisito**
- 5-10 nuovi clienti acquisiti/mese via Telesales = **€150-600k LTV aggregate generato/mese**

**Value-based pricing accettabile**: 5-15% del valore generato = €7.500-90.000/mese teorici. Sweet spot: **€2.500-5.000/mese** (4-8% del valore, sotto pressione concorrenziale).

### 3.2 Valore generato per Premium (cliente flagship B2C / infomarketer)

Ipotesi (cliente flagship B2C con 80k lead dormienti):
- 20 app/giorno × 22 gg/mese = 440 app/mese
- 30-50% show-up = 130-220 mostranti
- 5-15% close rate su mostranti × €2.000-5.000 ticket medio = **€13.000-165.000/mese revenue attribuibile**
- Media stimata: **€60-100k/mese revenue lord generato** per cliente flagship B2C-type

**Value-based pricing accettabile**: 15-25% revenue generata = **€9.000-25.000/mese**. Confermato dal range €100-200k ARPU annuo.

### 3.3 Valore generato per Starter AI-only

Ipotesi (Persona 1 piccola o test):
- 8-12 app/mese × 25% close × €4.000 deal = **€8.000-12.000 revenue mensile**

**Value-based ceiling**: 15-25% = €1.200-3.000/mese. Coerente con prezzo target €1.490/mese.

---

## 4. Price elasticity estimate

### 4.1 Sensibilità per persona

| Persona | Elasticità prezzo | Razionale | Range tollerabile |
|---|---|---|---|
| **Persona 1 — Agenzia** | Media-alta | Confronta sempre con build in-house e altri vendor | €2.000-4.500/mese |
| **Persona 2 — Scale-up** | Media | ROI calc richiesto; performance bonus accettato | €3.000-7.000/mese |
| **Persona 3 — Infomarketer** | Bassa | Valuta % di revenue generato, non prezzo assoluto | €5.000-25.000/mese |
| **Persona 4 — PMI manifatturiera** | Alta | Price-sensitive ("sotto €2.000 non lo prendo sul serio" ma anche "€5.000 troppo") | €2.500-4.500/mese |

### 4.2 Soglie psicologiche identificate

- **Sotto €1.500/mese**: percepito "non serio" per Persona 1, 2, 4 (Persona 3 OK come pilot)
- **Tra €2.000-3.500/mese**: sweet spot mass market PMI (Persona 1, 4)
- **Tra €3.500-6.000/mese**: scale-up + agenzie strutturate (Persona 1, 2)
- **Tra €6.000-15.000/mese**: enterprise / infomarketer / premium (Persona 2, 3)
- **Oltre €15.000/mese**: solo Persona 3 con valore generato dimostrato + brand premium

---

## 5. Psychological pricing strategies

### 5.1 Anchoring
**Prezzo anchor in pitch**: parlare prima del costo SDR in-house (€35-45k/anno) + cost-of-failure (3-6 mesi onboarding) → poi Telesales Pro Hybrid €39k/anno appare razionale e meno rischioso.

### 5.2 Charm pricing
- Starter: **€1.490/mese** (sotto soglia €1.500)
- Pro Hybrid: **€3.290/mese** (sotto soglia €3.500)
- Premium: **€5.990/mese** + variabile (sotto soglia €6.000)

### 5.3 Decoy strategy
- Pro Hybrid è il "tier obiettivo": include AI Voice + setter dedicato + dashboard + reporting weekly.
- Starter è il decoy "limited" (no setter dedicato, max 10 app/mese, no integrazione CRM premium).
- Premium è il decoy "ambitious" (per spingere customer middle-tier verso Pro Hybrid come "il prodotto giusto").

### 5.4 Bundling
- Pro Hybrid include: AI Voice + 1 setter dedicato 30% + dashboard + 1 case study + onboarding playbook.
- Add-on possibili: voice cloning founder (+€500/mese setup + €100/mese), integrazione CRM custom (+€800 setup), reporting white-label (+€200/mese).

---

## 6. Tiering recommendation — 3 pricing tier

### 6.1 Tier 1 — Starter AI-only

**Prezzo**: €1.490/mese (€17.880/anno)
**Target persona**: Persona 4 piccolo (PMI piccola test), Persona 1 piccola (agenzia <€200k), coach singolo
**Cosa include**:
- 1 agente AI Voice italiano (ElevenLabs Multilingual v2)
- Fino a 300 chiamate outbound/mese
- Max 10 appuntamenti qualificati/mese (oltre, scatta upsell)
- Dashboard self-serve (read-only)
- Integrazione CRM base (GHL o HubSpot)
- Setter umano supervisor 10% (review chiamate critiche)
- Reporting mensile via email PDF
- Onboarding 2 settimane
- Compliance AI Act + GDPR base

**Cosa NON include**:
- Setter dedicato
- Multi-canale (email/LinkedIn sincronizzato)
- Reporting weekly live
- Voice cloning
- Garanzia performance
- Integrazione custom

**Gross margin target**: 60% (€590 cost → €1.490 price = €900 margin = 60%)

**Quota stimata customer base 2026-27**: 30-40% dei clienti

### 6.2 Tier 2 — Pro Hybrid (recommended / star tier)

**Prezzo**: €3.290/mese (€39.480/anno)
**Target persona**: Persona 1 (agenzia €500k-1M), Persona 2 (scale-up early), Persona 4 (PMI manifatturiera media)
**Cosa include**:
- 2 agenti AI Voice italiani configurabili (per multi-vertical)
- Fino a 900 chiamate outbound/mese
- 25-30 appuntamenti qualificati/mese (oltre, performance bonus €30/app)
- Dashboard live + accesso founder/team
- Integrazione CRM premium (GHL, HubSpot, Pipedrive, Salesforce native)
- 1 setter umano dedicato 30% (qualifica top decisori)
- Reporting weekly live + QBR mensile
- Onboarding 14 giorni con success manager dedicato
- Compliance AI Act Art. 50 + GDPR + DPA + lead provenance audit
- Voice cloning founder cliente (opzionale, +€500 setup)

**Cosa NON include**:
- Riattivazione database >50k lead
- Strategy consulting esteso (campaign architecture)
- White-label per uso terzi

**Gross margin target**: 55% (€1.825 cost → €3.290 price = €1.465 margin = 45%; con upsell add-on sale al 55%)

**Quota stimata customer base 2026-27**: 50-60% dei clienti

### 6.3 Tier 3 — Premium Performance

**Prezzo base**: €5.990/mese (€71.880/anno) + €/appuntamento variabile (€40-80) o % revenue
**Target persona**: Persona 3 (cliente flagship B2C / infomarketer), Persona 2 (scale-up scaling), enterprise customer
**Cosa include**:
- N agenti AI Voice italiani custom + voice cloning premium (Cartesia 3s clone)
- Chiamate outbound illimitate (fair use 8.000-15.000/mese)
- Setter umano full-time dedicato + strategist senior 25% (campaign architecture)
- Riattivazione database storico (50k-500k lead)
- Dashboard live custom + branded
- Integrazione CRM custom + webhook + dataflow specifico
- Reporting weekly + QBR mensile + advisory bimestrale
- Compliance AI Act + GDPR + DPA + recording + audit log per cliente regolato
- Strategy consulting illimitato (campaign architecture, retargeting, multicanale)
- Garanzia minima: 15 appuntamenti qualificati/settimana o credito proporzionale
- Onboarding 7-10 giorni con head of customer success

**Variable add-on**:
- Performance bonus: €30-50/appuntamento sopra threshold
- Revenue share opzionale: 5-10% delle vendite generate (per cliente B2C alto-ticket)
- Custom voice cloning: +€2.000 setup + €300/mese

**Gross margin target**: 50% (€10.000 cost → €5.990 base + €/app variabile = blended €15-25k/mese → 40-60% margin)

**Quota stimata customer base 2026-27**: 10-15% dei clienti ma 40-50% del revenue

---

## 7. Discount strategy

### 7.1 Quando scontare

| Scenario | Sconto consigliato | Razionale |
|---|---|---|
| **Pagamento annuale upfront** | -10% (€39k diventa €35k) | Cash flow + retention |
| **Pilot 90 giorni a forfait** | -30% (€3.290 diventa €2.290 × 3 mesi) | Reduce risk perception, kick start |
| **Marquee logo / referente strategico** | -20% per 6-12 mesi | Costruire portfolio |
| **Founder/CEO peer referral** | -15% primi 12 mesi al referenziato + 20% revenue share al referente | Growth engine |
| **Multi-anno (24-36 mesi)** | -15% | Retention long-term |
| **Volume (clienti multipli stessa holding)** | -10-25% | Account expansion |

### 7.2 Quando NON scontare

- Cliente Persona 3 (cliente flagship B2C) con WTP €100k+ → mai sconto base, eventualmente upsell
- Cliente Persona 4 manifatturiera che pretende sconto al primo contatto → walk away (price sensitivity sovra-media, churn alto)
- Senza commitment 6+ mesi → no sconto

---

## 8. Revenue projection — 3 scenari (24 mesi)

### 8.1 Assunzioni base

- Q1: 12 clienti acquisiti (stato attuale + 6)
- Mix tier base/Pro/Premium = 30% / 60% / 10%
- ARPU blended: 30%×17.880 + 60%×39.480 + 10%×72k = **€36.252/anno**
- Churn annuo: 18% (in linea con benchmark B2B services 17% — [CustomerGauge](https://customergauge.com/blog/average-churn-rate-by-industry))
- Net revenue retention: 105% (upsell e cross-sell add-on)

### 8.2 Scenario CONSERVATIVO

- 12 clienti Q1, +3 netti/trimestre, churn 20% annuo
- Q4 2026: 18 clienti × €36.252 ARPU = €652.500 ARR
- Q4 2027: 26 clienti × €36.252 = €943.000 ARR
- Q4 2028: 34 clienti × €36.252 = €1.232.500 ARR

### 8.3 Scenario MODERATO (base case)

- 12 clienti Q1, +5 netti/trimestre, churn 18% annuo
- Q4 2026: 24 clienti × €36.252 = €870.000 ARR
- Q4 2027: 44 clienti × €36.252 = €1.595.000 ARR
- Q4 2028: 66 clienti × €36.252 = €2.392.500 ARR

### 8.4 Scenario AGGRESSIVO

- 12 clienti Q1, +8 netti/trimestre, churn 15% annuo
- Q4 2026: 36 clienti × €36.252 = €1.305.000 ARR
- Mix tier shift: 20% Starter / 55% Pro / 25% Premium → blended ARPU €48.500
- Q4 2027: 68 clienti × €48.500 ARPU = €3.298.000 ARR
- Q4 2028: 112 clienti × €48.500 = €5.432.000 ARR
- + 5-8 clienti DACH/UK contributo €500k-1M

### 8.5 Sintesi 3 anni ARR scenarios

| Scenario | Q4 2026 ARR | Q4 2027 ARR | Q4 2028 ARR |
|---|---|---|---|
| Conservative | €650k | €943k | €1,2 M |
| **Moderato** | **€870k** | **€1,6 M** | **€2,4 M** |
| Aggressive | €1,3 M | €3,3 M | €5,4 M |

---

## 9. Monetization opportunities (upsell / cross-sell / usage-based)

### 9.1 Upsell

- Da Starter → Pro Hybrid (+€1.800/mese): in media il 25% degli Starter sale entro 6 mesi
- Da Pro Hybrid → Premium (+€2.700/mese): in media il 10% sale entro 12 mesi
- Performance bonus per appuntamenti extra (Pro Hybrid): €30/app sopra threshold 25 → ARPU effettivo +€500-1.500/mese

### 9.2 Cross-sell

- **Voice cloning premium**: +€500 setup + €100/mese
- **Custom dashboard branded**: +€800/mese
- **Multi-canale orchestration (email/LinkedIn integrato)**: +€700/mese
- **Strategy advisory bimestrale**: +€1.500/mese
- **Compliance audit annuale (per cliente regolato)**: +€2.000 una tantum

### 9.3 Usage-based add-on

- Chiamate aggiuntive oltre fair use: €0,30/min (markup 2,5× su costo $0,12/min)
- Riattivazione database storico una tantum: €2.000-15.000 setup + per-call

### 9.4 White-label / partner revenue

- Programma white-label per agenzie marketing IT: €5.000 setup + 20-30% revenue share su clienti portati
- Target: 10-20 partner attivi entro Q4 2027 → potenziale €500k-1M ARR aggiuntivo

---

## 10. Specific dollar/euro recommendations

### 10.1 Listino raccomandato (effective Q3 2026)

```
┌─────────────────────────────────────────────────────────────┐
│ TELESALES — LISTINO 2026/2027                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  STARTER AI-only                                             │
│  €1.490/mese — Annuale €15.488 (-13%)                        │
│  Fino a 10 appuntamenti/mese, 1 agente AI, dashboard         │
│                                                              │
│  PRO HYBRID *(consigliato)*                                  │
│  €3.290/mese — Annuale €35.532 (-10%)                        │
│  25-30 appuntamenti/mese, 2 agenti, setter dedicato          │
│  +€30/app oltre 30 (performance bonus)                       │
│                                                              │
│  PREMIUM PERFORMANCE                                         │
│  €5.990/mese + €40-80/app                                    │
│  Volume illimitato, riattivazione database, strategist       │
│  Garantizza minimo 15 app/sett o credito                     │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  Add-on:                                                     │
│  Voice cloning founder         €500 setup + €100/mese        │
│  Multi-canale orchestration    €700/mese                     │
│  Strategy advisory             €1.500/mese                   │
│  Compliance audit annuale      €2.000 una tantum             │
│  Custom dashboard branded      €800/mese                     │
└─────────────────────────────────────────────────────────────┘
```

### 10.2 Pricing policy (sintesi)

- **No public pricing online sul tier Premium** (call required) — riserva flessibilità per casi value-based.
- **Starter e Pro Hybrid pubblicati** sul sito → trasparenza come wedge vs L'Ippogrifo + altri.
- **Annuale = sconto -10-13%** (vs mensile).
- **Pilot 90 gg a forfait** -30% disponibile su Pro Hybrid solo (no Starter, no Premium).
- **Performance bonus** sempre su Pro Hybrid (sopra threshold) e Premium.

---

## 11. So what — implicazioni

1. **Pubblicare listino Starter + Pro Hybrid online** per primo nel segmento boutique IT = brand-leadership + lead inbound qualificati.
2. **Concentrare 60% del marketing sull'acquisizione tier Pro Hybrid** (sweet spot ARPU/scale).
3. **Premium tier è il "growth engine ARR"** — un cliente Premium = 4-5 clienti Pro Hybrid in valore. Andare a caccia di 2-3 nuovi Premium/anno.
4. **Performance bonus** è leva chiave per upsell senza vendita aggressiva — cliente paga di più solo se ottiene di più.
5. **Multi-anno + annuale upfront** strategici per cash flow + retention; pricing già impostato per incentivarli.

Continua in [`07_gtm_playbook.md`](07_gtm_playbook.md).
