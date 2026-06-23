# ROADMAP OPERATIVA - Campagna Telesales v4

Campaign Director - sintesi finale squadra. Aggiornata 10/06/2026. Freeze attivo fino ~16/06.

---

## 1. STATO ATTUALE (numeri veri)

- 30 giorni (11/05-09/06): spesa 326,76 EUR, 9 lead CRM (fonte vera), CPL lordo 36,3 EUR ma CPL netto 65,4 EUR sui 5 lead realmente in target. Frequenza bassa (no saturazione), problema = CPM stagionale (picco 43, ora gia rientrato a 20,9 il 09/06).
- Quality clienti reali eccellente (P.IVA valida 78%, fatturato >50k, decisori), ma contaminata: 3/9 lead (33%) sono agenzie/concorrenti telemarketing che bruciano CPL e tempo setter; 2/9 P.IVA fake passate dal form.
- Unico ad set produttivo: "cos'e telesales" 6982220524465 (25 EUR/g). Instagram converte al doppio di Facebook (CPL 28 vs 52). Sweet spot maschi 35-54.

---

## 2. AZIONI ORA (durante freeze, rischio zero)

Tutto preparato/applicato senza toccare nulla di live.

| # | Azione | Owner | Impatto atteso | Come si misura |
|---|--------|-------|----------------|----------------|
| A1 | Applicare le 11 colonne CRM (24-34, X-AH) con dropdown chiusi + formattazione condizionale; backfill dei 9 lead (X=Da contattare, Y=Da chiamare, Z=0, AC=Non assegnato, AF=Meta v4) | Director | Pipeline tracciabile, base per misurare quality% e CPL netto | Foglio CRM con 9 lead backfillati, 0 celle vuote |
| A2 | Marcare nel CRM Teresa/Lorenzo/Moizo come "fuori target - partner/concorrente"; chiamare Samuele Simonetti per P.IVA reale (ora placeholder 00000000000) | Setter (Karima) | Recupera ~33% spreco CPL gia oggi sui lead esistenti | Lead utili 5/9 -> conteggio netto separato in CRM |
| A3 | Priorita commerciale sui 5 HOT: chiudere Busia ("si chiude dal 18") e Sciuto (webcall mar 12.30), ricontattare Del Sordo e Ruocchi, fissare Convertini dal 24 | Setter | Conversione lead gia pagati = ROI immediato senza nuovo spend | Stato Pipeline -> Appuntamento/Cliente |
| A4 | Preparare modulo v5 (5 domande): aggiungere Q "ambito azienda" con uscita telemarketing/agenzia; P.IVA da testo libero a campo numerico 11 cifre vincolato; fatturato a 4 fasce. NON pubblicare, solo bozza pronta | Director | Filtra 33% lead-partner + blocca P.IVA fake alla fonte. Target quality 56%->80% | Bozza form v5 pronta in draft |
| A5 | Preparare 3 creative Reels 9:16 (A risultato, B dolore, C prova/autorita) gia rese, sottotitoli, CTA "Invia messaggio", primary <125 parole | Director | Refresh creativo pronto da caricare nell'ad set winner | 3 asset finiti in 05_creative.md |
| A6 | Preparare le Custom Audience curl-ready: 1A LeadForm engagers 90gg, 1B SiteVisitors 180gg (pixel 399320589867296). NON creare ancora | Director | Sorgente Lookalike futura (CRM <100 record, non basta per LAL) | Script pronti in 04_audience.md |

Nota: indagare a parte il buco di tracciamento -31% Meta API -> CRM (4 lead persi) PRIMA del lancio v5, altrimenti il confronto A/B e inquinato. Owner: Director. Fuori scope freeze, ma da chiudere entro 16/6.

---

## 3. AZIONI AL 16/6 (fine freeze) - UNA MODIFICA PER VOLTA, IN QUEST'ORDINE

Ordine per impatto/rischio. Si attiva la PRIMA, si osserva 5-7 giorni a budget stabile, poi la successiva.

| Ordine | Azione | Owner | Impatto atteso | Come si misura |
|--------|--------|-------|----------------|----------------|
| 1 | Pubblicare il modulo v5 e farlo girare A/B vs v4 sull'ad set winner. Questa e la leva a piu alto impatto/minor rischio: non tocca budget ne audience | Director | Quality 56%->80%, CPL netto 65->40-45 EUR, taglia 33% spreco partner | Submission rate (baseline 10,9%), % lead utili, % P.IVA Luhn valide (78%->95%) |
| 2 | Caricare le 3 creative Reels come ad NUOVI dentro l'ad set winner (non frammentare l'apprendimento, non creare ad set nuovo) | Director | Combatte la contaminazione lato messaggio (variante C) + recupera CPM basso Reels | CPL reale CRM per ad dopo 5-7gg |
| 3 | Applicare LEVA 1 performance: in posizionamenti manuali escludere facebook/notification, reels_overlay, biz_disco_feed, marketplace; restringere eta 35-64 (taglio 25-34 e 65+) | Director | Recupera ~24 EUR posizioni morte + ~64 EUR da fasce inefficienti, reinvestibili | CPM/CPC per posizione, CPL per fascia eta |

Regola: NON spegnere FB feed (3 lead veri) ne escludere le femmine in modo secco - volume troppo basso per decidere, lasciare allocare l'algoritmo.

---

## 4. AZIONI SETTIMANE 2-4 (scaling/test)

| Settimana | Azione | Owner | Impatto atteso | Come si misura |
|-----------|--------|-------|----------------|----------------|
| Sett. 2 | Quando LeadForm engagers supera 100 match, creare Lookalike 1% Italia (2A, ratio 0.01) dalla miglior sorgente | Director | Sorgente nuova qualita, prepara test IG-only | reachestimate, overlap check PRIMA di attivare |
| Sett. 3 | LEVA 2: ad set LAL SEPARATO in campagna v4 6982220525065, anti-Leonardo (solo LAL, esclude le 3 Custom sorgente, Advantage OFF, eta 35-64, 9 citta winner), budget incrementale 15 EUR/g (non raddoppio) | Director | Se CPL IG 28 EUR regge su volume, CPL medio 36->~30 EUR | CPL netto CRM ad set LAL, % concorrenti |
| Sett. 4 | LEVA 3: budget contro-ciclico sul CPM - alzare nei giorni a CPM basso (tipo 09/06 a 20,9), NON scalare nei picchi (07/06 a 43). Concentrare creativa Reels su 35-54 M | Director | Riduce CPL medio sfruttando la stagionalita CPM | CPM giornaliero vs spend allocato |

Criterio LAL: VINCE se CPL<=35 EUR e qualita pari ai HOT; SPEGNI se CPL>45 a freq<1.3 o >30% concorrenti.

---

## 5. KPI TARGET E SOGLIE

| Metrica | Baseline attuale | Target | Soglia allarme (intervieni) |
|---------|------------------|--------|------------------------------|
| CPL netto (lead in target, da CRM) | 65,4 EUR | 40-45 EUR | >50 EUR sostenuto 7gg |
| CPL lordo (tutti i lead CRM) | 36,3 EUR | <30 EUR | >45 EUR |
| Volume lead utili | ~5/mese | 8-10/mese | <4/mese |
| Quality % (lead in target su totale) | 56% | >=80% | <60% |
| % P.IVA valide (Luhn) | 78% | >=95% | <85% |
| CPM | 20,9 (09/06) | <25 | >35 sostenuto |
| Frequenza | bassa, no saturazione | <1,5 | >2,0 (refresh creativo) |

Conteggio lead: SEMPRE dal CRM. I lead API/lead_grouped (13) servono solo per ranking relativo nei breakdown, mai come conteggio assoluto.

---

## 6. REGOLA D'ORO ANTI-AUTODISTRUZIONE

UNA SOLA MODIFICA STRUTTURALE PER SETTIMANA. Dopo ogni modifica: minimo 5-7 giorni di osservazione a budget stabile prima della successiva.

- Mai cambiare due variabili insieme (budget + audience, o form + creative): non sapresti cosa ha mosso il dato.
- Mai scalare il budget durante un picco di CPM - e contro-ciclico (la storia v4 mostra che l'instabilita budget passata ha fatto danni).
- Mai decidere su volumi sotto 5 lead: aspetta dati, non spegnere FB feed/femmine d'istinto.
- La sequenza e: prima il FORM (quality), poi la CREATIVE (messaggio), poi i POSIZIONAMENTI (efficienza), poi l'AUDIENCE (scaling). Mai invertire: scalare audience su un funnel ancora contaminato moltiplica lo spreco.
