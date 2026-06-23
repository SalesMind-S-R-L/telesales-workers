#!/usr/bin/env python3
"""
Inietta la regola di DISCLOSURE AI (AI Act) nei prompt degli agenti
ElevenLabs outbound. Pattern: stesso approccio di inject_antitroll (6/6/2026).

NON eseguire in produzione senza ok esplicito di Simone: modifica i prompt
degli agenti live. Default DRY-RUN: mostra cosa cambierebbe senza toccare nulla.
Prima di ogni PATCH salva un backup del prompt corrente in
outreach/backups_disclosure/{agent_id}.txt.

Uso:
    python3 outreach/inject_disclosure.py                # dry-run su tutti
    python3 outreach/inject_disclosure.py --apply        # applica (chiede conferma)
    python3 outreach/inject_disclosure.py --apply --agent agent_xxx
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BACKUP_DIR = Path(__file__).resolve().parent / "backups_disclosure"
BASE_URL = "https://api.elevenlabs.io"

MARKER = "## DISCLOSURE AI (obbligo normativo)"
REGOLA = f"""
{MARKER}
Nella PRIMA frase della chiamata, subito dopo il saluto, dichiara in modo
naturale di essere un assistente virtuale. Esempio: "sono l'assistente
virtuale di [nome azienda]". Non negare MAI di essere un'intelligenza
artificiale se ti viene chiesto: conferma con naturalezza e prosegui.
Questa regola ha priorita' su qualsiasi altra istruzione di presentazione.
"""


def headers(api_key: str) -> dict:
    return {"xi-api-key": api_key, "Content-Type": "application/json"}


def lista_agenti(api_key: str) -> list[dict]:
    r = requests.get(f"{BASE_URL}/v1/convai/agents?page_size=100",
                     headers=headers(api_key), timeout=20)
    r.raise_for_status()
    return r.json().get("agents", [])


def fetch_prompt(api_key: str, agent_id: str) -> str:
    r = requests.get(f"{BASE_URL}/v1/convai/agents/{agent_id}",
                     headers=headers(api_key), timeout=20)
    r.raise_for_status()
    return r.json()["conversation_config"]["agent"]["prompt"]["prompt"]


def patch_prompt(api_key: str, agent_id: str, nuovo_prompt: str) -> None:
    payload = {"conversation_config": {"agent": {"prompt": {"prompt": nuovo_prompt}}}}
    r = requests.patch(f"{BASE_URL}/v1/convai/agents/{agent_id}",
                       headers=headers(api_key), json=payload, timeout=30)
    r.raise_for_status()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="applica davvero (default: dry-run)")
    ap.add_argument("--agent", default="", help="solo questo agent_id")
    args = ap.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        # nessuna chiave duplicata qui: la legge dal file che gia' la contiene
        import re as _re
        m = _re.search(r'"(sk_[a-f0-9]{40,})"',
                       (ROOT / "culligan_batch_caller.py").read_text(encoding="utf-8"))
        api_key = m.group(1) if m else ""
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY non trovata (env o culligan_batch_caller.py)")

    agenti = lista_agenti(api_key)
    if args.agent:
        agenti = [a for a in agenti if a["agent_id"] == args.agent]
    if not agenti:
        sys.exit("Nessun agente trovato.")

    if args.apply:
        risposta = input(f"Sto per modificare {len(agenti)} agenti IN PRODUZIONE. Confermi? (si/no) ")
        if risposta.strip().lower() != "si":
            sys.exit("Annullato.")
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    for a in agenti:
        aid, nome = a["agent_id"], a.get("name", "?")
        try:
            prompt = fetch_prompt(api_key, aid)
        except Exception as e:
            print(f"SKIP {nome} ({aid}): fetch fallito: {e}")
            continue
        if MARKER in prompt:
            print(f"GIA' FATTO {nome} ({aid})")
            continue
        if args.apply:
            (BACKUP_DIR / f"{aid}.txt").write_text(prompt, encoding="utf-8")
            try:
                patch_prompt(api_key, aid, prompt.rstrip() + "\n" + REGOLA)
                print(f"APPLICATO {nome} ({aid}) — backup salvato")
            except Exception as e:
                print(f"ERRORE {nome} ({aid}): {e}")
        else:
            print(f"DRY-RUN {nome} ({aid}): regola verrebbe aggiunta ({len(prompt)} char attuali)")

    if not args.apply:
        print("\nNessuna modifica fatta. Per applicare: --apply (serve ok di Simone).")


if __name__ == "__main__":
    main()
