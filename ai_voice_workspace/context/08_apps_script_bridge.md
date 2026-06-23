# Apps Script Bridge — Pattern per post-call → Google Sheets

## Cos'è
Un Google Apps Script container-bound a un foglio Google che:
1. Espone `doPost(e)` come web app pubblica per ricevere il webhook post-call ElevenLabs
2. Aggiorna le righe del foglio interno con esito/note/email/transcript_link
3. Espone un menu custom sul foglio per lanciare batch/sincronizzare

Esempio funzionante: `/Users/simocors/Desktop/telesales/demo_mik/apps_script_culligan.gs` (27 KB).

## Struttura tipica

```js
var SHEET_ID = '1PiezlYSd5...';
var SHEET_NAME = 'aziende_bolzano_VERIFICATE';
var AGENT_ID = 'agent_5101kreejrz1e98rfzjrf3brhd50';
var PHONE_ID = 'phnum_1501kr3sx76sfxeap503jqy1m7j9';
var ELEVEN_BASE = 'https://api.elevenlabs.io';

var COL = {
  NOME_AZIENDA: 1, NOME_TITOLARE: 2, NOTE_FONTE: 3,
  INDIRIZZO: 4, TELEFONO: 5, PRESENTE: 6,
  DATA_CHIAMATA: 7, DATA_APPUNTAMENTO: 8,
  ESITO: 9, NOTE_AI: 10, EMAIL_RACCOLTA: 11, TRANSCRIPT_LINK: 12
};

function onOpen() {
  SpreadsheetApp.getUi().createMenu('☎ Marco AI <Cliente>')
    .addItem('Setup foglio (colonne+dropdown)', 'setupSheet')
    .addItem('Lancia chiamata su riga selezionata', 'callSelectedRow')
    .addItem('▶ AVVIA Batch 30 sequenziali', 'startBatch30Sequential')
    .addItem('■ FERMA Batch in corso', 'stopBatch')
    .addItem('Autorizza scope (una tantum)', 'authorizeAll')
    .addToUi();
}

function doPost(e) {
  var d = JSON.parse(e.postData.contents);
  var convId = (d.metadata||{}).conversation_id || d.conversation_id;
  var dyn = (d.conversation_initiation_client_data||{}).dynamic_variables || {};
  var rowIdx = parseInt(dyn.row_index || '0', 10);
  // fallback match per nome_azienda
  if (!rowIdx) {
    var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    var col = sh.getRange(2, COL.NOME_AZIENDA, sh.getLastRow()-1, 1).getValues();
    for (var i=0; i<col.length; i++) {
      if (String(col[i][0]).trim() === String(dyn.nome_azienda||'').trim()) {
        rowIdx = i + 2; break;
      }
    }
  }
  if (!rowIdx) return;
  // Deduce esito + nota + scrivi colonne F-L
  // ... (vedi file completo)
  return ContentService.createTextOutput('ok');
}
```

## Deploy come web app

1. Editor Apps Script → **Deploy** → **New deployment**
2. Type: **Web app**
3. Execute as: **Me**
4. Who has access: **Anyone**
5. Copia l'URL `/exec`
6. Su ElevenLabs: aggiungi un workspace webhook con `webhook_url = <URL/exec>`, `auth_type = hmac` (o none per test)
7. Sull'agente, in `platform_settings.workspace_overrides.webhooks.post_call_webhook_id` metti l'ID webhook

## OAuth scopes necessari

Quando autorizzi la prima volta:
- `script.external_request` — per UrlFetchApp (chiamare ElevenLabs)
- `spreadsheets` — per leggere/scrivere foglio
- `script.send_mail` — per mandare email recap (opzionale)
- `script.scriptapp` — per gestire trigger

## Sequential batch con time-based triggers (oltre i 6 min)

Apps Script ha limite 6 minuti per esecuzione. Per batch sequenziali >>6 min usa pattern:

```js
function startBatch30Sequential() {
  var queue = [...]; // 30 row indexes
  PropertiesService.getScriptProperties()
    .setProperties({BATCH_QUEUE: JSON.stringify(queue), BATCH_INDEX: '0'});
  processBatchStep_();
}

function processBatchStep_() {
  var ps = PropertiesService.getScriptProperties();
  var queue = JSON.parse(ps.getProperty('BATCH_QUEUE') || '[]');
  var idx = parseInt(ps.getProperty('BATCH_INDEX') || '0', 10);
  if (idx >= queue.length) { stopBatch(); return; }
  triggerCallFromRow_(queue[idx]);
  ps.setProperty('BATCH_INDEX', String(idx+1));
  cleanupBatchTriggers_();
  ScriptApp.newTrigger('processBatchStep_')
    .timeBased().after(90*1000).create();   // 90s pausa tra chiamate
}

function stopBatch() {
  cleanupBatchTriggers_();
  PropertiesService.getScriptProperties().deleteAllProperties();
}

function cleanupBatchTriggers_() {
  ScriptApp.getProjectTriggers().forEach(function(t){
    if (t.getHandlerFunction() === 'processBatchStep_')
      ScriptApp.deleteTrigger(t);
  });
}
```

**Alternativa migliore**: usa `target_concurrency_limit=1` sul batch ElevenLabs e lascia che ElevenLabs gestisca il throttle (più affidabile). Vedi `sop_batch_sequential.md`.

## Pattern multi-cliente

Un Apps Script per cliente (container-bound al suo foglio interno). Ognuno con:
- `SHEET_ID`, `SHARED_SHEET_ID` (foglio cliente)
- Menu custom
- Deploy URL unico
- Webhook ElevenLabs dedicato

NON condividere lo stesso bridge tra clienti — separa per evitare conflitti.

## Gotchas

- **Encoding caratteri italiani** — alcuni `ì`/`è` si corrompono via pbcopy+Cmd+V in editor → preferire upload via API `script.googleapis.com` o usare regex ASCII-safe (`luned[iì]` → `lunedi`)
- **doPost non vede gli aggiornamenti recenti** del prompt agente se lo deploy è vecchio → ridploya dopo modifiche al codice
- **Trigger time-based** consumano quota → max 20 trigger contemporanei
- **PropertiesService** non è atomico tra esecuzioni — meglio una sola scrittura per step
