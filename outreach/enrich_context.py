#!/usr/bin/env python3
"""
Arricchimento contesto per outreach personalizzato.

Per ogni azienda della lista: scarica il sito web (home + pagine chiave),
genera con Claude una scheda contesto (riassunto, pain point, hook di
personalizzazione, variante email consigliata) e la salva in
outreach/schede/{slug}.json + outreach/schede_contesto.csv.

Solo fatti presenti sul sito: niente invenzioni. LinkedIn non viene scrapato
(richiede login): il campo da_verificare elenca cosa controllare a mano.

Uso:
    python3 outreach/enrich_context.py                     # tutta la lista
    python3 outreach/enrich_context.py --limit 5           # prime 5 non fatte
    python3 outreach/enrich_context.py --solo "Akamas"     # singola azienda
    python3 outreach/enrich_context.py --model claude-haiku-4-5   # run economico
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
INPUT_DEFAULT = ROOT_DIR / "prospecting_b2b" / "LEAD_B2B_TELESALES_FINALE.csv"
SCHEDE_DIR = BASE_DIR / "schede"
CSV_OUT = BASE_DIR / "schede_contesto.csv"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PAGINE_CHIAVE = re.compile(r"chi.?siamo|about|servizi|services|soluzioni|solutions|prodott|products|azienda|company", re.I)
MAX_CHARS_SITO = 9000
MAX_PAGINE_INTERNE = 3

SYSTEM_PROMPT = """Sei un analista commerciale di Telesales, agenzia italiana che riempie le agende \
dei team commerciali B2B di appuntamenti qualificati (setter umani + AI Voice).

Ricevi il testo estratto dal sito web di un'azienda target e i dati del decisore. \
Produci una scheda contesto per personalizzare l'outreach (email e LinkedIn).

REGOLE FERREE:
- Usa SOLO informazioni presenti nel testo fornito. Mai inventare clienti, numeri, premi o dettagli.
- Se il testo e' scarso o non chiaro, imposta "scheda_completa": false e spiega in "da_verificare".
- L'hook deve citare qualcosa di SPECIFICO del sito (un servizio, un claim, un caso, un mercato), \
non frasi generiche tipo "ho visto il vostro sito".
- Il pain point e' un'ipotesi commerciale plausibile dedotta dal modello di business \
(es. vendita complessa, ciclo lungo, dipendenza da referral), formulata con prudenza.
- Tono: italiano professionale, zero emoji, zero anglicismi inutili.

Rispondi SOLO con JSON valido, nessun testo prima o dopo, con queste chiavi:
{
  "riassunto": "cosa fa l'azienda in 2 frasi",
  "pain_point": "ipotesi del problema commerciale piu' probabile, 1-2 frasi",
  "hook": "aggancio specifico dal sito per aprire il messaggio, 1 frase",
  "variante_email": "A" oppure "B",
  "motivo_variante": "1 frase: perche' A (proposta diretta) o B (questionario valutazione commerciale)",
  "da_verificare": "cosa controllare a mano su LinkedIn del decisore prima dell'invio",
  "scheda_completa": true/false
}"""


def slugify(nome: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", nome.lower()).strip("_")
    return s[:60] or "azienda"


def fetch_url(url: str, timeout: int = 12) -> str | None:
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout, allow_redirects=True)
        if r.status_code == 200 and "text/html" in r.headers.get("content-type", "text/html"):
            return r.text
    except requests.RequestException:
        return None
    return None


def estrai_testo(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()
    testo = re.sub(r"\s+", " ", soup.get_text(separator=" ")).strip()
    return testo


def scrape_sito(website: str) -> tuple[str, list[str]]:
    """Ritorna (testo aggregato, pagine lette). Home + fino a 3 pagine chiave."""
    dominio = website.strip().rstrip("/")
    if not dominio.startswith("http"):
        candidati = [f"https://{dominio}", f"https://www.{dominio}", f"http://{dominio}"]
    else:
        candidati = [dominio]

    home_html, base_url = None, None
    for c in candidati:
        home_html = fetch_url(c)
        if home_html:
            base_url = c
            break
    if not home_html:
        return "", []

    pagine_lette = [base_url]
    testi = [estrai_testo(home_html)]

    soup = BeautifulSoup(home_html, "html.parser")
    interni, visti = [], set()
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        p = urlparse(href)
        if p.netloc != urlparse(base_url).netloc:
            continue
        if href in visti or not PAGINE_CHIAVE.search(p.path):
            continue
        visti.add(href)
        interni.append(href)
        if len(interni) >= MAX_PAGINE_INTERNE:
            break

    for url in interni:
        html = fetch_url(url)
        if html:
            testi.append(estrai_testo(html))
            pagine_lette.append(url)
        time.sleep(0.5)

    return " || ".join(testi)[:MAX_CHARS_SITO], pagine_lette


def genera_scheda(client, model: str, riga: dict, testo_sito: str) -> dict:
    user_msg = (
        f"AZIENDA: {riga['nome_azienda']}\n"
        f"DECISORE: {riga['nome_decisore']} ({riga['ruolo_decisore']})\n"
        f"SETTORE: {riga['settore']} | CITTA': {riga.get('citta', '')}\n"
        f"ANGOLO PITCH ATTUALE: {riga.get('angolo_pitch', '')}\n\n"
        f"TESTO ESTRATTO DAL SITO ({riga['website']}):\n{testo_sito}"
    )
    resp = client.messages.create(
        model=model,
        max_tokens=2000,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = "".join(b.text for b in resp.content if b.type == "text").strip()
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        raise ValueError(f"risposta non JSON: {raw[:200]}")
    return json.loads(m.group(0))


def riscrivi_csv():
    """Rigenera il CSV cumulativo da tutti i JSON in schede/."""
    campi = [
        "nome_azienda", "nome_decisore", "ruolo_decisore", "email", "telefono",
        "citta", "settore", "website", "riassunto", "pain_point", "hook",
        "variante_email", "motivo_variante", "da_verificare", "scheda_completa",
    ]
    righe = []
    for f in sorted(SCHEDE_DIR.glob("*.json")):
        righe.append(json.loads(f.read_text(encoding="utf-8")))
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campi, extrasaction="ignore")
        w.writeheader()
        w.writerows(righe)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(INPUT_DEFAULT))
    ap.add_argument("--limit", type=int, default=0, help="max aziende da processare in questo run")
    ap.add_argument("--solo", default="", help="processa solo aziende il cui nome contiene questo testo")
    ap.add_argument("--model", default="claude-opus-4-8")
    ap.add_argument("--force", action="store_true", help="rigenera anche schede gia' esistenti")
    args = ap.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT_DIR / ".env")
    except ImportError:
        pass
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY mancante (atteso in .env o ambiente)")

    import anthropic
    client = anthropic.Anthropic()

    SCHEDE_DIR.mkdir(parents=True, exist_ok=True)
    with open(args.input, newline="", encoding="utf-8") as fh:
        righe = list(csv.DictReader(fh))

    fatte, tentate, errori = 0, 0, 0
    for riga in righe:
        nome = riga["nome_azienda"].strip()
        if args.solo and args.solo.lower() not in nome.lower():
            continue
        out_path = SCHEDE_DIR / f"{slugify(nome)}.json"
        if out_path.exists() and not args.force:
            continue
        if args.limit and tentate >= args.limit:
            break
        tentate += 1

        print(f"[{tentate}] {nome} ({riga['website']}) ...", flush=True)
        testo, pagine = scrape_sito(riga["website"])
        if len(testo) < 300:
            scheda = {
                "riassunto": "", "pain_point": "", "hook": "",
                "variante_email": "", "motivo_variante": "",
                "da_verificare": "Sito non raggiungibile o quasi vuoto: scheda da fare a mano.",
                "scheda_completa": False,
            }
            print("    sito non leggibile, scheda vuota")
        else:
            try:
                scheda = genera_scheda(client, args.model, riga, testo)
            except Exception as e:
                errori += 1
                print(f"    ERRORE: {e}")
                if "credit balance" in str(e):
                    print("\nCredito API esaurito: run interrotto. Ricaricare su console.anthropic.com.")
                    break
                continue

        scheda.update({k: riga.get(k, "") for k in (
            "nome_azienda", "nome_decisore", "ruolo_decisore", "email",
            "telefono", "citta", "settore", "website",
        )})
        scheda["pagine_lette"] = pagine
        out_path.write_text(json.dumps(scheda, ensure_ascii=False, indent=2), encoding="utf-8")
        fatte += 1
        time.sleep(1)

    riscrivi_csv()
    print(f"\nFatte {fatte} schede ({errori} errori). CSV: {CSV_OUT}")


if __name__ == "__main__":
    main()
