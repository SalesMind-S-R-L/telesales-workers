# Marketing Rextyle — Workspace

Cliente SMM Rextyle (Firenze, affitti brevi). Sistema di content factory hub-and-spoke su 4 profili.

## Struttura

```
rextyle/
├── _contesto/                        # contesti per la skill
│   ├── brand.md                      # chi sono, mission, valori, servizi
│   ├── voce.md                       # tono operativo, 4 pillar, blacklist
│   ├── target.md                     # 3 buyer persona + pain language
│   └── servizi-pacchetti.md          # catalogo servizi e pricing
├── _asset/
│   ├── palette.txt                   # 5 HEX + regole 60-30-10
│   ├── library/                      # halftone PNG riusabili (da generare)
│   └── foto-reali/                   # drip dai soci (cantieri, turnover, prima/dopo)
├── _template/
│   └── guida-stile-caroselli.md      # spec produzione carosello IG
├── scripts/
│   ├── publish_rextyle.py            # publisher Meta Graph API
│   ├── check_batch.py                # self-check 11 criteri
│   ├── refresh_token.py              # rinnovo token Meta
│   ├── .env.template                 # template credenziali (copia in .env)
│   └── .env                          # GIT-IGNORED, credenziali reali
├── output/                           # batch settimanali generati
│   └── 2026-WXX/
│       ├── 01-hub-lun-titolo/
│       │   ├── slide-1.png ... slide-N.png
│       │   ├── caption.md
│       │   ├── hashtag.txt
│       │   └── meta.json
│       └── ...
├── brand_kit_rextyle.md/.pdf         # brand kit polished per i soci
├── posizionamento_competitivo.md     # mappa 8 competitor + statement
├── flusso_pubblicazione.md           # sistema 5-gate operativo
├── richieste_avvio_contenuti.md      # Tier 0/1/2 ai soci
└── onboarding_rextyle.md/.pdf        # playbook incontro fisico (storico)
```

## Setup iniziale

1. **Configurare credenziali Meta**:
   ```bash
   cd scripts/
   cp .env.template .env
   # Riempire RX_META_TOKEN, RX_APP_ID, RX_APP_SECRET, RX_FB_PAGE_ID, RX_IG_*
   ```

2. **Token Meta**:
   - developers.facebook.com → app "Rextyle Marketing"
   - Graph API Explorer → Long-lived token con scopes:
     `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`,
     `instagram_content_publish`, `business_management`

3. **ID account**:
   - Pagina FB: `graph.facebook.com/me/accounts`
   - IG aziendale: `graph.facebook.com/{page_id}?fields=instagram_business_account`
   - IG personali: aggiunti al BM via Pagina, poi `graph.facebook.com/me/accounts`

4. **Library asset iniziale** (una tantum, ~€3-5):
   - Generare ~80 halftone PNG Teal+Oro in `_asset/library/`
   - Da fare con skill Claude Code una sola volta, poi riuso infinito

## Workflow settimanale

| Giorno | Comando | Output |
|---|---|---|
| LUN 09:00 | `/rextyle genera-batch settimana N` | 6 post in `output/2026-WXX/` + preview.html |
| LUN 09:05 | `python scripts/check_batch.py output/2026-WXX/` | `check.md` con OK/ISSUES |
| LUN 12:00 | Review visual + mandi preview su WhatsApp gruppo | 24h tacita |
| MAR 12:00 | `python scripts/publish_rextyle.py output/2026-WXX/ --dry-run` | Simula chiamate API |
| MAR 12:05 | `python scripts/publish_rextyle.py output/2026-WXX/` | Schedula su Meta |
| MER + VEN | `/rextyle brief-storie giorno` | 3 brief WhatsApp per soci |
| VEN 18:00 | `/rextyle insights settimana N` | Report KPI |

## Stato attuale

- [x] Brand kit PDF
- [x] Posizionamento competitivo
- [x] Flusso pubblicazione documentato
- [x] Scaffolding cartelle + contesti
- [x] Skeleton script Python (publish, check, refresh)
- [ ] Token Meta + ID dei 4 profili (azione utente)
- [ ] Library asset iniziale (da generare)
- [ ] Skill Claude Code `rextyle-social-designer` (fork da Telesales)
- [ ] Sprint test 1-5 (10 giorni di validation)
- [ ] Go live

## Cosa NON committare in git

- `scripts/.env` (token Meta)
- `_asset/foto-reali/` (foto clienti, privacy)
- `output/*/` (asset intermedi, peso)
- Token Meta in qualsiasi file

## Vedi anche

- `brand_kit_rextyle.pdf` — da mandare ai soci per approvazione palette + font
- `posizionamento_competitivo.md` — referenza per ogni brief contenuto
- `flusso_pubblicazione.md` — riferimento operativo 5-gate
- Memorie `project_rextyle.md` e `feedback_content_factory_smm.md` — auto-memory persistente
