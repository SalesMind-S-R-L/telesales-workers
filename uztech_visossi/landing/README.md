# Landing Webinar UZ Tech — Digital Product Passport (9 luglio, 16:00)

Landing di iscrizione Telesales (copia funzionale della pagina partner UZ Tech) → form → Google Sheet via Apps Script. Stesso pattern di `osm_firenze`.

## File
- `index.html` — landing + form di iscrizione
- `app.js` — validazione + invio no-cors all'Apps Script
- `config.js` — incolla qui l'URL della Web App (`ENDPOINT`)
- `apps_script_uztech.gs` — Web App che crea il foglio e scrive le iscrizioni
- `vercel.json` — deploy
- `serve.py` — anteprima locale

## Setup foglio + endpoint (una volta)
1. [script.google.com](https://script.google.com) → Nuovo progetto → incolla `apps_script_uztech.gs`.
2. Esegui la funzione `setup` (autorizza) → nei Log trovi il link del foglio creato (`UZ Tech DPP 09-07 - Iscrizioni Telesales`).
3. Distribuisci → Nuova distribuzione → App web → Esegui come: Me · Accesso: Chiunque → copia URL `.../exec`.
4. Incolla l'URL in `config.js` → `UZTECH_CONFIG.ENDPOINT`.

## Deploy
`vercel --prod` dalla cartella (team `telesales1`). Senza `ENDPOINT` la landing gira in modalità DEMO (invio simulato, nessuna scrittura).

## Colonne del foglio
Timestamp · Nome · Cognome · Email · Prefisso · Telefono · Azienda · Figura professionale · Provincia · Interesse webinar · Interesse Partner Kit · Consenso privacy · Fonte

I campi coincidono con le dynamic variables dell'agente AI Voice Elena (nome_contatto, nome_azienda, categoria, citta) per chiudere il cerchio chiamata → iscrizione.
