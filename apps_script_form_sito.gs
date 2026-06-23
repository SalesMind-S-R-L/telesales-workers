/**
 * Apps Script — FORM SITO sync da Supabase → pipeline_opportunita
 * Tab: 'FORM SITO' nel foglio 1wFYXFDFo6W2GT6HT3HKHLYx8eN-C4VUGnxlU_dIiNyk
 *
 * Setup:
 *   1) Estensioni → Apps Script → incolla questo file
 *   2) Impostazioni progetto → Proprietà script → aggiungi:
 *      SUPABASE_URL  = https://pbcyteqcmlzjmuzgwfnz.supabase.co
 *      SUPABASE_KEY  = <la tua anon key>
 *   3) Esegui setupSheet() una volta per verificare le intestazioni
 *   4) Esegui syncFromSupabase() per importare subito tutti i lead
 *   5) Trigger automatico: Trigger → Aggiungi trigger
 *      Funzione: syncFromSupabase | Evento: Basato su tempo | Ogni 15 minuti
 */

var SHEET_ID = '1wFYXFDFo6W2GT6HT3HKHLYx8eN-C4VUGnxlU_dIiNyk';
var TAB_NAME = 'FORM SITO';
var DATA_ROW = 4; // prima riga dati (sotto 3 righe di titolo/header)

// Tabelle Supabase da sincronizzare
var TABLES = [
  { name: 'leads',              form: 'Form Azienda' },
  { name: 'ai_voice_callbacks', form: 'AI Voice Demo' },
  { name: 'job_applications',   form: 'Candidatura Setter' },
];

// -----------------------------------------------------------------------
// Sync principale — legge Supabase, scrive righe nuove nel tab
// -----------------------------------------------------------------------
function syncFromSupabase() {
  var props = PropertiesService.getScriptProperties();
  var SUPABASE_URL = props.getProperty('SUPABASE_URL');
  var SUPABASE_KEY = props.getProperty('SUPABASE_KEY');

  if (!SUPABASE_URL || !SUPABASE_KEY) {
    Logger.log('ERRORE: SUPABASE_URL e SUPABASE_KEY non configurate nelle proprietà script');
    return;
  }

  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(TAB_NAME);
  if (!sh) { Logger.log('Tab non trovato: ' + TAB_NAME); return; }

  // Leggi tutti gli ID già presenti (colonna O = indice 15)
  var existingIds = new Set();
  var lastRow = sh.getLastRow();
  if (lastRow >= DATA_ROW) {
    var idCol = sh.getRange(DATA_ROW, 15, lastRow - DATA_ROW + 1, 1).getValues();
    idCol.forEach(function(r) { if (r[0]) existingIds.add(String(r[0])); });
  }

  var newRows = 0;

  TABLES.forEach(function(table) {
    try {
      var url = SUPABASE_URL + '/rest/v1/' + table.name + '?select=*&order=created_at.desc&limit=500';
      var resp = UrlFetchApp.fetch(url, {
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': 'Bearer ' + SUPABASE_KEY,
          'Content-Type': 'application/json'
        },
        muteHttpExceptions: true
      });

      if (resp.getResponseCode() !== 200) {
        Logger.log('Errore ' + table.name + ': HTTP ' + resp.getResponseCode());
        return;
      }

      var records = JSON.parse(resp.getContentText());
      Logger.log(table.name + ': ' + records.length + ' record trovati');

      records.forEach(function(rec) {
        var id = String(rec.id || rec.created_at || '');
        if (existingIds.has(id)) return; // già presente

        var row = buildRow(rec, table.form);
        sh.appendRow(row);
        coloraStato(sh, sh.getLastRow(), row[13]); // col N = Stato
        existingIds.add(id);
        newRows++;
      });
    } catch(e) {
      Logger.log('Errore sync ' + table.name + ': ' + e);
    }
  });

  Logger.log('Sync completata: ' + newRows + ' nuove righe aggiunte');
}

// -----------------------------------------------------------------------
// Mappa record Supabase → riga foglio
// -----------------------------------------------------------------------
function buildRow(rec, formName) {
  // Normalizza data
  var data = '';
  if (rec.created_at) {
    try {
      var d = new Date(rec.created_at);
      data = Utilities.formatDate(d, Session.getScriptTimeZone(), 'dd/MM/yyyy');
    } catch(e) { data = rec.created_at; }
  }

  // Gestisci varianti nomi campo (diversi form hanno campi diversi)
  var nome      = rec.nome || rec.first_name || rec.name || '';
  var cognome   = rec.cognome || rec.last_name || '';
  var email     = rec.email || '';
  var telefono  = rec.telefono || rec.phone || '';
  var azienda   = rec.azienda || rec.company || rec.nome_azienda || '';
  var ruolo     = rec.ruolo || rec.role || rec.job_title || '';
  var fatturato = rec.fatturato || rec.revenue || '';
  var dimDb     = rec.dimensione_database || rec.db_size || '';
  var obiettivo = Array.isArray(rec.obiettivo) ? rec.obiettivo.join(', ') : (rec.obiettivo || rec.goal || '');
  var canale    = Array.isArray(rec.canale_attuale) ? rec.canale_attuale.join(', ') : (rec.canale_attuale || '');
  var note      = rec.messaggio || rec.message || rec.note || '';
  var stato     = 'Da contattare';
  var id        = String(rec.id || rec.created_at || '');

  return [data, formName, nome, cognome, email, telefono, azienda, ruolo,
          fatturato, dimDb, obiettivo, canale, note, stato, id];
}

// -----------------------------------------------------------------------
// Colora cella Stato in base al valore
// -----------------------------------------------------------------------
function coloraStato(sh, rowNum, stato) {
  var colors = {
    'Da contattare': '#FFC107',
    'Contattato':    '#2196F3',
    'Interessato':   '#4CAF50',
    'Non interessato': '#9E9E9E',
    'Cliente':       '#8BC34A',
  };
  var col = 14; // colonna N
  var cell = sh.getRange(rowNum, col);
  var bg = colors[stato] || '#FFFFFF';
  cell.setBackground(bg);
  cell.setFontColor(['Da contattare','Interessato','Contattato','Cliente'].indexOf(stato) >= 0 ? '#000000' : '#FFFFFF');
}

// -----------------------------------------------------------------------
// Setup intestazioni (esegui una volta)
// -----------------------------------------------------------------------
function setupSheet() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(TAB_NAME);
  if (!sh) { Logger.log('Tab non trovato: ' + TAB_NAME); return; }
  Logger.log('Tab trovato: ' + TAB_NAME + ' — intestazioni già presenti, sync pronta.');
}
