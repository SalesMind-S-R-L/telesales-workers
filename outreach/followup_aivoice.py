#!/usr/bin/env python3
"""
Genera bozze email di follow-up post batch AI Voice, in base all'esito.

Input: CSV esiti con colonne minime: nome,azienda,email,esito[,quando,recap]
  - esito: "non interessato" | "da richiamare" | "interessato"
  - quando: per "da richiamare", cosa ha detto al telefono (es. "alle 15")
  - recap:  per "interessato", una frase di riassunto della chiamata

Output: outreach/bozze_followup/{slug}.txt — una bozza per riga, da inviare
SOLO dopo preflight manuale 1-a-1.

Uso:
    python3 outreach/followup_aivoice.py esiti_batch.csv
    python3 outreach/followup_aivoice.py esiti_batch.csv --cal-link https://cal.com/... --firma "Niccolo' - Telesales"
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_MD = BASE_DIR / "TEMPLATES_COPY.md"
OUT_DIR = BASE_DIR / "bozze_followup"

SEZIONI_ESITO = {
    "non interessato": "### Esito: non interessato",
    "da richiamare": "### Esito: da richiamare",
    "interessato": "### Esito: interessato / appuntamento fissato",
}


def slugify(nome: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", nome.lower()).strip("_")[:60] or "contatto"


def carica_template() -> dict:
    md = TEMPLATES_MD.read_text(encoding="utf-8")
    templates = {}
    for esito, marker in SEZIONI_ESITO.items():
        if marker not in md:
            sys.exit(f"Sezione '{marker}' non trovata in {TEMPLATES_MD}")
        corpo = md.split(marker, 1)[1]
        corpo = corpo.split("\n### ")[0].split("\n---")[0].strip()
        templates[esito] = corpo
    return templates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_esiti", help="CSV con nome,azienda,email,esito[,quando,recap]")
    ap.add_argument("--cal-link", default="")
    ap.add_argument("--firma", default="")
    args = ap.parse_args()

    templates = carica_template()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fatte, scartate = 0, 0
    with open(args.csv_esiti, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            esito = (r.get("esito") or "").strip().lower()
            email = (r.get("email") or "").strip()
            if esito not in templates or not email:
                scartate += 1
                continue

            testo = templates[esito]
            nome = (r.get("nome") or "").split()[0] if r.get("nome") else ""
            testo = testo.replace("{nome}", nome)
            testo = testo.replace("{quando_detto}", r.get("quando", "").strip() or "{quando_detto}")
            recap = r.get("recap", "").strip()
            testo = testo.replace("{recap_breve}", recap or "{recap_breve}")
            # blocchi condizionali interessato: senza data appuntamento usa il
            # ramo no_appuntamento (i blocchi contengono placeholder annidati)
            blocco = r"(?:[^{}]|\{[A-Za-z_]+\})*"
            testo = re.sub(r"\{se_appuntamento:" + blocco + r"\}\n?", "", testo)
            testo = re.sub(r"\{se_no_appuntamento:\s*(" + blocco + r")\}", r"\1", testo)
            if args.cal_link:
                testo = testo.replace("{CAL_LINK}", args.cal_link)
            if args.firma:
                testo = testo.replace("{firma}", args.firma)

            out = OUT_DIR / f"{slugify(r.get('azienda') or nome)}.txt"
            out.write_text(f"A: {email}\n\n{testo.strip()}\n", encoding="utf-8")

            irrisolti = sorted(set(re.findall(r"\{[A-Za-z_]+\}", testo)))
            flag = f"  [da risolvere: {', '.join(irrisolti)}]" if irrisolti else ""
            print(f"OK {r.get('azienda', nome)} ({esito}) -> {out.name}{flag}")
            fatte += 1

    print(f"\n{fatte} bozze in {OUT_DIR} ({scartate} righe scartate: esito non gestito o email mancante)")
    print("RICORDA: 'Non risposto' e 'Segreteria' NON ricevono follow-up email.")
    print("Preflight 1-a-1 obbligatorio prima di ogni invio.")


if __name__ == "__main__":
    main()
