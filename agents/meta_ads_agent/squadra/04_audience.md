# Strategia Pubblici v4 - Rompere il tetto volume senza perdere qualita

Audience Strategist. Piano pronto da eseguire DOPO il 16/6 (FREEZE attivo: niente di quanto segue va lanciato ora). Tutto in EUR, account `act_40219042`, timezone Europe/Rome, campagna v4 `6982220525065` (OUTCOME_LEADS, AUCTION, special_ad_categories vuoto), pixel `399320589867296`.

## Dati di partenza verificati (oggi)
- Custom audience esistenti sull'account: NESSUNA (`/customaudiences` ritorna `data:[]`). Si parte da zero.
- Ad set winner `6982220524465` (AS_DecisionMakers_B2B_IT_v4): budget 25 EUR/g, OFFSITE_CONVERSIONS/LEAD, dest WEBSITE_AND_LEAD_FORM, 9 citta IT raggio 40km, eta 25-65, Advantage Audience expansion = ON (`targeting_automation.advantage_audience:1`).
- Volume reale: 9 lead CRM, di cui 5 HOT clienti reali. Pool sorgente per Custom/Lookalike e PICCOLO: questo guida tutta la strategia (vedi nota soglie sotto).
- special_ad_categories vuoto: i Lookalike sono PERMESSI (se fosse categoria speciale tipo lavoro/credito sarebbero vietati). Confermato OK.

## Logica della strategia (perche in quest'ordine)
1. La fonte v4 `cos'e telesales` gia funziona ma e tarata a interesse/comportamento + Advantage. Per scalare il VOLUME senza degradare qualita non si allarga quell'ad set (rischio CPM e overlap), si crea una sorgente di qualita e si lascia che l'algoritmo trovi gente SIMILE ai clienti veri.
2. Custom Audience = "chi sono i miei lead buoni". Due fonti: (A) chi ha interagito col Lead Form Meta (zero attriti, parte subito), (B) lista CRM email+telefono dei soli HOT (qualita massima ma volume bassissimo).
3. Lookalike 1% Italia dalla migliore sorgente disponibile. Si parte all'1% (piu simile = piu qualita), si scala a 1-3% solo se l'1% regge il CPL.
4. Audience SEPARATA e MUTUAMENTE ESCLUSA da `cos'e telesales` per non ripetere l'errore Leonardo (overlap = aste interne, CPM gonfiato, money pit). Il nuovo ad set Lookalike ESCLUDE in targeting le stesse interessi/custom usate dal winner e, dove possibile, esclude le Custom Audience sorgente.

### NOTA SOGLIE (vincolo critico, leggere prima di lanciare)
Meta richiede un MINIMO di corrispondenze per generare un Lookalike: servono ~100 match nel paese sorgente, idealmente 1.000-5.000 per qualita. Con 5-9 lead NON si genera un Lookalike dalla lista CRM. Percio:
- La sorgente Lookalike PRIMARIA e la **Custom Audience da Lead Form** (engagement, si riempie da sola col tempo) o meglio ancora la **Custom Audience da Pixel/visitatori sito** se il pixel `399320589867296` ha traffico.
- La lista CRM HOT serve come **seed di qualita futuro** e come **audience di esclusione/retargeting**, non come sorgente Lookalike finche non supera ~100 record.
- Strategia ponte finche il pool non cresce: Lookalike da chi ha aperto/inviato il Lead Form (volume piu alto del CRM).

---

## PUBBLICO 1 - Custom Audiences (le sorgenti di qualita)

### 1A. Custom Audience da Lead Form Meta (engagement) - PARTE SUBITO, zero dipendenze
Chi ha aperto o inviato il modulo lead. Serve il page_id e il form_id; il page_id si ricava dal promoted_object/pagina collegata all'inserzione. Sostituire `<PAGE_ID>` e, se vuoi solo chi ha inviato, `<LEAD_FORM_ID>`.

```bash
export $(grep -E '^FB_' /Users/simocors/Desktop/telesales/.env | xargs)

# (prerequisito) trovare PAGE_ID e i form lead collegati:
curl -sG "https://graph.facebook.com/v21.0/act_40219042/promote_pages" \
  --data-urlencode "access_token=$FB_ACCESS_TOKEN" --data-urlencode "fields=id,name"
# poi i form della pagina:
# curl -sG "https://graph.facebook.com/v21.0/<PAGE_ID>/leadgen_forms" \
#   --data-urlencode "access_token=$FB_ACCESS_TOKEN" --data-urlencode "fields=id,name,status"

# Custom Audience: chi ha INTERAGITO col modulo lead negli ultimi 90gg
curl -s -X POST "https://graph.facebook.com/v21.0/act_40219042/customaudiences" \
  -d "access_token=$FB_ACCESS_TOKEN" \
  -d "name=CA_LeadForm_Engagers_90d_v4" \
  -d "subtype=ENGAGEMENT" \
  -d 'rule={"inclusions":{"operator":"or","rules":[{"event_sources":[{"type":"page","id":"<PAGE_ID>"}],"retention_seconds":7776000,"filter":{"operator":"and","filters":[{"field":"event","operator":"eq","value":"lead_form_open"}]}},{"event_sources":[{"type":"page","id":"<PAGE_ID>"}],"retention_seconds":7776000,"filter":{"operator":"and","filters":[{"field":"event","operator":"eq","value":"lead_form_submit"}]}}]}}' \
  -d "description=Aperture e invii modulo lead, finestra 90 giorni, sorgente per Lookalike"
```
Valutazione: dopo 7-14gg controllare `approximate_count_lower_bound`. Se supera ~100 e ideale come seed Lookalike. Buona perche cattura intento reale anche di chi non ha completato.

### 1B. Custom Audience da Pixel (visitatori sito) - se il pixel ha traffico
Cattura tutti i visitatori del sito negli ultimi 180gg: bacino piu ampio del CRM, ottimo seed Lookalike.

```bash
curl -s -X POST "https://graph.facebook.com/v21.0/act_40219042/customaudiences" \
  -d "access_token=$FB_ACCESS_TOKEN" \
  -d "name=CA_SiteVisitors_180d_v4" \
  -d "subtype=WEBSITE" \
  -d "pixel_id=399320589867296" \
  -d 'rule={"inclusions":{"operator":"or","rules":[{"event_sources":[{"type":"pixel","id":"399320589867296"}],"retention_seconds":15552000,"filter":{"operator":"and","filters":[{"field":"url","operator":"i_contains","value":"telesales"}]}}]}}' \
  -d "description=Visitatori sito 180gg da pixel, sorgente Lookalike e retargeting"
```
Valutazione: verificare `approximate_count_lower_bound` >100 prima di usarla come seed. Se il pixel ha poco traffico, ripiegare su 1A.

### 1C. Custom Audience da lista CRM (HOT) - seed di qualita massima, volume basso
Caricamento lista hash. ATTENZIONE: oggi sono 5-9 record, SOTTO la soglia Lookalike (~100). Crearla ora SOLO come (a) audience di esclusione per non ri-spammare chi gia e cliente/in chiusura, (b) seed che crescera. NON aspettarsi un Lookalike utilizzabile finche non supera ~100.

Passo 1 - crea il contenitore:
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/act_40219042/customaudiences" \
  -d "access_token=$FB_ACCESS_TOKEN" \
  -d "name=CA_CRM_HOT_clienti_v4" \
  -d "subtype=CUSTOM" \
  -d "customer_file_source=USER_PROVIDED_ONLY" \
  -d "description=Lead HOT validati da CRM v4, esclusione e futuro seed Lookalike"
# ritorna {"id":"<CA_ID>"}
```
Passo 2 - carica i record con email (EMAIL) e telefono (PHONE) HASHATI SHA-256. Gli identificatori vanno normalizzati (lowercase, trim; telefono in E.164 senza +, es. 393331234567) e poi hashati. Usare uno script lato locale; di seguito lo schema della chiamata (NON inviare dati in chiaro):
```bash
# schema_addusers (gli hash vanno calcolati prima, NON usare valori in chiaro)
curl -s -X POST "https://graph.facebook.com/v21.0/<CA_ID>/users" \
  -d "access_token=$FB_ACCESS_TOKEN" \
  -d 'payload={"schema":["EMAIL","PHONE"],"data":[["<sha256_email_1>","<sha256_phone_1>"],["<sha256_email_2>","<sha256_phone_2>"]]}'
```
Snippet generazione hash (locale, da lista CRM):
```python
# python: normalizza+hash, non carica nulla in chiaro
import hashlib
def h(x): return hashlib.sha256(x.strip().lower().encode()).hexdigest()
# email -> h(email); telefono -> h("39"+numero_senza_zero_iniziale_e_senza_+)
```
Valutazione: utile da subito SOLO come esclusione. Diventa seed Lookalike quando i record HOT superano ~100 (accumulare nel CRM nel tempo).

---

## PUBBLICO 2 - Lookalike 1% Italia (poi 1-3%)

Genera un Lookalike dalla migliore sorgente sopra la soglia. Ordine di preferenza per `origin_audience_id`: 1B SiteVisitors > 1A LeadForm engagers > (futuro) 1C CRM HOT quando >100. Sostituire `<SEED_CA_ID>`.

### 2A. Lookalike 1% (massima somiglianza, parti da qui)
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/act_40219042/customaudiences" \
  -d "access_token=$FB_ACCESS_TOKEN" \
  -d "name=LAL_IT_1pct_v4" \
  -d "subtype=LOOKALIKE" \
  -d "origin_audience_id=<SEED_CA_ID>" \
  -d 'lookalike_spec={"type":"similarity","country":"IT","ratio":0.01}' \
  -d "description=Lookalike 1% Italia da sorgente di qualita, ad set separato"
```

### 2B. Lookalike 1-3% (scala SOLO dopo conferma CPL su 1%)
Crea un secondo Lookalike a banda 1-3% (esclude lo 0-1% gia coperto da 2A per non sovrapporsi):
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/act_40219042/customaudiences" \
  -d "access_token=$FB_ACCESS_TOKEN" \
  -d "name=LAL_IT_1_3pct_v4" \
  -d "subtype=LOOKALIKE" \
  -d "origin_audience_id=<SEED_CA_ID>" \
  -d 'lookalike_spec={"type":"similarity","country":"IT","ratio":0.03,"starting_ratio":0.01}' \
  -d "description=Lookalike 1-3% Italia, espansione volume dopo validazione 1pct"
```
Valutazione Lookalike: lo stato `operation_status` deve diventare pronto (popolamento ~6-24h) prima dell'uso in un ad set.

---

## PUBBLICO 3 - Ad set Lookalike SEPARATO e anti-overlap (lezione Leonardo)

Nuovo ad set DENTRO la campagna v4 `6982220525065`, stessa ottimizzazione del winner (OFFSITE_CONVERSIONS/LEAD, pixel `399320589867296`, dest WEBSITE_AND_LEAD_FORM), MA:
- usa SOLO il Lookalike `<LAL_1pct_ID>` come `custom_audiences`;
- ESCLUDE le Custom sorgente (CRM HOT, LeadForm engagers, SiteVisitors) per non ricomprare chi e gia lead/cliente;
- niente interessi sovrapposti al winner;
- geo e eta allineati alla diagnosi performance: 9 citta winner, eta ristretta 35-64 (taglia 25-34 peggiore tra i maschi e 65+ a 0 lead), pubblico chiave maschi 35-54 lasciato all'algoritmo;
- Advantage Audience expansion OFF su questo ad set (`advantage_audience:0`): il Lookalike e gia la nostra espansione controllata, non vogliamo che Meta lo allarghi e ricrei overlap col winner.

```bash
# eta 35-64, 9 citta winner, SOLO LAL 1%, esclusione Custom sorgente
curl -s -X POST "https://graph.facebook.com/v21.0/act_40219042/adsets" \
  -d "access_token=$FB_ACCESS_TOKEN" \
  -d "name=AS_LAL_IT_1pct_v4" \
  -d "campaign_id=6982220525065" \
  -d "daily_budget=1500" \
  -d "billing_event=IMPRESSIONS" \
  -d "optimization_goal=OFFSITE_CONVERSIONS" \
  -d "destination_type=WEBSITE_AND_LEAD_FORM" \
  -d 'promoted_object={"pixel_id":"399320589867296","custom_event_type":"LEAD"}' \
  -d 'targeting={
        "age_min":35,
        "age_max":64,
        "geo_locations":{"cities":[
          {"key":"1174824","radius":40,"distance_unit":"kilometer"},
          {"key":"1175277","radius":40,"distance_unit":"kilometer"},
          {"key":"1175693","radius":40,"distance_unit":"kilometer"},
          {"key":"1180847","radius":40,"distance_unit":"kilometer"},
          {"key":"1184376","radius":40,"distance_unit":"kilometer"},
          {"key":"1186051","radius":40,"distance_unit":"kilometer"},
          {"key":"1188733","radius":40,"distance_unit":"kilometer"},
          {"key":"1192826","radius":40,"distance_unit":"kilometer"},
          {"key":"1193343","radius":40,"distance_unit":"kilometer"}
        ],"location_types":["home","recent"]},
        "custom_audiences":[{"id":"<LAL_1pct_ID>"}],
        "excluded_custom_audiences":[
          {"id":"<CA_CRM_HOT_ID>"},
          {"id":"<CA_LeadForm_Engagers_ID>"},
          {"id":"<CA_SiteVisitors_ID>"}
        ],
        "targeting_automation":{"advantage_audience":0}
      }' \
  -d "status=PAUSED"
```
Nota: creare PAUSED, allegare almeno 1 inserzione (riusare la creative vincente di `cos'e telesales`), poi attivare manualmente. Budget iniziale 15 EUR/g (sotto i 25 del winner: e un test, non un raddoppio di spesa). Il winner resta intatto a 25 EUR/g.

### Verifica overlap PRIMA di attivare (evita Leonardo)
```bash
# stima sovrapposizione tra il pubblico LAL e quello del winner
curl -sG "https://graph.facebook.com/v21.0/act_40219042/reachestimate" \
  --data-urlencode "access_token=$FB_ACCESS_TOKEN" \
  --data-urlencode 'targeting_spec={"geo_locations":{"countries":["IT"]},"custom_audiences":[{"id":"<LAL_1pct_ID>"}]}'
# se l overlap funzionale e alto, restringere eta o escludere anche il pubblico interessi del winner
```

---

## Budget e sequenza di lancio (post 16/6)
| Step | Quando | Azione | Budget |
|------|--------|--------|--------|
| 1 | giorno 0 | Crea CA 1A LeadForm + 1B SiteVisitors + 1C CRM (solo esclusione) | 0 (asset) |
| 2 | giorno 0-1 | Verifica `approximate_count_lower_bound` della miglior sorgente >100 | 0 |
| 3 | quando seed >100 | Crea LAL 1% (2A) | 0 (asset) |
| 4 | LAL pronto (~24h) | Crea ad set 3 PAUSED + allega creative winner | 15 EUR/g |
| 5 | dopo verifica overlap | Attiva ad set LAL 1% | 15 EUR/g |
| 6 | dopo 7-10gg se CPL<=35 EUR | Crea LAL 1-3% (2B) e/o alza ad set a 20-25 EUR/g | +5-10 EUR/g |

Il winner `cos'e telesales` NON si tocca: resta a 25 EUR/g come fonte certa. Spesa incrementale del test = 15 EUR/g, non un raddoppio.

## Criteri di valutazione (decisione a 7-10gg, fonte lead = CRM, mai API)
- VINCE e si scala (vai a 2B / alza budget): CPL <= 35 EUR (sotto la media campagna ~36-40) e qualita lead pari ai HOT (P.IVA valida, fatturato >50k, decisore, non concorrente). Il filtro form anti-telemarketing della Lead Quality Audit deve essere gia attivo per non contare i lead-partner.
- TIENI in osservazione: CPL 35-45 EUR ma qualita alta -> non scalare, raccogliere piu volume.
- SPEGNI: CPL > 45 EUR a frequenza <1.3 (cioe inefficienza non da saturazione) oppure qualita scadente (>30% concorrenti/agenzie come nel pool attuale).
- Anti-overlap continuo: monitorare la frequenza del winner dopo l'attivazione; se sale oltre 1.5 senza spiegazioni, c'e cannibalizzazione -> rivedere esclusioni.
- KPI guida: lead CRM validi come clienti (non lead_grouped API), CPL reale per ad set, % concorrenti sul totale.

## Errori da non ripetere
- Leonardo era un money pit per overlap/audience troppo larga: qui ogni nuovo ad set ESCLUDE le sorgenti e ha Advantage OFF.
- Non usare la lista CRM da 5-9 record come seed Lookalike: sotto soglia, qualita del LAL casuale. Usare engagement/pixel finche il CRM non cresce.
- Conteggio lead SEMPRE da CRM. I lead_grouped API servono solo per ranking relativo.
- Non lanciare nulla prima del 16/6 (freeze). Questo file e solo esecuzione pronta.
