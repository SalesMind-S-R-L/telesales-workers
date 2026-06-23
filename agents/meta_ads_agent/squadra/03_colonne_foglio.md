# Spec colonne tracking commerciale — CRM Telesales v4

Foglio: `1wFYXFDFo6W2GT6HT3HKHLYx8eN-C4VUGnxlU_dIiNyk`
Tab: `TS_LeadQualificati_v4b_Mag2026`
Stato attuale: colonne 1-21 dati Meta, 22 flag email, 23 note. **Da NON toccare.**
Nuove colonne: **dalla 24 (X) in poi**. Tutto in italiano, ZERO emoji, dropdown CHIUSI.

Nota convenzioni: i fogli cliente post-28/04 sono neutri senza dropdown. Questo invece e' un foglio
INTERNO di gestione lead Meta (non un foglio cliente): qui i dropdown chiusi servono per dare al team
telesales una pipeline strutturata e filtrabile. Le note restano scritte come un commerciale umano,
senza termini tecnici (mai agente/AI/bot/sistema).

---

## 1. Riga header esatta (colonne 24-34 = X-AH)

Incolla in `X1` (si espande in orizzontale fino a `AH1`):

```
Stato Pipeline	Esito Ultima Chiamata	N Tentativi	Data Ultimo Contatto	Data Prossimo Follow-up	Setter Assegnato	Quality Score	Motivo Perso	Fonte	CPL Stimato (EUR)	Note Commerciali
```

Mappa colonna -> lettera:

| Col | Lettera | Nome header              | Tipo            |
|-----|---------|--------------------------|-----------------|
| 24  | X       | Stato Pipeline           | Dropdown chiuso |
| 25  | Y       | Esito Ultima Chiamata    | Dropdown chiuso |
| 26  | Z       | N Tentativi              | Numero intero   |
| 27  | AA      | Data Ultimo Contatto     | Data DD/MM/YYYY |
| 28  | AB      | Data Prossimo Follow-up  | Data DD/MM/YYYY |
| 29  | AC      | Setter Assegnato         | Dropdown chiuso |
| 30  | AD      | Quality Score            | Dropdown chiuso |
| 31  | AE      | Motivo Perso             | Dropdown chiuso |
| 32  | AF      | Fonte                    | Dropdown chiuso |
| 33  | AG      | CPL Stimato (EUR)        | Numero (valuta) |
| 34  | AH      | Note Commerciali         | Testo libero    |

---

## 2. Valori dropdown chiusi

### X — Stato Pipeline (applica a X2:X1000)
Lista chiusa, ordine = avanzamento funnel:
```
Da contattare
Contattato
In nurturing
Appuntamento fissato
Show
No show
Cliente
Perso
Non valido
```
- Default per ogni nuovo lead: `Da contattare`.
- `Non valido` = P.IVA fittizia (es. 00000000000), numero inesistente, troll. Resta fuori dal funnel.
- `In nurturing` = ha risposto ma non pronto adesso (timing "tra qualche mese").

### Y — Esito Ultima Chiamata (applica a Y2:Y1000)
```
Da chiamare
Non risponde
Da richiamare
Richiamo programmato
Numero errato
Interessato
Da valutare
Non interessato
Appuntamento preso
```
- `Non risponde` SOLO se squilla a vuoto / nessuno risponde.
- Segreteria / IVR / centralino / fail tecnico -> `Da richiamare` (mai "Non risponde").
- `Non interessato` SOLO se ha parlato il decisore in persona; altrimenti `Da richiamare`.
- `Richiamo programmato` quando c'e' una data concordata (compilare AB).

### AC — Setter Assegnato (applica a AC2:AC1000)
Team interno:
```
Karima
Rebecca
Barbara
Non assegnato
```
- Default: `Non assegnato`.

### AD — Quality Score (applica a AD2:AD1000)
Compilato dall'auditor. Scala chiusa A/B/C/D:
```
A - Top (decisore, >50k, timing subito)
B - Buono (decisore, fit ok)
C - Debole (fit parziale / fatturato basso)
D - Scarto (no P.IVA / no decisore / dati falsi)
```
- Lead da Meta v4 storicamente A/B (fatturato >50k, aziende reali).

### AE — Motivo Perso (applica a AE2:AE1000)
Compilare SOLO se Stato Pipeline = `Perso`:
```
Prezzo
Tempistiche
Gia' fornitore
Non decisore reale
Non richiamabile
Concorrenza
Nessun interesse reale
Altro
```

### AF — Fonte (applica a AF2:AF1000)
```
Meta v4
Meta v4 - cos'e telesales
Organico
Referral
Altro
```
- Default per questo tab: `Meta v4 - cos'e telesales` (ad set winner 6982220524465).

---

## 3. Colonne non-dropdown

### Z — N Tentativi (Z2:Z1000)
- Numero intero, default `0`. Incrementa di 1 a ogni chiamata effettuata.
- Validazione dati: numero intero >= 0.

### AA — Data Ultimo Contatto / AB — Data Prossimo Follow-up
- Formato `DD/MM/YYYY`. Mai date future in AA. Mai date passate in AB.
- AB obbligatoria quando Y = `Richiamo programmato` o `Da richiamare`.

### AG — CPL Stimato (EUR) (AG2:AG1000)
- Numero, formato valuta `€ #,##0`. CPL recente di riferimento ~29-40 EUR.
- Si puo' precompilare con valore costante del periodo o lasciare per calcolo aggregato.

### AH — Note Commerciali (AH2:AH1000)
- Testo libero, corto e professionale come un commerciale umano.
- MAI termini tecnici (agente/AI/bot/prompt/sistema/SIP/variabili).
- Esempi: "Parlato col titolare, vuole rivedere a settembre", "Centralino, chiesto del Sig. Rossi assente",
  "Appuntamento confermato 12/06 ore 10", "Email inviata, attende preventivo".

---

## 4. Formattazione condizionale — Stato Pipeline (colonna X)

Applica a `X2:X1000`, regola "il testo e' esattamente". Colori sobri, leggibili (sfondo + testo scuro):

| Valore                | Sfondo    | Hex      | Significato            |
|-----------------------|-----------|----------|------------------------|
| Da contattare         | Grigio    | #E0E0E0  | nuovo, da lavorare     |
| Contattato            | Azzurro   | #BBDEFB  | in lavorazione         |
| In nurturing          | Lavanda   | #D1C4E9  | caldo ma non pronto    |
| Appuntamento fissato  | Giallo    | #FFE082  | impegno preso          |
| Show                  | Verde chi.| #C8E6C9  | si e' presentato       |
| No show               | Arancione | #FFCC80  | salta appuntamento     |
| Cliente               | Verde     | #66BB6A  | chiuso/vinto           |
| Perso                 | Rosso chi.| #EF9A9A  | perso                  |
| Non valido            | Grigio sc.| #BDBDBD  | scartato funnel        |

Regola extra utile (facoltativa) su **AB — Data Prossimo Follow-up**:
- evidenzia ROSSO `#FFCDD2` se la data e' < OGGI (follow-up in ritardo). Formula condizionale:
  `=E($AB2<>"";$AB2<OGGI())` applicata a AB2:AB1000.

---

## 5. Procedura applicazione (post-freeze, dopo ~16/6)

1. Selezionare `X1`, incollare la riga header del punto 1 (tab-separated -> riempie X1:AH1).
2. Per ogni colonna dropdown (X, Y, AC, AD, AE, AF): Dati -> Convalida dati -> Elenco di elementi ->
   incollare i valori del punto 2 -> "Rifiuta input non incluso" (dropdown CHIUSO).
3. Z: convalida Numero >= 0. AG: formato valuta EUR. AA/AB: formato Data DD/MM/YYYY.
4. Formato -> Formattazione condizionale: aggiungere le 9 regole del punto 4 su X2:X1000 +
   la regola follow-up in ritardo su AB2:AB1000.
5. Backfill iniziale dei 9 lead esistenti: X=`Da contattare`, Y=`Da chiamare`, Z=`0`,
   AC=`Non assegnato`, AF=`Meta v4 - cos'e telesales`, AD da compilare dall'auditor.

Nessuna emoji in header, dropdown o note. Dropdown a lista chiusa su tutte le colonne categoriche.
