/**
 * Webhook landing Sales Six (sales-six.html) -> tab "SALES SIX" foglio pipeline.
 *
 * Deploy: Estensioni > Apps Script > Deploy > Web App
 *   - Execute as: me  |  Who has access: Anyone
 * Poi incollare l'URL del deploy in sales-six.html (WEBHOOK_URL).
 *
 * Convenzioni: date DD/MM/YYYY HH:MM, niente emoji nei dati.
 */

const SHEET_ID = '1nLvvZ98RLp-ic81Wa8NBNGI0Ig_t8Sl4XIzx7GBnuww'; // pipeline_opportunita
const TAB_SALES_SIX = 'SALES SIX';

const HEADER = [
  'Data', 'Nome', 'Azienda', 'Email', 'Telefono',
  'N commerciali', 'App/settimana ciascuno', 'Lead/mese',
  'Richiamati 24h (%)', 'Follow-up medi', 'Valore cliente (EUR)',
  'Stima persa annua (EUR)', 'Stato',
];

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    if (d.fonte !== 'sales-six') {
      return ContentService.createTextOutput('ignored');
    }
    const sh = getOrCreateTab_();
    const now = Utilities.formatDate(new Date(), 'Europe/Rome', 'dd/MM/yyyy HH:mm');
    sh.appendRow([
      now,
      d.nome || '', d.azienda || '', d.email || '', d.telefono || '',
      Number(d.n_commerciali) || '', Number(d.app_settimana) || '',
      Number(d.lead_mese) || '', Number(d.ricontatto) || '',
      Number(d.followup) || '', Number(d.valore_cliente) || '',
      Number(d.stima_persa_annua) || '',
      'Da analizzare',
    ]);
    return ContentService.createTextOutput('ok');
  } catch (err) {
    return ContentService.createTextOutput('error: ' + err);
  }
}

function getOrCreateTab_() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sh = ss.getSheetByName(TAB_SALES_SIX);
  if (!sh) {
    sh = ss.insertSheet(TAB_SALES_SIX);
    sh.appendRow(HEADER);
    sh.getRange(1, 1, 1, HEADER.length)
      .setFontWeight('bold')
      .setBackground('#d9e2f3');
    sh.setFrozenRows(1);
  }
  return sh;
}
