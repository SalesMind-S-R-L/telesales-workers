# 🤖 Meta Ads Senior Manager Agent

Agente Claude autonomo per gestione long-term Meta Ads Telesales.

## Cosa fa

- **Monitora** giornalmente performance (daily pulse 08:00)
- **Analizza** settimanalmente trend e quality (weekly audit lunedì 09:00)
- **Bilancia** mensilmente ROI e roadmap (monthly review 1° del mese)
- **Consiglia** ogni decisione strategica con dati e razionale
- **Risponde** a crisi (CPL salita, 0 lead, ad rifiutate, etc.)
- **Propone** scaling progressivo budget quando metriche lo permettono
- **Refresha** creative quando segnali di fatigue

## Cosa NON fa autonomamente

Decisioni "potenti" solo su approvazione Simone:
- Lancio nuove campagne
- Pausa campagne attive
- Aumenti budget >30%
- Cambio targeting strutturale
- Modifica modulo lead form

## Come si invoca

### Via Claude Code (skill)

In una conversazione Claude:
```
/meta-ads-agent
```

oppure linguaggio naturale che triggera la skill:
```
controlla meta ads
audit settimanale meta
posso scalare budget?
crisi 0 lead
refresh creative
```

### Via Scheduled Tasks (automatico)

Già schedulati:
- `meta-v4-relaunch-check-1giu` (1/6 09:00) — verifica setup
- `meta-v4-audit-settimana1-5giu` (5/6 09:00) — scaling decision
- `meta-v4-audit-settimana2-12giu` (12/6 09:00) — creative refresh
- `meta-v4-bilancio-30giu` (30/6 09:00) — bilancio mensile

## Struttura files

```
/Users/simocors/Desktop/telesales/agents/meta_ads_agent/
├── AGENT.md                 # Sistema prompt principale
├── README.md                # Questo file
├── action_log.md            # Diario operativo (mantenuto dall'agente)
└── playbooks/
    ├── daily_pulse.md       # Check quotidiano
    ├── weekly_audit.md      # Audit settimanale
    ├── monthly_review.md    # Review mensile + ROI
    ├── scaling_decision.md  # Algoritmo scaling budget
    ├── crisis_response.md   # Procedure emergenza
    └── creative_refresh.md  # Rotation creative

/Users/simocors/.claude/skills/meta-ads-agent/
└── SKILL.md                 # Skill Claude Code che invoca l'agente

/Users/simocors/.claude/projects/-Users-simocors-Desktop-telesales/memory/
└── meta_ads_telesales.md    # Memoria storica + vincoli + decisioni

/Users/simocors/Desktop/telesales/reports/
├── 01_campagne_overview.csv # Dataset campagne
├── 02_ads_performance.csv   # Performance per ad
├── 03_decisioni_log.csv     # Log decisioni con outcome
└── README.md                # Doc dataset
```

## Stato attuale (29/05/2026)

### Campagna ATTIVA
- **TS_LEADS_v4_Manual_2026-05-04** (ID 6982220525065)
- Budget €25/giorno (target scaling €66/giorno per €2000/mese)
- 11 lead cumulativi (1 apr - 11 mag), CPL medio €16.38
- 2 ad attive: cos'è telesales (winner volume), Leonardo (winner efficienza)
- Pausa pending da Opzione C ristrutturazione

### Roadmap 30gg già pianificata
Vedi sezione "PIANO RIATTIVAZIONE v4 - OPZIONE C" in `memory/meta_ads_telesales.md`

### Vincoli noti
- Advantage+ leads campaign hardcoded (no Manual reale)
- Età max non settabile (filtro pensionati solo via modulo)
- Moduli non modificabili post-publish
- Browser automation Meta UI inaffidabile

## Filosofia operativa

1. **Dati prima**: ogni proposta basata su numeri, non opinioni
2. **Conservativo > aggressivo**: 80% delle volte la mossa giusta è "non toccare"
3. **Concise**: 5 righe meglio di 20
4. **Italiano**: rispetto regola memoria
5. **No emoji nei deliverable formali**: rispetto regola memoria

## Accesso ai dati live

- **Foglio Google leads (v4b)**: https://docs.google.com/spreadsheets/d/1wFYXFDFo6W2GT6HT3HKHLYx8eN-C4VUGnxlU_dIiNyk/edit (tab `TS_LeadQualificati_v4b_Mag2026` gid=926835576)
- **Ads Manager**: https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=40219042
- **Lead Center**: https://business.facebook.com/latest/leads_center?asset_id=943053402232754

## Come aggiornare l'agente

L'agente si aggiorna da solo aggiungendo righe in `action_log.md`, CSV reports e `meta_ads_telesales.md`.

Se vuoi cambiare comportamento/regole:
- Edit `AGENT.md` per regole strutturali
- Edit playbooks per scenari specifici
- Edit `meta_ads_telesales.md` per stato/vincoli

## Limiti tecnici noti

1. Lettura Ads Manager via browser → tabella canvas, JS non legge i numeri. Workaround: chiede a Simone screenshot.
2. Scrittura su foglio Google → senza OAuth token, paste manuale richiesto.
3. CRM Setup Meta → integrazione "Crea contatto" del test tool NON triggera webhook. Solo lead reali da campagna live triggerano CRM.

## Contatti emergenza

Se l'agente non funziona o serve override umano: Simone Corsani direttamente.

Per problematiche Meta Ads platform-level: Meta Business Support (24/7 via chat in Business Suite).
