#!/usr/bin/env python3
"""
Batch invio mattutino schedulato.
Invia 10 email Culligan Sebastiano + aggiorna col M del foglio interno.
Tempi: 3 minuti tra ogni invio per evitare spam-flag Gmail.
Richiede env GMAIL_APP_PASSWORD (16 caratteri).
"""

import smtplib
import os
import sys
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Config
SENDER_EMAIL = "sebastiano.culligan@gmail.com"
REPLY_TO = "sebastiano.callegari@culligan.it"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
SHEET_KEY_FILE = "/Users/simocors/Downloads/claude-telesales-3afb5b11861c.json"
INTERNO_ID = "1PiezlYSd5TZNBCRTvzBhx_yVCGfN6aMI3PXdOYU4xu8"
LOG_FILE = "/tmp/scheduled_morning_batch.log"

# 10 email da inviare: (sheet_tab, sheet_row, recipient, lang, nome_struct, subject, body_intro_role)
EMAILS = [
    ("aziende_bolzano_VERIFICATE", 519, "info@hotelwerth.com",           "DE", "Parkhotel Werth",        "Hotels"),
    ("aziende_caldaro_VERIFICATE", 13,  "info@hotelbadl.com",            "DE", "Hotel Das Badl",         "Hotels und Restaurants"),
    ("aziende_caldaro_VERIFICATE", 14,  "info@designhotel-panorama.com", "DE", "Hotel Das Panorama",     "Hotels und Restaurants"),
    ("aziende_caldaro_VERIFICATE", 15,  "info@das-wanda.com",            "DE", "Hotel Das Wanda",        "Hotels und Restaurants"),
    ("aziende_caldaro_VERIFICATE", 24,  "info@kreithof.it",              "DE", "Hotel Kreithof",         "Hotels und Restaurants"),
    ("aziende_caldaro_VERIFICATE", 77,  "info@diesonne.it",              "DE", "Hotel Die Sonne",        "Hotels"),
    ("aziende_caldaro_VERIFICATE", 79,  "info@schlosshotel.it",          "DE", "Schlosshotel Aehrental", "Schlosshotels"),
    ("aziende_caldaro_VERIFICATE", 82,  "info@preyhof.com",              "DE", "Residence Prey Hof",     "Residences und Hotels"),
    ("aziende_caldaro_VERIFICATE", 12,  "info@pension-christl.it",       "DE", "Hotel Christl",          "Hotels und Pensionen"),
    ("aziende_bolzano_VERIFICATE", 387, "info@villaverdebolzano.com",    "IT", "B&B Villaverde",         "B&B e affittacamere"),
]

# Subject variati anti-spam
SUBJECTS = {
    "DE": [
        "Wasser vom Zapfhahn für {nome}",
        "Vorschlag für {nome} — Trinkwasser-Lösung",
        "Mikrofiltration für {nome}",
        "Trinkwasser-Idee für {nome}",
        "Wasseraufbereitung für {nome} — Culligan",
        "Vorschlag von Culligan für {nome}",
        "Wasser-Idee für {nome}",
        "Trinkwasser für {nome} — kurzer Vorschlag",
        "Mikrofiltration vom Zapfhahn für {nome}",
        "Culligan Vorschlag für {nome}",
    ],
    "IT": [
        "Acqua microfiltrata per {nome}",
        "Una proposta per {nome}",
        "Acqua alla spina per {nome}",
        "Idea acqua alla spina per {nome}",
        "Proposta di Culligan per {nome}",
        "Acqua microfiltrata — proposta per {nome}",
        "Soluzione acqua per {nome}",
        "Riduci i costi dell'acqua — {nome}",
        "Acqua di qualità alla spina per {nome}",
        "Proposta acqua per {nome}",
    ],
}

BODY_DE = """Guten Tag,

mein Name ist Sebastiano Callegari, ich betreue für Culligan persönlich die Region Bozen für die Mikrofiltration von Trinkwasser.

Mit vielen {cat} in der Gegend arbeiten wir bereits zusammen: keine Flaschen mehr einkaufen oder lagern, dafür natürliches und prickelndes Wasser direkt vom Zapfhahn in gleichbleibender Qualität, auch zu Stoßzeiten. Wartung, Filterwechsel und Sanierung sind im Service inklusive.

Wenn es Sie interessiert, würde ich gerne diese oder nächste Woche kurz bei {nome} vorbeikommen — unverbindlich, einfach um die Möglichkeiten zu zeigen.

Vielen Dank im Voraus.

Mit freundlichen Grüßen,

Sebastiano Callegari
Commercial Drinking Water — Culligan Italia
Mobile: +39 366 679 5048
Office: 800 901999
sebastiano.callegari@culligan.it

P.S.: Bei kein Interesse einfach mit "nein danke" antworten — ich melde mich dann nicht mehr."""

BODY_IT = """Buongiorno,

mi chiamo Sebastiano Callegari, mi occupo della zona di Bolzano per Culligan, marchio storico nella microfiltrazione dell'acqua potabile.

Con diversi {cat} della zona lavoriamo già: il vantaggio è poter offrire ai propri clienti acqua naturale o frizzante alla spina di qualità costante, senza dover acquistare, stoccare e smaltire bottiglie. Manutenzione, filtri e sanificazione sono inclusi.

Sarei lieto di passare da voi questa settimana o la prossima per una breve chiacchierata senza impegno presso {nome}.

Grazie e buon lavoro.

Sebastiano Callegari
Commercial Drinking Water — Culligan Italia
Mobile: +39 366 679 5048
Office: 800 901999
sebastiano.callegari@culligan.it

P.S.: se non è di suo interesse, mi risponda semplicemente "no grazie" e non la disturberò più."""


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def send_email(to_addr, subject, body):
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_addr
    msg["Reply-To"] = REPLY_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, [to_addr], msg.as_string())


def mark_col_m(tab, row):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SHEET_KEY_FILE, scopes=scopes)
    gc = gspread.authorize(creds)
    wb = gc.open_by_key(INTERNO_ID)
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    wb.worksheet(tab).update_cell(row, 13, f"outreach inviata {now}")


def main():
    if not APP_PASSWORD:
        log("ERROR: GMAIL_APP_PASSWORD not set. Aborting.")
        sys.exit(1)

    log(f"=== Starting morning batch — {len(EMAILS)} emails ===")
    sent_ok = 0
    sent_fail = []

    for idx, (tab, row, to_addr, lang, nome, cat) in enumerate(EMAILS, 1):
        subject = SUBJECTS[lang][idx - 1].format(nome=nome)
        body_tpl = BODY_DE if lang == "DE" else BODY_IT
        body = body_tpl.format(nome=nome, cat=cat)

        log(f"[{idx}/10] Sending to {to_addr} ({nome}, {lang})...")
        try:
            send_email(to_addr, subject, body)
            mark_col_m(tab, row)
            sent_ok += 1
            log(f"[{idx}/10] OK → {to_addr} | col M updated")
        except Exception as e:
            sent_fail.append((to_addr, str(e)))
            log(f"[{idx}/10] FAIL → {to_addr}: {e}")

        # Pausa 3 min tra invii (tranne ultimo)
        if idx < len(EMAILS):
            log(f"Sleeping 180s before next email...")
            time.sleep(180)

    log(f"=== Batch complete: {sent_ok}/{len(EMAILS)} sent ===")
    if sent_fail:
        log(f"Failures: {sent_fail}")


if __name__ == "__main__":
    main()
