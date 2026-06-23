# Kit cliente Telesales - standardizzato

Genera per ogni nuovo cliente gli stessi 3 deliverable, con struttura identica:
1. `Dossier_Mercato_<CLIENTE>.docx` - ricerca di mercato con fonti.
2. `Master_<CLIENTE>.xlsx` - 6 tab: HOME, GUIDA_SETTER, LISTA_PROSPECT, ICP_e_INSIGHT, KPI_TRACKING, DB_COMPLETO.
3. `Questionario_<CLIENTE>.docx` - domande al cliente, prioritizzate, max 15.

## Come funziona
I **builder Python sono fissi** (struttura sempre uguale). La ricerca alimenta solo i **dati JSON**.
Cosi l'output e standardizzato: cambia il cliente, non la forma.

```
_KIT_CLIENTE/
  PROMPT_MASTER.md        <- incollalo a inizio sessione col nuovo cliente + onboarding
  builders/
    build_master.py       <- config.json + prospects.json (+ guida.json, kpi.json) -> Master_<CLIENTE>.xlsx
    build_dossier.py      <- dossier.json -> Dossier_Mercato_<CLIENTE>.docx
    build_questionario.py <- questions.json (max 15 domande, prioritizzate) -> Questionario_<CLIENTE>.docx
  esempi/                 <- contratto dati JSON funzionante (cliente fittizio "Lux SRL")
```

## Uso rapido
1. Apri una sessione, incolla `PROMPT_MASTER.md` + il materiale di onboarding del cliente.
2. L'agente fa la ricerca (scouting o pulizia DB), verifica i telefoni, e scrive i JSON nella cartella del cliente.
3. Lancia i builder:
   ```
   python3 builders/build_master.py /Users/simocors/Desktop/telesales/<cliente>
   python3 builders/build_dossier.py /Users/simocors/Desktop/telesales/<cliente>
   python3 builders/build_questionario.py /Users/simocors/Desktop/telesales/<cliente>
   ```

## Modalita lista
- `scouting`: cliente senza database -> la lista si costruisce con ricerca di mercato (fan-out per settore).
- `db_esistente`: cliente con file -> si pulisce, deduplica e arricchisce.
Si imposta in `config.json` -> `modalita_lista`.

## Telefoni
- `telefono_centralino`: ufficiale, verificato e incrociato su piu fonti. Sempre.
- `telefono_diretto`: reparto/decisore SOLO se pubblico verificabile, altrimenti vuoto. Mai inventato.
- Formato nazionale ("030 522672"), mai +39, mai cifre attaccate.

## Regole fisse
Niente emoji. Tutto in italiano. Colori A verde / B giallo / C grigio. Dropdown chiusi. In chiamata niente prezzi.
Vuoto e meglio di inventato.

## Dipendenze
`pip install openpyxl python-docx`
