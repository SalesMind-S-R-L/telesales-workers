# PIANO AI VOICE LOOK — Lunedì 22/06/2026

Basato sul pilota di venerdì 19/06 (44 chiamate, 20 conversazioni, 2 interessati, 1 referente, 12 fail SIP).

## 0. Pre-flight (prima di chiamare)
- [ ] **Giorni consulenza**: impostare `LOOK_GIORNI="<giorni reali>"` (es. "lunedì e mercoledì"). Oggi default = "dal lunedì al venerdì". *(serve il dato dall'onboarding)*
- [ ] **Numero outbound**: +390554652406 (phnum_1501). NON usare +390574814928 (morto, SIP 404).
- [ ] **Concorrenza**: 1 (sicura). Si può salire a 2 SOLO in una fascia in cui Culligan/Marco Ferretti NON chiamano (evita contesa trunk).
- [ ] **Master/Drive**: già allineati. Esiti in colonna giusta (21). Caller salta già i lead conclusi.

## 1. Finestra e volume
- **~60 chiamate**, in 2 blocchi (no pausa pranzo, mai prima delle 9):
  - Mattina **09:30–12:30** → ~30
  - Pomeriggio **14:30–17:30** → ~30
- Concorrenza 1 → ~75 min per 30 chiamate (come oggi). Fermo a fine finestra.

## 2. Sequenza (ordine di chiamata)
### A) Follow-up CALDI di venerdì (primi della mattina — priorità assoluta)
- **Line Express Service** → richiamare in orario amministrazione (lun-ven 8–16)
- **Piemonteco** (interessato) → responsabile commerciale
- **Nuova Prima** (interessato) → cercare operatore umano (venerdì rispose un automatico)
- **Battiston Traslochi** → chiedere di **Germano Battiston** (titolare)
- **Control Calor** → **Francesco Paolo Moro** (titolare)
- **Parma Clima**, **Climatech** (interesse alto, da richiamare)
- **Esa Eco Servizi** (responsabile assente venerdì)
### B) MAIL (non chiamata)
- **Centro Caldaie Bove**: numero verde in pacchetto con broker → mandare mail di presentazione da numeroverdebusiness@gmail.com, poi richiamo a valle.
### C) Nuovi prospect
- Continuare la lista dal Master in ordine di priorità (il caller salta da solo i conclusi e i no).

## 3. Esecuzione (comandi)
```
# blocco mattina
LOOK_GIORNI="<giorni>" python3 look/look_batch_caller.py --limit 30
# ...a fine blocco, scrivere esiti:
python3 look/look_post_batch_analyze.py
# blocco pomeriggio
LOOK_GIORNI="<giorni>" python3 look/look_batch_caller.py --limit 30
python3 look/look_post_batch_analyze.py
```
- Dry-run di controllo prima: `python3 look/look_batch_caller.py --dry-run --limit 30`

## 4. Post-chiamata
- `look_post_batch_analyze.py` scrive esito + nota umana (breve se non risposto, ricca se risposto) su Master + ricarica su Drive.
- Review dei nuovi caldi a fine giornata.

## 5. Agente (già aggiornato venerdì sera)
- Rileva da solo segreteria/IVR e chiude (Da richiamare).
- Propone "una consulenza" nei giorni concordati — niente "15 minuti", niente richiesta fattura.
- Non alza la voce se non lo sentono ("Adesso mi sente?").
- Gatekeeper: pitch da azienda esperta ("si paga tanto e si usa poco / crediti mai usati"), CTA "Il titolare è disponibile?".

## 6. Rischi e mitigazioni
| Rischio | Mitigazione |
|---|---|
| SIP error da contesa con Culligan/Ferretti | Concorrenza 1; o finestra dedicata a Look |
| Numeri errati (SIP 404) | Marcati "Numero/contatto errato", non ritentati |
| Linea +390574814928 | NON usarla (morta) |
| Doppie chiamate | Caller salta i conclusi; follow-up mirato sui caldi |

## Decisioni che servono da te
1. **Giorni consulenza** (per la variabile {{giorni_consulenza}}).
2. **Fascia oraria libera da Culligan** lunedì (per poter salire a concorrenza 2), oppure resto a concorrenza 1.
3. Conferma volume **~60 in 2 blocchi** e gli orari 09:30–12:30 / 14:30–17:30.
