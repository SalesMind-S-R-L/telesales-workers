#!/usr/bin/env python3
"""Culligan outreach via Gmail SMTP — invio email personalizzate a HoReCa Bolzano.

Caratteristiche:
- Variabili: {{NomeStruttura}}, {{categoria}}, {{categoria_plural}}
- 6 PDF allegati per ogni mail
- Personalizzazione per categoria (Hotel/Ristorante/Bar)
- Dedup per email (no doppi a stesso indirizzo)
- Esclude Appuntamento + Non interessato
- Pausa 12-18s casuali tra invii (anti-spam)
- Log su /tmp + marcatura colonna M foglio interno (outreach_inviata_DD/MM/YYYY)
- Dry-run di default; --send per invio reale
"""
import os, re, sys, time, random, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate, make_msgid
from email import encoders
from datetime import datetime
sys.path.insert(0, '/Users/simocors/Desktop/telesales')
from culligan_batch_caller import get_sheets_service, SHEET_ID, TAB_NAME

# === CONFIG ===
GMAIL_USER = "sebastiano.culligan@gmail.com"
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")  # 16-char app password, no Culligan2026!
REPLY_TO = "sebastiano.callegari@culligan.it"
ASSETS = "/Users/simocors/Desktop/telesales/culligan_assets"
ATTACHMENTS = [
    "Culligan - Scheda Prodotto - Aquabar Elettronico.pdf",
    "Culligan - Scheda Prodotto - Rebel60 (1).pdf",
    "Culligan - Scheda Prodotto - Purity Prime.pdf",
    "Culligan - Scheda Prodotto - Colonne di spillatura HORECA.pdf",
    "Culligan - colonna Tbar.pdf",
    "Culligan - Scheda Prodotto - CB Ultra.pdf",
]
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
PAUSE_MIN = 12
PAUSE_MAX = 18

EXCLUDE_ESITI = {"Appuntamento", "Non interessato"}

CAT_SINGULAR = {
    "hotel": "hotel", "b&b": "B&B", "albergo": "albergo",
    "ristorante": "ristorante", "trattoria": "trattoria",
    "pizzeria": "pizzeria", "bar": "bar",
    "café": "bar", "caffe": "bar", "caffè": "bar",
}
CAT_PLURAL = {
    "hotel": "hotel", "b&b": "B&B e alberghi",
    "albergo": "alberghi", "ristorante": "ristoranti",
    "trattoria": "ristoranti", "pizzeria": "pizzerie",
    "bar": "bar", "café": "bar", "caffe": "bar", "caffè": "bar",
}


def norm_cat(s):
    sl = (s or "").strip().lower()
    return CAT_SINGULAR.get(sl, "attività"), CAT_PLURAL.get(sl, "attività come la vostra")


SUBJECT_TPL = "CULLIGAN — Microfiltrazione acqua per {nome}"

BODY_TPL = """Buongiorno {nome},

Siamo dell'Azienda CULLIGAN, marchio leader internazionale nella produzione, noleggio e vendita di macchinari per la microfiltrazione dell'acqua potabile, con oltre 90 anni di esperienza e più di 5.000 strutture clienti in Italia.

Mi occupo personalmente della zona di Bolzano e lavoriamo già con diversi {cat_plural} come il vostro, aiutandoli a:

- Aumentare il margine sull'acqua, senza più acquistare e stoccare bottiglie
- Servire acqua naturale e frizzante alla spina di qualità costante, anche nelle ore di punta
- Tutto incluso: manutenzione, cambio filtri e sanificazione, senza pensieri

Le riporto negli allegati alcune nostre proposte di macchinari pensate specificamente per {cat_plural} come {nome}, e le motivazioni per sostenere questo piccolo cambiamento che migliorerà per sempre la vostra gestione dell'acqua da bere.

Rimaniamo a Sua completa disposizione per fissare un appuntamento gratuito e senza impegno presso {nome}, questa settimana o la prossima, per valutare insieme la soluzione migliore alle Sue esigenze.

La ringrazio anticipatamente per la disponibilità.

Le porgo i miei più cordiali saluti, augurandole buon lavoro nella speranza di incontrarla al più presto.

Sebastiano Callegari
Commercial Drinking Water — Culligan Italia
Mobile: +39 366 679 5048
Office: 800 901999
sebastiano.callegari@culligan.it
www.culligan.it
"""


def build_message(to_email, nome, categoria_plural):
    msg = MIMEMultipart()
    msg["From"] = f"Sebastiano Callegari <{GMAIL_USER}>"
    msg["To"] = to_email
    msg["Reply-To"] = REPLY_TO
    msg["Subject"] = SUBJECT_TPL.format(nome=nome)
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="gmail.com")
    body = BODY_TPL.format(nome=nome, cat_plural=categoria_plural)
    msg.attach(MIMEText(body, "plain", "utf-8"))
    for fname in ATTACHMENTS:
        fpath = os.path.join(ASSETS, fname)
        with open(fpath, "rb") as f:
            part = MIMEBase("application", "pdf")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=\"{fname}\"")
        msg.attach(part)
    return msg


def collect_recipients(svc):
    rows = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"'{TAB_NAME}'!A:L").execute().get('values', [])
    email_re = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
    cat_re = re.compile(r'\[([^\]]+)\]')
    seen_emails = set()
    out = []
    for i, r in enumerate(rows[1:], start=2):
        if not r or not r[0].strip():
            continue
        full = ' '.join(str(c) for c in r)
        em = email_re.search(full)
        if not em:
            continue
        email = em.group(1).strip().rstrip('.,;').lower()
        if email == 'none' or email in seen_emails:
            continue
        esito = (r[8].strip() if len(r) > 8 else '')
        if esito in EXCLUDE_ESITI:
            continue
        cat_raw = cat_re.search(r[2] if len(r) > 2 else '')
        cat_sing, cat_plur = norm_cat(cat_raw.group(1) if cat_raw else '')
        seen_emails.add(email)
        out.append({
            "row": i, "nome": r[0].strip(), "email": email,
            "categoria_sing": cat_sing, "categoria_plural": cat_plur,
            "esito": esito,
        })
    return out


def send_one(server, msg, to_email):
    server.sendmail(GMAIL_USER, [to_email], msg.as_string())


def main():
    send = "--send" in sys.argv
    # --limit N argument
    limit = None
    for i,a in enumerate(sys.argv):
        if a == "--limit" and i+1 < len(sys.argv):
            try: limit = int(sys.argv[i+1])
            except: pass
    print(f"Modalità: {'INVIO REALE' if send else 'DRY-RUN'} | Limit: {limit or 'NESSUNO'}")
    svc = get_sheets_service()
    # Skip già inviati (col M ha 'outreach inviata')
    rows_full = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"'{TAB_NAME}'!A:M").execute().get('values',[])
    skip_rows = set()
    for i,r in enumerate(rows_full[1:], start=2):
        if len(r)>=13 and r[12] and 'outreach' in str(r[12]).lower():
            skip_rows.add(i)
    print(f"Righe da saltare (già outreach inviata col M): {len(skip_rows)}")
    recipients = [r for r in collect_recipients(svc) if r['row'] not in skip_rows]
    if limit: recipients = recipients[:limit]
    print(f"Destinatari finali (post-dedupe + limit): {len(recipients)}\n")

    # Anteprima
    for r in recipients:
        subj = SUBJECT_TPL.format(nome=r['nome'])
        print(f"  r{r['row']:3d} | {r['nome']:<38} ({r['categoria_sing']:<10}) → {r['email']}")
        print(f"        Subject: {subj}")

    if not send:
        print(f"\nDry-run completato. Lancia con --send per inviare. Assicurati GMAIL_APP_PASSWORD env var sia impostata.")
        return

    if not GMAIL_APP_PASSWORD:
        print("\nERRORE: GMAIL_APP_PASSWORD non impostata. Esempio:")
        print('  export GMAIL_APP_PASSWORD="abcd efgh ijkl mnop"')
        print("  python3 demo_mik/culligan_outreach_gmail.py --send")
        return

    print(f"\nConnessione SMTP {SMTP_HOST}:{SMTP_PORT}...")
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
        server.starttls(context=context)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        print("Login OK.\n")
    except smtplib.SMTPAuthenticationError as e:
        print(f"AUTH ERROR: {e}")
        print("Verifica App Password: https://myaccount.google.com/apppasswords")
        return

    log = []
    for i, r in enumerate(recipients, 1):
        try:
            msg = build_message(r['email'], r['nome'], r['categoria_plural'])
            send_one(server, msg, r['email'])
            print(f"  [{i:2d}/{len(recipients)}] OK → {r['email']:<40} ({r['nome']})")
            log.append((r['row'], r['nome'], r['email'], "sent"))
        except Exception as e:
            print(f"  [{i:2d}/{len(recipients)}] FAIL → {r['email']}: {e}")
            log.append((r['row'], r['nome'], r['email'], f"fail: {e}"))
        if i < len(recipients):
            pause = random.uniform(PAUSE_MIN, PAUSE_MAX)
            time.sleep(pause)
    server.quit()
    print(f"\nFINE. Invii: {sum(1 for _,_,_,s in log if s=='sent')}/{len(recipients)}")

    # Mark column M sul foglio interno
    oggi = datetime.now().strftime("%d/%m/%Y %H:%M")
    updates = [{"range": f"'{TAB_NAME}'!M{row}", "values": [[f"outreach inviata {oggi}" if "sent" == status else status]]} for row, _, _, status in log]
    if updates:
        svc.spreadsheets().values().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={"valueInputOption": "USER_ENTERED", "data": updates},
        ).execute()
        print(f"Colonna M aggiornata su {len(updates)} righe del foglio interno.")


if __name__ == "__main__":
    main()
