/**
 * Post-call webhook ElevenLabs -> Google Sheet (Studio Evoluzione Fiscale - Reception)
 * Web App: Deploy > New deployment > Web app > Execute as: Me > Who has access: Anyone.
 * Poi registra l'URL /exec come post-call webhook dell'agente (override per-agente).
 * 12 colonne: Data e ora | Nome | Azienda | Telefono | Email | Motivo | Servizio | Appuntamento | Esito | Riassunto | Trascrizione | Conversation ID
 */
const SHEET_ID = '<ID_FOGLIO>';
const SHEET_NAME = 'Foglio1';
const AGENT_ID = 'agent_8501kv5j5ee9eakr1tj5c231eg8w';

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var d = data.data || data;
    var convId = d.conversation_id || data.conversation_id || '';
    // idempotenza: stesso webhook puo arrivare 2 volte (retry)
    var props = PropertiesService.getScriptProperties();
    if (convId && props.getProperty('CONV_' + convId)) {
      return ContentService.createTextOutput(JSON.stringify({ ok: true, dup: true })).setMimeType(ContentService.MimeType.JSON);
    }
    var dc = (d.analysis && d.analysis.data_collection_results) || {};
    function g(k) { return (dc[k] && dc[k].value != null) ? dc[k].value : ''; }
    var agentId = d.agent_id || AGENT_ID;
    var summary = (d.analysis && d.analysis.transcript_summary) || '';
    var link = convId ? 'https://elevenlabs.io/app/agents/agents/' + agentId + '/history/' + convId : '';
    SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME).appendRow([
      Utilities.formatDate(new Date(), 'Europe/Rome', 'dd/MM/yyyy HH:mm'),
      g('nome_chiamante'), g('azienda'), g('telefono'), g('email'),
      g('motivo'), g('servizio_interesse'), g('appuntamento'), g('esito'),
      summary, link, convId
    ]);
    if (convId) props.setProperty('CONV_' + convId, '1');
    return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) { return ContentService.createTextOutput('webhook attivo'); }
