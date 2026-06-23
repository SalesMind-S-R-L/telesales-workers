#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import warnings; warnings.filterwarnings('ignore')
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
SID='1FouyBIaKCT92zfOXVoqJlArhC5iPvIRIHLoz9b4TcMM'
cred=Credentials.from_service_account_file('service-account.json',scopes=['https://www.googleapis.com/auth/spreadsheets'])
svc=build('sheets','v4',credentials=cred)
def rgb(h):
    h=h.lstrip('#'); return {'red':int(h[0:2],16)/255,'green':int(h[2:4],16)/255,'blue':int(h[4:6],16)/255}
DARK=rgb('#0E0F12');GOLD=rgb('#D4AF37');GREEN=rgb('#2E7D32');LIGHT=rgb('#F4F1E8');WHITE=rgb('#FFFFFF');INK=rgb('#1B1C1F');RED=rgb('#B00020');GREY=rgb('#6B6E76');ANSWERBG=rgb('#FFFDF5')
name='Domande per Marcello'; ncols=4; cw=[150,360,95,300]
R=[]
R.append(('title',['DOMANDE PER MARCELLO (compilare la colonna Risposta)','','','']))
R.append(('legend',['BLOCCANTE = senza questa risposta non possiamo costruire lo step successivo. INFO = utile ma non blocca. Scrivi le risposte nella colonna a destra.','','','']))
R.append(('header',['Area','Domanda','Priorità','Risposta']))
def sec(t): R.append(('section',[t,'','','']))
def q(area,dom,prio): R.append(('data',[area,dom,prio,'']))
sec('A. TELEFONIA E TEST')
q('Telefonia','Qual è il numero esatto su cui facciamo arrivare la chiamata di test (+39 0574 814928 o un DDI dedicato)?','BLOCCANTE')
q('Telefonia','Hai deviato quel numero sul trunk verso il nostro server in TLS?','BLOCCANTE')
q('Telefonia','Quanti canali contemporanei ti dà il contratto voce (1-10)?','INFO')
sec('B. REPARTI E TRASFERIMENTI')
q('Reparti','Numeri interni reali dei 3 reparti (amministrativo, tecnico, commerciale): confermi 2000/2001/2003 o quali sono?','BLOCCANTE')
q('Reparti','Un trunk solo o uno per reparto?','BLOCCANTE')
q('Reparti','Elenco nomi → interno per gestire l\'omonimia (i vari "Marco": Valori, Vannucchi, Marini Grassi… chi risponde a quale interno).','BLOCCANTE')
q('Reparti','In quali orari l\'AI trasferisce davvero e quando invece solo raccolta + email? Gli 8:30-17:00 valgono per tutti i reparti?','BLOCCANTE')
q('Reparti','Conferma comportamento se l\'interno è occupato o non risponde: "ti faccio ricontattare" + email all\'interno coi dettagli.','INFO')
q('Reparti','Email di ogni reparto per le notifiche.','BLOCCANTE')
sec('C. EMAIL E NOTIFICHE')
q('Email','Avete creato l\'email dedicata (es. aivoicetelnet@telnet.it) e le credenziali SMTP (server in/out, porta, user, password)?','BLOCCANTE')
q('Email','A quali indirizzi mandiamo le notifiche per ogni reparto e per il fuori orario?','BLOCCANTE')
sec('D. CONTENUTI / KNOWLEDGE BASE')
q('Contenuti','Il file Word con servizi, interni, nomi, reparti, email, script casistiche e teleassistenza: quando lo mandate?','BLOCCANTE')
q('Contenuti','Oltre a prezzi/preventivi/coperture, quali altri argomenti l\'AI non deve gestire da sola?','INFO')
q('Contenuti','I consigli tecnici che può dare da sola (riavvio telefono/centralino…): confermi la lista?','INFO')
q('Contenuti','Teleassistenza: quale software esatto (Supremo?), come si manda il link, cosa farsi dare dal cliente (ID + password)?','INFO')
q('Contenuti','Ci sono pronunce particolari (dominio, nomi) da mettere in KB?','INFO')
sec('E. APPUNTAMENTI / CALENDARIO')
q('Appuntamenti','Quale calendario reale usate: Google Calendar dedicato, Cal.com o il vostro gestionale?','BLOCCANTE')
q('Appuntamenti','Quali reparti fissano appuntamenti e per cosa? Durata slot, orari prenotabili, reminder a chi?','INFO')
q('Appuntamenti','Volete ancora la qualifica con rating finanziario dell\'azienda prima di fissare l\'appuntamento? Con che fonte?','INFO')
sec('F. CRM / MOSAICO')
q('CRM','Mosaico: hanno risposto sull\'accesso API? Servono user/pass dedicati o API key + documentazione.','BLOCCANTE')
q('CRM','Cosa deve fare esattamente l\'AI su Mosaico (aprire un intervento: con quali campi)?','INFO')
q('CRM','Su Mexal serve qualcosa o solo Mosaico?','INFO')
sec('G. IDENTITÀ DELL\'AGENTE')
q('Agente','Confermate il nome "Willy" o ne preferite un altro?','INFO')
q('Agente','Solo italiano + inglese, oppure serve anche il cinese (Prato)?','INFO')
q('Agente','Confermate tono (cordiale/calmo/professionale) e il messaggio di apertura?','INFO')
sec('H. REPORT')
q('Report','Cosa volete nel report beta (gestite/non gestite + note) e dove: foglio, email, con che frequenza? Già per persona o generico?','INFO')
sec('I. RIVENDITA (più avanti)')
q('Rivendita','Quando ne parliamo con Marco Valori e con quale modello (SaaS ~300/mese o setup custom)?','INFO')

meta=svc.spreadsheets().get(spreadsheetId=SID).execute()
ex={sh['properties']['title']:sh['properties']['sheetId'] for sh in meta['sheets']}
if name in ex:
    svc.spreadsheets().batchUpdate(spreadsheetId=SID,body={'requests':[{'deleteSheet':{'sheetId':ex[name]}}]}).execute()
add=svc.spreadsheets().batchUpdate(spreadsheetId=SID,body={'requests':[{'addSheet':{'properties':{'title':name,'index':1,'gridProperties':{'rowCount':len(R)+5,'columnCount':ncols}}}}]}).execute()
sid=add['replies'][0]['addSheet']['properties']['sheetId']
svc.spreadsheets().values().update(spreadsheetId=SID,range=f"'{name}'!A1",valueInputOption='RAW',body={'values':[r for _,r in R]}).execute()
def fmt(r0,r1,c0,c1,**cell):
    return {'repeatCell':{'range':{'sheetId':sid,'startRowIndex':r0,'endRowIndex':r1,'startColumnIndex':c0,'endColumnIndex':c1},'cell':{'userEnteredFormat':cell},'fields':'userEnteredFormat('+','.join(cell.keys())+')'}}
def merge(idx):
    return {'mergeCells':{'range':{'sheetId':sid,'startRowIndex':idx,'endRowIndex':idx+1,'startColumnIndex':0,'endColumnIndex':ncols},'mergeType':'MERGE_ALL'}}
reqs=[]
for i,w in enumerate(cw):
    reqs.append({'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'COLUMNS','startIndex':i,'endIndex':i+1},'properties':{'pixelSize':w},'fields':'pixelSize'}})
for idx,(kind,row) in enumerate(R):
    if kind=='title':
        reqs+=[merge(idx),fmt(idx,idx+1,0,ncols,backgroundColor=DARK,textFormat={'foregroundColor':GOLD,'bold':True,'fontSize':14},verticalAlignment='MIDDLE',padding={'top':6,'bottom':6,'left':8})]
        reqs.append({'updateDimensionProperties':{'range':{'sheetId':sid,'dimension':'ROWS','startIndex':idx,'endIndex':idx+1},'properties':{'pixelSize':34},'fields':'pixelSize'}})
    elif kind=='legend':
        reqs+=[merge(idx),fmt(idx,idx+1,0,ncols,backgroundColor=LIGHT,textFormat={'foregroundColor':INK,'italic':True,'fontSize':9},wrapStrategy='WRAP',padding={'top':4,'bottom':4,'left':8})]
    elif kind=='section':
        reqs+=[merge(idx),fmt(idx,idx+1,0,ncols,backgroundColor=GOLD,textFormat={'foregroundColor':DARK,'bold':True,'fontSize':10},padding={'top':4,'bottom':4,'left':8})]
    elif kind=='header':
        reqs.append(fmt(idx,idx+1,0,ncols,backgroundColor=DARK,textFormat={'foregroundColor':WHITE,'bold':True,'fontSize':9},wrapStrategy='WRAP',verticalAlignment='MIDDLE',padding={'top':4,'bottom':4,'left':6}))
    elif kind=='data':
        reqs.append(fmt(idx,idx+1,0,ncols,wrapStrategy='WRAP',verticalAlignment='TOP',textFormat={'fontSize':9,'foregroundColor':INK},padding={'top':3,'bottom':3,'left':6}))
        reqs.append(fmt(idx,idx+1,0,1,textFormat={'fontSize':9,'bold':True,'foregroundColor':GREY}))
        col = RED if row[2]=='BLOCCANTE' else GREEN
        reqs.append(fmt(idx,idx+1,2,3,textFormat={'fontSize':9,'bold':True,'foregroundColor':col},horizontalAlignment='CENTER'))
        reqs.append(fmt(idx,idx+1,3,4,backgroundColor=ANSWERBG))
reqs.append({'updateSheetProperties':{'properties':{'sheetId':sid,'gridProperties':{'frozenRowCount':3,'frozenColumnCount':0}},'fields':'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'}})
# bordo verticale a sinistra della colonna Risposta
reqs.append({'updateBorders':{'range':{'sheetId':sid,'startRowIndex':2,'endRowIndex':len(R),'startColumnIndex':3,'endColumnIndex':4},'left':{'style':'SOLID','width':2,'color':GOLD}}})
svc.spreadsheets().batchUpdate(spreadsheetId=SID,body={'requests':reqs}).execute()
print('OK tab Domande per Marcello — righe:', len(R))
print('https://docs.google.com/spreadsheets/d/%s/edit'%SID)
