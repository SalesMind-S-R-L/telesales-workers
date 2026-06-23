/**
 * APPS SCRIPT — PIPELINE COMMERCIALE (Telesales) v2
 * Foglio: 1nLvvZ98RLp-ic81Wa8NBNGI0Ig_t8Sl4XIzx7GBnuww
 *
 * doPost smista per source:
 *  - source=demo    → tab '📥 FORM Demo'
 *  - source=voice   → tab '📥 FORM Voice'
 *  - source=careers → tab '📥 FORM Careers'
 *
 * IMPORTANTE: i form sito NON vanno in pipeline opportunità automaticamente.
 * Le opportunità si materializzano solo quando il commerciale chiama il prospect.
 *
 * Instantly webhook continua a popolare OUTREACH INSTANTLY + auto-promuove a
 * Email Outreach SOLO se reply_count >= 1 (lead caldo qualificato).
 */

const SHEET_ID = '1nLvvZ98RLp-ic81Wa8NBNGI0Ig_t8Sl4XIzx7GBnuww';
const INSTANTLY_KEY_FALLBACK = 'YzkyODNiOTAtNWRmNi00OTc1LWExODktZTY5MjAyMmQxNjRhOmhqZWlhaGtNWEh2cA==';

const TAB_OUTR_INST = 'OUTREACH INSTANTLY';
const TAB_FORM_DEMO = '📥 FORM Demo';
const TAB_FORM_VOICE = '📥 FORM Voice';
const TAB_FORM_CAREERS = '📥 FORM Careers';
const TAB_EMAIL_OUTREACH = 'Email Outreach';
const TAB_MARCO_FERRETTI = '📞 Marco Ferretti';
const MARCO_FERRETTI_AGENTS = {
  'agent_5301kpdv4sd9e15vcz4qpm8e7vrn': 'Marco Ferretti — Outreach Telesales',
  'agent_9201krn8z6ptevxsmx3g5e6vy69b': 'Marco Ferretti — Spiegazione Aziendale',
};

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);

    // ElevenLabs post-call webhook (Marco Ferretti)
    if (body.type === 'post_call_transcription' || (body.data && body.data.agent_id && MARCO_FERRETTI_AGENTS[body.data.agent_id])) {
      return handleMarcoFerrettiPostCall(body);
    }

    const src = (body.source || body.form_type || body.event_type || 'unknown').toLowerCase();
    if (src === 'demo' || src === 'form_demo') return handleFormDemo(body);
    if (src === 'voice' || src === 'form_voice') return handleFormVoice(body);
    if (src === 'careers' || src === 'form_careers') return handleFormCareers(body);
    if (src.indexOf('instantly') === 0 || src === 'reply_received' || src === 'email_opened') return handleInstantlyWebhook(body);

    return jsonOut({ok:false, msg:'unknown source: '+src});
  } catch (err) {
    return jsonOut({ok:false, error: err.toString()});
  }
}

// =========================================================
// Marco Ferretti post-call webhook (ElevenLabs)
// Riceve sia INBOUND (landing chiamami) sia OUTBOUND (batch outreach)
// =========================================================
function handleMarcoFerrettiPostCall(body) {
  const d = body.data || body;
  const agentId = d.agent_id || '';
  const agentName = MARCO_FERRETTI_AGENTS[agentId] || agentId;
  const convId = d.conversation_id || '';
  const meta = d.metadata || {};
  const phone = (meta.phone_call && meta.phone_call.external_number) || d.phone_number || '';
  const direction = (meta.phone_call && meta.phone_call.direction) || 'unknown';
  const duration = meta.call_duration_secs || 0;
  const startUnix = meta.start_time_unix_secs || Math.floor(Date.now()/1000);
  const dt = new Date(startUnix * 1000);
  const dateStr = Utilities.formatDate(dt,'Europe/Rome','dd/MM/yyyy');
  const timeStr = Utilities.formatDate(dt,'Europe/Rome','HH:mm');

  // Analysis + data collection
  const analysis = d.analysis || {};
  const summary = analysis.transcript_summary || '';
  const dc = (analysis.data_collection_results || {});
  const get = (k) => (dc[k] && (dc[k].value || dc[k].result)) || '';

  const nome = get('nome_contatto') || get('nome') || get('full_name') || '';
  const ruolo = get('ruolo') || get('role') || '';
  const azienda = get('azienda') || get('company') || '';
  const email = get('email') || '';
  const prodotto = get('prodotto_interesse') || get('product_interest') || '';
  const pain = get('pain_point') || '';
  const stato = get('stato_lead') || get('lead_status') || analysis.call_successful || '';
  const appuntamento = get('appuntamento') || get('appointment') || '';
  const noteAI = analysis.transcript_summary_short || analysis.short_summary || '';

  const transcriptLink = 'https://elevenlabs.io/app/conversational-ai/history/' + convId;

  const row = [
    dateStr, timeStr, direction,
    nome, ruolo, azienda, email, phone,
    prodotto, pain, stato, appuntamento,
    noteAI, duration, transcriptLink, summary,
    convId, agentId
  ];

  const sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB_MARCO_FERRETTI);
  sh.appendRow(row);
  Logger.log('Marco Ferretti post-call scritto: ' + convId + ' (' + direction + ')');
  return jsonOut({ok:true, conv:convId, direction:direction, agent:agentName});
}

function jsonOut(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// =========================================================
// Form Demo (questionario lungo Telesales)
// =========================================================
function handleFormDemo(b) {
  const sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB_FORM_DEMO);
  const obiettivo = Array.isArray(b.obiettivo) ? b.obiettivo.join(', ') : (b.obiettivo || '');
  const canale = Array.isArray(b.canale_attuale) ? b.canale_attuale.join(', ') : (b.canale_attuale || '');
  const dimensione = Array.isArray(b.dimensione_database) ? b.dimensione_database.join(', ') : (b.dimensione_database || '');
  sh.appendRow([
    new Date(),
    b.nome || b.firstName || '',
    b.cognome || b.lastName || '',
    b.email || '',
    b.telefono || b.phone || '',
    b.azienda || b.company || '',
    b.ruolo || b.role || '',
    b.citta || b.city || '',
    b.fatturato || '',
    dimensione,
    obiettivo,
    canale,
    b.messaggio || b.message || b.note || '',
    b.source_url || b.referrer || '',
    b.user_agent || '',
    'Nuovo',
    ''
  ]);
  return jsonOut({ok:true, tab:'Demo'});
}

// =========================================================
// Form Voice (callback AI Voice)
// =========================================================
function handleFormVoice(b) {
  const sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB_FORM_VOICE);
  sh.appendRow([
    new Date(),
    b.nome || b.firstName || '',
    b.cognome || b.lastName || '',
    b.email || '',
    b.telefono || b.phone || '',
    b.azienda || b.company || '',
    b.ruolo || b.role || '',
    b.fascia_oraria || b.preferred_time || '',
    b.messaggio || b.message || b.note || '',
    b.source_url || b.referrer || '',
    b.user_agent || '',
    'Nuovo',
    ''
  ]);
  return jsonOut({ok:true, tab:'Voice'});
}

// =========================================================
// Form Careers (candidature)
// =========================================================
function handleFormCareers(b) {
  const sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB_FORM_CAREERS);
  sh.appendRow([
    new Date(),
    b.nome || b.firstName || '',
    b.cognome || b.lastName || '',
    b.email || '',
    b.telefono || b.phone || '',
    b.citta || b.city || '',
    b.ruolo_desiderato || b.position || b.ruolo || '',
    b.esperienza || b.experience || '',
    b.cv_link || b.cv || '',
    b.linkedin || '',
    b.messaggio || b.message || b.cover_letter || '',
    b.source_url || b.referrer || '',
    'Nuovo',
    ''
  ]);
  return jsonOut({ok:true, tab:'Careers'});
}

// =========================================================
// Instantly webhook (reply_received → auto-promuove a Email Outreach)
// =========================================================
function handleInstantlyWebhook(b) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const sh = ss.getSheetByName(TAB_OUTR_INST);
  const data = sh.getDataRange().getValues();
  const hdr = data[0];
  const colEmail = hdr.indexOf('email');
  const colReply = hdr.indexOf('reply_count');
  const colOpen = hdr.indexOf('aperture');
  const colStatus = hdr.indexOf('status_lead');
  const colLast = hdr.indexOf('data_ultima_attivita');

  const email = (b.email || (b.lead && b.lead.email) || '').toLowerCase();
  if (!email) return jsonOut({ok:false, msg:'no email'});
  const event = b.event_type || '';
  const oggi = Utilities.formatDate(new Date(),'Europe/Rome','yyyy-MM-dd');

  let found = -1;
  for (let i=1;i<data.length;i++){
    if ((data[i][colEmail]||'').toLowerCase() === email) { found = i; break; }
  }
  if (found < 0) {
    const lead = b.lead || b;
    sh.appendRow([oggi,oggi,email,lead.first_name||'',lead.last_name||'',lead.company_name||'',
      '',lead.phone||'',lead.website||'','','',lead.campaign_name||'',
      'status:webhook','0','0','0','','','','Instantly-Webhook',lead.id||'','']);
    found = sh.getLastRow()-1;
  }

  if (event === 'reply_received') {
    sh.getRange(found+1,colReply+1).setValue((parseInt(data[found][colReply])||0)+1);
    sh.getRange(found+1,colStatus+1).setValue('REPLY');
    sh.getRange(found+1,colLast+1).setValue(oggi);
    promuoviLead(email);
  } else if (event === 'email_opened') {
    sh.getRange(found+1,colOpen+1).setValue((parseInt(data[found][colOpen])||0)+1);
    sh.getRange(found+1,colLast+1).setValue(oggi);
  } else if (event === 'lead_clicked' || event === 'email_clicked') {
    const colClick = hdr.indexOf('click');
    sh.getRange(found+1,colClick+1).setValue((parseInt(data[found][colClick])||0)+1);
  }
  return jsonOut({ok:true, email:email, event:event});
}

// =========================================================
// Promuovi Instantly reply → Email Outreach pipeline
// =========================================================
function promuoviLead(email) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const src = ss.getSheetByName(TAB_OUTR_INST);
  const dst = ss.getSheetByName(TAB_EMAIL_OUTREACH);
  const data = src.getDataRange().getValues();
  const hdr = data[0];
  const colEmail = hdr.indexOf('email');
  email = email.toLowerCase();
  for (let i=1;i<data.length;i++){
    if ((data[i][colEmail]||'').toLowerCase() === email) {
      const r = data[i];
      const existing = dst.getRange('H:H').getValues();
      for (let j=0;j<existing.length;j++) if ((existing[j][0]||'').toLowerCase()===email) return;

      const idOpp = 'INST-LIVE-'+Utilities.getUuid().substring(0,8).toUpperCase();
      const oggi = Utilities.formatDate(new Date(),'Europe/Rome','dd/MM/yyyy');
      dst.appendRow([
        idOpp, oggi, 'Email Outreach', 'P0 ASAP',
        r[5], (r[3]+' '+r[4]).trim(), r[6],
        r[2], r[7], '', r[8], '', r[9],
        'Instantly-Live-Reply', 'Niccolò',
        '🔥 Qualificato','70','','','Telesales B2B','','','',
        'Chiamare entro 24h', oggi, oggi, '1',
        'Reply ricevuta su Instantly. Engagement: aperture='+r[13]+' click='+r[14],
        'Open',''
      ]);
      Logger.log('Promosso '+email+' → Email Outreach');
      return;
    }
  }
}

// =========================================================
// Cron orario: pull Instantly leads via API
// =========================================================
function pullInstantlyAll() {
  const key = PropertiesService.getScriptProperties().getProperty('INSTANTLY_KEY') || INSTANTLY_KEY_FALLBACK;
  if (!key) { Logger.log('INSTANTLY_KEY mancante'); return; }
  const headers = {'Authorization':'Bearer '+key,'Content-Type':'application/json'};
  const camps = JSON.parse(UrlFetchApp.fetch('https://api.instantly.ai/api/v2/campaigns?limit=100',
    {headers:{'Authorization':'Bearer '+key}}).getContentText()).items || [];

  const ss = SpreadsheetApp.openById(SHEET_ID);
  const sh = ss.getSheetByName(TAB_OUTR_INST);
  const existingEmails = new Set();
  const colE = sh.getRange('C:C').getValues();
  for (let i=0;i<colE.length;i++) if (colE[i][0]) existingEmails.add(String(colE[i][0]).toLowerCase());

  const newRows = [];
  for (const c of camps) {
    let starting = null;
    while (true) {
      const body = {campaign: c.id, limit: 100};
      if (starting) body.starting_after = starting;
      const res = JSON.parse(UrlFetchApp.fetch('https://api.instantly.ai/api/v2/leads/list',
        {method:'post', contentType:'application/json', headers:headers, payload:JSON.stringify(body),
         muteHttpExceptions:true}).getContentText());
      const items = res.items || [];
      if (!items.length) break;
      for (const L of items) {
        const em = (L.email||'').toLowerCase().trim();
        if (!em || existingEmails.has(em)) continue;
        existingEmails.add(em);
        newRows.push([
          (L.timestamp_created||'').substring(0,10),
          (L.timestamp_last_touch||'').substring(0,10),
          em, L.first_name||'', L.last_name||'',
          L.company_name||'', '', L.phone||'', L.website||'', '', '',
          c.name, 'status:'+(L.status||'?'),
          String(L.email_open_count||0), String(L.email_click_count||0),
          String(L.email_reply_count||0), '', '', '',
          'Instantly-API-Cron', L.id||'',
          (L.personalization||'').substring(0,200)
        ]);
      }
      starting = res.next_starting_after;
      if (!starting) break;
    }
  }
  if (newRows.length) {
    sh.getRange(sh.getLastRow()+1,1,newRows.length,newRows[0].length).setValues(newRows);
  }
  Logger.log('pullInstantlyAll: +'+newRows.length+' nuovi lead');
}

// =========================================================
// Cron: promuovi tutti i lead con reply_count>=1
// =========================================================
function promuoviInstantly() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const src = ss.getSheetByName(TAB_OUTR_INST);
  const data = src.getDataRange().getValues();
  const hdr = data[0];
  const cReply = hdr.indexOf('reply_count');
  const cEmail = hdr.indexOf('email');
  let promossi = 0;
  for (let i=1;i<data.length;i++){
    if (parseInt(data[i][cReply])>=1 && data[i][cEmail]) {
      promuoviLead(data[i][cEmail]);
      promossi++;
    }
  }
  Logger.log('promuoviInstantly: '+promossi+' lead processati');
}
