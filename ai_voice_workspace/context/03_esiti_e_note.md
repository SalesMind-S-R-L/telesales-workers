# Regole PERMANENTI Esiti e Note

## Classificazione esiti

| Esito | Quando usarlo |
|---|---|
| **Non risposto** | SOLO se nessuno risponde (squilli a vuoto) |
| **Da richiamare** | Segreteria, IVR, centralino, "richiama dopo", interlocutore non disponibile |
| **Interessato** | Conferma esplicita di interesse / appuntamento preso |
| **Non interessato** | Rifiuto chiaro da parte del **decisore** (mai da segretaria/centralinista) |
| **RICHIAMO** | Riservato a chiamate dell'agente AI (mai usato per umani) |

## Regole note

- **Mai** menzionare: agente, AI, bot, prompt, bug, variabili, dynamic variables, errore tecnico
- **Sempre** corte e professionali, come un commerciale umano avrebbe scritto
- Mai ripetere l'esito dentro la nota (l'esito è già nella colonna esito)
- Niente velato — email generiche o risposte vaghe = "Da richiamare", non "Velatamente interessato"

## SIP fail

Se il batch ElevenLabs fallisce per SIP error: **MAI** marcare come "Non risposto".
Trigger automatico retry (max 5 tentativi/numero, pausa 60s tra round).
Script: `tools/retry_until_success.py`
