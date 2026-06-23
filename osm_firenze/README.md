# Landing OSM Firenze — Selezione del Personale + Delega (06/07/2026)

Copia fedele della landing OSM (`eventiosm.it`) dell'evento di Firenze, pensata per i
lead chiamati da Telesales: l'utente si iscrive e basta. I dati del modulo finiscono in
tempo reale su un Google Sheet tramite una Web App Apps Script.

## STATO: già configurato e live (17/06/2026)

- **Landing live:** https://osmfirenze.vercel.app (Vercel, team telesales1)
- **Google Sheet iscrizioni:** https://docs.google.com/spreadsheets/d/1EN3feEFYURRpaJiIliQluAafjUcJMB1EoXBQVeVgwoY/edit
  (Drive di simonecorsani18@gmail.com, tab "Iscrizioni")
- **Web App Apps Script:** deployata (v2), URL già inserito in `config.js`
- Flusso verificato end-to-end: invio dal sito → riga nel foglio in tempo reale.

Non serve rifare il setup: è tutto collegato. La sezione sotto serve solo se vuoi
ricreare/ripristinare l'integrazione da zero.

## File

| File | Cosa fa |
|------|---------|
| `index.html` | La pagina (hero, descrizione, speaker, modulo iscrizione) |
| `app.js` | Province, validazione, invio del modulo |
| `config.js` | **Unico file da modificare**: incolla qui l'URL della Web App |
| `apps_script_osm_firenze.gs` | Codice da incollare in Apps Script (crea il foglio + riceve le iscrizioni) |
| `assets/` | Immagini (cover evento + foto speaker) |

## Campi raccolti (uguali al modulo OSM)

Nome · Cognome · Email · Telefono (con prefisso) · Città · Provincia · Azienda ·
Ruolo (Titolare/Manager/Dipendente/Socio) · Consenso privacy · Consenso 3.1 (partner) ·
Consenso 3.2 (marketing) · Fonte (Telesales).

Ogni campo è una colonna del foglio. Viene aggiunta anche la colonna **Timestamp**.

## Collegamento al Google Sheet (una volta, ~3 minuti)

1. Vai su <https://script.google.com> → **Nuovo progetto**.
2. Incolla tutto il contenuto di `apps_script_osm_firenze.gs`.
3. Seleziona la funzione **`setup`** in alto → **Esegui** → autorizza.
   Crea il foglio nel tuo Drive; il link compare in *Visualizza → Log di esecuzione*.
4. **Distribuisci → Nuova distribuzione → App web**
   - *Esegui come*: **Me**
   - *Chi ha accesso*: **Chiunque**
   - **Distribuisci** → copia l'URL che finisce con `/exec`.
5. Incolla quell'URL in `config.js` → `ENDPOINT`.

Da quel momento ogni iscrizione viene scritta nel foglio in tempo reale.
Finché `ENDPOINT` è vuoto, il modulo funziona in **modalità demo** (mostra la conferma
ma non salva nulla).

## Pubblicazione (Vercel)

Dalla cartella `osm_firenze/`:

```
npx vercel deploy --prod --yes
```

## Anteprima locale

```
python3 serve.py   # http://127.0.0.1:8913
```
