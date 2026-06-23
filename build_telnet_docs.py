#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera 4 PDF brandizzati TelNet: Fattibilita ElevenLabs, Flussi, Piano operativo, Mercato."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, NextPageTemplate, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

DARK = colors.HexColor('#0E0F12')
GOLD = colors.HexColor('#D4AF37')
INK = colors.HexColor('#1B1C1F')
GREY = colors.HexColor('#6B6E76')
LIGHT = colors.HexColor('#F4F1E8')
GREEN = colors.HexColor('#2E7D32')
AMBER = colors.HexColor('#B8860B')
RED = colors.HexColor('#B00020')
LINEGREY = colors.HexColor('#D8D8D8')

styles = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop('parent', styles['Normal'])
    return ParagraphStyle(name, parent=base, **kw)

body = S('body', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=5)
h1 = S('h1', fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=DARK, spaceBefore=10, spaceAfter=6)
h2 = S('h2', fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=DARK, spaceBefore=8, spaceAfter=3)
small = S('small', fontName='Helvetica', fontSize=8, leading=10.5, textColor=GREY)
cellh = S('cellh', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white)
cell = S('cell', fontName='Helvetica', fontSize=8.5, leading=11, textColor=INK)
cellb = S('cellb', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=INK)
bullet = S('bullet', parent=body, leftIndent=10, bulletIndent=0, spaceAfter=3)
covertitle = S('covertitle', fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=colors.white)
coversub = S('coversub', fontName='Helvetica', fontSize=12, leading=16, textColor=GOLD)
covermeta = S('covermeta', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#C7C7C7'))

PW, PH = A4
DOC_TITLE = ['']

def cover_bg(c, doc):
    c.setFillColor(DARK); c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, PH-6*mm, PW, 6*mm, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(22*mm, 92*mm, 40*mm, 1.4*mm, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 11); c.setFillColor(GOLD)
    c.drawString(22*mm, PH-20*mm, 'TELESALES')
    c.setFont('Helvetica', 8); c.setFillColor(colors.HexColor('#9A9A9A'))
    c.drawString(22*mm, PH-24.5*mm, 'AI Voice Inbound  ·  Documento riservato')
    c.setFont('Helvetica', 8); c.setFillColor(colors.HexColor('#8A8A8A'))
    c.drawString(22*mm, 14*mm, 'TelNet Italia  ·  Progetto reception AI  ·  16 giugno 2026')

def page_bg(c, doc):
    c.setFillColor(colors.white); c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, PH-4*mm, PW, 4*mm, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 8); c.setFillColor(GREY)
    c.drawString(20*mm, PH-12*mm, 'TELESALES  ×  TELNET ITALIA')
    c.setFont('Helvetica', 8); c.setFillColor(GREY)
    c.drawRightString(PW-20*mm, PH-12*mm, DOC_TITLE[0])
    c.setStrokeColor(LINEGREY); c.setLineWidth(0.5)
    c.line(20*mm, PH-14*mm, PW-20*mm, PH-14*mm)
    c.setFont('Helvetica', 7.5); c.setFillColor(GREY)
    c.drawString(20*mm, 10*mm, 'Telesales / Sales Mind SRL — riservato')
    c.drawRightString(PW-20*mm, 10*mm, 'Pag. %d' % doc.page)

def build(path, title, subtitle, story_fn):
    DOC_TITLE[0] = title
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                          topMargin=20*mm, bottomMargin=16*mm, title=title, author='Telesales')
    cover_frame = Frame(22*mm, 30*mm, PW-44*mm, 55*mm, id='cover')
    body_frame = Frame(20*mm, 16*mm, PW-40*mm, PH-34*mm, id='body')
    doc.addPageTemplates([
        PageTemplate(id='cover', frames=[cover_frame], onPage=cover_bg),
        PageTemplate(id='body', frames=[body_frame], onPage=page_bg),
    ])
    story = [Paragraph(title, covertitle), Spacer(1, 4*mm), Paragraph(subtitle, coversub),
             Spacer(1, 8*mm),
             Paragraph('Cliente: TelNet Italia (Prato) — reception telefonica AI inbound.<br/>'
                       'A cura di: Telesales / Sales Mind SRL.<br/>'
                       'Fonti tecniche: documentazione ufficiale ElevenLabs Agents. Fonti mercato: vedi note.',
                       covermeta),
             NextPageTemplate('body'), PageBreak()]
    story += story_fn()
    doc.build(story)
    print('OK', path)

def verdict_chip(text, color):
    return Paragraph(f'<font color="#{color.hexval()[2:]}"><b>{text}</b></font>', cell)

def tbl(data, colWidths, header_bg=DARK, style_extra=None):
    st = [
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT]),
        ('LINEBELOW', (0,0), (-1,-1), 0.4, LINEGREY),
        ('LINEBELOW', (0,0), (-1,0), 0.8, GOLD),
    ]
    if style_extra: st += style_extra
    t = Table(data, colWidths=colWidths, repeatRows=1)
    t.setStyle(TableStyle(st))
    return t

def P(t, st=body): return Paragraph(t, st)
def B(items, st=bullet):
    return [Paragraph('•&nbsp;&nbsp;' + i, st) for i in items]

# ---------------------------------------------------------------- DOC 1
def doc_fattibilita():
    s = []
    s.append(P('Fattibilità tecnica con ElevenLabs', h1))
    s.append(P('Per ogni funzione richiesta o emersa nella call di kickoff con TelNet abbiamo verificato, '
               'sulla documentazione ufficiale ElevenLabs Agents, se è realizzabile e con quale meccanismo. '
               'Legenda esito: <b><font color="#2E7D32">SÌ nativo</font></b> = funzione integrata della piattaforma; '
               '<b><font color="#B8860B">SÌ via tool</font></b> = realizzabile tramite tool/webhook o integrazione esterna; '
               '<b><font color="#B8860B">PARZIALE</font></b> = supportata in parte, richiede verifica o accorgimenti; '
               '<b><font color="#B00020">NO</font></b> = non disponibile.', body))
    s.append(Spacer(1, 3*mm))
    rows = [
        ['Funzione', 'Esito', 'Come si realizza', 'Cosa serve / nota'],
        ['Rispondere alle chiamate in entrata (reception H24)',
         ['SÌ nativo', GREEN],
         'Numero SIP assegnato all\'agente; risponde sempre, anche fuori orario.',
         'Trunk attivo + numero inbound.'],
        ['Multilingue italiano/inglese con rilevamento automatico',
         ['SÌ nativo', GREEN],
         'System tool "Language detection": l\'agente cambia lingua e voce da solo quando il chiamante parla inglese.',
         'Configurare le lingue sull\'agente.'],
        ['Instradamento ai reparti (commerciale, tecnico, amministrazione)',
         ['SÌ nativo', GREEN],
         '"Agent transfer" + "Workflows": rami con condizioni in linguaggio naturale o su variabili.',
         'Numeri interni dei reparti.'],
        ['Instradamento per nominativo con gestione omonimia',
         ['PARZIALE', AMBER],
         'Nessuna rubrica nativa: la disambiguazione (chiedere reparto/dettaglio in caso di omonimi) si costruisce nel prompt/workflow.',
         'Elenco nomi/reparti da gestire.'],
        ['Trasferimento con annuncio all\'operatore ("ti chiama X, vuoi rispondere?")',
         ['PARZIALE', AMBER],
         'L\'annuncio (agent_message) è nativo solo con Twilio. Su trunk SIP il trasferimento è "diretto" (SIP REFER) senza annuncio. Il warm transfer con accetta/rifiuta NON è documentato come nativo.',
         'Da testare sul campo. Vedi sezione "Punti aperti".'],
        ['Fallback se l\'interno non risponde (raccogli dati e fai richiamare)',
         ['PARZIALE', AMBER],
         'Il segnale "no-answer" esiste a fine chiamata, ma il rientro automatico all\'AI dopo un trasferimento fallito non è nativo. Si gestisce a monte (regola sul centralino) o evitando il trasferimento sui reparti critici.',
         'Regola Yeastar: se interno non risponde entro N squilli → rientro.'],
        ['Email automatica (chiamata persa / riepilogo fuori orario al reparto)',
         ['SÌ via tool', AMBER],
         'Non c\'è un "invia email" nativo: si usa il webhook post-chiamata verso un nostro Apps Script che invia l\'email e scrive sul foglio.',
         'Email dedicata + credenziali SMTP.'],
        ['Appuntamenti su calendario reale (verifica slot e prenota in chiamata)',
         ['SÌ nativo', GREEN],
         'Integrazione nativa Cal.com: l\'agente vede gli slot liberi e crea l\'evento durante la telefonata. Google Calendar si collega tramite Cal.com.',
         'Decidere quale agenda usano i clienti.'],
        ['Aprire un intervento sul gestionale (Mosaico/Mexal) durante la chiamata',
         ['SÌ via tool', AMBER],
         '"Server tool": l\'agente chiama l\'API del gestionale in tempo reale. Possibile solo se Mosaico espone API.',
         'Documentazione/credenziali API Mosaico.'],
        ['Inviare link teleassistenza (Supremo) via SMS/WhatsApp',
         ['SÌ via tool', AMBER],
         'Server tool verso un provider di messaggistica (es. Twilio/WhatsApp Business). Non esiste un "invia SMS" nativo dedicato.',
         'Account provider messaggi. Alternativa: invio via email.'],
        ['Report delle chiamate (gestite / non gestite + note)',
         ['SÌ nativo', GREEN],
         'Webhook post-chiamata: trascrizione, riassunto, dati raccolti ed esito finiscono sul foglio. Già attivo oggi.',
         'Nessuna dipendenza (già operativo).'],
        ['Telefonia dal loro centralino Yeastar (SIP trunk, no Twilio)',
         ['SÌ nativo', GREEN],
         'ElevenLabs accetta trunk SIP inbound con autenticazione digest o IP, TCP 5060 / TLS 5061, instradamento per DID.',
         'TLS + DID dedicato verso sip.rtc.elevenlabs.io.'],
        ['L\'AI che "impara da sola" in tempo reale dalle chiamate',
         ['NO', RED],
         'La knowledge base non si aggiorna da sola. Le migliorie si applicano manualmente da noi.',
         'Aggiornamenti KB periodici a cura nostra.'],
    ]
    data = [[P(r[0], cellb) if i==0 else P(r[0], cell),
             verdict_chip(*r[1]) if i>0 else P('Esito', cellh),
             P(r[2], cell), P(r[3], cell)] for i, r in enumerate(rows)]
    data[0] = [P('Funzione', cellh), P('Esito', cellh), P('Come si realizza', cellh), P('Cosa serve / nota', cellh)]
    s.append(tbl(data, [46*mm, 22*mm, 56*mm, 46*mm]))
    s.append(Spacer(1, 4*mm))

    s.append(P('Sintesi', h2))
    s.append(P('Tutto ciò che TelNet ha chiesto è realizzabile, ma su due livelli diversi. '
               'La maggior parte delle funzioni (risposta, multilingue, instradamento ai reparti, calendario Cal.com, '
               'report, SIP dal loro Yeastar) è <b>nativa</b> e attivabile subito. '
               'Un secondo gruppo (email, apertura interventi sul gestionale, link via SMS/WhatsApp) è pienamente fattibile ma '
               'tramite <b>integrazioni</b> che costruiamo noi e che dipendono da dati/accessi che loro devono fornire. '
               'Restano <b>due punti da testare</b> prima di prometterli al 100%.', body))

    s.append(P('Punti aperti da verificare sul campo', h2))
    for x in B([
        '<b>Trasferimento con annuncio + accetta/rifiuta.</b> Marcello ha chiesto che l\'agente dica all\'operatore '
        '"ti chiama X per Y, vuoi rispondere?" e passi la chiamata solo se accetta. Questo flusso "warm" non è documentato '
        'come nativo sul trunk SIP: l\'annuncio dedicato esiste solo con Twilio, che loro non vogliono usare. '
        'Sul loro Yeastar il trasferimento sarà "diretto" all\'interno. Va testato cosa succede su non risposta.',
        '<b>Rientro all\'AI dopo trasferimento fallito.</b> Se l\'interno non risponde, il rientro automatico all\'agente '
        'non è nativo. Soluzione pratica: configurare sul Yeastar che, dopo N squilli senza risposta, la chiamata torni '
        'a una casella o all\'AI; oppure, per i reparti dove il richiamo è accettabile, far raccogliere subito i dati '
        'all\'AI senza trasferire.',
    ]):
        s.append(x)
    s.append(Spacer(1, 2*mm))
    s.append(P('Proposta operativa: per la prima messa in linea adottiamo il modello più robusto e già nativo — '
               'l\'AS raccoglie nome/azienda/motivo, trasferisce ai reparti quando ha senso e, in caso di mancata risposta, '
               'invia email + scrive a foglio. L\'annuncio "vuoi rispondere?" lo verifichiamo come secondo step su una linea reale.',
               body))
    return s

# ---------------------------------------------------------------- DOC 2
def doc_flussi():
    s = []
    s.append(P('Flussi di chiamata possibili', h1))
    s.append(P('Schemi operativi della reception AI. Ogni flusso parte dalla risposta dell\'agente "Willy" e arriva a un esito '
               'tracciato sul foglio. I flussi convivono: l\'agente sceglie il percorso in base a ciò che dice il chiamante.', body))

    flows = [
        ('Flusso A — Richiesta chiara verso un reparto',
         ['Il chiamante dice subito cosa gli serve (es. "vorrei parlare con l\'assistenza tecnica").',
          'Willy identifica il reparto e, se in orario, trasferisce all\'interno corretto.',
          'Se l\'interno risponde → chiamata gestita. Se non risponde → passa al Flusso C.',
          'Esito: "trasferito - tecnico" oppure "ricontatto tecnico".']),
        ('Flusso B — Richiesta di una persona per nome',
         ['Il chiamante chiede una persona ("c\'è Marco?").',
          'Willy verifica il reparto della persona; in caso di omonimia chiede un dettaglio ("Marco del commerciale o dell\'amministrazione?").',
          'Trasferisce all\'interno giusto; in mancata risposta raccoglie i dati.',
          'Esito: "trasferito" o "ricontatto".']),
        ('Flusso C — Operatore non disponibile / non risponde',
         ['Willy comunica che il collega non è raggiungibile in questo momento.',
          'Raccoglie nome, azienda, telefono, email e motivo.',
          'Invia email di notifica al reparto competente e registra tutto sul foglio.',
          'Esito: "ricontatto - [reparto]".']),
        ('Flusso D — Chiamata fuori orario',
         ['Willy comunica gli orari di apertura (Lun-Ven 8:30-17:00).',
          'Raccoglie i dati e il motivo della chiamata.',
          'Invia email di riepilogo al reparto per il richiamo il giorno lavorativo successivo.',
          'Esito: "fuori orario - ricontatto".']),
        ('Flusso E — Appuntamento',
         ['Il chiamante chiede un appuntamento o una consulenza.',
          'Willy propone gli slot liberi (Cal.com) e fissa l\'incontro in diretta, oppure registra la preferenza sul foglio.',
          'Conferma data e ora a voce e via email.',
          'Esito: "appuntamento".']),
        ('Flusso F — Assistenza tecnica cliente',
         ['Il chiamante è un cliente con un problema in corso.',
          'Willy riconosce l\'urgenza, instrada al tecnico o, se concordato, apre un intervento sul gestionale (Mosaico).',
          'Se utile, invia il link alla teleassistenza (Supremo) via email/SMS.',
          'Esito: "assistenza" / "intervento aperto".']),
        ('Flusso G — Richiesta commerciale / preventivo',
         ['Il chiamante chiede prezzi o un preventivo.',
          'Willy NON comunica prezzi: spiega che un commerciale ricontatterà con la proposta.',
          'Raccoglie esigenza e dati, trasferisce al commerciale se disponibile, altrimenti registra il ricontatto.',
          'Esito: "commerciale - preventivo".']),
        ('Flusso H — Chiamante in inglese',
         ['Willy rileva l\'inglese e prosegue l\'intera conversazione in inglese, mantenendo gli stessi percorsi.',
          'Esito: come sopra, con nota lingua.']),
        ('Flusso I — Spam / chiamata non pertinente',
         ['Numeri di vendita, troll o chiamate fuori contesto.',
          'Willy resta professionale, non si fa trascinare e chiude con cortesia.',
          'Esito: "spam / non pertinente".']),
    ]
    for title, steps in flows:
        s.append(P(title, h2))
        for i, st in enumerate(steps, 1):
            s.append(Paragraph(f'<b><font color="#B8860B">{i}.</font></b>&nbsp;&nbsp;{st}', bullet))
    s.append(Spacer(1, 3*mm))
    s.append(P('Regole trasversali', h2))
    for x in B([
        'Dati minimi da raccogliere sempre che non si trasferisce: nome, azienda, telefono, email, motivo.',
        'Mai comunicare prezzi o impegni contrattuali: quelli passano a un umano.',
        'Tono cordiale e professionale; nessun riferimento a sistemi, bot o tecnologia.',
        'Ogni chiamata chiude con un esito tracciato a foglio per il report.',
    ]):
        s.append(x)
    return s

# ---------------------------------------------------------------- DOC 3
def doc_piano():
    s = []
    s.append(P('Piano operativo e responsabilità', h1))
    s.append(P('Chi fa cosa, in quale fase. Il progetto è diviso in blocchi: la Fase 1 non dipende da nulla di loro e parte subito; '
               'le fasi successive si sbloccano man mano che TelNet fornisce dati e accessi.', body))

    s.append(P('Cosa facciamo noi (Telesales)', h2))
    noi = [
        ['Agente reception in italiano + KB dal sito', 'Fatto', GREEN],
        ['Cattura dati chiamante → foglio Google + report post-chiamata', 'Fatto', GREEN],
        ['Landing demo brandizzata (telnetdemo.vercel.app)', 'Fatto', GREEN],
        ['Nome "Willy", tono cordiale/professionale, primo messaggio', 'Fase 1', AMBER],
        ['Multilingue IT/EN con rilevamento automatico', 'Fase 1', AMBER],
        ['Workflow instradamento reparti + gestione nominativi/omonimia', 'Fase 1', AMBER],
        ['Tool di trasferimento ai 3 interni (alla consegna numeri)', 'Fase 2', AMBER],
        ['Webhook post-chiamata → email automatica (Apps Script)', 'Fase 2', AMBER],
        ['Assegnazione numero inbound all\'agente + test telefonata reale', 'Fase 2', AMBER],
        ['Demo prenotazione su Cal.com', 'Fase 2', AMBER],
        ['Server tool apertura interventi su Mosaico (se API disponibili)', 'Fase 3', AMBER],
        ['Server tool invio link teleassistenza via SMS/WhatsApp', 'Fase 3', AMBER],
        ['Report beta (gestite/non gestite + note)', 'Fase 3', AMBER],
    ]
    data = [[P('Attività', cellh), P('Fase', cellh), P('', cellh)]]
    for a, f, col in noi:
        data.append([P(a, cell), verdict_chip(f, col), P('', cell)])
    s.append(tbl(data, [128*mm, 24*mm, 8*mm]))
    s.append(Spacer(1, 3*mm))

    s.append(P('Cosa devono fare loro (TelNet / Marcello)', h2))
    loro = [
        ['Abilitare TLS sul trunk e instradare un DID dedicato verso sip.rtc.elevenlabs.io', 'Sblocca Fase 2'],
        ['Fornire credenziali SIP (registration: host, username, password, porta)', 'Sblocca Fase 2'],
        ['Numeri interni dei reparti (commerciale, tecnico, amministrazione) e orari di trasferimento', 'Sblocca Fase 2'],
        ['Numero pubblico inbound da assegnare all\'agente', 'Sblocca Fase 2'],
        ['Email dedicata + credenziali SMTP per le notifiche automatiche', 'Sblocca Fase 2'],
        ['Confermare quale agenda/calendario usano per gli appuntamenti dei clienti', 'Sblocca Fase 2'],
        ['Documentazione/credenziali API del gestionale Mosaico (se vogliono apertura interventi)', 'Sblocca Fase 3'],
        ['Decidere se inviare il link teleassistenza e con quale canale (account provider)', 'Sblocca Fase 3'],
        ['Contenuti KB aggiuntivi: FAQ, procedure, casistiche (NO listini prezzi)', 'Continuo'],
        ['Modello di rivendita ai loro clienti (referente Marco Valori)', 'Fase 4'],
    ]
    data = [[P('Attività a carico TelNet', cellh), P('Effetto', cellh)]]
    for a, e in loro:
        data.append([P(a, cell), P(e, cellb)])
    s.append(tbl(data, [122*mm, 38*mm]))
    s.append(Spacer(1, 3*mm))

    s.append(P('Le fasi in breve', h2))
    for x in B([
        '<b>Fase 1 — Subito, senza dipendenze:</b> rifinitura agente (nome, tono, multilingue, instradamento logico). Lavoriamo da soli.',
        '<b>Fase 2 — Telefonia reale:</b> con trunk, interni, numero e SMTP colleghiamo l\'agente alla loro linea, trasferimenti ed email. Test su chiamata vera.',
        '<b>Fase 3 — Integrazioni:</b> gestionale Mosaico, link teleassistenza, report beta.',
        '<b>Fase 4 — Rivendita:</b> definizione del modello con cui TelNet rivende l\'AI ai propri clienti.',
    ]):
        s.append(x)

    s.append(P('Domande aperte da chiudere con loro', h2))
    for x in B([
        'Il trunk è in sola registration (no IP statico): confermano che possono instradare un DID dedicato a noi e abilitare il TLS?',
        'Quali sono esattamente gli interni e in quali orari l\'agente deve trasferire invece di raccogliere e far richiamare?',
        'Sul "vuoi rispondere?" prima del trasferimento: accettano che nella prima versione il trasferimento sia diretto (lo testiamo) e si rifinisca dopo?',
        'Quale agenda usano per gli appuntamenti: Cal.com nostro, un Google Calendar dedicato o il loro gestionale?',
        'Mosaico espone API per aprire interventi? Chi ci dà la documentazione?',
        'Vogliono davvero inviare il link teleassistenza via SMS/WhatsApp (serve un account provider) o basta via email/voce?',
        'Email dedicata: quale indirizzo e con quale provider SMTP?',
        'Tempi: qual è la data realistica per avere trunk + interni + numero, così pianifichiamo la Fase 2?',
    ]):
        s.append(x)
    return s

# ---------------------------------------------------------------- DOC 4
def doc_mercato():
    s = []
    s.append(P('Ricerca di mercato — AI Voice inbound', h1))
    s.append(P('Sintesi del mercato dei receptionist vocali AI, dei concorrenti, dei prezzi e del posizionamento, '
               'con la lettura specifica per TelNet come azienda di telecomunicazioni che può rivendere il servizio ai propri clienti. '
               'Le stime macro variano molto tra le fonti per differenze di definizione: vanno lette come ordini di grandezza.', body))

    s.append(P('1. Mercato e crescita', h2))
    for x in B([
        'Mercato AI voice agents stimato ~2,4-2,5 mld USD nel 2024-2025, con CAGR ~35% e proiezioni verso 35-47 mld entro 2033-2034 (Grand View Research, Market.us).',
        'Adozione concreta: stime Q1 2026 indicano ~34% delle PMI USA (10-500 dip.) con voice AI già in uso o in pilota; punta ~41% in ambito medico/dentistico.',
        'Soglia di qualità percepita: latenza sotto i ~300 ms e voce naturale sono i fattori che fanno accettare (o rifiutare) il servizio.',
        'Europa/Italia: dati granulari scarsi (mercato voice AI europeo stimato ~4,7 mld USD entro il 2030); l\'italiano resta un\'area poco presidiata e quindi un\'opportunità.',
    ]):
        s.append(x)

    s.append(P('2. Principali piattaforme', h2))
    rows = [
        ['Piattaforma', 'Posizionamento', 'Note'],
        ['ElevenLabs Agents', 'Qualità voce (TTS) al top, ottimo italiano', 'Bundle minuti + LLM passthrough; quella che usiamo'],
        ['Vapi / Retell AI', 'Developer-first, infrastruttura al minuto', 'Massima flessibilità, da ~0,05 $/min'],
        ['Bland AI', 'Voice agent enterprise end-to-end', '~0,09 $/min, finanziamenti rilevanti'],
        ['Synthflow', 'No-code, white-label nativo', 'Comodo per reseller/agenzie, fino a ~0,20 $/min'],
        ['PolyAI', 'Customer service vocale enterprise', 'Prezzo a preventivo, grandi clienti'],
        ['Yeastar AI Receptionist', 'AI nativa dentro il PBX (da apr 2026)', 'Rilevante: upsell diretto per chi vende già Yeastar'],
    ]
    data = [[P(c, cellh) for c in rows[0]]] + [[P(c, cellb) if i==0 else P(c, cell) for i,c in enumerate(r)] for r in rows[1:]]
    s.append(tbl(data, [40*mm, 66*mm, 54*mm]))
    s.append(P('Nota: Air AI è da escludere (servizio chiuso a fine 2024 e azione FTC con sanzione). '
               'Player italiani/localizzati per credibilità lingua e GDPR: CuDriEc, Vocalis AI, Teslatel, AND Italia, Zudu.AI; '
               'lato centralino, Imagicle.', small))
    s.append(Spacer(1, 2*mm))

    s.append(P('3. Modelli di prezzo (al cliente finale PMI)', h2))
    for x in B([
        '<b>Setup una-tantum:</b> €150-800 (fino a €1.500+ con integrazioni sul gestionale).',
        '<b>Canone mensile:</b> €150-600/mese per la PMI tipica, spesso con pacchetti di minuti inclusi.',
        '<b>Costo al minuto:</b> €0,05-0,15 al cliente. Attenzione: i prezzi "vetrina" delle piattaforme vanno moltiplicati per il costo reale all-in (LLM, voce, telefonia): in produzione si paga spesso 2-3x.',
    ]):
        s.append(x)

    s.append(P('4. Settori a più alta domanda', h2))
    for x in B([
        'Studi medici e dentistici (il caso più forte: prenotazioni/disdette H24, alto costo della chiamata persa).',
        'Immobiliare (qualifica lead, prenotazione visite).',
        'Studi professionali e PMI di servizi (accoglienza H24, FAQ, smistamento, dati a CRM).',
        'Retail/e-commerce (tracking ordini, resi) e, naturalmente, le telco stesse.',
        'Il denominatore comune: molte chiamate ripetitive + costo alto della chiamata persa + orari limitati.',
    ]):
        s.append(x)

    s.append(P('5. Perché TelNet è ben posizionata per rivendere', h2))
    for x in B([
        '<b>La parte difficile è già loro.</b> Il fattore di successo n.1 nel voice AI è gestire telefonia reale, SIP, numerazioni e instradamento: TelNet lo fa già di mestiere. È la barriera che blocca le agenzie marketing.',
        '<b>Bundle col centralino.</b> "Il tuo centralino che ora risponde da solo, H24, in italiano" è un upsell naturale sul prodotto che già vendono.',
        '<b>Relazione e fiducia esistenti.</b> Vendono già un servizio business-critical (il telefono): aggiungere l\'AI aumenta retention e ricavo per cliente, senza acquisizione da zero.',
        '<b>Margini ricorrenti.</b> Il modello white-label tipico ha margini lordi alti su ricavo mensile ricorrente: si passa dal progetto una-tantum a entrate ripetute.',
        '<b>Contesto.</b> Yeastar stessa ha lanciato (apr 2026) un AI Receptionist nativo nel PBX, distribuito via partner: segnale che il canale telco è esattamente dove il mercato sta spingendo.',
    ]):
        s.append(x)

    s.append(P('6. Barriere e fattori di successo', h2))
    for x in B([
        '<b>Frenano:</b> latenza, voce robotica, scarsa integrazione col gestionale, dubbi GDPR, scetticismo da casi negativi del settore.',
        '<b>Fanno vincere:</b> fallback umano ben progettato (l\'AI raccoglie il contesto e passa all\'umano con la trascrizione), scope ristretto ad alto volume, integrazione profonda col gestionale del cliente, voce italiana naturale e telefonia robusta.',
        '<b>Per TelNet:</b> vendere su affidabilità e referenze, mettere nero su bianco la conformità GDPR, evitare promesse esagerate.',
    ]):
        s.append(x)

    s.append(P('Cosa significa per TelNet', h2))
    s.append(P('Il posizionamento non è "vendere un software AI" (commodity a basso margine) ma "il tuo centralino che risponde da solo, '
               'H24, in italiano", venduto come bundle setup + canone + minuti sfruttando SIP e relazione già in casa. '
               'Verticali di partenza consigliati: studi medici/dentistici, poi immobiliare e studi professionali. '
               'Il progetto TelNet attuale è, di fatto, il primo caso pilota su cui costruire questa offerta.', body))
    s.append(Spacer(1, 2*mm))
    s.append(P('Fonti principali: Grand View Research, Market.us, Ringly, Speechmatics, Retell AI, Synthflow, Viirtue, '
               'Famulor, Yeastar/PRNewswire, CuDriEc. URL completi disponibili su richiesta.', small))
    return s

# ---------------------------------------------------------------- DOC 5
def doc_roadmap():
    s = []
    s.append(P('Roadmap operativa — 16-26 giugno 2026', h1))
    s.append(P('Noi lavoriamo subito sulle attività che non dipendono da TelNet (Fase 1), mentre Marcello in parallelo ci consegna '
               'i dati di telefonia. Quei dati sono il collo di bottiglia: tutto il go-live della seconda settimana dipende da lì.', body))
    s.append(Spacer(1, 1*mm))
    s.append(Table([[Paragraph('<b>CRITICO:</b> tutta la Settimana 2 parte solo se entro <b>venerdì 19/6</b> arrivano da TelNet '
                     'trunk+TLS, interni, numero inbound e credenziali SMTP.', cell)]],
                   colWidths=[160*mm],
                   style=TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FBE9E7')),
                                     ('BOX',(0,0),(-1,-1),0.6,RED),('LEFTPADDING',(0,0),(-1,-1),8),
                                     ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
                                     ('TEXTCOLOR',(0,0),(-1,-1),RED)])))
    s.append(Spacer(1, 3*mm))

    def week(title, rows):
        s.append(P(title, h2))
        data = [[P('Data', cellh), P('Noi (Telesales)', cellh), P('Marcello / TelNet', cellh), P('Esito atteso', cellh)]]
        for d in rows:
            data.append([P(d[0], cellb), P(d[1], cell), P(d[2], cell),
                         Paragraph(f'<font color="#2E7D32"><b>{d[3]}</b></font>', cell)])
        s.append(tbl(data, [18*mm, 60*mm, 50*mm, 32*mm]))
        s.append(Spacer(1, 3*mm))

    week('Settimana 1 — rifinitura agente (noi) + raccolta dati (loro)', [
        ['Mar 16/6', 'Inviare la lista unica dei dati che ci servono + condividere il foglio. Avviare Fase 1: nome "Willy", tono, primo messaggio.',
         'Conferma ricezione; gira la richiesta al tecnico (trunk/interni) e a chi gestisce le email.', 'Fase 1 avviata; richieste loro in moto'],
        ['Mer 17/6', 'Multilingue IT/EN; workflow instradamento reparti + gestione nominativi/omonimia; demo Cal.com pronta.',
         'Prepara il DID dedicato e abilita il TLS sul Yeastar; raccoglie interni e orari di trasferimento.', 'Agente bilingue + instradamento pronti'],
        ['Gio 18/6', 'Rifinitura prompt sui flussi reali; test in simulazione; tool di trasferimento pre-configurato (placeholder interni).',
         'Consegna credenziali SIP + numero inbound + email dedicata/SMTP; decide quale agenda.', 'Dati di telefonia consegnati'],
        ['Ven 19/6', 'Call di allineamento (30 min): chiusura delle 8 domande aperte. Se il trunk è pronto, assegniamo il numero e primo test reale.',
         'Presente in call; conferma i punti aperti.', '8 domande chiuse; eventuale 1ª chiamata reale'],
        ['20-21/6', 'Buffer.', 'Buffer.', 'Recupero di eventuali ritardi'],
    ])
    week('Settimana 2 — telefonia reale + go-live', [
        ['Lun 22/6', 'Collegamento SIP; test chiamata reale; trasferimenti ai 3 interni; fallback email. Test del "vuoi rispondere?" (warm transfer).',
         'Disponibile per i test; interni raggiungibili.', 'Telefonia reale funzionante'],
        ['Mar 23/6', 'Webhook email automatica + report; test fuori orario; Cal.com collegato all\'agenda scelta.',
         'Conferma email/agenda.', 'Notifiche e calendario attivi'],
        ['Mer 24/6', 'Test end-to-end di tutti i flussi con Marcello in ascolto; fix.', 'In ascolto; feedback.', 'Flussi validati'],
        ['Gio 25/6', 'Go-live soft (numero pubblicato o deviazione parziale); monitoraggio.', 'Pubblica o devia il numero.', 'Reception AI in linea'],
        ['Ven 26/6', 'Review della settimana; report delle prime chiamate; lista migliorie KB.', 'Feedback sulle prime chiamate.', 'Report + roadmap migliorie'],
    ])
    s.append(P('Dopo — Fase 3 e 4 (su conferma)', h2))
    for x in B([
        '<b>Fase 3:</b> integrazione gestionale Mosaico (se espone API), invio link teleassistenza, report beta consolidato.',
        '<b>Fase 4:</b> definizione del modello di rivendita ai clienti TelNet (referente Marco Valori).',
    ]):
        s.append(x)
    return s

# ---------------------------------------------------------------- DOC 6
def doc_test_tutorial():
    s = []
    s.append(P('Test chiamata live con Marcello', h1))
    s.append(P('<b>Lunedì 22 giugno 2026, ore 10:00.</b> Obiettivo: far entrare la prima chiamata vera dal trunk SIP del '
               'centralino Yeastar di TelNet fino all\'agente reception, e verificare che risposta, audio e codec funzionino. '
               'Questo documento è la guida operativa completa, passo per passo.', body))

    s.append(Table([[Paragraph('<b>Situazione di partenza (già verificata lato nostro):</b> il numero +39 0574 814928 è creato e '
                     'assegnato all\'agente "TelNet Italia - Reception"; il trunk inbound è in TLS con autenticazione a credenziali '
                     '(username 6701), nessun blocco IP, media flessibile (RTP o SRTP), codec G722/PCMA/PCMU. Marcello ha già attivato '
                     'il trunk in TLS sul suo Yeastar (certificato self-signed, va bene). Manca solo la prova: una telefonata reale.', cell)]],
                   colWidths=[160*mm],
                   style=TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),0.6,GOLD),
                                     ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                                     ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)])))
    s.append(Spacer(1, 3*mm))

    s.append(P('Chi fa cosa', h2))
    data = [[P('Ruolo', cellh), P('Responsabilità durante il test', cellh)]]
    for r in [['Marcello (TelNet)','Lato Yeastar: instrada un DID sul trunk ElevenLabs (o imposta una regola che manda al trunk le chiamate verso il numero) e fa partire la telefonata di prova. Tiene il telefono per ascoltare e parlare con l\'agente.'],
              ['Simone (Telesales)','Coordina la call con Marcello, lancia il monitor live, fa da "chiamante" se serve provare i flussi, dà l\'ok finale.'],
              ['Monitor (script)','Mostra in tempo reale l\'arrivo della chiamata, la trascrizione turno per turno e l\'esito. È la nostra prova oggettiva che tutto gira.']]:
        data.append([P(r[0], cellb), P(r[1], cell)])
    s.append(tbl(data, [34*mm, 126*mm]))
    s.append(Spacer(1, 3*mm))

    s.append(P('Fase 1 — Preparazione (entro venerdì o domenica sera)', h2))
    for x in B([
        'Confermare con Marcello giorno e ora: lunedì 22/6 alle 10:00, e che sarà raggiungibile in chiamata/WhatsApp per coordinarsi live.',
        'Chiedere a Marcello di avere pronto: il trunk TLS attivo (fatto), un DID o una regola di instradamento che porti la chiamata sul trunk, e un telefono per chiamare.',
        'Dalla nostra parte non serve modificare nulla: è già tutto configurato. Si fa solo il pre-flight la mattina.',
    ]):
        s.append(x)

    s.append(P('Fase 2 — Pre-flight, ore 9:45 (15 minuti prima)', h2))
    for x in B([
        'Aprire il terminale nella cartella del progetto e lanciare il monitor: <font name="Helvetica-Bold">python3 monitor_telnet_test.py</font>',
        'Il monitor fa da solo il controllo di prontezza (numero, trunk, credenziali, agente) e deve mostrare "TUTTO PRONTO".',
        'Lasciarlo in ascolto: registra le conversazioni già esistenti come baseline e aspetta la chiamata nuova.',
        'Mettersi in contatto con Marcello (telefonata o videocall) per dare il via insieme.',
    ]):
        s.append(x)

    s.append(P('Fase 3 — Esecuzione del test, ore 10:00', h2))
    for i, st in enumerate([
        'Marcello fa partire la chiamata verso il numero/DID che passa dal trunk ElevenLabs.',
        'Sul monitor, entro pochi secondi, deve comparire "CHIAMATA IN ARRIVO" con il numero del chiamante: è la conferma che la chiamata è arrivata a noi via SIP.',
        'L\'agente risponde con "TelNet Italia, buongiorno! Come posso aiutarla?". Marcello deve sentirlo chiaro: conferma l\'audio in uscita.',
        'Marcello parla (es. si presenta e dice cosa gli serve). Sul monitor compaiono i suoi turni come "CHIAMANTE": conferma l\'audio in entrata (lo stiamo trascrivendo).',
        'Provare un flusso reale: Marcello chiede un reparto, ad esempio "vorrei l\'assistenza tecnica", per vedere l\'instradamento logico. Opzionale: una frase in inglese per testare il bilingue.',
        'Chiudere la chiamata. Il monitor mostra "CHIAMATA TERMINATA" con durata, esito e il riepilogo audio entrata/uscita.',
    ], 1):
        s.append(Paragraph(f'<b><font color="#B8860B">{i}.</font></b>&nbsp;&nbsp;{st}', bullet))

    s.append(P('Criteri di successo (spuntare tutto)', h2))
    for x in B([
        'La chiamata compare sul monitor con il numero del chiamante (è una vera chiamata SIP, non una sessione web).',
        'L\'agente risponde col messaggio di benvenuto e Marcello lo sente pulito.',
        'I turni del chiamante vengono trascritti (audio in entrata OK).',
        'Marcello sente le risposte dell\'agente senza tagli (audio in uscita OK).',
        'Nessun eco, nessun ritardo eccessivo, voce naturale.',
        'A fine chiamata lo stato va in "done" con un esito tracciato.',
    ]):
        s.append(x)

    s.append(PageBreak())
    s.append(P('Se qualcosa non va — diagnosi rapida', h2))
    data = [[P('Sintomo', cellh), P('Causa probabile', cellh), P('Cosa fare', cellh)]]
    for r in [
        ['Sul monitor non arriva nulla','Il DID/regola non punta al trunk, oppure il TLS non si stabilisce','Marcello verifica l\'instradamento inbound sul Yeastar e che la porta 5061 TLS verso ElevenLabs sia raggiungibile (no firewall che blocca).'],
        ['Chiamata rifiutata (401/403)','Credenziali del trunk errate','Ricontrollare username 6701 e password sul trunk Yeastar; devono coincidere con quelle del nostro trunk.'],
        ['La chiamata arriva ma cade subito (0-3s)','Nessun codec in comune o problema media','Assicurarsi che il trunk Yeastar offra almeno uno tra G722, PCMA, PCMU. Il media è "allowed", quindi accetta sia RTP sia SRTP.'],
        ['Audio solo da un lato','RTP che non passa (NAT/firewall sulle porte media)','Verificare che il Yeastar invii e riceva RTP; aprire/instradare le porte media verso ElevenLabs.'],
        ['Voce robotica o a scatti','Jitter o banda insufficiente','Provare a forzare PCMA (G711a), più tollerante; controllare la rete del centralino.'],
        ['Eco in chiamata','Cancellazione eco non attiva','Abilitare la cancellazione d\'eco sul trunk/centralino Yeastar.'],
        ['Agente non parte / silenzio totale','Codec non negoziato o media bloccato','Forzare PCMA sul trunk e ripetere; se persiste, raccogliere i log SIP.'],
    ]:
        data.append([P(r[0], cellb), P(r[1], cell), P(r[2], cell)])
    s.append(tbl(data, [42*mm, 52*mm, 66*mm]))
    s.append(Spacer(1, 3*mm))
    s.append(P('Nota: sul nostro trunk il salvataggio dei messaggi SIP è attivo, quindi in caso di problemi possiamo recuperare lo scambio '
               'SIP (INVITE e risposte) per capire dove si blocca. Le chiamate restano comunque visibili nello storico dell\'agente.', small))

    s.append(P('Dopo il test', h2))
    for x in B([
        '<b>Se è andato bene:</b> confermare a Marcello, segnare "test SIP superato" sul calendario operativo, e passare ai pezzi successivi della Fase 2 (trasferimenti ai reparti, che richiedono i numeri interni, ed email automatiche, che richiedono email + SMTP).',
        '<b>Se non è andato:</b> annotare il sintomo dalla tabella sopra, raccogliere i log lato Yeastar, e fissare un retry. Nella maggior parte dei casi è instradamento DID o codec, entrambi risolvibili lato centralino.',
    ]):
        s.append(x)

    s.append(Spacer(1, 2*mm))
    s.append(Table([[Paragraph('<b>Comando da lanciare lunedì alle 9:45:</b>&nbsp;&nbsp;<font name="Courier">python3 monitor_telnet_test.py</font>'
                     '<br/>Dalla cartella Desktop/telesales. Resta in ascolto e mostra la chiamata in diretta. Ctrl+C per chiudere.', cell)]],
                   colWidths=[160*mm],
                   style=TableStyle([('BACKGROUND',(0,0),(-1,-1),DARK),('LEFTPADDING',(0,0),(-1,-1),8),
                                     ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),
                                     ('BOTTOMPADDING',(0,0),(-1,-1),6),('TEXTCOLOR',(0,0),(-1,-1),colors.white)])))
    return s

# ---------------------------------------------------------------- build all
build('/Users/simocors/Desktop/telesales/TelNet_06_Test_Live_Tutorial.pdf',
      'Test chiamata live', 'Guida operativa passo-passo — lunedì 22/6 ore 10:00', doc_test_tutorial)
build('/Users/simocors/Desktop/telesales/TelNet_05_Roadmap_Operativa.pdf',
      'Roadmap operativa', 'Il progetto giorno per giorno con TelNet / Marcello', doc_roadmap)
build('/Users/simocors/Desktop/telesales/TelNet_01_Fattibilita_ElevenLabs.pdf',
      'Fattibilità con ElevenLabs', 'Cosa è possibile e come — funzione per funzione', doc_fattibilita)
build('/Users/simocors/Desktop/telesales/TelNet_02_Flussi_Chiamata.pdf',
      'Flussi di chiamata', 'I percorsi della reception AI, dall\'inizio all\'esito', doc_flussi)
build('/Users/simocors/Desktop/telesales/TelNet_03_Piano_Operativo.pdf',
      'Piano operativo e responsabilità', 'Chi fa cosa, in quale fase, e cosa resta da definire', doc_piano)
build('/Users/simocors/Desktop/telesales/TelNet_04_Ricerca_Mercato.pdf',
      'Ricerca di mercato', 'Mercato, concorrenti, prezzi e posizionamento per TelNet', doc_mercato)
print('TUTTI I DOCUMENTI GENERATI')
