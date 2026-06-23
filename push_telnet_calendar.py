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
DARK=rgb('#0E0F12');GOLD=rgb('#D4AF37');GREEN=rgb('#2E7D32');LIGHT=rgb('#F4F1E8');WHITE=rgb('#FFFFFF');INK=rgb('#1B1C1F');REDBG=rgb('#FBE9E7')
name='Calendario operativo'; ncols=4; cw=[78,330,250,185]
R=[]
R.append(('title',['CALENDARIO OPERATIVO TELNET (16-26 GIUGNO 2026)','','','']))
R.append(('alert',['CRITICO: tutta la Settimana 2 parte solo se entro VEN 19/6 arrivano da TelNet trunk+TLS, interni, numero inbound e credenziali SMTP.','','','']))
R.append(('section',['SETTIMANA 1 — Rifinitura agente (noi) + raccolta dati telefonia (loro), in parallelo','','','']))
R.append(('header',['Data','Cosa facciamo noi','Cosa fa Marcello / TelNet','Esito atteso']))
w1=[
 ['Mar 16/6','Inviare la lista unica dei dati che ci servono + condividere il foglio. Avviare Fase 1: nome "Willy", tono, primo messaggio.','Conferma ricezione; gira la richiesta al tecnico (trunk/interni) e a chi gestisce le email.','Fase 1 avviata; richieste loro in moto'],
 ['Mer 17/6','Multilingue IT/EN; workflow instradamento reparti + gestione nominativi/omonimia; demo Cal.com pronta.','Prepara il DID dedicato e abilita il TLS sul Yeastar; raccoglie interni e orari di trasferimento.','Agente bilingue + instradamento pronti'],
 ['Gio 18/6','Rifinitura prompt sui flussi reali; test in simulazione; tool di trasferimento pre-configurato (placeholder interni).','Consegna credenziali SIP + numero inbound + email dedicata/SMTP; decide quale agenda.','Dati di telefonia consegnati'],
 ['Ven 19/6','Call di allineamento (30 min): chiusura delle 8 domande aperte. Se il trunk e pronto, assegniamo il numero e primo test reale.','Presente in call; conferma i punti aperti.','8 domande chiuse; eventuale 1a chiamata reale'],
 ['20-21/6','Buffer.','Buffer.','Recupero di eventuali ritardi'],
]
for d in w1: R.append(('data',d))
R.append(('section',['SETTIMANA 2 — Telefonia reale + go-live','','','']))
R.append(('header',['Data','Cosa facciamo noi','Cosa fa Marcello / TelNet','Esito atteso']))
w2=[
 ['Lun 22/6','Collegamento SIP; test chiamata reale; trasferimenti ai 3 interni; fallback email. Test del "vuoi rispondere?" (warm transfer).','Disponibile per i test; interni raggiungibili.','Telefonia reale funzionante'],
 ['Mar 23/6','Webhook email automatica + report; test fuori orario; Cal.com collegato all’agenda scelta.','Conferma email/agenda.','Notifiche e calendario attivi'],
 ['Mer 24/6','Test end-to-end di tutti i flussi con Marcello in ascolto; fix.','In ascolto; feedback.','Flussi validati'],
 ['Gio 25/6','Go-live soft (numero pubblicato o deviazione parziale); monitoraggio.','Pubblica o devia il numero.','Reception AI in linea'],
 ['Ven 26/6','Review della settimana; report delle prime chiamate; lista migliorie KB.','Feedback sulle prime chiamate.','Report + roadmap migliorie'],
]
for d in w2: R.append(('data',d))
R.append(('section',['DOPO — Fase 3 e 4 (su conferma)','','','']))
R.append(('note',['Fase 3: integrazione gestionale Mosaico (se espone API), invio link teleassistenza, report beta consolidato.','','','']))
R.append(('note',['Fase 4: definizione del modello di rivendita ai clienti TelNet (referente Marco Valori).','','','']))

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
    elif kind=='alert':
        reqs+=[merge(idx),fmt(idx,idx+1,0,ncols,backgroundColor=REDBG,textFormat={'foregroundColor':rgb('#B00020'),'bold':True,'fontSize':10},wrapStrategy='WRAP',padding={'top':5,'bottom':5,'left':8})]
    elif kind=='section':
        reqs+=[merge(idx),fmt(idx,idx+1,0,ncols,backgroundColor=GOLD,textFormat={'foregroundColor':DARK,'bold':True,'fontSize':10},wrapStrategy='WRAP',padding={'top':4,'bottom':4,'left':8})]
    elif kind=='header':
        reqs.append(fmt(idx,idx+1,0,ncols,backgroundColor=DARK,textFormat={'foregroundColor':WHITE,'bold':True,'fontSize':9},wrapStrategy='WRAP',verticalAlignment='MIDDLE',padding={'top':4,'bottom':4,'left':6}))
    elif kind=='data':
        reqs.append(fmt(idx,idx+1,0,ncols,wrapStrategy='WRAP',verticalAlignment='TOP',textFormat={'fontSize':9,'foregroundColor':INK},padding={'top':3,'bottom':3,'left':6}))
        reqs.append(fmt(idx,idx+1,0,1,textFormat={'fontSize':9,'bold':True,'foregroundColor':INK}))
        reqs.append(fmt(idx,idx+1,3,4,textFormat={'fontSize':9,'bold':True,'foregroundColor':GREEN}))
    elif kind=='note':
        reqs+=[merge(idx),fmt(idx,idx+1,0,ncols,wrapStrategy='WRAP',verticalAlignment='TOP',textFormat={'fontSize':9,'foregroundColor':INK},padding={'top':3,'bottom':3,'left':10})]
reqs.append({'updateSheetProperties':{'properties':{'sheetId':sid,'gridProperties':{'frozenRowCount':2}},'fields':'gridProperties.frozenRowCount'}})
svc.spreadsheets().batchUpdate(spreadsheetId=SID,body={'requests':reqs}).execute()
print('OK tab Calendario operativo')
