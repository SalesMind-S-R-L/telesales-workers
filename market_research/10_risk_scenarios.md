# 10 — Risk Assessment & Scenario Planning

**Telesales — Maggio 2026**
*Deloitte risk partner analysis: 15 risk in 5 categorie con probability×impact + 4 scenari.*

> Per il modello live, vedi [`risk_matrix.xlsx`](risk_matrix.xlsx).

---

## TL;DR — Top 5 risk prioritari

| Rank | Risk | Score | Categoria |
|---|---|---|---|
| 1 | AI Act Art. 50 non compliance al 2 ago 2026 | 20 (P5×I4) | Regulatory |
| 2 | Commoditization piattaforme Voice AI (Vapi/Synthflow italianizzano UX) | 16 (P4×I4) | Market |
| 3 | Dipendenza tecnica da ElevenLabs (single supplier) | 12 (P3×I4) | Operational |
| 4 | Founder bandwidth saturato (key person dependency) | 12 (P4×I3) | Operational |
| 5 | Sanzione Garante per cliente B2C riattivazione (filiera cliente flagship B2C) | 10 (P2×I5) | Regulatory |

---

## 1. Risk identification — 15 risk

Probability rating 1-5 (1 = improbabile, 5 = quasi certo).
Impact severity rating 1-5 (1 = minimo, 5 = catastrofico).
Risk score = P × I.

### 1.1 Market risks (R1-R3)

**R1 — Commoditization piattaforme Voice AI**
- **Descrizione**: Vapi, Synthflow, Retell italianizzano UX entro 12-24 mesi → cliente PMI può fare in-house con €500/mese di subscription invece di pagare Telesales €3.290/mese.
- **Probability**: 4 (alta — trend in atto, Vapi $500M mag 2026)
- **Impact**: 4 (perdita 30-50% di ARPU su nuove acquisizioni)
- **Score**: **16**
- **Early warning indicators**: aumento self-serve voice AI tool in italiano; recensioni G2 / Capterra player con UI italiano nativo; saturazione SERP "AI voice agent italiano".
- **Mitigation**:
  - Brand-leadership di pensiero entro Q3 2026 (report di settore)
  - Vertical specialization: dominare 2-3 verticali (infomarketing, agency, manifatturiera) con KB proprietaria difficile da replicare
  - Managed service value proposition (no self-serve)
- **Contingency**: pivot a strategia "premium managed service" + abbandono fascia low; oppure white-label per partner per coprire fascia commodity.

**R2 — Recession economica EU / IT 2026-2027**
- **Descrizione**: clienti tagliano budget marketing/sales; ICP "scale-up" più esposti.
- **Probability**: 3 (cycle economic, geopolitica)
- **Impact**: 3 (churn +5pp, new logo rate -30%)
- **Score**: **9**
- **Early warning indicators**: PMI italiana sentiment index (Confindustria); LinkedIn job cuts; CPM Meta in calo (segnale di taglio budget marketing).
- **Mitigation**:
  - Diversificazione clienti (no >15% revenue da singolo cliente)
  - Pricing flexibility tier (Starter come downgrade option vs churn)
  - Riserva cash 6 mesi OpEx sempre disponibile
- **Contingency**: freeze hiring; rinegoziazione partner; sconti retention (-20% per 6 mesi).

**R3 — Concorrenza enterprise (Sierra/Parloa/NICE Cognigy) scende a PMI**
- **Descrizione**: dopo M&A wave 2025-2026 (NICE/Cognigy €955M, Sierra $15,8B), gli enterprise voice AI scendono di posizionamento per crescere → competere su PMI italiana.
- **Probability**: 2 (improbabile nel breve, alta nel 2028+)
- **Impact**: 4 (commoditization aggressiva pressing margins)
- **Score**: **8**
- **Early warning**: launch SMB tier di Sierra/Parloa; assunzioni VP Sales SMB in Italia/EU.
- **Mitigation**: costruire brand-loyalty + comunità clienti + casi studio specifici PMI italiane prima del 2028.
- **Contingency**: posizionarsi come "Parloa Italia partner ufficiale" o cercare M&A friendly.

### 1.2 Operational risks (R4-R6)

**R4 — Dipendenza tecnica da ElevenLabs**
- **Descrizione**: se ElevenLabs aumenta prezzi 2-3×, ha downtime prolungato, o cambia ToS limitando outbound → Telesales subisce immediatamente.
- **Probability**: 3 (medio — ElevenLabs è private, pressioni pricing crescenti dopo $11B raise)
- **Impact**: 4 (40-60% costo servizio + brand voice change)
- **Score**: **12**
- **Early warning**: pricing changes ElevenLabs; downtime incidents (status page); cambiamenti ToS.
- **Mitigation**:
  - Multi-vendor stack pronto entro Q3 2026: Cartesia (Sonic 3) + Deepgram Voice Agent come backup
  - Astrazione provider TTS nello stack interno
  - Contratto enterprise ElevenLabs con SLA
- **Contingency**: switch a Cartesia per nuovi clienti in 30 giorni; comunicazione preventiva clienti esistenti.

**R5 — Founder key person dependency**
- **Descrizione**: il founder è single point of failure su sales, prodotto, strategia. Burnout, malattia, o fortuna esterna → azienda paralizzata.
- **Probability**: 4 (alta — bandwidth founder già stressato secondo memory)
- **Impact**: 3 (operations possono continuare 2-3 mesi senza founder, poi degrado)
- **Score**: **12**
- **Early warning**: founder non risponde >24h; missing 2+ QBR cliente; ridotta velocity post LinkedIn.
- **Mitigation**:
  - Hire marketing manager entro 1 giu 2026 + enterprise AE entro Q4 2026
  - Documentazione processi (Notion playbook esecuzione)
  - Power of attorney commerciale a setter senior
  - Founder "off-time" obbligatorio 1 sett/trimestre
- **Contingency**: setter senior promosso ad interim COO; pausa hiring nuovo + focus retention.

**R6 — Setter umano turnover (setter senior)**
- **Descrizione**: setter dedicati dimettono → cliente perde continuità → churn signal.
- **Probability**: 3 (turnover SDR alto industria)
- **Impact**: 3 (3-6 settimane di disruption per cliente)
- **Score**: **9**
- **Early warning**: setter NPS basso interno; missing 1:1 meeting; richieste salario.
- **Mitigation**:
  - Performance bonus + carriera path (es. da Setter → Account Manager → Strategist)
  - Hire backup setter (1 in più del bisogno) come safety
  - Standardize playbook script + KB per facilità handover
- **Contingency**: redistribuzione clienti su setter residui per 2 settimane; hire urgente (talent ex-BPO disponibile post-crisi).

### 1.3 Financial risks (R7-R9)

**R7 — Cash flow stress da onboarding lungo / pagamento ritardato**
- **Descrizione**: contratti pluri-mensili con pagamento dilazionato 30-60 gg → working capital negativo durante crescita rapida.
- **Probability**: 3 (medio — comune nelle agency in fase scaling)
- **Impact**: 3 (cash crunch a metà Y1 se hiring + marketing accelerano)
- **Score**: **9**
- **Mitigation**:
  - Stripe / Paypal automated billing per Starter + Pro (no bonifico)
  - Pagamento annuale upfront con sconto -10/13%
  - Linea di credito banca/factoring rotativa €100-200k
  - Cash reserve 6 mesi OpEx (€200k+)
- **Contingency**: rallentare hiring per 1 trimestre; concentrare new logo su pagamento upfront.

**R8 — CAC esplode (>€3.000) su canali esterni**
- **Descrizione**: LinkedIn ads costo +50% YoY 2025, content slowing, partner channel saturazione → CAC blended sale a €3.000+.
- **Probability**: 3 (CPC LinkedIn aumentato 12,88% YoY 2025)
- **Impact**: 4 (LTV:CAC ratio scende a 10× ancora ok, ma marginalmente)
- **Score**: **12**
- **Mitigation**:
  - Diversificare canali (no >40% acquisition da singolo canale)
  - Investire 35% budget in referral/partner (CAC più basso)
  - Content marketing per ridurre dipendenza paid
- **Contingency**: shift budget verso referral; rivedere ICP per fitness più tight.

**R9 — Currency / inflation rischi (USD up vs EUR)**
- **Descrizione**: ElevenLabs, Deepgram, Apollo billing in $; se USD si rafforza +15% vs EUR, gross margin scende 5-7pp.
- **Probability**: 2 (moderato — Fed/ECB policy dipendente)
- **Impact**: 2 (cost-shift contenuto)
- **Score**: **4**
- **Mitigation**: piano hedging valutario se esposizione >€100k/anno; preferire vendor EU dove possibile.

### 1.4 Regulatory risks (R10-R12)

**R10 — AI Act Art. 50 non compliance al 2 ago 2026**
- **Descrizione**: Telesales o un cliente non implementa disclosure vocale audibile → sanzione fino €15M o 3% turnover globale di gruppo.
- **Probability**: 5 (deadline binding certa; rischio implementazione tecnica imperfetta)
- **Impact**: 4 (sanzione + reputazione + cliente perso)
- **Score**: **20** (TOP RISK)
- **Early warning**: Garante annunci pre-binding; ispezioni industria.
- **Mitigation** (top priority operativa):
  - Disclosure vocale italiana implementata in tutti gli agenti entro **15 luglio 2026** (buffer 18 giorni)
  - Test compliance su 100+ chiamate per 3 clienti
  - DPA aggiornato per ogni cliente con clausola disclosure
  - Consulente DPA on board entro 1 luglio 2026
- **Contingency**: pausa servizio AI Voice automatizzato fino a piena compliance; comunicazione cliente preventiva.

**R11 — Sanzione Garante per cliente B2C riattivazione (filiera cliente flagship B2C)**
- **Descrizione**: cliente flagship B2C o simile usa lead senza consenso GDPR valido → sanzione cascade a Telesales come responsabile filiera (accountability).
- **Probability**: 2 (cliente flagship B2C è strutturato, ma rischio non zero in B2C)
- **Impact**: 5 (sanzione tipo Enel €79M, brand kill, class action possibile)
- **Score**: **10**
- **Early warning**: revisione lead provenance ogni cliente B2C; reclami consumatori; ispezione preliminare Garante.
- **Mitigation**:
  - Lead provenance audit obbligatorio per ogni cliente prima signing
  - Clausola contrattuale: cliente garantisce consenso, indennizza Telesales
  - DPA con audit right Telesales su lead origin
  - No accettazione clienti con lead da scraping / non-GDPR
- **Contingency**: separazione legale entity per B2C (se rischio cresce); insurance D&O.

**R12 — Class action consumatori contro telemarketing aggressivo (Telesales o filiera)**
- **Descrizione**: 3 nuove class action al mese in IT nel 2024 ([CF News](https://www.cfnews.it/societ%C3%A0-e-impresa/la-sempre-pi%C3%B9-estesa-applicazione-e-diffusione-in-italia-delle-nuove-azioni-di-classe/)). Telesales potenzialmente coinvolta per cliente fuori-compliance.
- **Probability**: 2 (Telesales compliance-first, ma rischio cascata cliente)
- **Impact**: 4 (litigation cost + reputazione)
- **Score**: **8**
- **Mitigation**: stessa R11; insurance professional liability €1-3M coverage.

### 1.5 Reputational risks (R13-R15)

**R13 — Voice AI scandal (clone fraud, impersonation case)**
- **Descrizione**: cliente Telesales clona voce e la usa per impersonation / frode → caso "Crosetto" (deepfake usato per truffe imprenditori 2025) cascade.
- **Probability**: 2 (Telesales controlla tooling, ma rischio cliente bad-actor)
- **Impact**: 5 (PR disaster, brand kill)
- **Score**: **10**
- **Mitigation**:
  - Voice cloning solo voci consensuali (founder cliente o sintetiche)
  - Watermark digitale tracciabile su voci clonate
  - Audit trail uso voci
  - Clausola contrattuale: cliente non usa voci per impersonation
- **Contingency**: cessazione immediata servizio cliente coinvolto + comunicato stampa.

**R14 — Data breach (cliente DB lead esposto)**
- **Descrizione**: hacker compromette CRM/database Telesales → 80-100k lead cliente flagship B2C o B2B database esposti.
- **Probability**: 2 (low — Telesales infrastructure è cloud-secure)
- **Impact**: 5 (sanzione GDPR + class action + brand)
- **Score**: **10**
- **Mitigation**:
  - GoHighLevel + Cloudflare + Cribis = vendor SOC 2 compliant
  - Access control / 2FA per ogni operatore
  - Penetration test annuale
  - Cyber insurance €1M coverage
- **Contingency**: incident response plan; notifica Garante entro 72h.

**R15 — Reputational contagion (associazione con cliente B2C controverso)**
- **Descrizione**: Telesales associata pubblicamente a cliente infomarketing controverso (es. Trustpilot critiche, MOW magazine) → backlash media.
- **Probability**: 3 (segmento info-business polarizzato)
- **Impact**: 3 (impatto su acquisizione clienti B2B / scale-up)
- **Score**: **9**
- **Mitigation**:
  - Due diligence cliente prima signing (review pubblica, Trustpilot, sentenze)
  - Separazione brand per fascia B2C vs B2B (eventuale sub-brand)
  - Comunicazione PR proattiva su compliance + qualità
- **Contingency**: termination clausola in contratto per associazione con cliente in litigation pubblica.

---

## 2. Risk matrix visual (probability × impact)

```
              IMPACT
              1     2     3     4     5
        ┌─────┬─────┬─────┬─────┬─────┐
PROB  5 │     │     │     │ R10 │     │  ← R10 score 20 [ATTN]
        ├─────┼─────┼─────┼─────┼─────┤
      4 │     │     │ R5  │ R1  │     │  ← R1 16 [ATTN] / R5 12
        │     │     │ R8  │     │     │
        ├─────┼─────┼─────┼─────┼─────┤
      3 │     │     │ R6  │ R4  │     │  ← R4 12 / R6 9
        │     │     │ R2  │     │     │
        │     │     │ R7  │     │     │
        ├─────┼─────┼─────┼─────┼─────┤
      2 │     │ R9  │ R15 │ R12 │ R11 │  ← R11 10 / R12 8
        │     │     │     │     │ R13 │  ← R13 10
        │     │     │     │     │ R14 │  ← R14 10
        │     │     │     │ R3  │     │  ← R3 8
        ├─────┼─────┼─────┼─────┼─────┤
      1 │     │     │     │     │     │
        └─────┴─────┴─────┴─────┴─────┘
```

**Zone**:
- **Rossa (score ≥15)**: R10 (20), R1 (16) — azione immediata richiesta
- **Arancione (score 10-14)**: R4, R5, R8 (12 ognuno), R11/R13/R14 (10) — mitigation attiva
- **Gialla (score 7-9)**: R2, R6, R7, R12, R15, R3 — monitorare
- **Verde (score <7)**: R9 — accettabile

---

## 3. Scenario planning — 4 scenari

### 3.1 Best case scenario

**Cosa va bene**:
- AI Act Art. 50 implementation perfetta (no sanzioni); compliance diventa moat
- WMF Bologna porta 8 nuovi clienti diretti
- cliente flagship B2C case study video raggiunge 200k views su LinkedIn → 30 leads inbound
- Partnership GHL Solutions Partner Gold porta 15 clienti via referral
- ElevenLabs prezzi stabili o in calo; voice italiana migliore
- Recession evitata; PMI italiana risorgere post-Q3 2026
- Seed round €1,5M @ €18M valuation Q1 2027 con multipla 18× ARR

**Revenue impact**: Y3 ARR €5,4M (scenario aggressive)
**Timeline**: 2026-2028 piena finestra opportunità
**Strategic response**: accelerare assunzioni + UE expansion + white-label launch + customer event Q4 2027

### 3.2 Base case scenario

**Cosa va come previsto**:
- 24 clienti Q4 2026, €870k ARR
- AI Act implementato in tempo, no sanzioni
- 1 partnership tier 1 attivata (GHL o HubSpot)
- 3 case study pubblicati con KPI reali
- ElevenLabs prezzo stabile
- Y3: €2,4M ARR, EBITDA 24%

**Revenue impact**: Y3 ARR €2,4M
**Strategic response**: bootstrap + selective hire + DACH market test Q3 2027

### 3.3 Worst case scenario

**Cosa va male simultaneamente**:
- AI Act implementation ritardata (post 2 ago 2026) → Garante apre ispezione, sanzione preventiva €50k
- Cliente cliente flagship B2C chiude rapporto (cambio strategia interno) → -25% revenue B2C linea
- Setter chiave dimette (Setter senior) → 3 clienti B2B churnano in 60 giorni
- ElevenLabs aumenta pricing +40% → gross margin scende a 38%
- Recession EU H2 2026 → new logo rate -50%
- Founder bandwidth saturato → burnout 30 giorni rallentamento

**Revenue impact**: Y3 ARR €1,2M (vs €2,4M base)
**Timeline**: 2026-2027 crisi
**Strategic response**:
- Freeze hiring + 20% OpEx cut
- Multi-vendor stack accelerato (Cartesia + Deepgram)
- Re-onboarding aggressivo clienti at-risk
- Pivot pricing più aggressivo (sconti 6 mesi per retention)
- Possibile equity bridge €500k convertibile

### 3.4 Black swan scenario

**Evento improbabile ad alto impatto**:
- **Garante Privacy IT vieta totalmente AI voice outbound** (regolamento di emergenza simile a Clothoff ott 2025 estensione)
- OR: **Big Tech (Meta o Google) lancia voice AI italiano gratuito B2B** consumer-grade
- OR: **Sentenza UE rende disclosure AI così invasiva da rendere outbound economicamente impossibile**
- OR: **Cyber attack supply chain (ElevenLabs hack) espone 80k lead clienti**

**Revenue impact**: -60-80% ARR in 6 mesi
**Strategic response**:
- Pivot a modello inbound-only / opt-in puro
- Riconversione a setter umano + AI for routing/scripting (no chiamate AI dirette)
- Possibile fundraising emergenza o M&A friendly
- Cessazione segmento B2C riattivazione

**Probability**: <2% nei prossimi 24 mesi, ma da considerare in strategic risk register.

---

## 4. Risk mitigation timeline (gennaio 2026 → maggio 2027)

| Mese | Mitigation azione | Risk addressed |
|---|---|---|
| **Giu 2026** | Hire consulente DPA part-time | R10 |
| **Giu 2026** | Validare Cartesia + Deepgram come backup ElevenLabs | R4 |
| **Lug 2026** | Disclosure AI Act Art. 50 live in tutti agenti | R10 |
| **Lug 2026** | Test compliance 100 chiamate × 3 clienti | R10 |
| **Lug 2026** | Lead provenance audit per cliente flagship B2C + 4 B2B esistenti | R11 |
| **Lug 2026** | Hire marketing manager part-time | R5 |
| **Ago 2026** | Stripe payment automation Starter + Pro | R7 |
| **Set 2026** | Backup setter hire (3° setter dedicato) | R6 |
| **Set 2026** | Cyber insurance €1M + D&O €500k | R14 |
| **Ott 2026** | Brand audit + 3 case study pubblicati | R1, R15 |
| **Nov 2026** | Partnership GHL Solutions Partner Gold | R1, R8 |
| **Dic 2026** | Customer Health Score dashboard live | R5, R7, R8 |
| **Gen 2027** | Multi-vendor stack production (Cartesia + Deepgram parallel) | R4 |
| **Feb 2027** | Penetration test sicurezza | R14 |
| **Mar 2027** | Strategic risk review (board / advisor) + scenario test | All |
| **Apr 2027** | Hire enterprise AE | R5, R8 |
| **Mag 2027** | Customer Advisory Board (5-8 clienti top) | R15 |

---

## 5. Risk score totale e attractiveness adjustment

**Risk score aggregato**: somma di tutti i 15 risk score = 148 / 375 max teorico = **39,5%**

Adjusted industry attractiveness (cfr. `05_swot_porter.md` overall 6,4/10):
- Risk-adjusted: 6,4 × (1 - 0,395 × 0,3) = 6,4 × 0,88 = **5,6/10**

Significato: l'industria resta attraente per early mover, ma i 5 top risk (R10, R1, R4, R5, R11) richiedono mitigation continuativa.

---

## 6. So what — implicazioni strategiche

1. **R10 (AI Act) è priorità ASSOLUTA Q3 2026**: ogni altra iniziativa marketing/sales è inutile se non siamo compliant il 2 agosto.
2. **R5 (Founder dependency) è il rischio strutturale più sottovalutato**: l'organizzazione 2-3 persone è fragile, hire #1 marketing manager è urgente.
3. **R1 + R4 (Commoditization + dipendenza ElevenLabs)** sono i rischi long-term più severi: investimento brand + multi-vendor stack è la difesa.
4. **R11 + R15 (Filiera B2C / reputazione)** richiedono due diligence rigorosa: meglio rinunciare a cliente B2C rischioso che fronteggiare €79M Enel-style sanzione.
5. **Worst case scenario è gestibile**: Telesales arriva a €1,2M ARR comunque profittevole. Black swan scenario richiede pivot ma non chiusura.

Continua in [`11_market_entry_expansion.md`](11_market_entry_expansion.md).
