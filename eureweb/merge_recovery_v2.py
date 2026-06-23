#!/usr/bin/env python3
"""Merge recovery v2: centralini + cellulari + nomi DM nel master locale."""
import json, glob, re, unicodedata, openpyxl

def norm(s):
    s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower()
    s=re.sub(r'\(.*?\)',' ',s)
    s=re.sub(r'[^a-z0-9 ]',' ',s)
    s=re.sub(r'\b(italia|italy|group|gruppo|spa|srl|snc|sas|sr|s p a|s r l)\b',' ',s)
    return re.sub(r'\s+',' ',s).strip()

WD='/Users/simocors/Desktop/telesales/eureweb'

# Carica recovery centralini (tutti i file rc_out_*.json)
cent_map={}
for f in glob.glob(f'{WD}/tel/rc_out_*.json'):
    try:
        arr=json.load(open(f))
        for e in (arr if isinstance(arr,list) else []):
            t=(e.get('tel','') or '').strip()
            if t:
                key=norm(e.get('azienda',''))
                cent_map[key]=t
    except Exception as ex: print(f'  WARN {f}: {ex}')
print(f'Centralini recovery: {len(cent_map)}')
for k,v in sorted(cent_map.items()): print(f'  {k}: {v}')

# Cellulare Velasca (unico con 2 fonti indipendenti)
mob_manual={
    norm('Velasca'): {'c':'346 3660989','n':'Enrico Casati (Co-Founder)'}
}

# Carica nomi DM gap (da agente aa6912a35194697d0)
dmgap_map={}
try:
    arr=json.load(open(f'{WD}/tel/dm_gap_names.json'))
    for e in (arr if isinstance(arr,list) else []):
        n=(e.get('dm_nome','') or '').strip()
        r=(e.get('dm_ruolo','') or '').strip()
        if n: dmgap_map[norm(e.get('azienda',''))]={'n':n,'r':r}
    print(f'Nomi DM gap: {len(dmgap_map)}')
except Exception as ex: print(f'dm_gap_names mancante: {ex}')

# Carica cellulari v2 (da agente aa6912a35194697d0)
mob_extra={}
try:
    arr=json.load(open(f'{WD}/tel/dm_mobiles_v2.json'))
    for e in (arr if isinstance(arr,list) else []):
        c=(e.get('cell_diretto','') or '').strip()
        np=(e.get('nome_persona','') or '').strip()
        if c and c not in ('','""'): mob_extra[norm(e.get('azienda',''))]={'c':c,'n':np}
    print(f'Cellulari extra: {len(mob_extra)}')
except Exception as ex: print(f'dm_mobiles_v2 mancante: {ex}')

# Unisci mob_manual + mob_extra
mob_map={**mob_extra, **mob_manual}  # manual override per Velasca

# Apri master
wb=openpyxl.load_workbook(f'{WD}/Master_Eureweb_ADLab.xlsx')
ws=wb['LISTA_PROSPECT']

updated_cent=0; updated_mob=0; updated_name=0; already_cent=0
for r in range(5,ws.max_row+1):
    az=(ws.cell(r,2).value or '').strip()
    if not az: continue
    key=norm(az)

    # Centralino (col 10): aggiorna SOLO se vuoto
    existing_cent=(ws.cell(r,10).value or '').strip()
    if not existing_cent:
        if key in cent_map:
            ws.cell(r,10).value=cent_map[key]
            ws.cell(r,10).number_format='@'
            updated_cent+=1
    else:
        already_cent+=1

    # Cellulare diretto (col 11): aggiorna se vuoto
    if not (ws.cell(r,11).value or '').strip():
        if key in mob_map:
            ws.cell(r,11).value=mob_map[key]['c']
            ws.cell(r,11).number_format='@'
            updated_mob+=1

    # DM marketing nome (col 26): aggiorna se vuoto
    if not (ws.cell(r,26).value or '').strip():
        if key in dmgap_map:
            ws.cell(r,26).value=dmgap_map[key]['n']
            ws.cell(r,27).value=dmgap_map[key]['r']
            updated_name+=1

wb.save(f'{WD}/Master_Eureweb_ADLab.xlsx')
print(f'\nMERGE OK: +{updated_cent} centralini, +{updated_mob} cellulari, +{updated_name} nomi DM')
print(f'(invariati: {already_cent} centralini gia presenti)')

# Statistiche finali
wb2=openpyxl.load_workbook(f'{WD}/Master_Eureweb_ADLab.xlsx')
ws2=wb2['LISTA_PROSPECT']
tot=sum(1 for r in range(5,ws2.max_row+1) if (ws2.cell(r,2).value or '').strip())
has_cent=sum(1 for r in range(5,ws2.max_row+1) if (ws2.cell(r,10).value or '').strip())
has_mob=sum(1 for r in range(5,ws2.max_row+1) if (ws2.cell(r,11).value or '').strip())
has_dm=sum(1 for r in range(5,ws2.max_row+1) if (ws2.cell(r,26).value or '').strip())
has_tit=sum(1 for r in range(5,ws2.max_row+1) if (ws2.cell(r,23).value or '').strip())
no_cent=[ws2.cell(r,2).value for r in range(5,ws2.max_row+1) 
         if (ws2.cell(r,2).value or '').strip() and not (ws2.cell(r,10).value or '').strip()]
print(f'\nSTATO FINALE: {tot} righe')
print(f'  Centralino: {has_cent}/{tot}')
print(f'  Cellulare diretto: {has_mob}/{tot}')
print(f'  DM marketing nome: {has_dm}/{tot}')
print(f'  Titolare/AD: {has_tit}/{tot}')
print(f'  Ancora senza centralino ({len(no_cent)}): {no_cent[:15]}')
