#!/usr/bin/env python3
"""
Phone hunter — per ogni azienda Vibe, visita il sito (home + pagine contatti)
ed estrae telefoni ITALIANI verificati (validazione AGCOM prefissi).
Output: CSV unico formato Ferretti pronto per batch ElevenLabs.
"""
import re, sys, csv, json, time
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

PREFISSI_MOBILE = {'310','311','312','313','314','315','317','319','320','322','323','324','327','328','329','330','331','333','334','335','336','337','338','339','340','342','343','344','345','346','347','348','349','350','351','352','353','360','366','368','370','371','373','377','380','383','388','389','391','392','393','398'}

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
CONTACT_PATHS = ['', '/contatti', '/contatti/', '/contact', '/contacts', '/chi-siamo', '/azienda', '/about', '/contattaci']

# Regex telefoni italiani: cattura sequenze plausibili
PHONE_RE = re.compile(r'(?:(?:\+|00)39[\s.\-]?)?(?:0\d{1,3}[\s.\-]?\d{5,8}|3\d{2}[\s.\-]?\d{6,7})')

def normalize(raw):
    """Ritorna E.164 italiano o None."""
    s = re.sub(r'[^\d+]', '', raw)
    s = re.sub(r'^00', '+', s)
    if s.startswith('+39'):
        d = s[3:]
    elif s.startswith('39') and len(s) >= 11:
        d = s[2:]
    elif s.startswith('+'):
        return None  # estero
    else:
        d = s
    if not d.isdigit():
        return None
    # mobile 3XX
    if d.startswith('3'):
        if len(d) == 10 and d[:3] in PREFISSI_MOBILE:
            return '+39' + d, 'cellulare'
        return None
    # fisso 0X (8-11 cifre totali tipiche: prefisso 2-4 + numero)
    if d.startswith('0'):
        if 9 <= len(d) <= 11:
            return '+39' + d, 'fisso'
        return None
    return None

def hunt(website):
    if not isinstance(website, str) or not website.strip():
        return None
    base = website.strip().rstrip('/')
    if not base.startswith('http'):
        base = 'https://' + base
    found = {}
    for path in CONTACT_PATHS:
        url = base + path
        try:
            r = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
            if r.status_code != 200 or not r.text:
                continue
            text = r.text
            # priorità ai numeri vicino a "tel:" link
            tel_links = re.findall(r'tel:([+\d\s.\-]{6,20})', text)
            candidates = tel_links + PHONE_RE.findall(text)
            for c in candidates:
                res = normalize(c)
                if res:
                    num, tipo = res
                    # priorità: cellulare > fisso ; primo trovato vince per tipo
                    found.setdefault(tipo, num)
            if found:
                # se ho già un numero da home/contatti, basta
                if path in ('/contatti', '/contatti/', ''):
                    break
        except Exception:
            continue
        time.sleep(0.1)
    if not found:
        return None
    # preferisci fisso (centralino business affidabile) ma tieni anche cell
    return found.get('cellulare') or found.get('fisso'), found.get('cellulare', ''), found.get('fisso', '')

def clean_name(full, first, last):
    n = str(full or '').strip()
    n = re.sub(r'[^\w\sàèéìòùÀÈÉÌÒÙ\'\.]', '', n).strip()  # togli emoji/simboli
    if not n or len(n) < 2:
        n = f"{first} {last}".strip()
    return n.title()

def main(inputs, out):
    rows = []
    for csv_path, settore in inputs:
        df = pd.read_csv(csv_path)
        for _, r in df.iterrows():
            rows.append({
                'nome_decisore': clean_name(r.get('prospect_full_name'), r.get('prospect_first_name'), r.get('prospect_last_name')),
                'ruolo_decisore': str(r.get('prospect_job_title') or '').strip(),
                'nome_azienda': str(r.get('prospect_company_name') or '').strip().title(),
                'website': str(r.get('prospect_company_website') or '').strip(),
                'citta': str(r.get('prospect_city') or '').strip().title(),
                'regione': str(r.get('prospect_region_name') or '').strip().title(),
                'settore': settore,
            })
    print(f"Aziende totali da processare: {len(rows)}")

    results = []
    def work(row):
        res = hunt(row['website'])
        if res:
            row['telefono'], row['cellulare'], row['fisso'] = res
            row['tipo_numero'] = 'cellulare' if row['cellulare'] else 'fisso'
        else:
            row['telefono'] = ''
        return row

    with ThreadPoolExecutor(max_workers=20) as ex:
        futs = {ex.submit(work, r): r for r in rows}
        done = 0
        for f in as_completed(futs):
            results.append(f.result())
            done += 1
            if done % 25 == 0:
                hit = sum(1 for x in results if x.get('telefono'))
                print(f"  {done}/{len(rows)} — telefoni trovati: {hit}")

    with_phone = [r for r in results if r.get('telefono')]
    print(f"\nTOTALE con telefono italiano valido: {len(with_phone)}/{len(results)} ({100*len(with_phone)//max(len(results),1)}%)")

    df_out = pd.DataFrame(results)
    df_out.to_csv(out, index=False)
    print(f"Salvato: {out}")
    # versione solo chiamabili
    df_call = pd.DataFrame(with_phone)
    call_path = out.replace('.csv', '_CHIAMABILI.csv')
    df_call.to_csv(call_path, index=False)
    print(f"Salvato (solo chiamabili): {call_path}")

if __name__ == '__main__':
    base = '/Users/simocors/Desktop/telesales/prospecting_b2b'
    main([
        (f'{base}/vibe_it_software.csv', 'IT / Software'),
        (f'{base}/vibe_consulenza.csv', 'Consulenza gestionale'),
    ], f'{base}/lead_b2b_telesales.csv')
