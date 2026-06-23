# PROMPT PER CLAUDE CODE DI NICOLÒ — Analisi completa social Telesales + 10 script nuovi

> Incolla TUTTO il testo qui sotto (dalla riga `=== INIZIO PROMPT ===` in poi) nel tuo Claude Code, dentro la cartella di lavoro che vuoi usare. Prima di inviare, controlla solo il blocco "DATI DA CONFERMARE": se gli handle non sono giusti, correggili.

---

=== INIZIO PROMPT ===

Sei un analista di marketing senior + content strategist. Obiettivo di questa sessione: analizzare in modo COMPLETO e REALE tutto ciò che il brand **Telesales** ha pubblicato su Instagram e Facebook, capire cosa abbiamo comunicato e come, e produrre **10 nuovi script pronti da girare** per i prossimi contenuti, basati sulla strategia che emerge dai dati.

Lavora in autonomia, a fondo, senza badare a tempo o costi. Non chiedermi conferme a ogni passo: procedi e fermati solo se sei davvero bloccato (es. login non riuscito).

## DATI DA CONFERMARE (controlla questi 3 valori prima di partire)
- Instagram: profilo `@telesalesita` → https://www.instagram.com/telesalesita/
- Facebook: pagina "Telesales Ita" (cerca la pagina ufficiale e prendi l'URL esatto)
- Periodo da analizzare: TUTTO lo storico disponibile (dall'inizio del profilo a oggi)

## CONTESTO BRAND (serve a generare script coerenti — integra/correggi se sbaglio)
Telesales è un'agenzia/servizio B2B nel mondo telesales e appuntamenti commerciali, con forte uso di AI (voice agent AI che chiamano i lead, setter umani, sistemi di qualificazione lead, CRM). Vendiamo a imprenditori e aziende che vogliono più appuntamenti qualificati e più vendite senza gonfiare il team commerciale. Pubblico target: imprenditori, titolari PMI, direttori commerciali, agenzie. Tono: concreto, diretto, no fuffa, dimostrativo (mostriamo risultati e meccanismi reali).

## REGOLE FERREE (non violarle mai)
1. **Zero allucinazioni.** Negli script di analisi usa SOLO ciò che è realmente nel transcript o realmente scritto a schermo/in didascalia. Non inventare mai cosa è stato detto in un video. Se un contenuto non è scaricabile/trascrivibile, segnalalo come "non analizzabile" anziché immaginarne il contenuto.
2. **Trascrizione vera del parlato.** Per ogni video/reel devi avere lo script REALE dell'audio (Whisper), non un riassunto della didascalia.
3. **Niente emoji** nei deliverable (report e script).
4. **Italiano** in tutti gli output.
5. Salva tutto su file nella cartella di lavoro: dataset, trascrizioni e deliverable finali.

---

## FASE 0 — Setup ambiente
Crea una cartella di lavoro `analisi_social_telesales/` con sottocartelle `raw/`, `transcripts/`, `frames/`, `report/`.
Installa e verifica gli strumenti (usa l'approccio più affidabile sul Mac; se manca `brew`, installalo):
- `ffmpeg` (estrazione audio + keyframe dai video)
- `yt-dlp` (download video/reel da URL pubblici, sia IG che FB)
- `instaloader` (download bulk del profilo Instagram con metadati: didascalie, like, commenti, view, date, tipo post)
- Whisper per la trascrizione: usa `faster-whisper` (più veloce) o `openai-whisper`, modello `large-v3` in italiano. Se la macchina è lenta usa `medium`.
- (Opzionale) `gallery-dl` come fallback per Instagram/Facebook se instaloader viene rate-limitato.

## FASE 1 — Raccolta contenuti (download reale)
Crea un sub-agente/processo dedicato alla raccolta. Obiettivo: scaricare OGNI contenuto pubblicato con i suoi metadati.

Instagram (via `instaloader`):
- Effettua il login (serve per evitare limiti e vedere tutto). Se ho una sessione Safari attiva, prova prima a importare i cookie; altrimenti chiedimi UNA volta user e password e fai `instaloader --login`.
- Scarica l'intero profilo `telesalesita`: post, reel, caroselli, con file JSON dei metadati (didascalia, data, like, commenti, view dei video, hashtag).
- Per i caroselli scarica TUTTE le immagini di ogni slide.

Facebook (via `yt-dlp` + navigazione):
- Per i video della pagina usa `yt-dlp` sugli URL dei singoli video/reel.
- Per i post non-video, raccogli testo e immagini. Se l'API/scraping è bloccato, usa Safari per scorrere la pagina e catturare manualmente i contenuti mancanti (screenshot/testo), segnando quali sono stati presi a mano.

Se qualcosa è rate-limitato: rallenta, riprova con pause, e usa il fallback `gallery-dl`. Logga ciò che NON sei riuscito a scaricare.

## FASE 2 — Trascrizione e lettura reale dei contenuti
Per ogni VIDEO/REEL:
- Estrai l'audio con `ffmpeg` e trascrivilo con Whisper (italiano). Salva il transcript completo in `transcripts/<id>.txt`.
- Estrai 3-6 keyframe con `ffmpeg` in `frames/` e LEGGILI tu direttamente (sei multimodale) per catturare il testo sovrimpresso, hook visivi e b-roll.

Per ogni CAROSELLO/IMMAGINE:
- LEGGI direttamente ogni slide (sei multimodale) ed estrai tutto il testo a schermo, in ordine di slide.

Per ogni contenuto:
- Estrai anche la didascalia completa e gli hashtag dai metadati.

## FASE 3 — Dataset strutturato
Costruisci un dataset unico (salvalo come `report/dataset_contenuti.csv` e una versione `.xlsx` leggibile) con UNA riga per contenuto e queste colonne:
`id | piattaforma | tipo (reel/carosello/foto/post) | data | url | hook_iniziale (prime 1-2 frasi reali) | tema/argomento | angle (problema, dimostrazione, autorità, social proof, offerta, educativo, dietro le quinte...) | testo_a_schermo | transcript_audio (link al file) | didascalia | CTA | hashtag | like | commenti | view | durata_sec | note`

## FASE 4 — Analisi strategica
Dal dataset, produci `report/analisi_strategia.md` che risponde a:
- **Pillar di contenuto**: quali 3-6 temi ricorrono, con quanti contenuti ciascuno e quale peso.
- **Angle e format**: che tipi di hook usiamo, quali format (talking head, dimostrazione AI, case study, meme, carosello educativo...), e quali ricorrono di più.
- **Brand voice**: tono, parole/frasi ricorrenti, livello di formalità, promesse tipiche.
- **CTA**: che call-to-action usiamo e quanto spesso.
- **Cosa performa**: incrocia like/commenti/view con tema/format/hook. Indica i top contenuti e i pattern dei vincenti (con i numeri reali; se i view non sono disponibili dillo).
- **Gap e opportunità**: temi del nostro funnel/offerta che NON abbiamo mai trattato, format poco usati, obiezioni del cliente mai affrontate, angle di differenziazione non sfruttate.
- **Riepilogo posizionamento attuale**: in 5 righe, come ci stiamo posizionando oggi secondo i contenuti reali.

## FASE 5 — 10 nuovi script pronti da girare
Sulla base di quanto performa + dei gap individuati, scrivi `report/10_script_nuovi.md` con **10 script** da iniziare a produrre da questa settimana. Mix **reel parlati + caroselli** (decidi il format ottimale per ciascuno in base ai pattern vincenti; bilancia circa 6 reel e 4 caroselli salvo che i dati suggeriscano altro).

Per OGNI script includi:
1. **Titolo interno + format** (reel 30-60s talking head / dimostrazione / carosello X slide)
2. **Pillar e obiettivo** (a quale tema appartiene e cosa deve ottenere: awareness, autorità, lead, ecc.)
3. **Perché questo script** (1-2 righe: collegamento al dato — cosa ha funzionato o quale gap colma)
4. **Hook** (le prime 3 secondi / prima slide, testuale, forte)
5. **Corpo completo, parola per parola** (per i reel: copione parlato con eventuali indicazioni di testo a schermo e b-roll; per i caroselli: testo di ogni singola slide in ordine)
6. **CTA finale**
7. **Caption suggerita + hashtag**

Gli script devono suonare come noi (usa la brand voice reale estratta in Fase 4), essere concreti e dimostrativi, niente fuffa, niente emoji.

## DELIVERABLE FINALI (verifica che esistano tutti)
- `report/dataset_contenuti.csv` e `.xlsx`
- `transcripts/` con tutte le trascrizioni reali
- `report/analisi_strategia.md`
- `report/10_script_nuovi.md`

Alla fine, dammi un riepilogo esecutivo di max 15 righe: quanti contenuti analizzati per piattaforma, i pillar trovati, i 3 pattern vincenti, i 3 gap principali, e l'elenco dei 10 nuovi script con titolo e format. Indica anche cosa non sei riuscito a scaricare/trascrivere, se qualcosa.

=== FINE PROMPT ===
