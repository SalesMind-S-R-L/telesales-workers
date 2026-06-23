#!/usr/bin/env python3
"""
Rextyle — Publisher Meta Graph API.

Schedula post su 4 profili (Pagina FB Rextyle + IG @rextyle_ + 3 IG personali)
leggendo i batch generati dalla skill rextyle-social-designer.

Uso:
    python publish_rextyle.py output/2026-W24/                  # publish reale
    python publish_rextyle.py output/2026-W24/ --dry-run        # solo simulazione
    python publish_rextyle.py output/2026-W24/ --target rextyle_business_ig
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERRORE: pip install requests")
    sys.exit(1)

# Carica .env dalla stessa cartella dello script
SCRIPT_DIR = Path(__file__).parent
ENV_PATH = SCRIPT_DIR / ".env"

if not ENV_PATH.exists():
    print(f"ERRORE: {ENV_PATH} non trovato. Copia .env.template in .env e riempilo.")
    sys.exit(1)

ENV = {}
for line in ENV_PATH.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        ENV[k.strip()] = v.strip()

TOKEN = ENV.get("RX_META_TOKEN")
if not TOKEN or TOKEN.startswith("EAAxxx"):
    print("ERRORE: RX_META_TOKEN non configurato in .env")
    sys.exit(1)

ACCOUNTS = {
    "rextyle_fb_page":     {"id": ENV.get("RX_FB_PAGE_ID"),   "type": "fb_page"},
    "rextyle_business_ig": {"id": ENV.get("RX_IG_REXTYLE"),   "type": "ig"},
    "mattia_ig":           {"id": ENV.get("RX_IG_MATTIA"),    "type": "ig"},
    "niccolo_ig":          {"id": ENV.get("RX_IG_NICCOLO"),   "type": "ig"},
    "alberto_ig":          {"id": ENV.get("RX_IG_ALBERTO"),   "type": "ig"},
}

GRAPH = "https://graph.facebook.com/v21.0"


# ---------- Meta API wrappers ----------

def upload_carousel_child_ig(ig_id: str, image_url: str) -> str:
    """Carica una singola immagine come child di un carosello IG."""
    r = requests.post(
        f"{GRAPH}/{ig_id}/media",
        data={
            "image_url": image_url,
            "is_carousel_item": "true",
            "access_token": TOKEN,
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["id"]


def create_carousel_container_ig(ig_id: str, children_ids: list, caption: str,
                                  scheduled_time: int = None) -> str:
    """Crea il container carosello IG. Ritorna creation_id."""
    data = {
        "media_type": "CAROUSEL",
        "children": ",".join(children_ids),
        "caption": caption,
        "access_token": TOKEN,
    }
    if scheduled_time:
        data["scheduled_publish_time"] = scheduled_time
        data["published"] = "false"
    r = requests.post(f"{GRAPH}/{ig_id}/media", data=data, timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def publish_container_ig(ig_id: str, creation_id: str) -> str:
    """Pubblica un container IG. Ritorna post_id."""
    r = requests.post(
        f"{GRAPH}/{ig_id}/media_publish",
        data={"creation_id": creation_id, "access_token": TOKEN},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["id"]


def publish_photo_fb_page(page_id: str, image_url: str, caption: str,
                           scheduled_time: int = None) -> str:
    """Pubblica/schedula una foto sulla Pagina FB. Ritorna post_id."""
    data = {
        "url": image_url,
        "message": caption,
        "access_token": TOKEN,
    }
    if scheduled_time:
        data["scheduled_publish_time"] = scheduled_time
        data["published"] = "false"
    r = requests.post(f"{GRAPH}/{page_id}/photos", data=data, timeout=30)
    r.raise_for_status()
    return r.json()["id"]


# ---------- Batch processing ----------

def process_post(post_dir: Path, dry_run: bool, target_filter: str = None):
    """Processa un singolo post. Pubblica/schedula su tutti i target indicati."""
    meta_path = post_dir / "meta.json"
    caption_path = post_dir / "caption.md"

    if not meta_path.exists():
        print(f"  SKIP — {post_dir.name}: meta.json mancante")
        return

    meta = json.loads(meta_path.read_text())
    caption = caption_path.read_text() if caption_path.exists() else ""

    images = sorted(post_dir.glob("slide-*.png"))
    targets = meta.get("targets", [])
    schedule_iso = meta.get("schedule")  # es. "2026-06-09T09:00:00+02:00"
    scheduled_ts = None
    if schedule_iso:
        scheduled_ts = int(datetime.fromisoformat(schedule_iso).timestamp())

    for target_name in targets:
        if target_filter and target_name != target_filter:
            continue
        account = ACCOUNTS.get(target_name)
        if not account or not account["id"]:
            print(f"  SKIP — {post_dir.name}: account '{target_name}' non configurato")
            continue

        label = f"{post_dir.name} → {target_name}"
        if scheduled_ts:
            label += f" @ {schedule_iso}"

        if dry_run:
            print(f"  [DRY-RUN] {label} | {len(images)} slide, {len(caption)} char caption")
            continue

        # Real publish — implementazione completa quando token + image URLs disponibili
        # Le immagini devono essere accessibili via URL pubblico (es. caricate su Drive
        # con link condiviso, o S3, o asset server proprio). Meta non accetta upload binario.
        # NOTA: questa è la struttura. L'upload immagini → URL pubblico è step da implementare
        # in base alla scelta di storage (Drive API, S3, Cloudinary, ecc.)
        try:
            if account["type"] == "ig" and len(images) > 1:
                # Carosello
                image_urls = [meta.get("image_urls", {}).get(img.name) for img in images]
                if not all(image_urls):
                    print(f"  ERRORE {label}: image_urls mancanti in meta.json")
                    continue
                children = [upload_carousel_child_ig(account["id"], url) for url in image_urls]
                # IG richiede 5-10 secondi di attesa tra create child e create container
                time.sleep(8)
                creation_id = create_carousel_container_ig(
                    account["id"], children, caption, scheduled_ts
                )
                time.sleep(5)
                if not scheduled_ts:
                    post_id = publish_container_ig(account["id"], creation_id)
                    print(f"  ✓ {label} | post_id: {post_id}")
                else:
                    print(f"  ✓ {label} | scheduled creation_id: {creation_id}")

            elif account["type"] == "fb_page":
                image_url = meta.get("image_urls", {}).get(images[0].name)
                if not image_url:
                    print(f"  ERRORE {label}: image_url mancante")
                    continue
                post_id = publish_photo_fb_page(
                    account["id"], image_url, caption, scheduled_ts
                )
                print(f"  ✓ {label} | post_id: {post_id}")

        except requests.HTTPError as e:
            print(f"  ✗ ERRORE {label}: {e.response.status_code} {e.response.text[:200]}")


def main():
    parser = argparse.ArgumentParser(description="Rextyle Meta publisher")
    parser.add_argument("batch_dir", help="Cartella batch, es. output/2026-W24/")
    parser.add_argument("--dry-run", action="store_true", help="Simula senza pubblicare")
    parser.add_argument("--target", help="Pubblica solo su un target specifico")
    args = parser.parse_args()

    batch_dir = Path(args.batch_dir)
    if not batch_dir.is_dir():
        print(f"ERRORE: {batch_dir} non è una cartella valida")
        sys.exit(1)

    mode = "DRY-RUN" if args.dry_run else "LIVE PUBLISH"
    print(f"\nRextyle Publisher — {mode}")
    print(f"Batch: {batch_dir}")
    print(f"Token: ...{TOKEN[-10:]}")
    if args.target:
        print(f"Target filter: {args.target}")
    print()

    post_dirs = sorted([d for d in batch_dir.iterdir() if d.is_dir()])
    print(f"Trovati {len(post_dirs)} post da processare:\n")

    for post_dir in post_dirs:
        print(f"→ {post_dir.name}")
        process_post(post_dir, args.dry_run, args.target)
        print()

    if args.dry_run:
        print("DRY-RUN completato. Rilancia senza --dry-run per pubblicare davvero.")
    else:
        print("Batch completato.")


if __name__ == "__main__":
    main()
