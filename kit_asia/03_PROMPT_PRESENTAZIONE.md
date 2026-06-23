# Prompt — Presentazione aziendale (stile Solectro)

> Obiettivo: ricostruire la presentazione Telesales come quelle slide eleganti oro+navy.
> Hai un template di partenza già pronto: `presentazione_telesales_TEMPLATE.html` (nella cartella telesales).
> Lavori a blocchi di 3-4 slide per volta, così Claude non si appesantisce.

---

## Come si lavora (token-saving)
1. Apri il template HTML: è già impostato col brand giusto. **Non si ridisegna**, si riempie.
2. In Claude, **una chat = un blocco di slide** (es. "cover + chi siamo + numeri").
3. Dai a Claude solo: quali slide vuoi e i contenuti. Lui ti restituisce il blocco HTML aggiornato.
4. Le tue foto le inserisci tu nei punti immagine del template.
5. A fine lavoro esporti in PDF (stampa → salva come PDF, oppure me lo passi e lo esporto io).

---

## Struttura consigliata (presentazione aziendale, 8-10 slide)
1. **Cover** — logo + claim "Sostituiamo interi reparti aziendali con AI" + "Made in Italy".
2. **Chi siamo / manifesto** — "Non vendiamo software. Costruiamo infrastrutture." + 3 numeri.
3. **Il problema** — i reparti lenti/costosi, i lead persi (pain point dal brief).
4. **La soluzione** — l'ecosistema dei 9 prodotti (griglia, AI Voice in evidenza).
5. **AI Voice in focus** — il flagship: cosa fa, 780ms, italiano nativo.
6. **I numeri / prove** — 1.033 chiamate, 98,4% accuracy, 194 paesi.
7. **Come lavoriamo** — parliamo → progettiamo → costruiamo → il sistema gira.
8. **Perché Telesales** — su misura, misurabile, 24/7, Made in Italy.
9. **Contatti / CTA** — "Parla con Marco" + sito + email.

(Per la versione con preventivo cliente: si aggiunge in fondo una slide "La nostra proposta" — la facciamo dopo, è già impostata nel template del preventivo.)

---

## PROMPT (copia da qui)
```
Sei il designer della presentazione aziendale Telesales. Conosci brand e contenuti dal Brand Brief del Project.
Sto lavorando su un template HTML di slide (formato 1280x720, oro #d4af6a + navy #0b1740 + crema, font Fraunces+Manrope, niente nero, niente emoji).

Creami il blocco di queste slide come HTML coerente col template:
- [elenca le slide del blocco, es: 1 cover, 2 chi siamo, 3 numeri]

Contenuti da usare:
- [incolla i testi / numeri / claim per ogni slide]
- Dove va una foto, metti un riquadro segnaposto con scritto "FOTO: [cosa]".

Tono deciso, frasi corte, solo numeri reali del brief. Dammi solo l'HTML del blocco, niente spiegazioni.
```

---

## Regole qualità
- Stesso font e stessi margini in tutte le slide (il template li ha già: non cambiarli).
- Una slide = un messaggio. Non riempire di testo.
- Le tue foto degli eventi sono il valore aggiunto: usale nelle slide "chi siamo", "come lavoriamo", "eventi".
- Niente nero, niente emoji, mai numeri inventati.
