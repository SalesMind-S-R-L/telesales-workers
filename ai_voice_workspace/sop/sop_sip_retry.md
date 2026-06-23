# SOP — SIP Retry Policy (PERMANENTE)

## Trigger
Batch ElevenLabs riporta SIP fail su uno o più numeri.

## Regola d'oro
**MAI** segnare come "Non risposto" un SIP fail. È un problema di rete/provider, non del contatto.

## Procedura

1. Estrai numeri con SIP fail dal report batch
2. Lancia retry automatico:
   - Script: `tools/retry_until_success.py`
   - Max **5 tentativi** per numero
   - **60 secondi** di pausa tra round
3. Solo dopo 5 fallimenti consecutivi → escala a "Da richiamare manualmente"
4. Aggiorna sheet **solo** dopo l'esito reale (mai durante i retry)

## Agente responsabile
`@retry-manager` — sorveglia tutti i batch ElevenLabs e applica questa policy automaticamente.
