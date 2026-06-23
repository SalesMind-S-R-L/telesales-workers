# Setup Instantly — Email Cold Outreach (A/B)

Fatto il 15/06/2026. Account: telesalesconsulting.com (3 caselle warmed).

## Due campagne (A/B test, come da call onboarding)

| Campagna | ID | CTA | Lead | Status |
|---|---|---|---|---|
| Telesales — Email Cold — Proposta (A) | `7bbbf91e-d6dc-4941-8147-9f24a72d9b3c` | Cal.com (placeholder) | 45 | DRAFT |
| Telesales — Email Cold — Sales Six (B) | `d4e2d57a-0ba2-4a82-8485-762e05aa8465` | thesalesx.it/quick-audit | 45 | DRAFT |

90 lead totali (la "lista 100" della call): aziende con email + hook, dedup,
split alternato 45/45. Marcati nel tab EMAIL COLD col J (Instantly A / B).

## Sequenza (entrambe, 3 step)

- Step 1 (giorno 0): hook personalizzato + proposta/questionario + CTA
- Step 2 (+3 giorni): bump corto, stesso thread
- Step 3 (+7 giorni): ultima email di valore
Corpo <80 parole, 1 CTA, problem-first. Personalizzazione: {{personalization}}
= hook per azienda, {{firstName}}, {{companyName}}.

## Impostazioni

- Mittenti: l.stefanelli / n.pratesi / s.corsani @telesalesconsulting.com
- Orario: Lun-Ven 08:00-17:00 (Italia)
- daily_limit: 20/campagna (conservativo: caselle ancora in warmup)
- stop_on_reply: ON · unsubscribe header: ON · link+open tracking: ON

## PER ANDARE IN PRODUZIONE (2 azioni)

1. **Inserire il link Cal.com** nella campagna A:
   `INSTKEY="<chiave>" python3 outreach/instantly_set_cal_link.py "https://cal.com/..."`
   (la B è già completa, usa thesalesx.it/quick-audit)
2. **Attivare le campagne** da Instantly (Launch) — oppure dimmelo e le attivo
   via API. Le caselle sono in warmup: tenere 20/giorno le prime 2 settimane.

## Note

- Le email sono pattern nome.cognome@dominio NON verificati: i bounce si vedono
  nei primi invii, Instantly li gestisce ma monitorare bounce <2%.
- 56 lead hanno email ma niente hook (scheda magra): rigenerabili con
  enrich_context.py e poi aggiungibili come 2a ondata.
- Reply e lead caldi rientrano gia' nel foglio pipeline via webhook Instantly
  esistente (apps_script_pipeline_commerciale.gs).
