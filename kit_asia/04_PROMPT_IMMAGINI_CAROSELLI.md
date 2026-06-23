# Prompt — Grafiche e caroselli (Claude Design)

> Claude non crea foto realistiche. Crea **grafiche brandizzate** (frasi, dati, copertine, slide carosello).
> Le foto vere le metti tu. Una chat = una grafica/un carosello.

---

## Cosa puoi creare con Claude
- **Grafica singola**: quote card (una frase forte), card-dato (un numero del brief), copertina.
- **Carosello** (Instagram/LinkedIn): 5-8 slide problema → soluzione → prova → CTA.
- **Testo su tua foto**: layout con la tua foto come sfondo e sopra un titolo brandizzato.

Claude te le costruisce come **artifact HTML** che vedi in anteprima a destra → fai screenshot o esporti.

---

## PROMPT — Grafica singola (copia da qui)
```
Crea una grafica social Telesales come artifact HTML, formato quadrato 1080x1080.
Brand: oro/champagne #d4af6a + navy profondo #0b1740, crema #f8f4ea, niente nero. Font Fraunces per il titolo, Manrope per il resto. Niente emoji.
Contenuto: [la frase o il numero da mostrare].
Tipo: [quote card / card-dato / copertina].
Stile: premium, pulito, tanto respiro, accento oro. Logo non serve (lo aggiungo io).
Dammi solo l'artifact, niente spiegazioni.
```

## PROMPT — Carosello (copia da qui)
```
Crea un carosello Telesales come artifact HTML: [N] slide in formato quadrato 1080x1080, una sotto l'altra.
Brand: oro/champagne #d4af6a + navy profondo #0b1740, crema #f8f4ea, niente nero. Font Fraunces (titoli) + Manrope (testo). Niente emoji. Tono deciso, frasi corte.
Struttura: slide 1 hook/problema, slide centrali sviluppo + 1 prova con numero reale del brief, ultima slide CTA.
Testo delle slide: [incolla qui il testo slide-per-slide che ti ha dato il prompt copy].
Lascia spazio dove indico per una mia foto: [sì, slide X / no].
Dammi solo l'artifact.
```

## PROMPT — Testo sulla tua foto
```
Crea un layout social 1080x1350 (verticale IG) come artifact HTML.
Sfondo: lascia un'area immagine in alto (ci metto io la foto) e una fascia navy in basso con il testo.
Brand: oro #d4af6a su navy #0b1740, font Fraunces. Niente emoji.
Testo: [titolo] + [sottotitolo breve].
Dammi solo l'artifact.
```

---

## Regola anti-spreco
Se una grafica ti piace e vuoi solo cambiare la frase: **non rigenerare tutto**, scrivi "stessa grafica, cambia solo il testo in: ...". Costa molto meno.

## Qualità alta (i tuoi 3 controlli prima di pubblicare)
1. Colori giusti (oro + navy, niente nero) e niente emoji.
2. Testo leggibile anche in piccolo (sullo smartphone).
3. Coerenza tra le slide del carosello (stessi font, stessi margini).
