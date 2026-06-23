# Flusso Pubblicazione Rextyle — Piano operativo

*Versione 1.0 — sistema completo, niente live publishing finché tutti i check non sono verdi*

---

## Obiettivo

Pubblicare 6 contenuti a settimana su 4 profili Rextyle (Pagina FB + IG @rextyle_ + 3 IG personali) con **qualità garantita** e **zero pubblicazioni mediocri**. Il sistema ha 5 cancelli di verifica prima che un singolo post vada online.

---

## Architettura del flusso

```
LUN mattina → Tu: comando genera-batch
              ↓
       [GATE 1] Generation
              ↓ (output/2026-WXX/)
       [GATE 2] Self-check automatico
              ↓ (pass/fail report)
       [GATE 3] Tua revisione visual
              ↓ (approve/iterate)
       [GATE 4] Approvazione soci 24h
              ↓ (silence = OK)
MAR sera   → Tu: comando schedule-batch
              ↓
       [GATE 5] Schedule API con dry-run
              ↓
LUN-MER-VEN → Pubblicazione automatica Meta
              ↓
VEN sera   → Tu: comando insights-week
```

5 cancelli. Zero post pubblicati se anche solo uno è rosso.

---

## GATE 1 — Generation

**Comando**: `/rextyle genera-batch settimana N`

**Cosa succede**:
1. Skill `rextyle-social-designer` legge `_contesto/`, `_asset/`, `brand_kit_rextyle.md`, `posizionamento_competitivo.md`
2. Genera 6 brief allineati ai pillar editoriali:
   - **Hub Pagina FB + IG @rextyle_**: 3 post (lun-mer-ven)
   - **Spoke IG Mattia (restyle)**: 1 post (mer)
   - **Spoke IG Nicolò (pulizie operative)**: 1 post (gio)
   - **Spoke IG Alberto (burocrazia annunci)**: 1 post (ven)
3. Per ogni brief: design plan + immagini via Gemini + caption + hashtag
4. Salva in `output/2026-WXX/01-..., 02-..., ...` con struttura:
   ```
   output/2026-W24/01-hub-lun-prima-dopo/
   ├── slide-1.png ... slide-6.png
   ├── caption.md
   ├── hashtag.txt
   └── meta.json
   ```

**Output al termine**: 6 cartelle pronte + `preview.html` (galleria visiva)

---

## GATE 2 — Self-check automatico (lo script blocca se fallisce)

**Comando**: `/rextyle check-batch settimana N` (lanciato automaticamente subito dopo generation)

**Checklist tecnica per ogni post** (script `check_batch.py`):

| Check | Pass se... |
|---|---|
| Logo presente | Logo Rextyle visibile su prima e ultima slide |
| Palette compliant | Solo i 5 HEX del brand kit usati, scarto +/-2 su ogni canale RGB |
| Font compliant | Solo Manrope e Inter rilevati (via metadata PNG generati con i font caricati) |
| Risoluzione corretta | 1080×1350 per post, 1080×1920 per storie |
| Numero slide | Tra 3 e 7 per carosello |
| Caption length | Tra 100 e 800 caratteri |
| Hashtag count | Tra 8 e 12 hashtag |
| CTA presente | Caption finisce con "link in bio", "scrivici", "DM" o equivalente |
| Vocabolario | Nessuna parola dalla blacklist ("massimizziamo", "chiavi in mano", "esperienza pluriennale", "su misura") |
| Brand voice tone | LLM check su tono operativo (no condizionali, no "vorremmo/potremmo") |
| Anti-duplicato | Hash perceptive immagini ≠ post pubblicati ultimi 90 giorni |

**Output**: `output/2026-WXX/check.md` con tabella OK/ISSUES per ogni post.

**Se anche 1 post ha ISSUES**: blocco automatico. Lo script non procede a Gate 3 finché non è tutto verde.

---

## GATE 3 — Revisione visual tua

**Comando**: apri `output/2026-WXX/preview.html` nel browser

**Cosa vedi**: galleria a griglia con i 6 post, ognuno con:
- Slide impilate
- Caption visibile
- Hashtag
- Target (su quale profilo va)
- Schedule (quando)
- Risultato check Gate 2

**Checklist tua** (5 minuti):
1. Coerenza visiva tra i 6 post (tutti riconoscibilmente Rextyle?)
2. Hook delle copertine: incuriosiscono?
3. Numeri credibili nei case study?
4. Differenziazione spoke: Mattia/Nicolò/Alberto hanno angle distinti?
5. CTA chiare e coerenti?

**Se modifiche servono**:
- Comando: `/rextyle fix post 3 cambia hook in "..."`
- Skill rigenera SOLO il post indicato
- Rilancia Gate 2 → Gate 3 finché OK

**Max 2 cicli di iterazione**: se al terzo giro non è OK, si passa a brief umano completo (call interna di 30 min, riscrittura manuale dei brief).

---

## GATE 4 — Approvazione soci

**Comando**: `/rextyle prepara-share settimana N`

**Cosa fa**:
1. Carica `preview.html` + tutti gli asset su Drive condiviso
2. Genera link pubblico viewable (`drive.google.com/...`)
3. Stampa il testo del messaggio WhatsApp pronto da copiare:

> "Ragazzi, preview settimana 24. Se non avete feedback entro 24h schedulo come da preview. Modifiche piccole le facciamo, modifiche grandi rimandiamo a settimana prossima.
>
> [link Drive]"

**Tu**: copi-incolli su gruppo WhatsApp Rextyle.

**Regole approvazione**:
- 24h di silenzio = approvazione tacita
- Feedback singolo punto (es. "cambia foto su post 3") = noi modifichiamo entro 4h, ri-mandiamo preview, nuovo conto alla rovescia 24h
- Feedback strutturale ("non mi convince il tono") = rimandiamo alla settimana successiva, brief umano

---

## GATE 5 — Schedule API con dry-run

**Comando step 1**: `/rextyle schedule-batch settimana N --dry-run`

**Cosa fa lo script `publish_rextyle.py --dry-run`**:
- Si connette a Meta Graph API (verifica token valido)
- Per ogni post simula la chiamata: verifica risoluzione, peso file, lunghezza caption, formato hashtag
- Verifica account: ogni `meta.json` target è raggiungibile?
- Stampa per ogni post: target, schedule time, OK/ERROR
- **Niente viene effettivamente schedulato**

**Output esempio**:
```
[DRY-RUN] Batch 2026-W24
✓ Post 01 → FB Pagina Rextyle | LUN 09:00 | OK (5 slide, 480 char caption)
✓ Post 01 → IG @rextyle_       | LUN 09:00 | OK
✓ Post 02 → IG Mattia          | MER 09:00 | OK
✓ Post 03 → IG Nicolò          | GIO 09:00 | OK
✓ Post 04 → IG Alberto         | VEN 09:00 | OK
✓ Post 05 → FB Pagina Rextyle  | MER 09:00 | OK
✓ Post 05 → IG @rextyle_       | MER 09:00 | OK
✓ Post 06 → FB Pagina Rextyle  | VEN 09:00 | OK
✓ Post 06 → IG @rextyle_       | VEN 09:00 | OK

9 publish actions ready. Run without --dry-run to execute.
```

**Comando step 2** (solo se dry-run è tutto verde e soci hanno approvato): `/rextyle schedule-batch settimana N`

Lo script chiama Meta API e schedula realmente. Pubblicazione automatica gestita da Meta nei giorni programmati.

---

## Cosa pubblichiamo su cosa — matrice 4 profili

| Giorno | Pagina FB Rextyle | IG @rextyle_ | IG Mattia | IG Nicolò | IG Alberto |
|---|---|---|---|---|---|
| **LUN 09:00** | Hub carosello case study | Hub carosello (cross-post FB) | — | — | — |
| **MAR** | — | — | — | — | — |
| **MER 09:00** | Hub educational | Hub educational | Spoke restyle (detail) | — | — |
| **GIO 09:00** | — | — | — | Spoke pulizie operativo | — |
| **VEN 09:00** | Hub listino/pacchetto | Hub listino/pacchetto | — | — | Spoke burocrazia annunci |

**Storie**: in parallelo continue, pubblicate dai soci col cellulare su brief nostro (non gestite via API, non rientrano in questo flusso).

---

## Fase di test prima di andare live (sequenza)

> *Decisione: prima di pubblicare anche un solo post, validiamo l'intero flusso con cicli a vuoto.*

### Sprint Test 1 — Pipeline validation (3 giorni)
- Genera 6 post di test in `output/test-w0/`
- Esegui Gate 1 → Gate 2 → Gate 3 (visual review tua)
- **Non vanno avanti a Gate 4 né 5**
- Output: confidence che generation + check funzionano

### Sprint Test 2 — Brand kit feedback (2 giorni)
- Mandi brand_kit_rextyle.pdf ai soci
- Tu mandi i 6 post di test (preview locale) come "anteprima stile" a Nicolò separato (non gruppo)
- Loro confermano: stile OK / cambia X / Y
- Iteri brand kit + skill

### Sprint Test 3 — Schedule dry-run (1 giorno)
- Esegui `publish_rextyle.py --dry-run` su batch test
- Verifica connessione Meta API per tutti i 4 profili
- Output: confidence che API si connette ovunque

### Sprint Test 4 — Pubblicazione singola pilota (1 giorno)
- 1 solo post pubblicato realmente, sulla Pagina FB Rextyle
- Monitora reach, engagement, errori per 24h
- Decisione: estendere a IG aziendale o iterare

### Sprint Test 5 — Rollout completo
- Da qui in poi: workflow standard sopra

**Totale fase test**: ~10 giorni di lavoro. Da quel momento il sistema è infallibile.

---

## Stato finale che ottieni

- **Tempo tuo a regime**: 30 min/sett (generate + review + share + schedule)
- **Tempo soci**: 24h di silenzio per approvazione, 30 min/sett per storie/reel da cellulare
- **Qualità garantita**: 5 cancelli prima della pubblicazione, anti-mediocrità by design
- **Costo**: ~€1-5/mese a regime
- **Risk profile**: basso. Niente post sbagliati. Niente brand drift. Niente penalty algoritmiche (vedi posizionamento_competitivo.md).

---

## Comandi disponibili a regime

| Comando | Quando |
|---|---|
| `/rextyle genera-batch settimana N` | Lunedì mattina |
| `/rextyle fix post X cambia Y in Z` | Iterazione Gate 3 |
| `/rextyle prepara-share settimana N` | Quando Gate 3 è verde |
| `/rextyle schedule-batch settimana N --dry-run` | Dopo approvazione tacita |
| `/rextyle schedule-batch settimana N` | Solo se dry-run è verde |
| `/rextyle brief-storie giorno` | Mer + Ven, output WhatsApp per i 3 soci |
| `/rextyle insights settimana N` | Venerdì sera |
| `/rextyle refresh-token` | Mensile, cron automatico |
| `/rextyle status` | Quando vuoi vedere cosa è schedulato |
