# SOP — Post-call webhook ElevenLabs → Google Sheets

## Obiettivo
Far sì che ogni volta che una conversazione su ElevenLabs termina, automaticamente:
- viene scritta su Google Sheets la riga corrispondente (esito, note, email, transcript link)
- volendo, viene mandata un'email recap (es. per chiamate positive)

## Flusso

```
[ElevenLabs conv termina]
        │
        ▼
post_call_webhook fires (workspace o agent-level)
        │
        ▼
POST <Apps Script web app URL>/exec    body = full conv JSON
        │
        ▼
Apps Script doPost(e)
        │
   match riga (row_index dynamic var O nome_azienda)
        │
   deduce esito da analysis.data_collection_results + transcript
        │
   scrive F (presente), H (data_app se appt), I (esito), J (note), K (email), L (link)
        │
        ▼
[Foglio Google aggiornato in tempo reale]
```

## Setup step-by-step

### 1. Crea Apps Script container-bound al foglio interno
- Apri foglio interno → Estensioni → Apps Script
- Incolla codice (vedi `context/08_apps_script_bridge.md` per template)
- Salva

### 2. Autorizza scope (una tantum)
- Da editor: Esegui `authorizeAll()` (funzione da implementare con dummy chiamate a Sheet/UrlFetch/Mail)
- Accetta scope: spreadsheets, script.external_request, script.send_mail

### 3. Deploy come web app
- Deploy → New deployment
- Type: Web app
- Execute as: **Me**
- Who has access: **Anyone**
- Copia URL `/exec`

### 4. Registra webhook su ElevenLabs

Via API:
```python
import requests
H = {"xi-api-key": API_KEY, "content-type":"application/json"}
body = {
  "name": "<Cliente> — Post Call to Sheet",
  "webhook_url": "<URL Apps Script /exec>",
  "auth_type": "hmac",  # o "none" per test
  "events": ["transcript"],
  "transcript_format": "json",
  "send_audio": False,
  "retry_enabled": False
}
r = requests.post("https://api.elevenlabs.io/v1/workspace/webhooks",
                  headers=H, json=body, timeout=30)
webhook_id = r.json()["webhook_id"]
```

### 5. Collega webhook all'agente

```python
body = {
  "platform_settings": {
    "workspace_overrides": {
      "webhooks": {
        "post_call_webhook_id": "<webhook_id>",
        "events": ["transcript"],
        "transcript_format": "json",
        "send_audio": False
      }
    }
  }
}
requests.patch(f"https://api.elevenlabs.io/v1/convai/agents/{AGENT_ID}",
               headers=H, json=body, timeout=30)
```

### 6. Test
Fai 1 chiamata di test → verifica:
- Su ElevenLabs UI la conv appare in Cronologia
- Su Apps Script editor → Esecuzioni: deve apparire doPost con status SUCCESS
- Sul foglio: la riga corrispondente è popolata

## Match riga foglio (ordine di priorità)

1. **`dynamic_variables.row_index`** — preferenziale (1-based). Va popolato nel payload outbound:
   ```python
   "conversation_initiation_client_data": {
     "dynamic_variables": {"row_index": "12", ...}
   }
   ```

2. **`dynamic_variables.nome_azienda`** — fallback. Match esatto (trim) sulla colonna A del foglio:
   ```js
   var col = sh.getRange(2, COL.NOME_AZIENDA, last-1, 1).getValues();
   for (var i=0; i<col.length; i++) {
     if (String(col[i][0]).trim() === String(dyn.nome_azienda).trim()) {
       rowIdx = i + 2; break;
     }
   }
   ```

3. **Telefono** (`metadata.phone_call.external_number`) — fallback ultimo:
   ```js
   var phoneCol = sh.getRange(2, COL.TELEFONO, last-1, 1).getValues();
   for (...) { if (normPhone === extPhone) { ... } }
   ```

## Deduce esito dal payload webhook

L'agente in `analysis.data_collection_results` può esporre campi strutturati. Per HoReCa Culligan:
- `appuntamento_preso` (bool)
- `data_appuntamento` (es. "martedì 13:00")
- `email_contatto`
- `telefono_diretto`
- `nome_contatto`
- `ruolo_contatto`
- `note_chiamata` (riassunto stile setter)
- `categoria`

Mai fidarsi cieco di `appuntamento_preso=True` — verifica con transcript (vedi `sop_post_batch_analysis.md`).

## Email recap (opzionale)

Pattern: alla fine di doPost, se `esito ∈ {Appuntamento, Email}`:
```js
MailApp.sendEmail({
  to: 'admin@telesales.it,lead@email.com',
  subject: 'AI Voice — Nuovo appuntamento ' + nome_azienda,
  body: 'Sebastiano passa il ' + data_app + ' a ' + indirizzo + '...'
});
```

NB: limite gratis 100 email/giorno per scope `script.send_mail`.

## Idempotenza

Lo stesso webhook può essere chiamato 2 volte (retry ElevenLabs). Per non duplicare scritture:
- Salva il `conv_id` come chiave in PropertiesService
- All'ingresso di doPost, controlla se già processato → return 200 senza scrivere

```js
var seen = PropertiesService.getScriptProperties().getProperty('CONV_'+convId);
if (seen) return ContentService.createTextOutput('dup');
PropertiesService.getScriptProperties().setProperty('CONV_'+convId, '1');
```

## Troubleshooting

| Sintomo | Causa probabile | Fix |
|---|---|---|
| doPost mai chiamato | Webhook URL sbagliato o agent non override | Verifica deploy URL + agent webhook_id |
| doPost 504 | Apps Script lento (>30s) | Aggiungi early return 200, scrivi async |
| Match riga sbagliato | `row_index` non passato + nomi simili | Forza `row_index` nel payload outbound |
| Caratteri italiani corrotti | Encoding pbcopy → Monaco editor | Usa regex ASCII-safe nel codice gs |
| Webhook signature fallisce | HMAC config sbagliato | Inizia con `auth_type: none`, alza poi |
