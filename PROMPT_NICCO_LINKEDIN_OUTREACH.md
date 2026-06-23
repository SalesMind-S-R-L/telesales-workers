# Prompt per la chat Claude Code di Nicco — Replica IG → LinkedIn

Copia tutto il blocco sotto in una nuova chat Claude Code di Nicco (o nella stessa dove gira il sistema Instagram):

---

Ciao. Devi replicare il sistema di outreach automatico che già gira su Instagram, ma per **LinkedIn**. Stessa logica (1° messaggio + follow-up dopo 2 giorni), copy diverso.

Inizia leggendo il codice/script dell'attuale sistema Instagram nel mio progetto per capire architettura, dipendenze, tool MCP usati, dove vengono salvati i log dei messaggi inviati. Poi replica la stessa struttura su un nuovo file/modulo dedicato a LinkedIn (es. `linkedin_outreach.py`, `linkedin_sender.py`, o equivalente al naming usato per IG).

## 1. Cosa devi capire dal sistema Instagram esistente

Prima di scrivere codice, fammi un report di:

1. **Quale MCP / tool usi per IG** (claude-in-chrome, browser automation, API non ufficiale, Phantombuster, ecc.)
2. **Dove leggi la lista contatti** (CSV? Google Sheet? Hardcoded? DB?)
3. **Come tracci lo stato di ogni contatto** (inviato? risposto? in attesa follow-up? bloccato?)
4. **Come gestisci la cadenza/timing** dei follow-up (cron? scheduled task? loop in chat?)
5. **Come estrai il nome del destinatario** per personalizzare il messaggio
6. **Rate limit / pause** che già applichi (importante per non far bannare l'account)

Poi mi proponi la stessa struttura su LinkedIn riadattata, dove serve.

## 1.bis Profilo LinkedIn da usare (importante)

L'outreach va eseguito **dal profilo aziendale LinkedIn di Telesales**, NON da un profilo personale.

- Verifica come avviene l'autenticazione/login del profilo Telesales (cookie session, Sales Navigator team seat, tool terzo connesso, ecc.)
- Se ti serve la sessione del profilo Telesales e non ce l'hai, chiedimela PRIMA di scrivere codice
- Tutte le connection request e tutti i messaggi devono partire da Telesales: la firma implicita è quella aziendale
- Se il sistema IG attuale gira su un profilo personale, NON replicare cieco quel pattern: per LinkedIn serve il profilo aziendale

## 2. Differenze chiave LinkedIn vs Instagram

LinkedIn ha vincoli diversi da IG che devi tenere a mente:

- **Connection request prima del messaggio**: su LinkedIn (no Premium/Sales Navigator) per scrivere a qualcuno devi prima collegarti. Il copy del 1° messaggio inizia con "grazie del collegamento" → suppone che il contatto abbia GIÀ accettato la connection.
- **Rate limit aggressivi**: LinkedIn banna account che spammano. Limiti safe:
  - Max 80-100 connection request/settimana (account standard)
  - Max 50 messaggi al giorno
  - Pause random tra azioni (3-10 secondi)
- **Sales Navigator** se abilitato permette InMail diretti senza connection (più costoso ma più libero)
- **Nome destinatario**: estrai sempre il **firstName** dal profilo LinkedIn, NON da username. LinkedIn ha campo dedicato "Nome".

Dimmi prima quale di queste opzioni stiamo usando:
- A) **Account LinkedIn standard** + connection request prima → poi messaggio
- B) **Sales Navigator** + InMail diretti senza connection
- C) **Tool terzo** (Phantombuster, Dripify, Heyreach, We-Connect, LinkedHelper) che orchestra la cosa

## 3. Copy da usare (copia/incolla esatto)

### Messaggio 1 (dopo accettazione connection)

```
Ciao {{nome}}, grazie del collegamento.

Volevo presentarmi al volo: con SalesMind aiutiamo le aziende ad avere ogni mese appuntamenti qualificati con clienti potenziali, sia nuovi mai contattati sia da riattivare, senza perdere tempo a cercarli e contattarli a freddo.

A muovere tutto c'è un sistema di setter professionali e AI Voice che cerca, contatta e fa una prima scrematura al posto tuo, così in agenda ti arrivano solo persone già pronte a parlare di lavoro.

Se può avere senso, ti propongo una call di 15 minuti per capire insieme se vale la pena approfondire.
```

### Messaggio 2 (follow-up dopo 2 giorni, SOLO se nessuna risposta)

```
Ciao {{nome}}, ti riprendo al volo.

Magari il momento non era quello giusto, volevo solo lasciarti uno spunto: spesso le opportunità più rapide da chiudere non sono i contatti nuovi, ma quelli che hai già in archivio e che si sono raffreddati nel tempo.

Se può avere senso parlarne, fammi un cenno.
```

## 4. Regole di personalizzazione

- `{{nome}}` deve essere sempre il **first name** del contatto LinkedIn (es. "Mena", "Marco", "Giulia")
- **Se manca il nome** (profilo anonimo / nome solo iniziale): NON inviare, skippa il contatto e logga "skip — nome mancante"
- **Mai inviare** se il nome contiene caratteri strani / sembra emoji / sembra titolo professionale (es. "Dott." "Avv.")
- **Capitalizza correttamente**: se il nome arriva in MAIUSCOLO da scraping, normalizza a `Nome` (es. "MENA" → "Mena")

## 5. Workflow operativo da replicare

```
Per ogni contatto in lista:
    1. Verifica che sia "connesso" (cioè ha accettato la richiesta)
    2. Verifica che NON gli abbiamo già scritto (consulta lo state file/sheet)
    3. Verifica che NON ci abbia risposto (se ha risposto, salta tutto)
    4. Invia Messaggio 1 con {{nome}} sostituito
    5. Logga: data invio + stato "messaggio_1_inviato"
    6. Pausa random 5-15 secondi prima del prossimo contatto

Dopo 2 giorni dall'invio Messaggio 1:
    7. Per ogni contatto con stato "messaggio_1_inviato":
        - Controlla se ha risposto
        - SE ha risposto: aggiorna stato a "risposto" e STOP (non mandare follow-up)
        - SE non ha risposto: invia Messaggio 2 con {{nome}}
        - Logga: data invio follow-up + stato "messaggio_2_inviato"
    8. Pausa random tra invii
```

## 6. State management consigliato

Replica esattamente lo stesso pattern del sistema IG (così abbiamo coerenza). Probabilmente è uno di questi:

- **Google Sheet** con colonne: `nome | profilo_linkedin | stato | data_invio_1 | data_invio_2 | data_risposta | nota`
- **CSV locale** + script che lo aggiorna a ogni invio
- **DB SQLite** locale

Stati possibili:
- `da_contattare` (connection accettata, mai scritto)
- `messaggio_1_inviato`
- `messaggio_2_inviato`
- `risposto` (terminal — non scrivere più)
- `skip` (nome mancante o altri motivi)

## 7. Sicurezza account LinkedIn

NON FARLO se non lo fai già su IG: limiti rigidi per non far bannare l'account:

- **Max 30-40 messaggi/giorno** (anche se LinkedIn permette di più, sotto la soglia di rilevamento)
- **Pause random** 5-15s tra un'azione e l'altra
- **Non operare h24**: simula orario lavorativo italiano (es. 9:00-12:00 + 14:30-17:30, no weekend)
- **Detect captcha / verifica account**: se LinkedIn mostra captcha o richiede verifica, FERMATI e loggami immediatamente

## 8. Cosa farmi vedere prima di iniziare

Dopo aver letto il codice IG esistente, mostrami:

1. **Diff/Plan**: cosa terrai uguale, cosa cambia per LinkedIn
2. **Architettura proposta**: file da creare, dipendenze MCP, dove tieni lo state
3. **Stima tempo** per il porting
4. **Domanda bloccante**: se hai dubbi su quale opzione usare per LinkedIn (Sales Nav vs standard vs tool terzo), chiedimelo PRIMA di scrivere codice

## 9. Inizio

Comincia con:
1. Leggi il codice IG attuale (Glob/Grep per trovarlo nel progetto)
2. Mostrami il report del punto 1 ("Cosa devi capire dal sistema Instagram esistente")
3. Aspettami per le risposte sulle scelte LinkedIn (punto 1.bis, 2 e 5)

Quando ho confermato, parti col codice.

## 10. Come pormi le domande

Se hai dubbi, domande, o serve una decisione mia su qualcosa, fammele **a risposta chiusa** — opzioni multiple tra cui scegliere (A / B / C), MAI domande aperte.

Esempi del formato che voglio:

> **Q: Quale variante LinkedIn usiamo?**
> A) Account standard + connection request → poi messaggio
> B) Sales Navigator + InMail diretti
> C) Tool terzo (Phantombuster / Dripify / Heyreach)

> **Q: Dove tieni lo state dei contatti?**
> A) Stesso Google Sheet del sistema IG
> B) Nuovo Google Sheet dedicato LinkedIn
> C) CSV locale + script

Così rispondo veloce con A/B/C senza dover scrivere troppo. Se proprio nessuna delle opzioni funziona, aggiungi sempre una **D) Altro (specifica)**.

---

Grazie Nicco, fammi sapere.
