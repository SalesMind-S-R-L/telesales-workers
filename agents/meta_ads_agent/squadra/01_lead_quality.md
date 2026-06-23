# Lead Quality Audit - Campagna Telesales v4 (Mag-Giu 2026)

Fonte: foglio CRM tab TS_LeadQualificati_v4b_Mag2026. Lead totali: 9.
Ad set: tutti da "cos'e telesales" (6982220524465), unico produttivo.
Data audit: 10/06/2026.

## Metodo di scoring (0-100)

- P.IVA valida (11 cifre + checksum Luhn-mod10 italiano): 30 pt
- Fit fatturato (>50k dichiarato): 15 pt
- Fit ruolo decisore reale (non concorrente/agenzia): 25 pt
- Timing "subito" (entro 30gg): 20 pt / "valutando": 8 pt
- Email aziendale (non gmail/icloud/ecc): 10 pt
- Classificazione: HOT >= 75 | WARM 45-74 | COLD < 45

Nota: i lead che sono agenzie/concorrenti in cerca di partnership NON sono clienti del servizio (telesales vende setter ad aziende che vogliono appuntamenti; un'agenzia di telemarketing che propone partnership e fuori target commerciale) -> azzerano il punteggio "ruolo decisore".

## Tabella per-lead

| # | Nome | Azienda | P.IVA | Valida | Email | Timing | Tel | Score | Classe |
|---|------|---------|-------|--------|-------|--------|-----|-------|--------|
| 1 | Giuseppe Sciuto | Affissione com srl | 05377400873 | SI | aziendale | subito | si | 100 | HOT |
| 2 | Michele Busia | Proffi | 12266730014 | SI | aziendale | subito | si | 100 | HOT |
| 3 | Enrico del Sordo | Come-inn.com | 04019560988 | SI | aziendale | subito | si | 100 | HOT |
| 4 | Camillo Ruocchi | Banca Fideuram | 03530370653 | SI | generica | subito | si | 90 | HOT |
| 5 | Nico Convertini | Ergomed srl | 07876830725 | SI | generica | valutando | si | 78 | HOT |
| 6 | Samuele Simonetti | Lynxis telecom sl | 00000000000 | NO (fake) | generica | subito | si | 60 | WARM |
| 7 | Federico Moizo | (imprenditore) | 09206650963 | SI | aziendale | valutando | no | 33 | COLD |
| 8 | LORENZO | Ronconi service | 09010901008 | SI | generica | subito | no | 30 | COLD |
| 9 | Teresa Caputo | Paradisecall | Paradisecallsrl | NO (testo) | generica | subito | no | 0 | COLD |

## Dettaglio e razionale

**1. Giuseppe Sciuto - Affissione com srl (HOT 100)**
P.IVA 05377400873 valida (checksum ok). Email dominio aziendale (@affissione.com), coerente col nome azienda. Decisore, subito, telefono presente, webcall gia fissata (martedi 12.30). Lead esemplare.

**2. Michele Busia - Proffi (HOT 100)**
P.IVA 12266730014 valida. Email commerciale@proffi.it aziendale. Subito, telefono presente, nota "ok si chiude dal 18" = vicino alla chiusura. Top lead.

**3. Enrico del Sordo - Come-inn.com (HOT 100)**
P.IVA 04019560988 valida. Email aziendale (@delsordo.com). Subito, telefono presente. Stato "nr e mex inviato" (da ricontattare ma qualita massima).

**4. Camillo Ruocchi - Banca Fideuram (HOT 90)**
P.IVA 03530370653 valida. Email gmail (-10). Subito, telefono presente, richiamo lunedi 15. Unico dubbio: "Banca Fideuram" come nome azienda con P.IVA personale/gmail suggerisce un promotore finanziario (P.IVA individuale), non la banca. Fit comunque alto: decisore con P.IVA che vuole appuntamenti B2B.

**5. Nico Convertini - Ergomed srl (HOT 78)**
P.IVA 07876830725 valida. Email icloud (-10). Timing "valutando" (-12 rispetto a subito), nota "fissare dal 24 in poi". Telefono presente. Buon lead ma piu lento.

**6. Samuele Simonetti - Lynxis telecom sl (WARM 60)**
P.IVA 00000000000 = FAKE (placeholder, -30). Email gmail. Subito, telefono presente, call gia in agenda ("call nicco domani pome"). La P.IVA fasulla penalizza, ma contatto reale e ingaggiato: WARM da verificare la P.IVA al telefono.

**7. Federico Moizo - imprenditore (COLD 33)**
P.IVA 09206650963 valida, email aziendale (@moizo.it). MA la nota lo qualifica come amministratore di piu aziende nel settore telecom/VoIP che propone una partnership commerciale ("proposta mia 500 euro/mese + 35 euro x 1to1"): e un potenziale fornitore/partner, non un cliente del servizio. Fuori target commerciale. Timing "valutando", telefono assente.

**8. LORENZO - Ronconi service (COLD 30)**
P.IVA 09010901008 valida. Email gmail. Nota: "nascere una potenziale partnership agenzia di telemarketing, APP PRESO" = altra agenzia/partner, non cliente finale. Telefono assente. Fuori target come cliente.

**9. Teresa Caputo - Paradisecall (COLD 0)**
P.IVA = "Paradisecallsrl" (testo, non numerica) -> NON valida. Email gmail, telefono assente. Nota: "nostra competitor perfetta, vuole dare una mano" = concorrente diretto, non cliente. Da escludere dal funnel commerciale.

## Validazione P.IVA (Luhn mod10 IT)

- Valide: 7/9 (Sciuto, Busia, Del Sordo, Ruocchi, Convertini, Moizo, Lorenzo)
- Fake/invalide: 2/9
  - Samuele Simonetti: 00000000000 (placeholder)
  - Teresa Caputo: "Paradisecallsrl" (testo libero)
- Duplicati: 0. Nessun telefono, P.IVA o email ripetuti.

## Sintesi qualita campagna

- Lead totali: 9
- P.IVA valida: 7/9 = 78%
- Lead validi come clienti (P.IVA ok + in target, esclusi concorrenti/agenzie): 5/9 = 56%
  - Esclusi dal target commerciale: Moizo, Lorenzo, Teresa (3 agenzie/partner/concorrenti)
  - Esclusa P.IVA fake da verificare: Samuele
- HOT: 5/9 = 56% (Sciuto, Busia, Del Sordo, Ruocchi, Convertini)
- WARM: 1/9 = 11% (Samuele, da verificare P.IVA)
- COLD: 3/9 = 33% (tutti concorrenti/agenzie o dati incompleti)
- Timing "subito": 7/9 (intento alto)
- Email aziendali: 4/9; generiche: 5/9

### Lettura
La qualita dei lead "veri clienti" e eccellente: i 5 HOT sono aziende reali con P.IVA validata, fatturato >50k, decisori, timing immediato, telefono presente e in molti casi appuntamento gia fissato. Conferma la diagnosi storica (quality ottima).

Il problema emergente non e la quality ma la CONTAMINAZIONE da concorrenti/agenzie: 3 lead su 9 (33%) sono operatori del settore telemarketing che intercettano l'ad e si candidano come partner/fornitori invece che come clienti. Bruciano CPL e tempo setter. La creative "cos'e telesales" attira anche chi gia fa questo mestiere.

## Raccomandazioni (pronte da eseguire dopo il freeze)

1. Priorita commerciale immediata sui 5 HOT (Sciuto e Busia gia in chiusura). Ricontattare Del Sordo e Ruocchi, fissare Convertini dal 24.
2. Samuele Simonetti: chiamare e farsi dettare la P.IVA reale (quella nel form e placeholder). Se confermata azienda reale sale a HOT.
3. Filtro anti-concorrenti: aggiungere al form una domanda di squalifica tipo "Operi gia nel settore telemarketing/lead generation?" oppure esclusione audience per interessi telemarketing/call center, per ridurre i lead-partner (33% di spreco).
4. Validazione P.IVA lato form: rendere il campo numerico a 11 cifre con check, cosi si bloccano placeholder come "Paradisecallsrl" e 00000000000 prima ancora dell'invio.
5. Marcare nel CRM Teresa/Lorenzo/Moizo come "fuori target - partner/concorrente" per non contarli nel CPL effettivo: il CPL sui clienti reali e migliore di quanto sembri (5-6 lead utili invece di 9).
