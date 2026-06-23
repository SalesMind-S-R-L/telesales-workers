#!/usr/bin/env python3
"""
Rextyle — Refresh Meta long-lived access token.

Da lanciare circa ogni 50 giorni per estendere il token (max 60gg di vita).
Lo aggiorna direttamente in .env.

Uso:
    python refresh_token.py
    python refresh_token.py --check   # mostra solo scadenza, non rinnova
"""

import argparse
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERRORE: pip install requests")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
ENV_PATH = SCRIPT_DIR / ".env"


def load_env():
    if not ENV_PATH.exists():
        print(f"ERRORE: {ENV_PATH} non trovato")
        sys.exit(1)
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def save_env(env: dict):
    """Riscrive .env preservando i commenti."""
    lines = []
    existing_keys = set()
    for line in ENV_PATH.read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k = line.split("=", 1)[0].strip()
            if k in env:
                lines.append(f"{k}={env[k]}")
                existing_keys.add(k)
            else:
                lines.append(line)
        else:
            lines.append(line)
    # Aggiungi chiavi nuove
    for k, v in env.items():
        if k not in existing_keys:
            lines.append(f"{k}={v}")
    ENV_PATH.write_text("\n".join(lines))


def check_token_validity(token: str) -> dict:
    """Chiama debug_token per vedere scadenza e validità."""
    r = requests.get(
        "https://graph.facebook.com/v21.0/debug_token",
        params={"input_token": token, "access_token": token},
        timeout=15,
    )
    r.raise_for_status()
    return r.json().get("data", {})


def extend_token(token: str, app_id: str, app_secret: str) -> str:
    """Scambia un long-lived token per uno nuovo (esteso ulteriori 60gg)."""
    r = requests.get(
        "https://graph.facebook.com/v21.0/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": token,
        },
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def main():
    parser = argparse.ArgumentParser(description="Refresh Meta token Rextyle")
    parser.add_argument("--check", action="store_true", help="Mostra scadenza senza rinnovare")
    args = parser.parse_args()

    env = load_env()
    token = env.get("RX_META_TOKEN", "")
    app_id = env.get("RX_APP_ID", "")
    app_secret = env.get("RX_APP_SECRET", "")

    if not token or token.startswith("EAAxxx"):
        print("ERRORE: RX_META_TOKEN non configurato")
        sys.exit(1)

    info = check_token_validity(token)
    expires_at = info.get("expires_at", 0)
    is_valid = info.get("is_valid", False)
    days_left = (expires_at - time.time()) / 86400 if expires_at else 0

    print(f"\nToken attuale:")
    print(f"  Valido: {is_valid}")
    print(f"  Scade: {datetime.fromtimestamp(expires_at) if expires_at else 'mai (token permanente)'}")
    print(f"  Giorni rimanenti: {days_left:.1f}")
    print()

    if args.check:
        return

    if days_left > 20:
        print(f"Token ancora valido per {days_left:.1f} giorni. Skip refresh (soglia: 20 giorni).")
        return

    if not app_id or not app_secret:
        print("ERRORE: RX_APP_ID e RX_APP_SECRET necessari per il refresh")
        sys.exit(1)

    print("Rinnovo token in corso...")
    new_token = extend_token(token, app_id, app_secret)
    env["RX_META_TOKEN"] = new_token
    env["RX_TOKEN_EXPIRES_AT"] = str(int(time.time() + 60 * 86400))
    save_env(env)
    print(f"Token rinnovato. Nuova scadenza ~60 giorni.")


if __name__ == "__main__":
    main()
