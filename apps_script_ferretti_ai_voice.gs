/**
 * Apps Script — OUTREACH AI VOICE (Marco Ferretti)
 * Riceve webhook post-call ElevenLabs e scrive nel tab 'OUTREACH AI VOICE'
 * del foglio pipeline_opportunita.
 *
 * Setup:
 *   1) Estensioni → Apps Script → incolla questo file
 *   2) Esegui setupSheet() una volta (crea/verifica intestazioni)
 *   3) Implementa → Nuova implementazione → App web
 *      Esegui come: me — Chi ha accesso: chiunque (anche anonimo)
 *   4) Copia URL e mettilo come webhook post-call sull'agente Marco Ferretti
 *      su ElevenLabs (Agent → Post-call webhook URL)
 */

var SHEET_ID   = '1wFYXFDFo6W2GT6HT3HKHLYx8eN-C4VUGnxlU_dIiNyk';
var TAB_NAME   = 'OUTREACH AI VOICE';
var DATA_START = 4; // prima riga dati (1-indexed), sopra ci sono 3 righe titolo/header

// Colonne (1-indexed)
var COLS = {
  data:           1,   // A
  batch_id:       2,   // B
  azienda:        3,   // C
  decisore:       4,   // D
  ruolo:          5,   // E
  telefono:       6,   // F
  email:          7,   // G
  citta:          8,   // H
  settore:        9,   // I
  esito:          10,  // J
  note:           11,  // K
  angolo_pitch:   12,  // L
  durata_s:       13,  // M
  conv_id:        14,  // N
  prossima_az:    15,  // O
  data_prox_az:   16,  // P
};

// -----------------------------------------------------------------------
// Entry point webhook (POST da ElevenLabs post-call)
// -----------------------------------------------------------------------
function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);
    processCall(payload);
    return ContentService.createTextOutput(JSON.stringify({ok: true}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch(err) {
    Logger.log('doPost error: ' + err);
    return ContentService.createTextOutput(JSON.stringify({ok: false, error: err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// -----------------------------------------------------------------------
// Processa singola chiamata dal webhook
// -----------------------------------------------------------------------
function processCall(payload) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(TAB_NAME);
  if (!sh) throw new Error('Tab ' + TAB_NAME + ' non trovato');

  // Estrai dati dal payload ElevenLabs post-call
  var convId    = payload.conversation_id || '';
  var dynVars   = (payload.conversation_initiation_client_data || {}).dynamic_variables || {};
  var meta      = payload.metadata || {};
  var analysis  = payload.analysis || {};
  var transcript= payload.transcript || [];

  var azienda   = dynVars.nome_azienda   || '';
  var decisore  = dynVars.nome_decisore  || '';
  var ruolo     = dynVars.ruolo_decisore || '';
  var telefono  = payload.phone_number   || '';
  var citta     = dynVars.citta          || '';
  var settore   = dynVars.settore        || '';
  var angolo    = dynVars.angolo_pitch   || '';
  var durata    = meta.call_duration_secs || '';
  var batchId   = payload.batch_call_id  || '';

  // Email raccolta (da tool call o transcript)
  var email = '';
  var tools = payload.tool_results || [];
  for (var i = 0; i < tools.length; i++) {
    if (tools[i].email) { email = tools[i].email; break; }
  }
  // Fallback: cerca email nel transcript con regex
  if (!email) {
    var fullText = transcript.map(function(t){ return t.message || ''; }).join(' ');
    var emailMatch = fullText.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/);
    if (emailMatch) email = emailMatch[0];
  }

  // Determina esito
  var esito = classificaEsito(analysis, transcript, payload.status);
  var note  = buildNote(analysis, transcript);
  var prossimaAz = suggerisciAzione(esito, email);
  var dataProxAz = esito !== 'Non interessato' && esito !== 'Non contattato'
    ? formatDate(new Date(Date.now() + 86400000)) : '';

  var today = formatDate(new Date());

  var row = new Array(16).fill('');
  row[COLS.data         - 1] = today;
  row[COLS.batch_id     - 1] = batchId;
  row[COLS.azienda      - 1] = azienda;
  row[COLS.decisore     - 1] = decisore;
  row[COLS.ruolo        - 1] = ruolo;
  row[COLS.telefono     - 1] = telefono;
  row[COLS.email        - 1] = email;
  row[COLS.citta        - 1] = citta;
  row[COLS.settore      - 1] = settore;
  row[COLS.esito        - 1] = esito;
  row[COLS.note         - 1] = note;
  row[COLS.angolo_pitch - 1] = angolo;
  row[COLS.durata_s     - 1] = durata;
  row[COLS.conv_id      - 1] = convId;
  row[COLS.prossima_az  - 1] = prossimaAz;
  row[COLS.data_prox_az - 1] = dataProxAz;

  sh.appendRow(row);

  // Colora riga in base all'esito
  var lastRow = sh.getLastRow();
  coloraRiga(sh, lastRow, esito);

  Logger.log('Scritto: ' + azienda + ' | ' + esito);
}

// -----------------------------------------------------------------------
// Classifica esito
// -----------------------------------------------------------------------
function classificaEsito(analysis, transcript, status) {
  if (status === 'failed') return 'Non contattato';
  if (status === 'voicemail') return 'Segreteria';

  var fullText = transcript.map(function(t){ return (t.message||'').toLowerCase(); }).join(' ');

  // Appuntamento fissato
  if (/martedì|mercoledì|giovedì|venerdì|lunedì|settimana|15 minuti|calendario|call|demo/.test(fullText) &&
      /perfetto|conferm|va bene|d'accordo/.test(fullText)) {
    return 'Appuntamento';
  }
  // Email raccolta
  if (/@/.test(fullText)) return 'Email raccolta';
  // Non interessato
  if (/non siamo interessati|non mi interessa|non abbiamo.*esigenza|non è il momento/.test(fullText)) {
    return 'Non interessato';
  }
  // Decisore assente
  if (/non c'è|non è in ufficio|richiamare|richiamo|quando torna/.test(fullText)) {
    return 'Da richiamare';
  }
  // Audio/IVR issues
  if (/pronto\?|mi sente\?|digitare uno|attendere in linea/.test(fullText)) {
    return 'Non contattato';
  }
  return 'Da richiamare';
}

function buildNote(analysis, transcript) {
  // Ultimi 2 turn dell'interlocutore
  var userTurns = transcript.filter(function(t){ return t.role === 'user' && t.message; });
  var last2 = userTurns.slice(-2).map(function(t){ return t.message; }).join(' / ');
  return last2.substring(0, 200);
}

function suggerisciAzione(esito, email) {
  if (esito === 'Appuntamento') return 'Confermare appuntamento via email';
  if (esito === 'Email raccolta') return 'Inviare email riepilogo + follow-up call';
  if (esito === 'Da richiamare') return email ? 'Follow-up email + richiamare' : 'Richiamare decisore direttamente';
  if (esito === 'Non contattato') return 'Trovare cellulare diretto + richiamare';
  return '';
}

// -----------------------------------------------------------------------
// Colora riga
// -----------------------------------------------------------------------
function coloraRiga(sh, rowNum, esito) {
  var colors = {
    'Appuntamento':    {r:0.13, g:0.55, b:0.13},  // verde
    'Email raccolta':  {r:0.06, g:0.46, b:0.74},  // blu
    'Da richiamare':   {r:0.95, g:0.76, b:0.20},  // giallo
    'Non interessato': {r:0.60, g:0.60, b:0.60},  // grigio
    'Non contattato':  {r:0.80, g:0.80, b:0.80},  // grigio chiaro
    'Segreteria':      {r:0.85, g:0.85, b:0.85},  // grigio chiaro
  };
  var c = colors[esito] || {r:1, g:1, b:1};
  var range = sh.getRange(rowNum, COLS.esito, 1, 1);
  range.setBackground('rgb(' +
    Math.round(c.r*255) + ',' +
    Math.round(c.g*255) + ',' +
    Math.round(c.b*255) + ')');
  range.setFontColor(esito === 'Appuntamento' || esito === 'Email raccolta' ? '#ffffff' : '#000000');
}

// -----------------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------------
function formatDate(d) {
  return Utilities.formatDate(d, Session.getScriptTimeZone(), 'dd/MM/yyyy');
}

// -----------------------------------------------------------------------
// Setup iniziale (esegui una volta dall'editor)
// -----------------------------------------------------------------------
function setupSheet() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(TAB_NAME);
  if (!sh) {
    sh = ss.insertSheet(TAB_NAME);
    Logger.log('Tab creato: ' + TAB_NAME);
  }
  // Verifica/imposta intestazioni riga 3
  var headers = ['Data','Batch ID','Azienda','Decisore','Ruolo','Telefono','Email',
                 'Città','Settore','Esito','Note','Angolo Pitch','Durata (s)',
                 'Conversation ID','Prossima Azione','Data Prossima Azione'];
  sh.getRange(3, 1, 1, headers.length).setValues([headers])
    .setFontWeight('bold');
  sh.setFrozenRows(3);
  Logger.log('Setup completato');
}
