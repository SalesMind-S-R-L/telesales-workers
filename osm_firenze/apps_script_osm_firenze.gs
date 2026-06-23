/**
 * OSM Firenze 06/07 - Iscrizioni Telesales
 * Web App che riceve le iscrizioni dalla landing e le scrive in tempo reale
 * su un Google Sheet creato nel TUO Drive.
 *
 * SETUP (una sola volta):
 *   1) https://script.google.com -> Nuovo progetto
 *   2) Incolla TUTTO questo file (sostituendo il contenuto di default)
 *   3) Seleziona la funzione "setup" -> Esegui (autorizza). Crea il foglio
 *      e ne stampa il link nei Log (Visualizza -> Log di esecuzione).
 *   4) Distribuisci -> Nuova distribuzione -> "App web"
 *        - Esegui come: Me
 *        - Chi ha accesso: Chiunque
 *      -> Distribuisci -> copia l'URL "App web" (finisce con /exec)
 *   5) Incolla quell'URL in config.js -> OSM_CONFIG.ENDPOINT
 *
 * Ad ogni iscrizione viene aggiunta una riga nel foglio, una colonna per campo.
 */

var SHEET_NAME = 'Iscrizioni';
var SPREADSHEET_TITLE = 'OSM Firenze 06-07 - Iscrizioni Telesales';

var HEADERS = [
  'Timestamp', 'Nome', 'Cognome', 'Email', 'Prefisso', 'Telefono',
  'Citta', 'Azienda', 'Ruolo', 'Provincia',
  'Consenso privacy', 'Consenso 3.1 (partner)', 'Consenso 3.2 (marketing)', 'Fonte'
];

// ---------- crea il foglio nel tuo Drive (esegui una volta) ----------
function setup() {
  var ss = getOrCreateSpreadsheet_();
  Logger.log('Foglio pronto. Aprilo qui:');
  Logger.log(ss.getUrl());
  return ss.getUrl();
}

function getOrCreateSpreadsheet_() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('SPREADSHEET_ID');
  var ss;
  if (id) {
    try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; }
  }
  if (!ss) {
    ss = SpreadsheetApp.create(SPREADSHEET_TITLE);
    props.setProperty('SPREADSHEET_ID', ss.getId());
  }
  var sh = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
  sh.setName(SHEET_NAME);
  if (sh.getLastRow() === 0 || sh.getRange(1, 1).getValue() !== HEADERS[0]) {
    sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sh.getRange(1, 1, 1, HEADERS.length)
      .setFontWeight('bold').setFontColor('#ffffff').setBackground('#db2777');
    sh.setFrozenRows(1);
    sh.autoResizeColumns(1, HEADERS.length);
  }
  return ss;
}

// ---------- ricezione iscrizioni dalla landing ----------
function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    } else if (e && e.parameter) {
      data = e.parameter;
    }

    var ss = getOrCreateSpreadsheet_();
    var sh = ss.getSheetByName(SHEET_NAME);

    var tz = ss.getSpreadsheetTimeZone() || 'Europe/Rome';
    var stamp = Utilities.formatDate(new Date(), tz, 'dd/MM/yyyy HH:mm:ss');

    var asText = function (v) { return "'" + (v || ''); };

    var row = [
      stamp,
      data.name || '',
      data.last_name || '',
      data.email || '',
      asText(data.prefix),            // testo, mantiene il "+"
      asText(data.phone),             // testo, mantiene lo 0 iniziale
      data.city || '',
      data.company || '',
      data.role || '',
      data.province || '',
      data.privacy || '',
      data.consent31 || '',
      data.consent32 || '',
      data.source || 'Telesales'
    ];

    sh.appendRow(row);

    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

// health check
function doGet(e) {
  return json_({ ok: true, service: 'OSM Firenze iscrizioni', ts: new Date().toISOString() });
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
