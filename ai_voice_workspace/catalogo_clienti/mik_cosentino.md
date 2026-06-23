# Cliente — Mik Cosentino (Infobusiness Accelerator)

## Tipo campagna
B2C riattivazione lead. Lead provengono dal modulo su `infobusiness.com` con campi:
- `cosa_fai_per_vivere`
- `obiettivo_3_6_mesi`
- `perche_importante`
- `cosa_ostacola`

## Volumi
- 80.000 – 100.000 lead totali da riattivare
- Target operativo: **20 appuntamenti/giorno** con un setter umano del team

## Asset
- Prompt: `/Users/simocors/Desktop/telesales/prompts/mik_cosentino_infobusiness_v1.md`
- Config: `/Users/simocors/Desktop/telesales/agents_config/mik_cosentino.json`
- Agent ID: `MIK_AGENT_ID` in `/Users/simocors/Desktop/telesales/config.py` (post-migrazione 2026-05-05)
- Bridge Apps Script: `/Users/simocors/Desktop/telesales/demo_mik/apps_script_sofia.gs` (legacy "Sofia Mik")

## Flow operativo

```
[80k lead Infobusiness]
       │
       ▼
   batch sequential Marco AI (concurrency=1, 20-30 chiamate/giorno)
       │
       ▼
  AI qualifica:
   - Riepilogo modulo (B passaggio obbligatorio)
   - Proposta call con consulente
   - Raccolta email + telefono
       │
       ▼
   Esito → foglio interno
       │
       ▼
  Esito ∈ {Appuntamento, Email caldo} → setter umano
       │
       ▼
   Setter conferma e calendarizza
       │
       ▼
   Closer chiude in call con consulente Mik
```

## Identità agente Marco (Mik)

```
Sei Marco, consulente del team di Mik Cosentino (infobusiness.com).
Stile spigliato, naturale, CALDO, da amico al telefono — NON call center.
Frasi brevi, ritmo veloce, "tu" sempre. Max 2 frasi per turno.

OBIETTIVO UNICO: fissare call gratuita 30 min tra il lead e un consulente Mik.
Non vendere, non dare prezzi, non spiegare il corso.
```

## Step obbligatori del prompt

- **STEP A**: apertura — verifica numero, presentazione
- **STEP B**: cita almeno 2 risposte testuali del modulo (per dimostrare contesto reale)
- **STEP C**: proposta call ("Quando ti incastriamo?")
- **STEP D**: se sì → raccogli email + cellulare + data preferita
- **STEP E**: se no → email per follow-up scritto

STEP B + C sono OBBLIGATORI per ogni call con lead reale.

## Slot validi

Lun-Ven 09-13 e 14-20. Sabato 09-13. MAI domenica/festivi/date passate.
Slot non valido → "Quel giorno il consulente non c'è, ti va [alternativa feriale più vicina]?"

## Data collection

- `interest_level`: high/medium/low/none
- `appuntamento_fissato`: true/false
- `data_appuntamento`: ISO 8601
- `situazione_attuale`: dipendente/freelance/imprenditore/disoccupato/studente/altro
- `obiettivo_dichiarato`: testo breve
- `obiezione_principale`: tempo/soldi/scetticismo/gia_provato/nessuna/altro
- `opt_out_richiesto`: true/false
- `email_confermata`: true/false
- `telefono_confermato`: true/false
- `note_ai`: 1 frase sintesi

## Tone of voice

- B2C, caldo, diretto, **tu** sempre
- Reference Mik come autorità del settore (ma senza adulazione)
- Empatia genuina: "Ahhh, ti capisco", "Eh, lo so com'è"
- Quando ricordi modulo: "Sì, esatto, te lo ricordo: avevi scritto che..."
- Mai inglesismi, niente "asap", "deadline", "kpi"

## Note operative

- Lead "non ricorda di aver compilato": "Forse al volo. Ti chiedevamo cosa fai, obiettivo, perché è importante, cosa ti blocca. Ti torna?"
- Lead chiede prezzo: "Te lo spiega il consulente coi numeri precisi. La call è gratis."
- Lead chiede come avete il numero: "L'hai lasciato tu compilando il modulo su infobusiness.com. Posso toglierti se preferisci."

## Foglio interno + foglio cliente

- Foglio interno: TBD (specifico per Mik)
- Foglio cliente Mik: TBD (al momento il flusso passa per setter, non per foglio condiviso)
