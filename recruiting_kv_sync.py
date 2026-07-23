#!/usr/bin/env python3
"""SYNC CLOUD (GitHub Action): processa i batch 'Recruiting' completati su ElevenLabs e scrive
i dati aggiornati della Talent Tower su Cloudflare KV. Gira 24/7 nel cloud, indipendente dal Mac.
La Tower legge KV via il Worker (/recruiting/candidates). Nessun redeploy, nessun token Vercel.

Env (secret GitHub): ELEVENLABS_API_KEY, CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID."""
import os, json, requests
import recruiting_auto as R

NS = "de8093d84a674862b18e6fda6f3b56fa"          # KV namespace del Worker telesales-workers
ACCT = os.environ["CLOUDFLARE_ACCOUNT_ID"]
CF_TOKEN = os.environ["CLOUDFLARE_API_TOKEN"]
KV = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/storage/kv/namespaces/{NS}/values"
CFH = {"Authorization": f"Bearer {CF_TOKEN}"}
SEED_PROCESSED = [
    "btcal_7001ky4xj2emf0s907arfw9a3bkn", "btcal_3601ky528d8yeh5t8t8hv05dkvmv",
    "btcal_7601ky59sp26emkb0f7xwvh2mffa", "btcal_8201ky59snrae8g8cr6j0n8b6mks",
]


def kv_get(key):
    r = requests.get(f"{KV}/{key}", headers=CFH, timeout=30)
    return r.text if r.status_code == 200 else None


def kv_put(key, value):
    r = requests.put(f"{KV}/{key}", headers=CFH, data=value.encode("utf-8"), timeout=30)
    r.raise_for_status()


def main():
    R.H = {"xi-api-key": R.key(), "Content-Type": "application/json"}
    # 1) dati candidati: da KV, o seed dalla Tower live al primo giro
    raw = kv_get("recruiting_candidates")
    if raw:
        data = json.loads(raw); R.log(f"KV: {len(data)} candidati caricati.")
    else:
        _, _, _, data = R.fetch_tower(); R.log(f"Seed da Tower live: {len(data)} candidati.")
    # 2) batch gia' processati
    pr = kv_get("recruiting_processed")
    done = set(json.loads(pr)) if pr else set(SEED_PROCESSED)
    # 3) batch Recruiting completati non ancora processati
    lst = R.api("GET", "/v1/convai/batch-calling/workspace").get("batch_calls", [])
    todo = [b for b in lst if str(b.get("name", "")).startswith("Recruiting")
            and b.get("status") == "completed" and b.get("id") not in done]
    if not todo and raw:
        R.log("Nessun batch nuovo da processare."); return
    R.log(f"Da processare: {[b['name'] for b in todo]}")
    newq = []
    for bm in todo:
        batch = R.api("GET", f"/v1/convai/batch-calling/{bm['id']}")
        newq += R.process(data, batch, [])
        done.add(bm["id"])
    # 4) scrivi su KV (fonte unica per la Tower)
    kv_put("recruiting_candidates", json.dumps(data, ensure_ascii=False))
    kv_put("recruiting_processed", json.dumps(sorted(done)))
    R.log(f"KV aggiornato. Nuovi qualificati (visibili a Leo): {newq}")


if __name__ == "__main__":
    main()
