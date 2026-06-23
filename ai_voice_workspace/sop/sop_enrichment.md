# SOP — Arricchimento Liste

## Fonte primaria
Cribis (export aziende per categoria/zona)

## Script
`Desktop/telesales/arricchisci_lista.py`

## Cosa aggiunge
- Email pattern decision maker (nome.cognome@dominio)
- Cellulare DM (con validazione anti-allucinazione)
- Categoria ATECO
- Citta + provincia

## Validazione cellulari DM

Regole anti-allucinazione (vedi `phone_hunting_rules.md` in memory):
- Solo prefissi mobili italiani validi: 3xx
- Gold standard: file `Filippo_Mobili_34.csv`
- Validatore: `tools/phone_validator.py`
- Fonti affidabili che funzionano: Cribis, Cerved, Telegate

## Output
File CSV con suffix `_VERIFICATE.csv` → pronto per upload ElevenLabs.

## Agente responsabile
`@list-ops`
