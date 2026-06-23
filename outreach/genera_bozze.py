#!/usr/bin/env python3
"""
Genera bozze outreach (email A/B, sequenza LinkedIn) dalle schede contesto.

Default OFFLINE: compila i template di TEMPLATES_COPY.md con i campi della
scheda (nessuna chiamata API). Con --api rifinisce ogni bozza con Claude per
renderla piu' naturale (richiede credito ANTHROPIC_API_KEY).

I placeholder non risolti ({CAL_LINK}, {SALES_SIX_LINK}, ecc.) restano visibili
nella bozza: il preflight manuale li deve risolvere prima dell'invio.

Uso:
    python3 outreach/genera_bozze.py --canale email --variante A --limit 5
    python3 outreach/genera_bozze.py --canale linkedin --solo "Akamas"
    python3 outreach/genera_bozze.py --canale tutti --cal-link https://cal.com/...
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEDE_DIR = BASE_DIR / "schede"
BOZZE_DIR = BASE_DIR / "bozze"
TEMPLATES_MD = BASE_DIR / "TEMPLATES_COPY.md"

# nome sezione nel md -> nome file bozza
SEZIONI = {
    "email_A": "EMAIL — Variante A",
    "email_B": "EMAIL — Variante B",
    "linkedin_connessione": "LINKEDIN — Nota di connessione",
    "linkedin_msg1": "LINKEDIN — Messaggio 1",
    "linkedin_msg2": "LINKEDIN — Messaggio 2",
    "email_followup_linkedin": "EMAIL — Follow-up LinkedIn",
}

CANALI = {
    "email": ["email_A", "email_B"],
    "linkedin": ["linkedin_connessione", "linkedin_msg1", "linkedin_msg2",
                 "email_followup_linkedin"],
}


def carica_template() -> dict:
    md = TEMPLATES_MD.read_text(encoding="utf-8")
    blocchi = re.split(r"^## ", md, flags=re.M)
    templates = {}
    for chiave, titolo in SEZIONI.items():
        for b in blocchi:
            if b.startswith(titolo):
                corpo = b.split("\n", 1)[1]
                corpo = corpo.split("\n---")[0].split("\n## ")[0].strip()
                templates[chiave] = corpo
                break
        else:
            sys.exit(f"Sezione '{titolo}' non trovata in {TEMPLATES_MD}")
    return templates


def campi_da_scheda(scheda: dict) -> dict:
    nome = scheda.get("nome_decisore", "").split()[0] if scheda.get("nome_decisore") else ""
    settore = scheda.get("settore", "")
    consulenza = "onsulenza" in settore
    pain = scheda.get("pain_point", "").rstrip(".")
    return {
        "nome": nome,
        "azienda": scheda.get("nome_azienda", ""),
        "hook": scheda.get("hook", "").rstrip("."),
        "pain_point_frase": f"{pain}." if pain else "",
        "settore_breve": "consulenza" if consulenza else "software B2B" if "IT" in settore else settore.lower(),
        "commerciali|consulenti": "consulenti" if consulenza else "commerciali",
    }


def compila(template: str, campi: dict, cal_link: str, six_link: str, firma: str) -> str:
    out = template
    for k, v in campi.items():
        out = out.replace("{" + k + "}", v)
    if cal_link:
        out = out.replace("{CAL_LINK}", cal_link)
    if six_link:
        out = out.replace("{SALES_SIX_LINK}", six_link)
    if firma:
        out = out.replace("{firma}", firma)
    return re.sub(r"\n{3,}", "\n\n", out).strip() + "\n"


def rifinisci_con_api(testo: str, scheda: dict, model: str) -> str:
    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=1500,
        thinking={"type": "adaptive"},
        system=("Sei un commerciale italiano esperto. Ricevi una bozza outreach "
                "gia' strutturata: riscrivila SOLO per renderla piu' fluida e "
                "naturale, mantenendo lunghezza simile, stesso contenuto, zero "
                "emoji, zero anglicismi inutili. Non toccare i placeholder tra "
                "graffe. Rispondi solo col testo finale."),
        messages=[{"role": "user", "content":
                   f"CONTESTO AZIENDA: {scheda.get('riassunto', '')}\n\nBOZZA:\n{testo}"}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--canale", choices=["email", "linkedin", "tutti"], default="tutti")
    ap.add_argument("--variante", choices=["A", "B", "auto"], default="auto",
                    help="auto = usa variante_email della scheda")
    ap.add_argument("--solo", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--cal-link", default="", help="URL Cal.com (altrimenti resta placeholder)")
    ap.add_argument("--six-link", default="", help="URL landing Sales Six")
    ap.add_argument("--firma", default="", help="Firma email (altrimenti resta placeholder)")
    ap.add_argument("--api", action="store_true", help="rifinisce le bozze con Claude")
    ap.add_argument("--model", default="claude-opus-4-8")
    args = ap.parse_args()

    if args.api:
        try:
            from dotenv import load_dotenv
            load_dotenv(BASE_DIR.parent / ".env")
        except ImportError:
            pass

    templates = carica_template()
    chiavi = CANALI["email"] + CANALI["linkedin"] if args.canale == "tutti" else CANALI[args.canale]

    schede = sorted(SCHEDE_DIR.glob("*.json"))
    if not schede:
        sys.exit(f"Nessuna scheda in {SCHEDE_DIR}: eseguire prima enrich_context.py")

    fatte = 0
    for path in schede:
        scheda = json.loads(path.read_text(encoding="utf-8"))
        if args.solo and args.solo.lower() not in scheda.get("nome_azienda", "").lower():
            continue
        if args.limit and fatte >= args.limit:
            break
        if not scheda.get("scheda_completa", False):
            print(f"SKIP {scheda.get('nome_azienda')}: scheda incompleta ({scheda.get('da_verificare', '')})")
            continue

        campi = campi_da_scheda(scheda)
        out_dir = BOZZE_DIR / path.stem
        out_dir.mkdir(parents=True, exist_ok=True)

        variante = scheda.get("variante_email", "A") if args.variante == "auto" else args.variante
        per_azienda = [k for k in chiavi
                       if not k.startswith("email_") or k == f"email_{variante}"
                       or k == "email_followup_linkedin"]

        for k in per_azienda:
            testo = compila(templates[k], campi, args.cal_link, args.six_link, args.firma)
            if args.api:
                testo = rifinisci_con_api(testo, scheda, args.model)
            (out_dir / f"{k}.txt").write_text(testo, encoding="utf-8")

        irrisolti = sorted(set(re.findall(r"\{[A-Za-z_|]+\}", " ".join(
            (out_dir / f"{k}.txt").read_text(encoding="utf-8") for k in per_azienda))))
        flag = f"  [placeholder da risolvere: {', '.join(irrisolti)}]" if irrisolti else ""
        print(f"OK {scheda['nome_azienda']} -> {out_dir.relative_to(BASE_DIR)} ({', '.join(per_azienda)}){flag}")
        fatte += 1

    print(f"\nBozze generate per {fatte} aziende in {BOZZE_DIR}")
    print("RICORDA: preflight 1-a-1 prima di ogni invio (destinatario, oggetto, placeholder).")


if __name__ == "__main__":
    main()
