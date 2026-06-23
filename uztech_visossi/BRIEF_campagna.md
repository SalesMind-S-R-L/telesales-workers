# Campagna AI Voice — Invito Webinar UZ Tech (Alessandra Visossi)

## Obiettivo
Riempire i posti del webinar gratuito UZ Tech sul **Digital Product Passport** chiamando ~400 anagrafiche (lato Telesales) e portandole all'iscrizione.

## Evento
- **9 luglio 2026, ore 16:00-17:00**, online, gratuito.
- Tema: DPP Studio (piattaforma UZ Tech, AI + blockchain), modello White Label, nuovi servizi da rivendere ai clienti.
- Target ideale (da pagina UZ Tech): software house, system integrator, consulenti e agenzie, fornitori NFC/RFID.
- Link ufficiale registrazione: https://uztech.it/uz-tech-partner-page/

## Agente
- **Elena** (assistente vocale UZ Tech) — prompt: `prompt_elena_uztech_dpp.md`.
- Adattato dai migliori voice agent sul profilo: struttura outbound B2B (Ferretti) + tono consulenziale (Luca). CTA UNICA = iscrizione.
- Config consigliata: LLM `claude-haiku-4-5`, turn_timeout 5.0, voce femminile premade (es. la voce usata per gli agenti femminili attuali).

## Dynamic variables da compilare PRIMA di pubblicare (regola fissa)
| Variabile | Contenuto |
|---|---|
| `tipo_numero` | `diretto` o `aziendale` (vuoto = aziendale) |
| `nome_contatto` | referente |
| `nome_azienda` | azienda |
| `categoria` | software house / system integrator / consulente / agenzia / NFC-RFID |
| `citta` | città |
| `note` | eventuale nota lead |

## Registrazione — RACCOMANDAZIONE (modello OSM, non link diretto)
**Non** affidarsi al solo link UZ Tech: l'AI non compila form di terzi in chiamata e perderemmo il tracking call→iscritto.

Approccio consigliato (come OSM):
1. **Foglio Google Telesales** = fonte di verità (nome, azienda, email, telefono, esito, fonte = AI Voice, timestamp).
2. In chiamata Elena raccoglie **conferma + email**, esito loggato sul foglio.
3. Subito dopo la chiamata: **email/SMS automatica con il link ufficiale UZ Tech** così la persona completa l'iscrizione (o registrazione massiva da parte nostra/UZ Tech a partire dal foglio).
4. **Reminder anti no-show**: email/SMS il giorno prima e la mattina del 9/7.

Vantaggi: vediamo la conversione reale della campagna, gestiamo i reminder, e la funnel UZ Tech resta intatta.
> Landing Telesales dedicata (stile OSM Firenze) = opzionale, solo se Alessandra vuole una pagina brandizzata intermedia. Altrimenti basta foglio + invio link ufficiale.

## Da decidere / mi serve
1. **Excel 400 anagrafiche** (lo incolli tu) → normalizzo telefoni in E.164, separo diretto/aziendale, compilo le dynamic variables.
2. **Identità di Elena**: si presenta come "Elena di UZ Tech" (assunto attuale) oppure a nome di Alessandra Visossi / Telesales? Confermami.
3. **Registrazione**: ok al modello foglio + invio link ufficiale? UZ Tech vuole gli iscritti direttamente sul loro form (allora servono email/SMS con link) o accetta che gli passiamo la lista?
4. Quota target iscritti che Alessandra vuole portare.
