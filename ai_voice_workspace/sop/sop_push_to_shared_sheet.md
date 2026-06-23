# SOP — Push dal foglio interno al foglio condiviso cliente

## Quando applicare
Quando il cliente ha un suo Google Sheet condiviso dove vede i risultati dei contatti (esiti, note, appuntamenti). Noi lavoriamo su un foglio interno separato, e SOLO dopo via libera esplicito dell'utente pushiamo le righe al foglio cliente.

## Principi

1. **Mai push automatico** — sempre via libera esplicito ("ok push", "trasferisci tutto", "via libera")
2. **Append, non match** — le aziende già nel foglio cliente sono filtrate a monte (vedi `sop_enrichment.md`)
3. **Mappare colonne reali del foglio cliente** — NON assumere — leggere headers via API prima di scrivere
4. **Stile note cliente** — lowercase, telegrafico, niente riferimenti tecnici (vedi sotto)
5. **Solo dati visibili al cliente** — niente transcript link, niente row_index, niente debug

## Trappola colonne (caso reale Sebastiano Culligan)

I fogli clienti possono avere headers che NON corrispondono all'ordine logico. Esempio reale del foglio Sebastiano:
- Header riga 1 dice: `A=NOME AZIENDA, B=NOME TITOLARE, C=NOTE, D=INDIRIZZO, E=TELEFONO, F=PRESENTE SI O NO, G=DATA DELLA CHIAMATA, H=DATA DELL'APPUNTAMENTO`
- MA Sebastiano scrive i dati in **I (data chiamata), J (note), K (data appuntamento)** — usa di fatto le colonne del "secondo giro"
- Le colonne C, G, H sono inutilizzate

Risultato: scrivere su A-H ti dà colonne shiftate o vuote. Verifica SEMPRE leggendo 2-3 righe esistenti del cliente per capire dove scrive davvero.

```python
# Verifica: leggi 3 righe esistenti e mostra colonne popolate
rows = svc.spreadsheets().values().get(
    spreadsheetId=DST, range="'Foglio1'!A140:L145"
).execute().get('values',[])
for ri,r in enumerate(rows):
    for ci,v in enumerate(r):
        if v: print(f"riga {140+ri} col {chr(65+ci)}: {v}")
```

## Mapping standard (esempio Culligan → Sebastiano)

| Foglio interno | Foglio cliente | Trasformazione |
|---|---|---|
| A NOME AZIENDA | A | copia |
| B NOME TITOLARE | B | solo se emerso in chiamata, altrimenti vuoto |
| D INDIRIZZO | D | copia |
| E TELEFONO | E | rimuovi spazi e formattazione |
| (derivato da I esito) | F | `sì` lowercase se esito ∈ {Appuntamento, Email, Da richiamare}, altrimenti vuoto |
| G DATA CHIAMATA | **I** (NB: I non G) | `DD/MM/YYYY HH:MM` → `DD/MM/YY` |
| J NOTE_AI (lunga) | **J** (NB: J non C) | accorciata stile telegrafico (vedi sotto) |
| H DATA_APP | **K** (NB: K non H) | solo per Appuntamento fisico, `DD/MM/YY ore HH:MM` |

**Posizioni delle scritture dipendono dal cliente**. Sempre verificare prima.

## Stile note per cliente (lowercase, telegrafico)

Da esempi reali del foglio Sebastiano:
- `inviare email info@hotel-città.com`
- `non interessati per ora`
- `non risp`
- `titolare fuori, rientra tra due settimane`
- `gestisce Manna Hotel 40 minuti da Bolzano`
- `ok appuntamento martedì 19/05 ore 13 con Luca Röhl, madre lo informa`

Regole:
- Lowercase (anche all'inizio)
- Max 100-150 caratteri
- Niente "(SIP fail)", niente "IVR multilingue", niente note tecniche
- Mai citare AI/agente/bot
- Mai citare row_index, conv_id, link

## Mapping per esito → nota cliente

| Esito interno | Template nota cliente |
|---|---|
| Appuntamento | `ok appuntamento <giorno> <ora> con <nome>, <dettaglio breve>` |
| Email | `inviare email <indirizzo>, <dettaglio>` |
| Da richiamare | `<chi ha risposto> <situazione>, <quando richiamare>` |
| Non interessato | `non interessati[, motivo breve]` |
| Non risposto (incluso SIP fail) | `non risp` |

## Script reference

`/Users/simocors/Desktop/telesales/demo_mik/push_culligan_to_sebastiano.py`

Pattern minimo:
```python
import re, sys
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import get_sheets_service

START_ROW = 146  # prima riga libera dopo le esistenti

# ROW_DATA: row_idx_interno → (titolare, nota_cliente)
ROW_DATA = {2: ("", "non interessati"), ...}
DATA_APP_K = {26: "19/05/26 ore 13:00"}

rows_out = []
for row_idx, (titolare, nota) in sorted(ROW_DATA.items()):
    r = src[row_idx-1]
    rows_out.append([
        r[0],          # A nome
        titolare,      # B titolare
        "",            # C vuoto (cliente usa altre col)
        r[3],          # D indirizzo
        re.sub(r"\D","",r[4]),  # E telefono pulito
        "sì" if esito_in_present_set else "",  # F
        "", "",        # G, H vuote (cliente usa I, K)
        fmt_date_short(r[6]),  # I data chiamata
        nota,          # J nota
        DATA_APP_K.get(row_idx, ""),  # K data appuntamento
    ])

svc.spreadsheets().values().update(
    spreadsheetId=DST_ID,
    range=f"'Foglio1'!A{START_ROW}:K{START_ROW+len(rows_out)-1}",
    valueInputOption="USER_ENTERED",
    body={"values": rows_out},
).execute()
```

## Verifica post-push

- [ ] Aprire il foglio cliente e scrollare alle righe nuove
- [ ] Verificare che A=nome, E=telefono, J=nota siano popolati
- [ ] Spot-check su 1 appuntamento: K=data ora completa
- [ ] Spot-check su 1 "non risp": nota = `non risp` (no SIP fail visibile)
- [ ] Nessuna riga ha "(SIP fail)" o "IVR" nelle note
