# Regole Compilazione Google Sheets

## Formati

- **Date**: `DD/MM/YYYY`, sempre cronologiche, **mai future**
- **Match contatto**: prima per **telefono**, poi per nome
- **Note**: concise, mai ripetono l'esito (l'esito è già nella sua colonna)
- **Slot orari**: ordinati cronologicamente

## Dropdown e colori

- Esiti chiusi su dropdown — niente valori liberi
- Colori coerenti per categoria (definiti per cliente in `catalogo_clienti/`)
- Mai modificare l'ordine delle colonne master

## Classificazione "Non interessato"

Vale **solo** se l'opposizione viene dal **decisore** vero.
Risposte da segretaria, centralinista, IVR → "Da richiamare".

## Sheet IDs

Mantenuti in `catalogo_clienti/<cliente>.md` per ogni cliente attivo.
