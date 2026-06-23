/**
 * Marco Culligan — Bridge foglio "culligan claude bolzano"
 * - Menu Sheets per lanciare chiamate SIP outbound batch
 * - Post-call webhook ElevenLabs → scrive risultati per riga
 *
 * Setup:
 *   1) Estensioni → Apps Script (questo file) dal foglio Culligan.
 *   2) Impostazioni progetto → Proprietà script: ELEVENLABS_API_KEY = sk_...
 *   3) Esegui setupSheet() una volta.
 *   4) Esegui authorizeAll() una volta per accettare gli scope.
 *   5) Implementa → Nuova implementazione → App web, esegui come "me", accesso "Chiunque".
 *   6) URL del deploy → impostalo nel webhook post-call dell'agente Culligan.
 */

var SHEET_ID    = '1PiezlYSd5TZNBCRTvzBhx_yVCGfN6aMI3PXdOYU4xu8';
var SHEET_NAME  = 'aziende_bolzano_VERIFICATE';

// Foglio condiviso con Sebastiano (vista cliente — non sa che e' AI)
var SHARED_SHEET_ID   = '1KsbFkAhJQDd2edYuKgbVC0yd87jK-Y6egKU254Y1wT0';
var SHARED_SHEET_NAME = 'Foglio1';
// Colonne foglio condiviso (1-based)
var SHARED_COL = {
  NOME_AZIENDA: 1,           // A (header vuoto)
  NOME_TITOLARE: 2,          // B
  NOTE_BREVE: 3,             // C — esito stile umano (ok/non risp/richiamare/email)
  INDIRIZZO: 4,              // D
  TELEFONO: 5,               // E
  PRESENTE: 6,               // F — Sì/No
  DATA_CHIAMATA_1: 7,        // G — 1° giro
  DATA_APP_1: 8,             // H — 1° giro
  DATA_CHIAMATA_2: 9,        // I — richiamo
  NOTE_2: 10,                // J — richiamo
  DATA_APP_2: 11             // K — richiamo
};
var AGENT_ID    = 'agent_5101kreejrz1e98rfzjrf3brhd50';   // Marco Culligan Bolzano HoReCa
var PHONE_ID    = 'phnum_1501kr3sx76sfxeap503jqy1m7j9';   // +390554652406 Telnyx
var ELEVEN_BASE = 'https://api.elevenlabs.io';

// Colonne (1-based)
var COL = {
  NOME_AZIENDA: 1,    // A
  NOME_TITOLARE: 2,   // B
  NOTE_FONTE: 3,      // C (con [Hotel/Bar/Ristorante] + email + sito)
  INDIRIZZO: 4,       // D
  TELEFONO: 5,        // E
  PRESENTE: 6,        // F (Sì/No)
  DATA_CHIAMATA: 7,   // G
  DATA_APPUNTAMENTO: 8, // H
  ESITO: 9,           // I — nuova (dropdown)
  NOTE_AI: 10,        // J — nuova
  EMAIL_RACCOLTA: 11, // K — nuova
  TRANSCRIPT_LINK: 12 // L — nuova
};

var ESITI = [
  'Appuntamento', 'Email', 'Da richiamare', 'Non interessato',
  'Non risposto', 'Segreteria', 'IVR/Centralino', 'Numero errato'
];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('☎ Marco AI Culligan')
    .addItem('Setup foglio (colonne+dropdown)', 'setupSheet')
    .addSeparator()
    .addItem('Lancia chiamata su riga selezionata', 'callSelectedRow')
    .addItem('Lancia chiamate su righe SELEZIONATE', 'callSelectedRows')
    .addSeparator()
    .addItem('Lancia chiamate su TUTTE le pending', 'callAllPending')
    .addItem('★ Lancia su pending NON presenti in foglio Sebastiano', 'callPendingNotInSebastiano')
    .addSeparator()
    .addItem('▶ AVVIA Batch 30 sequenziali (90s ognuno, ~45min)', 'startBatch30Sequential')
    .addItem('■ FERMA Batch in corso', 'stopBatch')
    .addSeparator()
    .addItem('► Trasferisci selezionate al foglio Sebastiano', 'syncSelectedToSebastiano')
    .addItem('► Trasferisci TUTTE le chiamate fatte al foglio Sebastiano', 'syncAllDoneToSebastiano')
    .addSeparator()
    .addItem('Autorizza scope (una tantum)', 'authorizeAll')
    .addToUi();
}

function authorizeAll() {
  // Esegui una volta dall'editor per concedere scope:
  // - Spreadsheets, UrlFetchApp, Mail
  SpreadsheetApp.openById(SHEET_ID).getName();
  UrlFetchApp.fetch(ELEVEN_BASE + '/v1/convai/agents/' + AGENT_ID, {
    headers: { 'xi-api-key': getApiKey_() || 'x' },
    muteHttpExceptions: true
  });
  Logger.log('Authorized');
}

function setupSheet() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) throw new Error('Foglio "' + SHEET_NAME + '" non trovato');

  // Assicura intestazioni I/J/K/L
  var headers = [['ESITO', 'NOTE AI', 'EMAIL RACCOLTA', 'TRANSCRIPT LINK']];
  sh.getRange(1, COL.ESITO, 1, 4).setValues(headers)
    .setFontWeight('bold').setBackground('#1f1f1f').setFontColor('#ffffff').setHorizontalAlignment('center');

  // Larghezze
  sh.setColumnWidth(COL.ESITO, 130);
  sh.setColumnWidth(COL.NOTE_AI, 360);
  sh.setColumnWidth(COL.EMAIL_RACCOLTA, 220);
  sh.setColumnWidth(COL.TRANSCRIPT_LINK, 260);

  // Dropdown su ESITO (I)
  var esitoRange = sh.getRange(2, COL.ESITO, Math.max(sh.getMaxRows()-1, 1000), 1);
  esitoRange.setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(ESITI, true).setAllowInvalid(false).build()
  );

  // Freeze prima riga
  sh.setFrozenRows(1);

  SpreadsheetApp.flush();
  SpreadsheetApp.getActiveSpreadsheet().toast('Foglio configurato: I=Esito, J=Note AI, K=Email, L=Transcript');
}

// ===================== LANCIO CHIAMATE =====================

function callSelectedRow() {
  var sh = SpreadsheetApp.getActiveSheet();
  var row = sh.getActiveRange().getRow();
  if (row < 2) { SpreadsheetApp.getUi().alert('Seleziona una riga lead (non l\'intestazione)'); return; }
  var res = triggerCallFromRow_(row);
  SpreadsheetApp.getActiveSpreadsheet().toast('Riga ' + row + ' → ' + (res.ok ? 'OK' : 'FAIL: ' + res.msg));
}

function callSelectedRows() {
  var sh = SpreadsheetApp.getActiveSheet();
  var ranges = sh.getActiveRangeList() ? sh.getActiveRangeList().getRanges() : [sh.getActiveRange()];
  var rows = [];
  ranges.forEach(function(r) {
    var start = r.getRow(); var end = start + r.getNumRows() - 1;
    for (var i = start; i <= end; i++) if (i >= 2) rows.push(i);
  });
  rows = rows.filter(function(v,i,a){return a.indexOf(v)===i});
  var ok = 0, fail = 0;
  rows.forEach(function(r){
    var res = triggerCallFromRow_(r);
    if (res.ok) ok++; else fail++;
    Utilities.sleep(800);  // throttle per rispettare rate limit ElevenLabs/Telnyx
  });
  SpreadsheetApp.getActiveSpreadsheet().toast('Selezione: ok=' + ok + ' fail=' + fail);
}

// Batch sequenziale 30 chiamate, una per volta con 90s di gap (anti-overlap)
// Usa time-based triggers per superare il limite 6 min di Apps Script.
function startBatch30Sequential() {
  var ui = SpreadsheetApp.getUi();
  var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  var ssh = SpreadsheetApp.openById(SHARED_SHEET_ID).getSheetByName(SHARED_SHEET_NAME);
  var seb = ssh.getRange(2, SHARED_COL.NOME_AZIENDA, ssh.getLastRow()-1, 1).getValues();
  var sebSet = {};
  seb.forEach(function(r){ var k=normalizeName_(r[0]); if (k) sebSet[k]=true; });

  var last = sh.getLastRow();
  var data = sh.getRange(2, 1, last-1, 12).getValues();
  var queue = [];
  for (var i = 0; i < data.length && queue.length < 30; i++) {
    var rowIdx = i + 2;
    var nome = String(data[i][COL.NOME_AZIENDA-1] || '').trim();
    var tel  = String(data[i][COL.TELEFONO-1] || '').trim();
    var dataCall = data[i][COL.DATA_CHIAMATA-1];
    if (!nome || !tel || dataCall) continue;
    if (sebSet[normalizeName_(nome)]) continue;
    queue.push(rowIdx);
  }
  if (!queue.length) { ui.alert('Nessuna riga candidata per il batch 30'); return; }

  var resp = ui.alert('Batch sequenziale 30 chiamate',
    'Verranno chiamate ' + queue.length + ' aziende, UNA PER VOLTA con 90 secondi tra una e l\\'altra (durata totale ~45 min).\\n\\nProcedere?',
    ui.ButtonSet.YES_NO);
  if (resp !== ui.Button.YES) return;

  cleanupBatchTriggers_();
  var ps = PropertiesService.getScriptProperties();
  ps.setProperty('BATCH_QUEUE', JSON.stringify(queue));
  ps.setProperty('BATCH_INDEX', '0');
  ps.setProperty('BATCH_TOTAL', String(queue.length));
  ps.setProperty('BATCH_OK', '0');
  ps.setProperty('BATCH_FAIL', '0');

  // Prima chiamata SUBITO
  processBatchStep_();
  SpreadsheetApp.getActiveSpreadsheet().toast('Batch avviato: ' + queue.length + ' chiamate ogni 90s', 'In corso', 10);
}

function processBatchStep_() {
  var ps = PropertiesService.getScriptProperties();
  var queue = JSON.parse(ps.getProperty('BATCH_QUEUE') || '[]');
  var idx = parseInt(ps.getProperty('BATCH_INDEX') || '0', 10);

  if (idx >= queue.length) {
    var ok = ps.getProperty('BATCH_OK') || '0';
    var fail = ps.getProperty('BATCH_FAIL') || '0';
    cleanupBatchTriggers_();
    try { SpreadsheetApp.getActiveSpreadsheet().toast('Batch FINITO: ok=' + ok + ' fail=' + fail, 'Done', 30); } catch (e) {}
    return;
  }

  var rowIdx = queue[idx];
  var res = triggerCallFromRow_(rowIdx);
  if (res.ok) ps.setProperty('BATCH_OK', String((parseInt(ps.getProperty('BATCH_OK')||'0',10))+1));
  else        ps.setProperty('BATCH_FAIL', String((parseInt(ps.getProperty('BATCH_FAIL')||'0',10))+1));

  ps.setProperty('BATCH_INDEX', String(idx + 1));

  // Schedula prossimo step fra 90s
  cleanupBatchTriggers_();
  ScriptApp.newTrigger('processBatchStep_').timeBased().after(90 * 1000).create();
}

function stopBatch() {
  cleanupBatchTriggers_();
  PropertiesService.getScriptProperties().deleteProperty('BATCH_QUEUE');
  PropertiesService.getScriptProperties().deleteProperty('BATCH_INDEX');
  SpreadsheetApp.getActiveSpreadsheet().toast('Batch FERMATO', 'Stop', 8);
}

function cleanupBatchTriggers_() {
  ScriptApp.getProjectTriggers().forEach(function(t){
    if (t.getHandlerFunction() === 'processBatchStep_') ScriptApp.deleteTrigger(t);
  });
}

function callPendingNotInSebastiano() {
  // Lancia chiamate sulle righe del foglio interno che NON sono presenti
  // nel foglio condiviso con Sebastiano (match per nome azienda normalizzato).
  var ui = SpreadsheetApp.getUi();
  var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  var ssh = SpreadsheetApp.openById(SHARED_SHEET_ID).getSheetByName(SHARED_SHEET_NAME);
  if (!sh || !ssh) { ui.alert('Foglio non trovato'); return; }

  // Set delle aziende gia su Sebastiano (normalizzate)
  var seb = ssh.getRange(2, SHARED_COL.NOME_AZIENDA, ssh.getLastRow()-1, 1).getValues();
  var sebSet = {};
  seb.forEach(function(r){ var k=normalizeName_(r[0]); if (k) sebSet[k]=true; });

  // Lista candidati: interno con telefono + senza DATA_CHIAMATA + NOT in sebSet
  var last = sh.getLastRow();
  if (last < 2) return;
  var data = sh.getRange(2, 1, last-1, 12).getValues();
  var candidates = [];
  for (var i = 0; i < data.length; i++) {
    var rowIdx = i + 2;
    var nome = String(data[i][COL.NOME_AZIENDA-1] || '').trim();
    var tel  = String(data[i][COL.TELEFONO-1] || '').trim();
    var dataCall = data[i][COL.DATA_CHIAMATA-1];
    if (!nome || !tel) continue;
    if (dataCall) continue;
    if (sebSet[normalizeName_(nome)]) continue;
    candidates.push(rowIdx);
  }

  if (!candidates.length) { ui.alert('Nessuna azienda da chiamare (tutte sono gia su Sebastiano o gia chiamate)'); return; }

  var resp = ui.alert('Lancio chiamate batch NOT-in-Sebastiano',
    'Trovate ' + candidates.length + ' aziende del foglio interno NON presenti nel foglio Sebastiano e non ancora chiamate.\\n\\nProcedere?',
    ui.ButtonSet.YES_NO);
  if (resp !== ui.Button.YES) return;

  var ok=0, fail=0;
  for (var j = 0; j < candidates.length; j++) {
    var res = triggerCallFromRow_(candidates[j]);
    if (res.ok) ok++; else fail++;
    Utilities.sleep(1500);  // throttle
  }
  SpreadsheetApp.getActiveSpreadsheet().toast('Batch NOT-in-Sebastiano: ok=' + ok + ' fail=' + fail, 'Done', 10);
}

function callAllPending() {
  var ui = SpreadsheetApp.getUi();
  var resp = ui.alert('Lanciare TUTTE le chiamate pending?',
    'Verranno chiamate tutte le righe con telefono valido e SENZA "Data chiamata" già compilata.\n\nProcedere?',
    ui.ButtonSet.YES_NO);
  if (resp !== ui.Button.YES) return;

  var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  var last = sh.getLastRow();
  var rows = sh.getRange(2, 1, last - 1, 12).getValues();
  var ok = 0, fail = 0, skip = 0;
  for (var i = 0; i < rows.length; i++) {
    var rowIdx = i + 2;
    var tel = String(rows[i][COL.TELEFONO-1] || '').trim();
    var dataCall = rows[i][COL.DATA_CHIAMATA-1];
    if (!tel) { skip++; continue; }
    if (dataCall) { skip++; continue; }
    var res = triggerCallFromRow_(rowIdx);
    if (res.ok) ok++; else fail++;
    Utilities.sleep(1500);
  }
  SpreadsheetApp.getActiveSpreadsheet().toast('Batch: ok=' + ok + ' fail=' + fail + ' skip=' + skip);
}

function triggerCallFromRow_(rowIdx) {
  var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  var r = sh.getRange(rowIdx, 1, 1, 12).getValues()[0];

  var nome_azienda  = String(r[COL.NOME_AZIENDA-1] || '').trim();
  var nome_titolare = String(r[COL.NOME_TITOLARE-1] || '').trim();
  var note_fonte    = String(r[COL.NOTE_FONTE-1] || '').trim();
  var indirizzo     = String(r[COL.INDIRIZZO-1] || '').trim();
  var telefono      = normalizePhone_(String(r[COL.TELEFONO-1] || ''));

  if (!telefono) return { ok: false, msg: 'telefono mancante o invalido' };

  // Estrai categoria dalle parentesi quadre in note_fonte
  var catMatch = note_fonte.match(/\[([^\]]+)\]/);
  var categoria = catMatch ? catMatch[1].toLowerCase() : '';

  // Costruisci dynamic_variables
  var dyn = {
    nome_azienda: nome_azienda,
    nome_titolare: nome_titolare,
    categoria: categoria,           // hotel | bar | ristorante ...
    citta: 'Bolzano',
    indirizzo: indirizzo,
    note_extra: note_fonte,
    row_index: String(rowIdx)       // chiave per match post-call
  };

  var apiKey = getApiKey_();
  if (!apiKey) return { ok: false, msg: 'API key non configurata' };

  var payload = {
    agent_id: AGENT_ID,
    agent_phone_number_id: PHONE_ID,
    to_number: telefono,
    conversation_initiation_client_data: {
      dynamic_variables: dyn
    }
  };

  try {
    var resp = UrlFetchApp.fetch(ELEVEN_BASE + '/v1/convai/sip-trunk/outbound-call', {
      method: 'post',
      contentType: 'application/json',
      headers: { 'xi-api-key': apiKey },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
    var code = resp.getResponseCode();
    var body = resp.getContentText();
    var data = {}; try { data = JSON.parse(body); } catch (e) {}
    var ok = code === 200 && data.success !== false;
    // Scrivi data chiamata anche su fail (così non riproviamo all'infinito)
    sh.getRange(rowIdx, COL.DATA_CHIAMATA).setValue(
      Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'Europe/Rome', 'dd/MM/yyyy HH:mm')
    );
    if (!ok && !sh.getRange(rowIdx, COL.ESITO).getValue()) {
      sh.getRange(rowIdx, COL.ESITO).setValue('Non risposto');
      sh.getRange(rowIdx, COL.NOTE_AI).setValue('SIP fail: ' + (data.message || code));
    }
    return { ok: ok, msg: ok ? 'ok' : (data.message || ('HTTP ' + code)) };
  } catch (err) {
    return { ok: false, msg: String(err) };
  }
}

function normalizePhone_(s) {
  var v = String(s || '').replace(/[^\d+]/g, '');
  if (!v) return '';
  if (v.startsWith('00')) v = '+' + v.slice(2);
  if (!v.startsWith('+')) {
    if (v.startsWith('39')) v = '+' + v;
    else v = '+39' + v;
  }
  return /^\+\d{9,15}$/.test(v) ? v : '';
}

// ===================== POST-CALL WEBHOOK =====================

function doPost(e) {
  try {
    var raw = e && e.postData && e.postData.contents ? e.postData.contents : '{}';
    var payload = JSON.parse(raw);

    if (payload && payload.type && String(payload.type).indexOf('post_call') === 0) {
      handlePostCall_(payload);
    } else {
      // Anche se non è exact match, prova
      if (payload && payload.data && payload.data.conversation_id) handlePostCall_(payload);
    }
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput('Culligan bridge — alive');
}

function handlePostCall_(payload) {
  var d = payload.data || {};
  var convId = d.conversation_id || '';
  var dur = (d.metadata && d.metadata.call_duration_secs) || '';
  var dc = (d.analysis && d.analysis.data_collection_results) || {};
  var get = function(k){ return (dc[k] && dc[k].value != null) ? String(dc[k].value) : ''; };
  var summary = (d.analysis && d.analysis.transcript_summary) || '';
  var transcript = d.transcript || [];

  // row_index dalle dynamic_variables
  var clientData = d.conversation_initiation_client_data || {};
  var dyn = clientData.dynamic_variables || {};
  var rowIdx = parseInt(dyn.row_index || '0', 10);

  var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  // Fallback: match per nome_azienda se row_index assente
  if (!rowIdx || rowIdx < 2) {
    if (dyn.nome_azienda) {
      var last = sh.getLastRow();
      var col = sh.getRange(2, COL.NOME_AZIENDA, last-1, 1).getValues();
      for (var i = 0; i < col.length; i++) {
        if (String(col[i][0]).trim() === String(dyn.nome_azienda).trim()) {
          rowIdx = i + 2; break;
        }
      }
    }
  }
  if (!rowIdx || rowIdx < 2) return; // niente match

  // Deduce ESITO dall'analisi
  var esito = deduceEsito_(get, summary, transcript);
  var present = esito === 'Appuntamento' || esito === 'Email' || esito === 'Da richiamare' ? 'Sì' : 'No';
  // Data appuntamento se nei dati o nel summary
  var dataApp = get('data_appuntamento') || extractDataApp_(summary);
  var email = get('email_contatto') || extractEmail_(summary, transcript);
  var noteAi = composeNote_(esito, summary, dur);

  var transcriptLink = convId ? ('https://elevenlabs.io/app/conversational-ai/history/' + convId) : '';

  // Distingui prima (call_attempt=1 o vuoto) da seconda chiamata (call_attempt=2)
  var callAttempt = String(dyn.call_attempt || '1');
  if (callAttempt === '2') {
    // Seconda chiamata → colonne M (13), N (14), O (15), P (16), Q (17)
    var oggi = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'Europe/Rome', 'dd/MM/yyyy HH:mm');
    sh.getRange(rowIdx, 13).setValue(oggi);          // M DATA_CHIAMATA_2
    sh.getRange(rowIdx, 14).setValue(esito);         // N ESITO_2
    sh.getRange(rowIdx, 15).setValue(noteAi);        // O NOTE_AI_2
    if (email) sh.getRange(rowIdx, 16).setValue(email); // P EMAIL_2
    sh.getRange(rowIdx, 17).setValue(transcriptLink);   // Q TRANSCRIPT_2
    return;
  }

  // Prima chiamata → colonne F, H, I, J, K, L (G era già stata scritta al trigger)
  sh.getRange(rowIdx, COL.PRESENTE).setValue(present);
  if (dataApp) sh.getRange(rowIdx, COL.DATA_APPUNTAMENTO).setValue(dataApp);
  sh.getRange(rowIdx, COL.ESITO).setValue(esito);
  sh.getRange(rowIdx, COL.NOTE_AI).setValue(noteAi);
  if (email) sh.getRange(rowIdx, COL.EMAIL_RACCOLTA).setValue(email);
  if (transcriptLink) sh.getRange(rowIdx, COL.TRANSCRIPT_LINK).setValue(transcriptLink);
}

function deduceEsito_(get, summary, transcript) {
  var s = (summary || '').toLowerCase();
  var fullTxt = s + ' ' + (transcript||[]).map(function(t){return (t.message||t.text||'').toLowerCase()}).join(' ');

  if (/appuntament(o|i) (preso|fissat|confermat)|sebastiano (passa|arriva|viene) (mar|mer|gio|ven|sab|lun|domani|oggi)/i.test(fullTxt)) return 'Appuntamento';
  if (/email\s*(inviat|mand|spedit)|le mando.*email|riepilogo via email|gliel(o|a) mando/i.test(fullTxt)) return 'Email';
  if (/segreteria|risposta automatica|non in ufficio|messaggio dopo il bip|voicemail/i.test(fullTxt)) return 'Segreteria';
  if (/menu numerico|premere il tasto|premi 1|premi 2/i.test(fullTxt)) return 'IVR/Centralino';
  if (/numero non esistente|inesistente|non attivo|disconnesso/i.test(fullTxt)) return 'Numero errato';
  if (/non.*interess|non.*fa.*per noi|non.*va bene|grazie ma no/i.test(fullTxt)) return 'Non interessato';
  if (/richiamar|risent|ripass|altro momento|piu tardi/i.test(fullTxt)) return 'Da richiamare';
  return 'Non risposto';
}

function extractDataApp_(summary) {
  if (!summary) return '';
  // Regex ASCII-safe: usa class \S che cattura sia "i" che "ì"
  var m = summary.match(/(?:lunedi|martedi|mercoledi|giovedi|venerdi|sabato|domenica|oggi|domani|dopodomani)\S?[^.]*?\d{1,2}[:.]\d{2}/i);
  if (m) return m[0];
  m = summary.match(/(?:lunedi|martedi|mercoledi|giovedi|venerdi|sabato|domenica|oggi|domani|dopodomani)\S?[^.]*/i);
  return m ? m[0].slice(0, 60) : '';
}

function extractEmail_(summary, transcript) {
  var txt = (summary || '') + ' ' + (transcript||[]).map(function(t){return t.message||t.text||''}).join(' ');
  var m = txt.match(/[\w.+-]+@[\w-]+\.[\w.-]+/);
  return m ? m[0] : '';
}

function composeNote_(esito, summary, dur) {
  // REGOLA PERMANENTE: Non risposto / Segreteria → SOLO "Non risposto." secco
  if (esito === 'Non risposto' || esito === 'Segreteria') return 'Non risposto.';
  // Sintetica, professionale, MAI menziona AI/bot/agente
  if (!summary) return esito + (dur ? ' (' + dur + 's)' : '');
  // Tagliamo a 280 char e rimuoviamo eventuali menzioni tecniche
  var s = String(summary).replace(/(agent|AI|bot|modello|prompt|webhook)/gi, '').trim();
  // Rimuovo anche eventuali stringhe SIP/errore tecnico se sopravvivono
  s = s.replace(/Chiamata non risposta \(errore tecnico SIP\)\.?/gi, 'Non risposto.').trim();
  if (s.length > 280) s = s.slice(0, 280).replace(/[,;.\s]+\S*$/, '') + '…';
  return s;
}

function getApiKey_() {
  return PropertiesService.getScriptProperties().getProperty('ELEVENLABS_API_KEY');
}

// ===================== SYNC AL FOGLIO SEBASTIANO =====================
// Trasferisce risultati chiamata dal foglio interno al foglio condiviso,
// mappando alle colonne di Sebastiano e usando note brevi stile umano.

function syncSelectedToSebastiano() {
  var sh = SpreadsheetApp.getActiveSheet();
  var ranges = sh.getActiveRangeList() ? sh.getActiveRangeList().getRanges() : [sh.getActiveRange()];
  var rows = [];
  ranges.forEach(function(r){
    var s = r.getRow(), e = s + r.getNumRows() - 1;
    for (var i = s; i <= e; i++) if (i >= 2) rows.push(i);
  });
  rows = rows.filter(function(v,i,a){return a.indexOf(v)===i});
  if (!rows.length) { SpreadsheetApp.getUi().alert('Seleziona almeno una riga lead'); return; }
  var ok=0, skip=0, fail=0, missing=[];
  rows.forEach(function(r){
    var res = syncRowToSebastiano_(r);
    if (res.ok) ok++;
    else if (res.reason === 'not_found') { fail++; missing.push(r); }
    else skip++;
  });
  var msg = 'Trasferiti: ' + ok + ' | non trovati su Sebastiano: ' + fail + (missing.length ? ' (righe ' + missing.join(',') + ')' : '') + ' | saltati: ' + skip;
  SpreadsheetApp.getActiveSpreadsheet().toast(msg, 'Sync', 8);
}

function syncAllDoneToSebastiano() {
  var ui = SpreadsheetApp.getUi();
  var resp = ui.alert('Trasferire TUTTE le righe gia chiamate?',
    'Tutte le righe con "Data chiamata" compilata verranno trasferite al foglio condiviso di Sebastiano.\\n\\nProcedere?',
    ui.ButtonSet.YES_NO);
  if (resp !== ui.Button.YES) return;
  var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  var last = sh.getLastRow();
  if (last < 2) return;
  var data = sh.getRange(2, 1, last - 1, 12).getValues();
  var ok=0, skip=0, fail=0;
  for (var i = 0; i < data.length; i++) {
    var rowIdx = i + 2;
    if (!data[i][COL.DATA_CHIAMATA-1]) { skip++; continue; }
    var res = syncRowToSebastiano_(rowIdx);
    if (res.ok) ok++; else if (res.reason==='not_found') fail++; else skip++;
    Utilities.sleep(150);
  }
  SpreadsheetApp.getActiveSpreadsheet().toast('Sync done: ok=' + ok + ' not_found=' + fail + ' skip=' + skip, 'Sync', 8);
}

function syncRowToSebastiano_(rowIdx) {
  var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  var src = sh.getRange(rowIdx, 1, 1, 12).getValues()[0];

  var nome_azienda = String(src[COL.NOME_AZIENDA-1] || '').trim();
  var nome_titolare = String(src[COL.NOME_TITOLARE-1] || '').trim();
  var telefono = String(src[COL.TELEFONO-1] || '').trim();
  var presente = String(src[COL.PRESENTE-1] || '').trim();
  var data_call = String(src[COL.DATA_CHIAMATA-1] || '').trim();
  var data_app = String(src[COL.DATA_APPUNTAMENTO-1] || '').trim();
  var esito = String(src[COL.ESITO-1] || '').trim();
  var note_ai = String(src[COL.NOTE_AI-1] || '').trim();
  var email = String(src[COL.EMAIL_RACCOLTA-1] || '').trim();

  if (!nome_azienda) return { ok: false, reason: 'no_company' };

  // Apri foglio condiviso
  var ssh = SpreadsheetApp.openById(SHARED_SHEET_ID).getSheetByName(SHARED_SHEET_NAME);
  if (!ssh) return { ok: false, reason: 'shared_sheet_not_found' };
  var sLast = ssh.getLastRow();
  if (sLast < 2) return { ok: false, reason: 'shared_sheet_empty' };

  // Match by NOME_AZIENDA (case insensitive), fallback TELEFONO
  var sData = ssh.getRange(2, 1, sLast - 1, 11).getValues();
  var targetRow = -1;
  var normA = normalizeName_(nome_azienda);
  var normP = telefono.replace(/[^\d]/g, '');
  for (var i = 0; i < sData.length; i++) {
    var rNomeA = normalizeName_(String(sData[i][SHARED_COL.NOME_AZIENDA-1] || ''));
    if (rNomeA && rNomeA === normA) { targetRow = i + 2; break; }
  }
  if (targetRow < 0) {
    for (var j = 0; j < sData.length; j++) {
      var rTel = String(sData[j][SHARED_COL.TELEFONO-1] || '').replace(/[^\d]/g, '');
      if (rTel && normP && (rTel === normP || rTel.endsWith(normP.slice(-7)) || normP.endsWith(rTel.slice(-7)))) {
        targetRow = j + 2; break;
      }
    }
  }
  if (targetRow < 0) return { ok: false, reason: 'not_found' };

  // Compose nota breve stile Sebastiano (max ~60 char)
  var notaBreve = composeShortNote_(esito, note_ai, email);
  var dataCallShort = shortDate_(data_call);
  var dataAppShort  = shortDate_(data_app);

  // Determina se e' 1° o 2° giro guardando G condiviso
  var existing_G = ssh.getRange(targetRow, SHARED_COL.DATA_CHIAMATA_1).getValue();
  var primoGiro = !existing_G;

  // Update colonne sul foglio condiviso
  // Sovrascrivi NOTE_BREVE (C) sempre con l'ultima
  ssh.getRange(targetRow, SHARED_COL.NOTE_BREVE).setValue(notaBreve);
  // PRESENTE (F) - mappa "Sì"/"No"
  if (presente) ssh.getRange(targetRow, SHARED_COL.PRESENTE).setValue(presente);
  // NOME TITOLARE (B) - solo se vuoto sul condiviso
  if (nome_titolare && !ssh.getRange(targetRow, SHARED_COL.NOME_TITOLARE).getValue()) {
    ssh.getRange(targetRow, SHARED_COL.NOME_TITOLARE).setValue(nome_titolare);
  }

  if (primoGiro) {
    if (dataCallShort) ssh.getRange(targetRow, SHARED_COL.DATA_CHIAMATA_1).setValue(dataCallShort);
    if (dataAppShort)  ssh.getRange(targetRow, SHARED_COL.DATA_APP_1).setValue(dataAppShort);
  } else {
    // Secondo giro: I / J / K
    if (dataCallShort) ssh.getRange(targetRow, SHARED_COL.DATA_CHIAMATA_2).setValue(dataCallShort);
    if (notaBreve)     ssh.getRange(targetRow, SHARED_COL.NOTE_2).setValue(notaBreve);
    if (dataAppShort)  ssh.getRange(targetRow, SHARED_COL.DATA_APP_2).setValue(dataAppShort);
  }
  return { ok: true, reason: primoGiro ? 'first_round' : 'second_round', targetRow: targetRow };
}

function normalizeName_(s) {
  return String(s || '').toLowerCase().replace(/[^a-z0-9]/g, '').trim();
}

function shortDate_(s) {
  if (!s) return '';
  // Es. "17/05/2026 16:30" -> "17/05/26"  (Sebastiano usa 11/05/2 cioe' troncato)
  var m = String(s).match(/(\d{1,2}\/\d{1,2}\/\d{2,4})/);
  if (m) {
    var d = m[1].split('/');
    var yy = d[2].length === 4 ? d[2].slice(-2) : d[2];
    return d[0].padStart(2,'0') + '/' + d[1].padStart(2,'0') + '/' + yy;
  }
  return String(s).slice(0, 12);
}

function composeShortNote_(esito, noteAi, email) {
  // Genera la nota breve stile Sebastiano (umana, MAI menzionare AI/agente/bot)
  var nome = '';
  var nm = (noteAi || '').match(/(?:nome|titolare)\s*[:\-]?\s*([A-Z][a-zA-Z]+)/i);
  if (nm) nome = nm[1];
  var e = esito.toLowerCase();
  if (e === 'appuntamento')      return 'ok';
  if (e === 'email')             return (nome ? nome + ' ' : '') + 'inviare email' + (email ? ' ' + email : '');
  if (e === 'da richiamare') {
    var giorno = (noteAi || '').match(/(lunedi|martedi|mercoledi|giovedi|venerdi|sabato|domenica|domani|oggi)/i);
    return 'richiamare' + (giorno ? ' ' + giorno[1].toLowerCase() : ' piu tardi');
  }
  if (e === 'non interessato')   return 'non interes';
  if (e === 'non risposto')      return 'non risp';
  if (e === 'segreteria')        return 'non risp';
  if (e === 'ivr/centralino')    return 'non risp';
  if (e === 'numero errato')     return 'numero errato';
  // fallback: prima parte note_ai (~40 char), nessuna menzione tecnica
  var s = noteAi.replace(/\b(AI|bot|agente|prompt|webhook|sistema)\b/gi, '').replace(/\s+/g, ' ').trim();
  return s.slice(0, 50);
}
