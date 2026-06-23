# 02 - Performance Analysis v4 (ultimi 30 giorni)

Campagna 6982220525065 - finestra 11/05 -> 09/06/2026
Spesa totale periodo: 326,76 EUR. Reach 6.247, frequenza media 1,14 (NESSUNA saturazione).
Lead VERI (foglio CRM): 9 totali (6 IG, 3 FB). Lead API "lead_grouped": 13 (sovrastima, attribuzione inaffidabile come da diagnosi).
CPL reale medio sul totale: 326,76 / 9 = 36,3 EUR.

NOTA: il breakdown `platform_position` da solo va in errore API (#100) per questa campagna; ottenuto solo combinato con `publisher_platform`. I lead nelle tabelle breakdown sono quelli API (lead_grouped), utili per ranking relativo ma non per il conteggio assoluto, che resta il CRM.

---

## TABELLA 1 - Publisher platform (FB vs IG)

| Piattaforma | Spend | Impr | Clicks | CTR% | CPC | CPM | Lead API | Lead CRM (veri) | CPL reale |
|---|---|---|---|---|---|---|---|---|---|
| Facebook | 157,34 | 5.699 | 123 | 2,16 | 1,28 | 27,6 | 6 | 3 | 52,45 |
| Instagram | 169,42 | 6.029 | 112 | 1,86 | 1,51 | 28,1 | 7 | 6 | 28,24 |

Lettura: spesa quasi pari (50/50), ma IG porta il DOPPIO dei lead veri di FB (6 vs 3). CPL reale IG 28 EUR contro FB 52 EUR. FB ha CTR e CPC migliori (clic piu economici) ma quei clic NON convertono in lead qualificati: e traffico piu rumoroso. IG e la piattaforma efficiente sul lead.

---

## TABELLA 2 - Platform position (feed / reels / stories)

| Piattaforma/Posizione | Spend | Impr | Clicks | CTR% | CPC | CPM |
|---|---|---|---|---|---|---|
| facebook/feed | 82,23 | 2.676 | 60 | 2,24 | 1,37 | 30,7 |
| instagram/instagram_reels | 69,64 | 3.132 | 50 | 1,60 | 1,39 | 22,2 |
| instagram/feed | 56,59 | 1.685 | 29 | 1,72 | 1,95 | 33,6 |
| facebook/facebook_reels | 54,90 | 2.741 | 54 | 1,97 | 1,02 | 20,0 |
| instagram/instagram_stories | 43,18 | 1.210 | 33 | 2,73 | 1,31 | 35,7 |
| facebook/facebook_notification | 16,74 | 161 | 9 | 5,59 | 1,86 | 104,0 |
| facebook/facebook_reels_overlay | 3,43 | 116 | 0 | 0,00 | - | 29,6 |
| facebook/biz_disco_feed | 0,02 | 3 | 0 | - | - | 6,7 |
| facebook/marketplace | 0,02 | 2 | 0 | - | - | 10,0 |

Lettura:
- **Migliore CPM**: facebook/reels (20,0) e instagram/reels (22,2) - i Reels comprano impression a meta prezzo dei feed.
- **Migliore CTR**: instagram/stories (2,73%) e facebook/feed (2,24%).
- **Migliore CPC**: facebook/reels (1,02 EUR) - di gran lunga il clic piu economico.
- **SPRECO 1 - facebook/notification**: 16,74 EUR per CPM 104 EUR (5x la media). Posizione che mostra l'ad come notifica, pubblico tiepido e costosissimo. CTR alto (5,59%) ma e clic accidentale, non intento.
- **SPRECO 2 - facebook/reels_overlay**: 3,43 EUR, 116 impr, ZERO clic. Posizione morta.
- **biz_disco_feed / marketplace**: traffico residuale irrilevante (2-3 impr).

---

## TABELLA 3 - Eta e genere

| Eta/Genere | Spend | CTR% | CPM | Lead API | CPL API |
|---|---|---|---|---|---|
| 45-54 M | 95,59 | 2,10 | 30,4 | 4 | 23,90 |
| 35-44 M | 68,70 | 1,86 | 23,2 | 4 | 17,18 |
| 55-64 M | 65,62 | 2,18 | 34,9 | 3 | 21,87 |
| 25-34 M | 43,94 | 2,05 | 18,0 | 1 | 43,94 |
| 65+ M | 19,49 | 2,21 | 43,0 | 0 | - |
| 45-54 F | 15,26 | 2,34 | 59,6 | 1 | 15,26 |
| 35-44 F | 5,83 | 0,83 | 24,3 | 0 | - |
| 55-64 F | 4,92 | 0,77 | 37,8 | 0 | - |
| 25-34 F | 3,67 | 2,63 | 18,0 | 0 | - |
| 65+ F | 0,87 | 0,00 | 54,4 | 0 | - |

Aggregato genere: **Maschi 293,34 EUR -> 12 lead API** ; Femmine 30,55 EUR -> 1 lead. Il pubblico e gia di fatto quasi tutto maschile (90% della spesa), coerente col target decisori B2B P.IVA.

Lettura eta:
- **Sweet spot 35-54 M**: assorbe 164 EUR (metmeta spesa), 8 lead API su 13, CPL API 17-24 EUR. E il cuore che converte. 35-44 M ha il CPL piu basso (17,18) con CPM basso (23,2).
- **55-64 M**: 3 lead, CPL 21,87, regge bene - tenere.
- **SPRECO 3 - 25-34 M**: 43,94 EUR per 1 solo lead (CPL 43,94, il peggiore tra i maschi). CPM bassissimo (18) ma non converte: troppo giovani per essere decisori P.IVA con >50k fatturato. Banda da comprimere.
- **SPRECO 4 - 65+ (M+F)**: 20,36 EUR, ZERO lead. Coerente col problema "pensionati" gia noto sul modulo. Banda da escludere.
- **Femmine 35-64**: 15,67 EUR, 0 lead, CTR sotto 0,9% nelle fasce centrali. Poco rilevante ma improduttivo.

---

## TABELLA 4 - Trend (primi 7 gg vs ultimi 7 gg attivi)

| Metrica | Primi 7 | Ultimi 7 | Delta |
|---|---|---|---|
| CPM | 24,14 | 31,61 | +31% |
| CPC | 1,09 | 1,99 | +82% |
| CTR | 2,31% | 1,76% | -24% |
| Frequenza | 1,17 | 1,14 | -3% |

Lettura: confermata la diagnosi. La frequenza e piatta a 1,14 (nessuna fatica creativa/saturazione). Il peggioramento e tutto **CPM/CPC in salita** (picco 07/06 con CPM 43,48) e **CTR in calo**. Causa = pressione costo asta stagionale + assestamento dopo le instabilita di budget passate. Il 09/06 il CPM e gia ridisceso a 20,9: segnale che il picco si sta sgonfiando.

---

## 3 LEVE DI EFFICIENZA (pronte da eseguire dopo il freeze ~16/6)

### LEVA 1 - Escludere posizioni e fasce che bruciano budget a zero resa
Azione: in modalita posizionamenti manuali sull'ad set winner 6982220524465, **deselezionare facebook/notification, facebook/reels_overlay, biz_disco_feed, marketplace**. Restringere eta a **35-64** (taglio 65+ a zero lead) e valutare taglio 25-34 (1 lead a 44 EUR).
Impatto stimato: recupero ~24 EUR/mese su posizioni morte + ~64 EUR/mese (25-34 + 65+) reinvestibili sullo sweet spot. A parita di budget = piu lead.
Rischio: minimo, sono segmenti senza conversioni reali. Mantenere genere ampio (no esclusione femmine secca: volume troppo basso per decidere, lasciare che l'algoritmo allochi).

### LEVA 2 - Spostare peso su Instagram (CPL reale 28 vs FB 52)
Azione: NON spegnere FB, ma siccome IG porta 6/9 lead veri a meta del CPL, valutare un **ad set duplicato IG-only** (Reels + Stories + Feed IG) per testare se concentrando la spesa IG il CPL reale scende ulteriormente, lasciando FB su budget ridotto come controllo. In alternativa, dentro l'ad set winner privilegiare le posizioni IG.
Impatto stimato: se il CPL IG (28 EUR) si conferma su volume maggiore, CPL medio campagna da 36 -> ~30 EUR.
Rischio: medio. FB feed comunque genera 3 lead veri, non azzerarlo; testare in parallelo, non sostituire.

### LEVA 3 - Concentrare creativa e budget sui Reels nello sweet spot 35-54 M
Azione: i Reels (FB 20 / IG 22 CPM, CPC FB 1,02) sono il posizionamento piu economico per impression e clic; lo sweet spot demografico 35-54 M ha CPL API 17-24. Allineare: spingere il formato video verticale Reels verso 35-54 M e usare il momentaneo rientro del CPM (09/06 a 20,9) per **non scalare il budget durante i picchi** (es. 07/06 CPM 43) ma alzarlo nei giorni a CPM basso.
Impatto stimato: riduzione CPM medio effettivo e CPL piu stabile; sfrutta la finestra stagionale in discesa invece di subirla.
Rischio: basso. Tutto coerente con cio che gia converte; nessun pubblico nuovo da zero.

---

## Sintesi spreco vs conversione
- **Dove si spreca**: facebook/notification (CPM 104), facebook/reels_overlay (0 clic), eta 65+ (0 lead, 20 EUR), 25-34 M (CPL 44), femmine fasce centrali (0 lead). FB clic economici ma poco qualificati.
- **Dove si converte meglio**: Instagram (CPL reale 28), Reels (CPM 20-22), sweet spot 35-54 maschi (8/13 lead API, CPL 17-24), Stories IG (CTR 2,73%).
