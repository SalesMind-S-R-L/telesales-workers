# 06 - Funnel & Form Analysis - Campagna Telesales v4

Finestra: 11/05 -> 09/06/2026. Campagna 6982220525065, ad set produttivo "cos'e telesales" (6982220524465).
Fonti: insights API (last_30d) + foglio CRM TS_LeadQualificati_v4b_Mag2026.
Data analisi: 10/06/2026. FREEZE attivo: tutto qui sotto e PRONTO da eseguire dopo, niente e live.

NOTA metodo: il modulo e un Instant Form Meta nativo. Meta NON espone "form open" come metrica diretta su questa campagna. Uso il **link click** come proxy di apertura modulo (chi clicca la CTA del lead ad apre la scheda del form). E un proxy ragionevole ma leggermente ottimistico (qualche click non apre, qualche apertura puo non contare come link click). I numeri vanno letti come ordine di grandezza, non al decimale.

---

## 1. IL FUNNEL REALE (numeri)

| Step | Metrica | Valore | Conversione step precedente |
|---|---|---|---|
| Impression | impressions | 11.728 | - |
| Persone raggiunte | reach | 6.047 | frequenza 1,94 |
| Aperture modulo (proxy) | link_clicks | 119 | 1,97% su persone / 1,01% su impr |
| Modulo inviato (Meta) | lead_grouped API | 13 | **10,9%** (submission rate) |
| Lead arrivati in CRM | lead veri foglio | 9 | -31% (4 persi tra API e CRM) |
| Lead in target commerciale | esclusi 3 partner + 1 P.IVA fake | ~5 | -44% sul CRM |

### Letture chiave

- **Submission rate ~11%** (13 invii / 119 aperture). Per un Instant Form B2B con 4 domande di qualifica + 4 campi contatto, **11% e nella norma bassa-media**. Un form Meta "lead generation" generico sta sul 15-25%; i form "higher intent" (piu domande, piu filtro) scendono fisiologicamente al 8-15%. Quindi: **il modulo NON sta spaventando in modo anomalo**. Sta filtrando, come deve. Ma c'e margine.
- **Costo per apertura modulo: 2,75 EUR** (326,76 / 119). Questo e il vero collo di bottiglia a monte, non il form: poche persone cliccano la CTA (CTR link 1,97% sulle persone). Il problema "pochi lead" e per la maggior parte un problema di **volume di click + CPM**, non di abbandono del form.
- **Drop API -> CRM: -31% (4 lead).** Tra i 13 invii Meta e i 9 in foglio mancano 4. Cause probabili: doppi invii dello stesso utente contati da Meta, lead-test, o invii incompleti non sincronizzati. **Questo e un buco di tracciamento da chiudere** (vedi sezione 4).
- **Contaminazione a valle: -44% sul CRM.** Dei 9, solo ~5 sono clienti reali in target. 3 sono agenzie/concorrenti che si candidano come partner (Moizo, Lorenzo, Teresa) e 1 ha P.IVA placeholder (Samuele, 00000000000). **Il form attuale fa passare il lead-partner perche non c'e una domanda che li intercetti.**

### CPL: i tre numeri da non confondere

| Base | CPL | A cosa serve |
|---|---|---|
| 13 lead API | 25,1 EUR | NON usare: sovrastima, attribuzione inaffidabile |
| 9 lead CRM | 36,3 EUR | CPL "lordo" reale, quello che si paga |
| 5 lead utili in target | 65,4 EUR | **CPL "netto" vero**: quanto costa un cliente potenziale reale |

Il salto da 36 a 65 EUR e tutto causato dai lead-partner e dalle P.IVA fake. **Tagliare la contaminazione lato form e la leva piu forte sul CPL netto, piu forte ancora dell'ottimizzazione media.**

---

## 2. VALUTAZIONE DEL MODULO ATTUALE (4 domande)

Form attuale: Q1 decisore P.IVA si/no -> Q2 fatturato -> Q3 timing -> Q4 P.IVA (testo libero) + 4 campi contatto (email, nome, telefono, nome azienda).

| Domanda | Funzione | Verdetto | Problema |
|---|---|---|---|
| Q1 - Sei titolare/decisore con P.IVA? | filtro decisore | **TIENI** | 9/9 hanno risposto "si". Filtra poco da solo, ma e il gancio iniziale corretto. |
| Q2 - Fatturato annuo? | filtro size | **TIENI ma rivedi opzioni** | 9/9 hanno scelto ">50.000 EUR". Se tutti scelgono la stessa opzione, la domanda non discrimina: o le soglie sono mal tarate o e troppo facile auto-selezionarsi in alto. |
| Q3 - Quando vuoi iniziare? | filtro timing | **TIENI** | funziona: 7/9 "subito", 2 "valutando". Buon segnale di intent. |
| Q4 - P.IVA (testo libero) | dato + filtro implicito | **PROBLEMA GROSSO** | testo libero -> ha fatto passare "00000000000" e "Paradisecallsrl" (testo). Non valida nulla. Inoltre la P.IVA come ULTIMO step a campo aperto e attrito alto: chi non la sa a memoria abbandona. |

### Risposte alle domande poste

**E troppo lungo?** No in numero di domande (4 e ok per B2B), ma **e mal ordinato e ha un campo ad alto attrito in fondo**. Il problema non e la lunghezza, e che la P.IVA a testo libero come ultima domanda e il punto di massimo abbandono potenziale e di massimo ingresso di spazzatura. Con submission ~11% non possiamo dire che spaventa in massa, ma e il punto debole.

**La Q3 P.IVA a testo libero filtra o spaventa?** **Ne l'uno ne l'altro: e il peggio dei due mondi.** Non filtra (accetta zeri e parole), e potenzialmente spaventa chi non ha la P.IVA sotto mano. Va trasformata in un campo numerico vincolato (vedi v5) o spostata fuori dal form (chiesta in chiamata).

**Cosa manca del tutto:** una domanda di **squalifica del lead-partner**. Il 33% dello spreco a valle (agenzie/concorrenti) entra perche nessuna domanda chiede "operi gia nel settore?". Questa e la singola aggiunta a piu alto ritorno.

---

## 3. MODULO v5 PROPOSTO (domanda per domanda)

Principio: stesso numero di step domanda (5, +1 sola rispetto a oggi), **filtro piu forte** sui non-target, **meno attrito** sul campo P.IVA, **completion rate atteso pari o superiore** perche si elimina il campo-testo finale.

Struttura: 1 schermata intro -> 5 domande qualifica -> campi contatto pre-compilati da Meta.

### Schermata intro (nuova, opzionale ma consigliata)
Testo: "Aiutiamo aziende con P.IVA a generare appuntamenti B2B qualificati. Rispondi a 5 domande veloci per capire se possiamo aiutarti."
Scopo: setta l'aspettativa ("aziende", "B2B") e auto-screma chi non e in target prima ancora di iniziare. Riduce lead spazzatura senza costare un campo.

### Q1 - Sei titolare, CEO o decisore di un'azienda con P.IVA?
- Si, sono titolare / CEO / decisore
- No (sono dipendente / non ho potere decisionale)

Logica: se "No" -> messaggio di chiusura cortese, niente contatto raccolto. TIENI identica a oggi ma con ramo di uscita esplicito.

### Q2 - NUOVA - In quale ambito opera la tua azienda?
- Servizi / consulenza
- Prodotti / e-commerce
- Industria / produzione
- **Telemarketing, lead generation o agenzia di vendita per conto terzi**
- Altro

Logica: chi sceglie l'opzione in grassetto e il lead-partner/concorrente. Due strade:
(a) ramo di uscita soft ("Grazie, al momento collaboriamo solo con aziende che vogliono acquisire clienti, non con agenzie partner") -> NON raccoglie contatto;
(b) lascia passare ma il dato arriva in CRM gia flaggato come "fuori target - partner" cosi il setter non lo chiama a freddo.
**Raccomando (a)**: e la domanda che recupera il 33% di spreco identificato dall'audit. Formularla in positivo evita di sembrare ostili.

### Q3 - Qual e il fatturato annuo della tua azienda?
- Meno di 50.000 EUR
- 50.000 - 250.000 EUR
- 250.000 - 1.000.000 EUR
- Oltre 1.000.000 EUR

Logica: **soglie ri-tarate**. Oggi 9/9 sceglie ">50k" perche e l'unica opzione "alta": non discrimina. Spezzando in 4 fasce sopra-soglia vedi davvero la dimensione e puoi prioritizzare i setter. Sotto-50k resta segnale debole ma non escludente (alcune ditte individuali valide stanno sotto). TIENI come domanda, CAMBIA le opzioni.

### Q4 - Quando vorresti iniziare a generare appuntamenti B2B?
- Subito (entro 30 giorni)
- Sto valutando (oltre 30 giorni)

Logica: invariata, funziona. Resta come segnale di intent per il ranking setter.

### Q5 - SOSTITUISCE la P.IVA testo libero - Partita IVA (11 cifre)
Campo numerico, **validazione: esattamente 11 cifre, solo numeri**. Instant Form Meta supporta campi "numerico" con limiti di lunghezza: impostare min=11, max=11, tipo numerico. Questo blocca alla fonte "Paradisecallsrl" (testo, rifiutato) e rende ovvio che "00000000000" e un placeholder (passa la validazione formato ma il checksum Luhn lato CRM lo segnala).

OPZIONE alternativa se la P.IVA in-form alza troppo l'attrito: **rimuovere la P.IVA dal form e chiederla in chiamata.** Pro: completion rate piu alto. Contro: si perde un filtro pre-contatto e si chiamano anche P.IVA inesistenti. **Raccomandazione: tenerla nel form ma come campo numerico vincolato** (Q5). Costa poco attrito in piu del testo libero attuale e taglia la spazzatura. Da A/B testare (vedi sezione 5).

### Campi contatto (invariati, pre-compilati da Meta)
Email, Nome e cognome, Telefono, Nome azienda. Lasciare il pre-fill Meta attivo: e quello che tiene alto il submission rate.

### Riepilogo differenze v4 -> v5
| | v4 (attuale) | v5 (proposto) |
|---|---|---|
| Domande qualifica | 4 | 5 (+1 filtro settore) |
| Filtro lead-partner | assente | Q2 (recupera 33% spreco) |
| Fatturato | 1 opzione utile (>50k) | 4 fasce discriminanti |
| P.IVA | testo libero (accetta spazzatura) | numerico 11 cifre vincolato |
| Schermata intro | assente | si, setta aspettativa "aziende B2B" |
| Ramo di uscita | assente | Q1 No + Q2 partner -> chiusura cortese |

Attrito netto atteso: **neutro o migliore**. Si aggiunge 1 domanda a scelta multipla (basso attrito) ma si elimina un campo testo libero (alto attrito). I rami di uscita riducono gli invii lordi ma alzano la % di lead utili: e voluto.

---

## 4. BUCO DI TRACCIAMENTO DA CHIUDERE (-31% API->CRM)

Tra 13 invii Meta e 9 in foglio mancano 4 lead. Prima di concludere che "il form rende poco", va capito dove vanno questi 4:
- verificare se il foglio prende TUTTI gli invii o solo quelli sincronizzati (Apps Script / integrazione Meta -> Sheet);
- controllare se ci sono lead duplicati contati 2x da Meta (stesso utente, doppio submit);
- escludere lead-test interni.
Finche questo gap non e spiegato, il submission rate vero potrebbe essere migliore di quanto sembra. **Da indagare prima del lancio v5.**

---

## 5. COSA MISURARE (post-freeze, con v5)

KPI di funnel da tracciare a livello di ad set "cos'e telesales":

1. **Submission rate = lead_grouped / link_clicks.** Baseline v4 = 10,9%. Obiettivo v5: >= 10,9% (la v5 non deve far crollare gli invii pur filtrando di piu). Se scende sotto ~8% la P.IVA in-form sta pesando troppo -> passare all'opzione "P.IVA in chiamata".
2. **Costo per apertura modulo = spend / link_clicks.** Baseline 2,75 EUR. E la leva a monte: si abbatte con CPM piu basso e creativa migliore, non col form.
3. **% lead utili in target = lead_target / lead_CRM.** Baseline v4 = 5/9 = 56%. Obiettivo v5: >= 80% (il filtro Q2 deve quasi azzerare i lead-partner).
4. **CPL netto = spend / lead utili.** Baseline 65,4 EUR. E il numero che conta davvero. Obiettivo: scendere verso 40-45 EUR combinando filtro form + ottimizzazione media (IG-only).
5. **Drop API->CRM.** Baseline -31%. Obiettivo: < 10% dopo aver chiuso il buco di tracciamento.
6. **% P.IVA valide (Luhn) sui lead CRM.** Baseline 7/9 = 78%. Obiettivo v5: >= 95% grazie al campo numerico vincolato.

### Come A/B testare la v5 (post-freeze)
Far girare per 10-14 giorni due Instant Form sullo stesso ad set / o su due ad set gemelli:
- A = v4 attuale (P.IVA testo libero, no filtro settore);
- B = v5 (filtro settore Q2 + P.IVA numerica).
Confronto sul **CPL netto** e sulla **% lead utili**, non sul numero grezzo di lead (la v5 ne fara di meno ma migliori, ed e l'esito voluto). Servono ~10-15 lead per ramo per una lettura indicativa: con questo volume vuol dire ~2 settimane.

---

## SINTESI OPERATIVA

- Il form **non spaventa** in modo anomalo (submission ~11%, normale per B2B qualificato). Il vero collo di bottiglia a monte e il volume di click + CPM, non l'abbandono del modulo.
- Il danno vero del form e a **valle**: lascia entrare lead-partner (33% spreco) e P.IVA spazzatura. CPL netto reale 65 EUR contro 36 EUR lordi.
- v5: +1 domanda di filtro settore (taglia i partner), fatturato a 4 fasce, P.IVA da testo libero a numerico 11 cifre, schermata intro, rami di uscita. Attrito netto neutro/migliore.
- Prima del lancio: chiudere il buco di tracciamento API->CRM (-31%).
- Misurare submission rate, % lead utili, CPL netto, % P.IVA valide. A/B test v4 vs v5 su CPL netto, 2 settimane.
