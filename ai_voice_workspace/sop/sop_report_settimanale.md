# SOP — Report Settimanale

## Formato output
**Excel (.xlsx)** sempre. Mai Word, PDF, Pages, AppleScript.

## Struttura file
Path: `reports/<cliente>/<YYYY-WW>_report.xlsx`

## Sheet richiesti
1. **Riepilogo** — totali chiamate, tasso risposta, tasso interesse
2. **Esiti dettagliati** — per contatto: nome, numero, esito, nota, data
3. **Da richiamare** — sotto-lista priorizzata (orario consigliato se disponibile)
4. **Interessati** — sotto-lista con dettagli per setter umano

## Classificazione realistica
- Non gonfiare i numeri
- Email generiche / risposte vaghe → "Da richiamare", non "Velato interessato"
- "RICHIAMO" è una categoria solo per AI, non confondere con interessato umano

## Naming
`<cliente>_<settimana>_report.xlsx` — es. `mik_cosentino_2026-W20_report.xlsx`

## Agente responsabile
`@call-analyst`
