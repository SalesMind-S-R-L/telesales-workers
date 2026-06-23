# Sales Mind — Shared Page Build Spec (READ FULLY BEFORE WRITING)

You are building ONE page of the Sales Mind multi-page website. Match the existing site EXACTLY in structure, classes, tone, and quality. Do NOT invent new CSS — only use the classes listed here (they already exist in `/shared/styles.css`). Do NOT add `<style>` blocks except tiny inline `style="..."` tweaks for spacing/centering (as the home does).

## BRAND CONTEXT
- **Sales Mind SRL** = holding di infrastrutture AI per la crescita commerciale. Tagline concept: "Una mente, interi reparti."
- **Telesales** = la divisione commerciale di Sales Mind (appointment setting B2B, voce AI "Marco", link esterno https://telesales.it). Sub-brand, non separato.
- **9 prodotti AI**: AI Voice (flagship), Outreach omnicanale, CRM intelligente, HR AI, Scraping mondiale, Eventi, Prodotti digitali, Marketing AI, Trova investitori.
- Posizionamento: non SaaS generico, infrastruttura su misura. "Parliamo, progettiamo, costruiamo. Poi il sistema gira."
- Contatto: **admin@telesales.it**. Demo: widget "Parla con Marco" (chiamata reale).
- Numeri ricorrenti (usali coerentemente): 1.033 chiamate reali/settimana · 780ms latenza voce · 98,4% accuracy dati · 194 paesi · 127k record/giorno · 47 fonti · proposta in 72 ore · setup 1-2 settimane.

## TONE / COPY RULES
- Lingua: **italiano**. Sicuro, concreto, diretto, premium. Frasi brevi. Niente buzzword vuote.
- **VIETATE le emoji** ovunque (titoli, testi, liste). Mai.
- Titoli di sezione: usano `<em>...</em>` per la parola chiave (diventa oro corsivo automaticamente). Es: `<h2 class="section-title">Quello che <em>succede</em> davvero.</h2>`
- Niente claim legali/finanziari rischiosi. I numeri sono illustrativi ma plausibili.

## TECH RULES (OBBLIGATORI)
1. **Tutti i path sono root-relative**: `/shared/styles.css`, `/assets/salesmind-mark.svg`, `/ai-voice/`, `/contatti/`, ecc. MAI `./` o `../`.
2. La nav e il footer NON si scrivono a mano: metti SOLO `<div id="site-nav"></div>` (subito dopo `<body>`) e `<div id="site-footer"></div>` (prima degli script). Li inietta `/shared/site.js`.
3. Script in fondo (in quest'ordine):
   ```html
   <script defer src="/shared/site.js"></script>
   <script defer src="/shared/marco.js"></script>
   ```
4. `.reveal` (+ opzionale `.d-1`..`.d-6`) per gli elementi che devono apparire allo scroll — l'animazione è gestita da site.js (aggiunge `.in`). Non scrivere JS di reveal.
5. FAQ: l'accordion è gestito da site.js. Non scrivere JS.
6. Widget Marco (chiamata reale): inserisci AL MASSIMO UNO per pagina:
   ```html
   <div id="marco-widget" data-marco-auto data-headline="Fatti chiamare da Marco <em>adesso</em>." data-sub="Inserisci il tuo numero: il telefono squilla entro pochi secondi. Marco parla con te in diretta, in italiano nativo."></div>
   ```
   Mettilo in una `<section class="section" id="marco">`. Se la pagina non ha senso col widget, usa una CTA verso `/contatti/`.

## HEAD BOILERPLATE (copia esatta, cambia solo TITLE/DESCRIPTION/OG)
```html
<!doctype html>
<html lang="it" data-theme="dark" data-accent="gold">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{TITOLO} — Sales Mind</title>
<meta name="description" content="{DESCRIZIONE 140-160 char}" />
<meta name="theme-color" content="#0a0a12" />
<link rel="icon" type="image/svg+xml" href="/assets/salesmind-mark.svg" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{OG TITLE}" />
<meta property="og:locale" content="it_IT" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400&family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/shared/styles.css">
</head>
<body>
<div id="site-nav"></div>

<!-- PAGE CONTENT HERE -->

<div id="site-footer"></div>
<script defer src="/shared/site.js"></script>
<script defer src="/shared/marco.js"></script>
</body>
</html>
```
(Solo se la pagina usa il widget Trustpilot, aggiungi nel <head>: `<script type="text/javascript" src="//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js" async></script>`)

## COMPONENTI / CLASSI DISPONIBILI (usa SOLO queste)
**Layout**: `.container`, `.section`, `.section-dense`, `.section-head`(+`.center`), `.section-eyebrow` con dentro `<span class="eyebrow">— Etichetta</span>`, `.section-title` (con `<em>`), `.section-sub`.
**Hero pagina interna**: `<header class="page-hero">` (o `.page-hero.center`) con dentro `.container`, `.breadcrumb` (es: `<a href="/">Home</a><span>/</span><a href="/prodotti/">Prodotti</a>`), `.section-eyebrow`, `<h1>` (con `<em>`), `<p class="lead">`, `.hero-cta`. Aggiungi `<div class="hero-bg"></div>` come primo figlio per il glow.
**Hero pieno (solo per pagine prodotto se vuoi impatto)**: `<header class="hero hero-full">` con `.hero-bg`, `.hero-grid-lines`, `.hero-orb.o1/.o2/.o3`, `.hero-inner` (griglia 2 col) o `.hero-inner.single`, `.hero-copy` (eyebrow, `.hero-headline` con `<em>`, `.hero-sub`, `.hero-cta`, `.hero-meta` con `.kv`>`.n.display`+`.l`), e a destra `.hero-visual` (vedi home per il markup con `#heroWave`).
**Bottoni**: `<a class="btn btn-primary">` (oro), `<a class="btn btn-ghost">` (outline). Freccia: `<span class="arrow">→</span>`.
**Bento prodotti**: `.services-grid` > `<a class="service-card hero|wide|std reveal">` > `<div class="card">` con `.num`(mono), `.icon`(svg 22-24px stroke), `<h3>`, `<p>`, `.tag`(mono). (Vedi home `/index.html`.)
**Stat grid**: `.stats-grid`(+`.three`) > `.stat-cell` (`.n`, `.l`, `.src.mono`).
**Proof**: `.proof-grid` > `.proof-cell` (`.n`, `.l`).
**Steps "come funziona"**: `.steps-grid`(+`.four`) > `.step` (`.n`, `<h4>`, `<p>`, `.dur.mono`).
**Problemi/pain**: `.problem-grid` > `.problem-card` (`.tag.mono`, `<h4>`, `<p>`).
**Value/feature**: `.value-grid` > `.value-card` (`.ic` con svg, `<h4>`, `<p>`).
**Two-col**: `.two-col` > (colonna testo con `.gold-list`) + `.col-visual` > `.mini-stat` (`.n`,`.l`).
**Gold list**: `<ul class="gold-list"><li><strong>Titolo.</strong> testo.</li></ul>`.
**Risultati/testimonial**: `.results-grid` > `<figure class="result-card reveal">` con `.result-metric`(`.n`,`.m`) + `<blockquote>"..."</blockquote>` + `<figcaption>`(`.who`,`.what.mono`).
**FAQ**: `<div class="faq-grid">` con a sinistra una `.section-head` e a destra `<div class="faq-list">` di `.faq-item` > `<button class="faq-q">Domanda<span class="faq-toggle">+</span></button>` + `<div class="faq-a"><div class="faq-a-inner">Risposta</div></div>`.
**Manifesto**: `<section class="manifesto"><div class="container"><p class="reveal">Testo con <em>parola</em>.</p></div></section>`.
**CTA finale**: `<section class="cta-block"><div class="container"><div class="cta-inner">` eyebrow + `.section-title` + `.section-sub` + `.hero-cta`.
**Overview list (per /prodotti)**: `.overview-list` > `<a class="overview-row" href="/slug/">` con `.ov-num`, `.ov-name`, `.ov-desc`, `.ov-go`(con `<span class="arrow">→</span>`).
**Team**: `.team-grid` > `.team-card` (`.avatar` con iniziale, `<h5>`, `.role`, `<p>`). NON inventare nomi reali di persone: usa RUOLI/funzioni (es. "Voice Engineering", "Data & Enrichment", "Commerciale"). 
**Contatti**: `.contact-grid` (2 col) > colonna form con `.form-field` (label+input/textarea) + colonna `.contact-channels` > `.contact-channel` (`.ic`, `<h5>`, `<p>` con `<a>`).
**Pacchetti/come-iniziare**: `.pkg-grid` > `.pkg-card`(+`.featured`) con `.pkg-badge`, `<h4>`, `.pkg-for`, `.gold-list`, `.btn`.
**Utility**: `.mono`, `.display`, `.eyebrow`, `.badge-live`+`.dot`, `.micro-stats`.

## STRUTTURA TIPO DI UNA PAGINA (ricca, scrollabile, non una landing corta)
1. page-hero (o hero pieno) con breadcrumb + titolo + lead + CTA
2. 4-7 sezioni `.section` alternate (problema → soluzione/feature → come funziona → casi/scenari → numeri → demo Marco o CTA intermedia)
3. FAQ (3-5 domande)
4. cta-block finale
Ogni sezione ha `.section-head` con eyebrow+titolo+sub. Usa `.reveal` con delay scaglionati sulle card.

## QUALITÀ
- Densità di contenuto alta: testi reali e specifici, non placeholder. Ogni card ha copy vero.
- Coerenza numeri col brand. Coerenza di tono con la home (`/index.html` è il gold standard — leggila).
- Mobile: usa solo le classi date (sono già responsive).
- Link interni sempre a pagine reali root-relative. Collega le pagine tra loro (es. da un prodotto rimanda a `/prodotti/`, `/risultati/`, `/contatti/`).

PRIMA di scrivere: leggi `/Users/simocors/Desktop/telesales/telesales-website-deploy/index.html` (gold standard) e, se rifai una pagina prodotto, leggi la versione esistente `/Users/simocors/Desktop/telesales/telesales-website-deploy/{slug}/index.html` per riusare/migliorare i contenuti. Poi scrivi il file completo.
