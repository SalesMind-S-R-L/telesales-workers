# TelNet Italia — Brief Onboarding AI Voice Inbound (lunedì)

Deal chiuso: >1000€ setup + retainer mensile. Demo inbound piaciuta molto.
Obiettivo lunedì: personalizzare la reception AI e sbloccare le 2 cose che la rendono "vera" → telefonia (loro trunk) e funzioni avanzate (trasferimento + calendario).

Stato attuale (già pronto e live):
- Agente reception in italiano (voce, Claude Haiku 4.5), KB completa dal sito, sa data/ora (gestisce "domani").
- Cattura dati chiamante → foglio Google automatico (link trascrizione ok).
- Landing demo brandizzata Telesales: https://telnetdemo.vercel.app (interfaccia custom, nessun marchio terzo).

---

## 1) Scaletta funzioni & scope — da confermare con loro
Per ogni voce: confermare SI/NO e dettaglio.

- Chi risponde e come: tono, primo messaggio, orari (Lun–Ven 8:30–17:00, fuori orario?).
- Reparti da riconoscere e gestire: **commerciale · amministrazione · tecnico/assistenza** (oggi instrada all'ufficio tecnico — confermare se vogliono distinguere di più).
- Cosa deve SAPER dire da sola (FAQ già in KB) vs cosa deve solo raccogliere e far richiamare.
- Dati obbligatori da raccogliere: nome, azienda, telefono, email, motivo (+ altri?).
- Esiti/etichette per il report: informazioni / appuntamento / assistenza / ricontatto tecnico / spam.
- Gestione clienti vs non-clienti (assistenza su guasto = priorità?).
- Lingua/e: solo italiano? (inglese in seconda battuta?)

## 2) Trasferimento di chiamata ai reparti
- Funziona quando l'agente è su una linea telefonica reale (transfer-to-number).
- **Serve da loro:** i numeri interni/diretti dei reparti (commerciale, amministrazione, tecnico) a cui passare la chiamata.
- Regola: se il chiamante chiede X e c'è qualcuno disponibile → trasferisci; altrimenti raccogli dati e fai richiamare.
- Da decidere: orari in cui trasferire vs sempre a foglio.

## 3) Appuntamenti su calendario
- Oggi: l'appuntamento viene registrato sul foglio (resta così per ora, come deciso).
- Opzioni da valutare con loro per la prenotazione REALE:
  - Cal.com (chiave già disponibile nel nostro workspace, attivabile in fretta — l'AI propone slot liberi e fissa).
  - Google Calendar dedicato TelNet.
  - Loro gestionale/agenda (via accesso credenziali / MCP, approccio no-API che hanno citato).
- **Da decidere:** quale calendario/agenda usano davvero per gli appuntamenti dei clienti.

## 4) Piano telefonia / SIP (per Marcello)
Punto più importante. Loro vogliono usare il **proprio trunk**, NON Twilio (è stato un blocco con un fornitore precedente).
- L'agente si collega via **SIP trunk** a uno o più numeri; può rispondere (inbound) e in futuro chiamare (outbound).
- **Domande tecniche per Marcello:**
  1. Da dove parte il numero inbound: un numero Telnyx che gestiamo noi, oppure il **loro PBX/Yeastar** via SIP trunk?
  2. Possono fornire le **credenziali SIP** (host/IP, username, password, porta) del loro trunk?
  3. Il numero che il cliente chiama è loro o nuovo? Quanti agenti per numero?
  4. Codec/registrazione SIP, eventuali whitelist IP.
- **Latenza:** server di elaborazione in **Europa** (più reattivo) — confermare. La latenza che conta è quella dati/elaborazione, non la voce. Turn-taking da calibrare per non parlare sopra.
- Output da noi: una volta avuto il trunk, assegniamo il numero inbound all'agente e testiamo una telefonata reale.

---

## Decisioni da estrarre lunedì (checklist)
- [ ] Numeri interni dei reparti per il trasferimento.
- [ ] Quale calendario/agenda per gli appuntamenti.
- [ ] Trunk: loro PBX/Yeastar o numero Telnyx nostro + credenziali SIP.
- [ ] Numero inbound da assegnare all'agente.
- [ ] Orari/regole di trasferimento vs richiamo.
- [ ] Eventuali integrazioni col loro gestionale/CRM (e con che approccio: credenziali/MCP).
- [ ] Modello con cui TelNet rivenderà ai clienti (setup vs abbonamento) — per costruire di conseguenza.

## Cosa posso costruire subito (su tua conferma)
- Pre-configurare il tool di trasferimento sull'agente (con i numeri appena li hai).
- Attivare una demo di prenotazione su Cal.com (se vuoi mostrarla funzionante lunedì).
- Affinare prompt/flussi su casi reali TelNet.
