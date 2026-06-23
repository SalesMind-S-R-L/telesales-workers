#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crea 4 tab (un topic ciascuno) nel foglio TelNet kickoff, formattati dark/gold con esiti colorati."""
import warnings; warnings.filterwarnings('ignore')
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SID = '1FouyBIaKCT92zfOXVoqJlArhC5iPvIRIHLoz9b4TcMM'
cred = Credentials.from_service_account_file('service-account.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets'])
svc = build('sheets', 'v4', credentials=cred)

def rgb(hexv):
    h = hexv.lstrip('#')
    return {'red': int(h[0:2],16)/255, 'green': int(h[2:4],16)/255, 'blue': int(h[4:6],16)/255}
DARK=rgb('#0E0F12'); GOLD=rgb('#D4AF37'); GREEN=rgb('#2E7D32'); AMBER=rgb('#B8860B')
RED=rgb('#B00020'); LIGHT=rgb('#F4F1E8'); WHITE=rgb('#FFFFFF'); INK=rgb('#1B1C1F')

VC = {'SÌ nativo': GREEN, 'SÌ via tool': AMBER, 'PARZIALE': AMBER, 'NO': RED,
      'Fatto': GREEN, 'Fase 1': AMBER, 'Fase 2': AMBER, 'Fase 3': AMBER, 'Fase 4': AMBER}

# ---------- topic definitions: list of (kind,row) where kind in title/legend/header/section/data/note/blank
def t_fattibilita():
    ncols=4; cw=[230,90,300,230]
    R=[]
    R.append(('title',['FATTIBILITÀ TECNICA CON ELEVENLABS','','','']))
    R.append(('legend',['Legenda esito: SÌ nativo = funzione integrata della piattaforma · SÌ via tool = via integrazione che costruiamo noi · PARZIALE = supportata in parte, da verificare · NO = non disponibile','','','']))
    R.append(('header',['Funzione','Esito','Come si realizza','Cosa serve / nota']))
    data=[
        ['Rispondere alle chiamate in entrata (reception H24)','SÌ nativo','Numero SIP assegnato all\'agente; risponde sempre, anche fuori orario.','Trunk attivo + numero inbound.'],
        ['Multilingue italiano/inglese con rilevamento automatico','SÌ nativo','System tool "Language detection": l\'agente cambia lingua e voce da solo quando il chiamante parla inglese.','Configurare le lingue sull\'agente.'],
        ['Instradamento ai reparti (commerciale, tecnico, amministrazione)','SÌ nativo','"Agent transfer" + "Workflows": rami con condizioni in linguaggio naturale o su variabili.','Numeri interni dei reparti.'],
        ['Instradamento per nominativo con gestione omonimia','PARZIALE','Nessuna rubrica nativa: la disambiguazione si costruisce nel prompt/workflow.','Elenco nomi/reparti da gestire.'],
        ['Trasferimento con annuncio all\'operatore ("ti chiama X, vuoi rispondere?")','PARZIALE','L\'annuncio (agent_message) è nativo solo con Twilio. Su trunk SIP il trasferimento è diretto (SIP REFER) senza annuncio. Il warm transfer con accetta/rifiuta NON è documentato come nativo.','Da testare su linea reale.'],
        ['Fallback se l\'interno non risponde (raccogli dati e fai richiamare)','PARZIALE','Il segnale no-answer esiste a fine chiamata, ma il rientro automatico all\'AI dopo un transfer fallito non è nativo. Si gestisce a monte sul centralino.','Regola Yeastar: se interno non risponde entro N squilli, rientro.'],
        ['Email automatica (chiamata persa / riepilogo fuori orario al reparto)','SÌ via tool','Webhook post-chiamata verso un nostro Apps Script che invia l\'email e scrive sul foglio.','Email dedicata + credenziali SMTP.'],
        ['Appuntamenti su calendario reale (verifica slot e prenota in chiamata)','SÌ nativo','Integrazione nativa Cal.com: l\'agente vede gli slot liberi e crea l\'evento in chiamata. Google Calendar via Cal.com.','Decidere quale agenda usano i clienti.'],
        ['Aprire un intervento sul gestionale (Mosaico/Mexal) durante la chiamata','SÌ via tool','"Server tool": l\'agente chiama l\'API del gestionale in tempo reale. Possibile solo se Mosaico espone API.','Documentazione/credenziali API Mosaico.'],
        ['Inviare link teleassistenza (Supremo) via SMS/WhatsApp','SÌ via tool','Server tool verso un provider di messaggistica (es. Twilio/WhatsApp Business).','Account provider messaggi. Alternativa: via email.'],
        ['Report delle chiamate (gestite / non gestite + note)','SÌ nativo','Webhook post-chiamata: trascrizione, riassunto, dati ed esito sul foglio. Già attivo oggi.','Nessuna dipendenza (già operativo).'],
        ['Telefonia dal loro centralino Yeastar (SIP trunk, no Twilio)','SÌ nativo','ElevenLabs accetta trunk SIP inbound (digest o IP), TCP 5060 / TLS 5061, instradamento per DID.','TLS + DID dedicato verso sip.rtc.elevenlabs.io.'],
        ['L\'AI che "impara da sola" in tempo reale dalle chiamate','NO','La knowledge base non si aggiorna da sola. Le migliorie le applichiamo noi.','Aggiornamenti KB periodici a cura nostra.'],
    ]
    for d in data: R.append(('data',d))
    R.append(('blank',['','','','']))
    R.append(('section',['PUNTI APERTI DA VERIFICARE SUL CAMPO','','','']))
    R.append(('note',['1) Trasferimento con annuncio + accetta/rifiuta: il flusso "warm" non è nativo su SIP (l\'annuncio dedicato esiste solo con Twilio, che loro non vogliono). Sul loro Yeastar il transfer sarà diretto. Da testare cosa accade su non risposta.','','','']))
    R.append(('note',['2) Rientro all\'AI dopo transfer fallito: non nativo. Soluzione: configurare sul Yeastar il rientro dopo N squilli, oppure per i reparti critici far raccogliere subito i dati senza trasferire.','','','']))
    R.append(('note',['Proposta: prima messa in linea con modello robusto e nativo (raccolta dati + trasferimento dove ha senso + email/foglio su mancata risposta). L\'annuncio "vuoi rispondere?" si verifica come secondo step su linea reale.','','','']))
    return ncols,cw,R

def t_flussi():
    ncols=4; cw=[150,55,420,180]
    R=[]
    R.append(('title',['FLUSSI DI CHIAMATA POSSIBILI','','','']))
    R.append(('legend',['Ogni flusso parte dalla risposta dell\'agente "Willy" e arriva a un esito tracciato sul foglio. I flussi convivono: l\'agente sceglie il percorso in base a ciò che dice il chiamante.','','','']))
    R.append(('header',['Flusso','Passo','Descrizione','Esito']))
    flows=[
        ('A — Richiesta chiara verso un reparto',[
            'Il chiamante dice subito cosa gli serve (es. "vorrei l\'assistenza tecnica").',
            'Willy identifica il reparto e, se in orario, trasferisce all\'interno corretto.',
            'Se l\'interno risponde, chiamata gestita; altrimenti passa al Flusso C.'],'trasferito / ricontatto tecnico'),
        ('B — Richiesta di una persona per nome',[
            'Il chiamante chiede una persona ("c\'è Marco?").',
            'Willy verifica il reparto; in caso di omonimia chiede un dettaglio.',
            'Trasferisce; in mancata risposta raccoglie i dati.'],'trasferito / ricontatto'),
        ('C — Operatore non disponibile / non risponde',[
            'Willy comunica che il collega non è raggiungibile ora.',
            'Raccoglie nome, azienda, telefono, email e motivo.',
            'Invia email al reparto e registra sul foglio.'],'ricontatto - [reparto]'),
        ('D — Chiamata fuori orario',[
            'Willy comunica gli orari (Lun-Ven 8:30-17:00).',
            'Raccoglie i dati e il motivo.',
            'Invia email di riepilogo per il richiamo successivo.'],'fuori orario - ricontatto'),
        ('E — Appuntamento',[
            'Il chiamante chiede un appuntamento o consulenza.',
            'Willy propone gli slot liberi (Cal.com) e fissa, o registra la preferenza.',
            'Conferma data e ora a voce e via email.'],'appuntamento'),
        ('F — Assistenza tecnica cliente',[
            'Il chiamante è un cliente con un problema in corso.',
            'Willy riconosce l\'urgenza, instrada al tecnico o apre un intervento (Mosaico).',
            'Se utile, invia il link teleassistenza (Supremo).'],'assistenza / intervento aperto'),
        ('G — Richiesta commerciale / preventivo',[
            'Il chiamante chiede prezzi o un preventivo.',
            'Willy NON comunica prezzi: un commerciale ricontatterà.',
            'Raccoglie esigenza e dati; trasferisce al commerciale se disponibile.'],'commerciale - preventivo'),
        ('H — Chiamante in inglese',[
            'Willy rileva l\'inglese e prosegue tutta la conversazione in inglese, stessi percorsi.'],'come sopra, con nota lingua'),
        ('I — Spam / non pertinente',[
            'Numeri di vendita, troll o chiamate fuori contesto.',
            'Willy resta professionale e chiude con cortesia.'],'spam / non pertinente'),
    ]
    for name,steps,esito in flows:
        for i,st in enumerate(steps):
            R.append(('data',[name if i==0 else '', str(i+1), st, esito if i==0 else '']))
    R.append(('blank',['','','','']))
    R.append(('section',['REGOLE TRASVERSALI','','','']))
    for r in ['Dati minimi se non si trasferisce: nome, azienda, telefono, email, motivo.',
              'Mai comunicare prezzi o impegni contrattuali: passano a un umano.',
              'Tono cordiale e professionale; nessun riferimento a sistemi, bot o tecnologia.',
              'Ogni chiamata chiude con un esito tracciato a foglio per il report.']:
        R.append(('note',[r,'','','']))
    return ncols,cw,R

def t_piano():
    ncols=3; cw=[470,110,90]
    R=[]
    R.append(('title',['PIANO OPERATIVO E RESPONSABILITÀ','','']))
    R.append(('legend',['La Fase 1 non dipende da nulla di loro e parte subito. Le fasi successive si sbloccano man mano che TelNet fornisce dati e accessi.','','']))
    R.append(('section',['COSA FACCIAMO NOI (TELESALES)','','']))
    R.append(('header',['Attività','Fase','Stato']))
    noi=[
        ['Agente reception in italiano + KB dal sito','-','Fatto'],
        ['Cattura dati chiamante, foglio Google + report post-chiamata','-','Fatto'],
        ['Landing demo brandizzata (telnetdemo.vercel.app)','-','Fatto'],
        ['Nome "Willy", tono cordiale/professionale, primo messaggio','Fase 1','Da fare'],
        ['Multilingue IT/EN con rilevamento automatico','Fase 1','Da fare'],
        ['Workflow instradamento reparti + nominativi/omonimia','Fase 1','Da fare'],
        ['Tool di trasferimento ai 3 interni (alla consegna numeri)','Fase 2','Da fare'],
        ['Webhook post-chiamata, email automatica (Apps Script)','Fase 2','Da fare'],
        ['Assegnazione numero inbound + test telefonata reale','Fase 2','Da fare'],
        ['Demo prenotazione su Cal.com','Fase 2','Da fare'],
        ['Server tool apertura interventi Mosaico (se API)','Fase 3','Da fare'],
        ['Server tool invio link teleassistenza via SMS/WhatsApp','Fase 3','Da fare'],
        ['Report beta (gestite/non gestite + note)','Fase 3','Da fare'],
    ]
    for d in noi: R.append(('data',d))
    R.append(('blank',['','','']))
    R.append(('section',['COSA DEVONO FARE LORO (TELNET / MARCELLO)','','']))
    R.append(('header',['Attività a carico TelNet','Effetto','']))
    loro=[
        ['Abilitare TLS sul trunk e instradare un DID dedicato verso sip.rtc.elevenlabs.io','Sblocca Fase 2',''],
        ['Fornire credenziali SIP (registration: host, username, password, porta)','Sblocca Fase 2',''],
        ['Numeri interni dei reparti + orari di trasferimento','Sblocca Fase 2',''],
        ['Numero pubblico inbound da assegnare all\'agente','Sblocca Fase 2',''],
        ['Email dedicata + credenziali SMTP per le notifiche','Sblocca Fase 2',''],
        ['Confermare quale agenda/calendario usano per gli appuntamenti','Sblocca Fase 2',''],
        ['Documentazione/credenziali API gestionale Mosaico (se vogliono interventi)','Sblocca Fase 3',''],
        ['Decidere se inviare link teleassistenza e con quale canale','Sblocca Fase 3',''],
        ['Contenuti KB aggiuntivi: FAQ, procedure, casistiche (NO listini)','Continuo',''],
        ['Modello di rivendita ai loro clienti (referente Marco Valori)','Fase 4',''],
    ]
    for d in loro: R.append(('data',d))
    R.append(('blank',['','','']))
    R.append(('section',['LE FASI IN BREVE','','']))
    for r in ['Fase 1 — Subito, senza dipendenze: rifinitura agente (nome, tono, multilingue, instradamento). Lavoriamo da soli.',
              'Fase 2 — Telefonia reale: con trunk, interni, numero e SMTP colleghiamo agente, trasferimenti ed email. Test su chiamata vera.',
              'Fase 3 — Integrazioni: gestionale Mosaico, link teleassistenza, report beta.',
              'Fase 4 — Rivendita: modello con cui TelNet rivende l\'AI ai propri clienti.']:
        R.append(('note',[r,'','']))
    R.append(('blank',['','','']))
    R.append(('section',['DOMANDE APERTE DA CHIUDERE CON LORO','','']))
    for r in ['Il trunk è in sola registration (no IP statico): possono instradare un DID dedicato a noi e abilitare TLS?',
              'Quali interni esattamente e in quali orari l\'agente deve trasferire invece di far richiamare?',
              'Sul "vuoi rispondere?": accettano che la prima versione abbia trasferimento diretto (lo testiamo) e si rifinisca dopo?',
              'Quale agenda per gli appuntamenti: Cal.com nostro, Google Calendar dedicato o il loro gestionale?',
              'Mosaico espone API per aprire interventi? Chi dà la documentazione?',
              'Vogliono il link teleassistenza via SMS/WhatsApp (serve account provider) o basta email/voce?',
              'Email dedicata: quale indirizzo e quale provider SMTP?',
              'Tempi: data realistica per trunk + interni + numero, per pianificare la Fase 2?']:
        R.append(('note',[r,'','']))
    return ncols,cw,R

def t_mercato():
    ncols=3; cw=[230,330,160]
    R=[]
    R.append(('title',['RICERCA DI MERCATO — AI VOICE INBOUND','','']))
    R.append(('legend',['Mercato, concorrenti, prezzi e posizionamento per TelNet come telco che può rivendere il servizio. Le stime macro variano tra le fonti: ordini di grandezza.','','']))
    R.append(('section',['1. MERCATO E CRESCITA','','']))
    for r in ['Mercato AI voice agents ~2,4-2,5 mld USD (2024-2025), CAGR ~35%, proiezioni 35-47 mld entro 2033-2034.',
              'Adozione: ~34% PMI USA (10-500 dip.) con voice AI in uso/pilota; punta ~41% in ambito medico/dentistico.',
              'Soglia qualità: latenza < ~300 ms e voce naturale = fattori che fanno accettare o rifiutare il servizio.',
              'Europa/Italia: dati scarsi (mercato EU ~4,7 mld USD entro 2030); l\'italiano è area poco presidiata, quindi opportunità.']:
        R.append(('note',[r,'','']))
    R.append(('blank',['','','']))
    R.append(('section',['2. PRINCIPALI PIATTAFORME','','']))
    R.append(('header',['Piattaforma','Posizionamento','Note']))
    for d in [['ElevenLabs Agents','Qualità voce (TTS) al top, ottimo italiano','Quella che usiamo'],
              ['Vapi / Retell AI','Developer-first, infrastruttura al minuto','Da ~0,05 $/min'],
              ['Bland AI','Voice agent enterprise end-to-end','~0,09 $/min'],
              ['Synthflow','No-code, white-label nativo','Comodo per reseller, fino ~0,20 $/min'],
              ['PolyAI','Customer service vocale enterprise','Prezzo a preventivo'],
              ['Yeastar AI Receptionist','AI nativa nel PBX (da apr 2026)','Upsell diretto per chi vende già Yeastar']]:
        R.append(('data',d))
    R.append(('note',['Air AI da escludere (chiuso fine 2024 + azione FTC). Player italiani per credibilità lingua/GDPR: CuDriEc, Vocalis AI, Teslatel, AND Italia, Zudu.AI; lato centralino, Imagicle.','','']))
    R.append(('blank',['','','']))
    R.append(('section',['3. MODELLI DI PREZZO (AL CLIENTE FINALE PMI)','','']))
    for r in ['Setup una-tantum: 150-800 euro (fino a 1.500+ con integrazioni sul gestionale).',
              'Canone mensile: 150-600 euro/mese per la PMI tipica, spesso con pacchetti di minuti inclusi.',
              'Costo al minuto: 0,05-0,15 euro al cliente. I prezzi "vetrina" delle piattaforme vanno moltiplicati per il costo reale all-in (LLM+voce+telefonia): spesso 2-3x.']:
        R.append(('note',[r,'','']))
    R.append(('blank',['','','']))
    R.append(('section',['4. SETTORI A PIÙ ALTA DOMANDA','','']))
    for r in ['Studi medici e dentistici (caso più forte: prenotazioni/disdette H24, alto costo della chiamata persa).',
              'Immobiliare (qualifica lead, prenotazione visite).',
              'Studi professionali e PMI di servizi (accoglienza H24, FAQ, smistamento, dati a CRM).',
              'Retail/e-commerce e le telco stesse. Denominatore: molte chiamate ripetitive + costo alto della chiamata persa + orari limitati.']:
        R.append(('note',[r,'','']))
    R.append(('blank',['','','']))
    R.append(('section',['5. PERCHÉ TELNET È BEN POSIZIONATA A RIVENDERE','','']))
    for r in ['La parte difficile è già loro: telefonia reale, SIP, numerazioni, instradamento. È la barriera che blocca le agenzie marketing.',
              'Bundle col centralino: "il tuo centralino che ora risponde da solo, H24, in italiano" è un upsell naturale.',
              'Relazione e fiducia esistenti: vendono già un servizio business-critical; aggiungere l\'AI aumenta retention e ricavo per cliente.',
              'Margini ricorrenti: il white-label tipico ha margini lordi alti su ricavo mensile ricorrente.',
              'Contesto: Yeastar stessa ha lanciato (apr 2026) un AI Receptionist nativo nel PBX via partner: il canale telco è dove spinge il mercato.']:
        R.append(('note',[r,'','']))
    R.append(('blank',['','','']))
    R.append(('section',['6. BARRIERE E FATTORI DI SUCCESSO','','']))
    for r in ['Frenano: latenza, voce robotica, scarsa integrazione col gestionale, dubbi GDPR, scetticismo da casi negativi.',
              'Fanno vincere: fallback umano ben progettato (l\'AI passa all\'umano con la trascrizione), scope ristretto ad alto volume, integrazione col gestionale, voce italiana naturale, telefonia robusta.',
              'Per TelNet: vendere su affidabilità e referenze, mettere nero su bianco la conformità GDPR, evitare promesse esagerate.',
              'Cosa significa: posizionarsi non come "software AI" (commodity) ma come "il tuo centralino che risponde da solo, H24, in italiano". Il progetto TelNet è il primo caso pilota.',
              'Fonti: Grand View Research, Market.us, Ringly, Speechmatics, Retell, Synthflow, Viirtue, Famulor, Yeastar/PRNewswire, CuDriEc.']:
        R.append(('note',[r,'','']))
    return ncols,cw,R

TOPICS=[('Fattibilità ElevenLabs',t_fattibilita),
        ('Flussi di chiamata',t_flussi),
        ('Piano operativo',t_piano),
        ('Ricerca di mercato',t_mercato)]

# remove existing tabs with same names (idempotent)
meta=svc.spreadsheets().get(spreadsheetId=SID).execute()
existing={sh['properties']['title']:sh['properties']['sheetId'] for sh in meta['sheets']}
del_reqs=[{'deleteSheet':{'sheetId':existing[name]}} for name,_ in TOPICS if name in existing]
if del_reqs:
    svc.spreadsheets().batchUpdate(spreadsheetId=SID,body={'requests':del_reqs}).execute()

for name,fn in TOPICS:
    ncols,cw,R=fn()
    add=svc.spreadsheets().batchUpdate(spreadsheetId=SID,body={'requests':[
        {'addSheet':{'properties':{'title':name,'gridProperties':{'rowCount':len(R)+5,'columnCount':ncols}}}}]}).execute()
    sid=add['replies'][0]['addSheet']['properties']['sheetId']
    values=[row for _,row in R]
    svc.spreadsheets().values().update(spreadsheetId=SID,range=f"'{name}'!A1",
        valueInputOption='RAW',body={'values':values}).execute()
    reqs=[]
    # column widths
    for i,w in enumerate(cw):
        reqs.append({'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'COLUMNS','startIndex':i,'endIndex':i+1},'properties':{'pixelSize':w},'fields':'pixelSize'}})
    def fmt(r0,r1,c0,c1,**cell):
        return {'repeatCell':{'range':{'sheetId':sid,'startRowIndex':r0,'endRowIndex':r1,'startColumnIndex':c0,'endColumnIndex':c1},'cell':{'userEnteredFormat':cell},'fields':'userEnteredFormat('+','.join(cell.keys())+')'}}
    for idx,(kind,row) in enumerate(R):
        if kind=='title':
            reqs.append({'mergeCells':{'range':{'sheetId':sid,'startRowIndex':idx,'endRowIndex':idx+1,'startColumnIndex':0,'endColumnIndex':ncols},'mergeType':'MERGE_ALL'}})
            reqs.append(fmt(idx,idx+1,0,ncols,backgroundColor=DARK,
                textFormat={'foregroundColor':GOLD,'bold':True,'fontSize':14},
                verticalAlignment='MIDDLE',padding={'top':6,'bottom':6,'left':8}))
            reqs.append({'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'ROWS','startIndex':idx,'endIndex':idx+1},'properties':{'pixelSize':34},'fields':'pixelSize'}})
        elif kind=='legend':
            reqs.append({'mergeCells':{'range':{'sheetId':sid,'startRowIndex':idx,'endRowIndex':idx+1,'startColumnIndex':0,'endColumnIndex':ncols},'mergeType':'MERGE_ALL'}})
            reqs.append(fmt(idx,idx+1,0,ncols,backgroundColor=LIGHT,
                textFormat={'foregroundColor':INK,'italic':True,'fontSize':9},wrapStrategy='WRAP',padding={'top':4,'bottom':4,'left':8}))
        elif kind=='section':
            reqs.append({'mergeCells':{'range':{'sheetId':sid,'startRowIndex':idx,'endRowIndex':idx+1,'startColumnIndex':0,'endColumnIndex':ncols},'mergeType':'MERGE_ALL'}})
            reqs.append(fmt(idx,idx+1,0,ncols,backgroundColor=GOLD,
                textFormat={'foregroundColor':DARK,'bold':True,'fontSize':10},padding={'top':4,'bottom':4,'left':8}))
        elif kind=='header':
            reqs.append(fmt(idx,idx+1,0,ncols,backgroundColor=DARK,
                textFormat={'foregroundColor':WHITE,'bold':True,'fontSize':9},wrapStrategy='WRAP',verticalAlignment='MIDDLE',padding={'top':4,'bottom':4,'left':6}))
        elif kind=='data':
            reqs.append(fmt(idx,idx+1,0,ncols,wrapStrategy='WRAP',verticalAlignment='TOP',
                textFormat={'fontSize':9,'foregroundColor':INK},padding={'top':3,'bottom':3,'left':6}))
            # bold first col
            reqs.append(fmt(idx,idx+1,0,1,textFormat={'fontSize':9,'bold':True,'foregroundColor':INK}))
            # verdict color on esito col (col 1) if matches
            val=row[1] if len(row)>1 else ''
            if val in VC:
                reqs.append(fmt(idx,idx+1,1,2,textFormat={'fontSize':9,'bold':True,'foregroundColor':VC[val]}))
        elif kind=='note':
            reqs.append({'mergeCells':{'range':{'sheetId':sid,'startRowIndex':idx,'endRowIndex':idx+1,'startColumnIndex':0,'endColumnIndex':ncols},'mergeType':'MERGE_ALL'}})
            reqs.append(fmt(idx,idx+1,0,ncols,wrapStrategy='WRAP',verticalAlignment='TOP',
                textFormat={'fontSize':9,'foregroundColor':INK},padding={'top':3,'bottom':3,'left':10}))
    # freeze top rows (title+legend or title only)
    frozen=2 if R[1][0] in ('legend','section') else 1
    reqs.append({'updateSheetProperties':{'properties':{'sheetId':sid,'gridProperties':{'frozenRowCount':frozen}},'fields':'gridProperties.frozenRowCount'}})
    svc.spreadsheets().batchUpdate(spreadsheetId=SID,body={'requests':reqs}).execute()
    print('OK tab:',name)
print('FATTO — 4 tab creati su', f'https://docs.google.com/spreadsheets/d/{SID}/edit')
