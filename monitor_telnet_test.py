#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor LIVE del test chiamata TelNet (lunedi 22/6 ore 10).
Avvialo ~15 min prima del test:  python3 monitor_telnet_test.py
- Fa un pre-flight check (numero assegnato, trunk inbound, agente attivo).
- Poi resta in ascolto: quando arriva una chiamata SIP la annuncia e
  stampa la trascrizione turno per turno in tempo reale, fino a fine chiamata.
Ctrl+C per uscire.
"""
import json, time, sys, urllib.request, urllib.error
from datetime import datetime

NUM_ID = 'phnum_8001ktxm3fvfevctyactwr4t8ea6'
AGENT  = 'agent_3801ktf72nn6fdvvjdz0fs5wcybw'

def load_key():
    for line in open('marco_ai/.env'):
        if line.startswith('ELEVENLABS_API_KEY='):
            return line.split('=',1)[1].strip().strip('"').strip("'")
    sys.exit('API key non trovata in marco_ai/.env')
K = load_key()

def get(path):
    req = urllib.request.Request('https://api.elevenlabs.io'+path, headers={'xi-api-key':K})
    return json.load(urllib.request.urlopen(req, timeout=20))

def hr(c='-'): print(c*64)

def preflight():
    hr('=')
    print(' PRE-FLIGHT  TEST TELNET  ', datetime.now().strftime('%d/%m %H:%M:%S'))
    hr('=')
    p = get('/v1/convai/phone-numbers/'+NUM_ID)
    ib = p.get('inbound_trunk',{})
    a  = get('/v1/convai/agents/'+AGENT)
    fm = a.get('conversation_config',{}).get('agent',{}).get('first_message')
    checks = [
        ('Numero',            p.get('phone_number')=='+390574814928', p.get('phone_number')),
        ('Inbound attivo',    p.get('supports_inbound') is True, p.get('supports_inbound')),
        ('Assegnato agente',  p.get('assigned_agent',{}).get('agent_id')==AGENT, p.get('assigned_agent',{}).get('agent_name')),
        ('Auth credenziali',  ib.get('has_auth_credentials') is True, 'username '+str(ib.get('username'))),
        ('Nessun blocco IP',  ib.get('allowed_addresses')==['0.0.0.0/0'], ib.get('allowed_addresses')),
        ('Media',             True, ib.get('media_encryption')),
        ('Messaggio benvenuto', bool(fm), (fm or '')[:50]),
    ]
    ok_all = True
    for name, ok, val in checks:
        print(f'  [{"OK" if ok else "X "}] {name:<20} {val}')
        ok_all = ok_all and ok
    hr()
    print('  STATO:', 'TUTTO PRONTO. In attesa della chiamata di test...' if ok_all else 'ATTENZIONE: qualcosa non torna, controlla sopra.')
    hr('=')
    return ok_all

def conv_list():
    import urllib.parse
    q = urllib.parse.urlencode({'agent_id':AGENT,'page_size':10})
    d = get('/v1/convai/conversations?'+q)
    return d.get('conversations', d) if isinstance(d,dict) else d

def is_phone(detail):
    return detail.get('metadata',{}).get('phone_call') is not None

def watch():
    baseline = {c['conversation_id'] for c in conv_list()}
    print(f'  Baseline: {len(baseline)} conversazioni gia presenti (ignorate).')
    print('  In ascolto ogni 3s. Fai partire la chiamata quando vuoi.\n')
    active = None        # conversation_id della chiamata in corso
    printed_turns = 0
    while True:
        try:
            if active is None:
                for c in conv_list():
                    cid = c['conversation_id']
                    if cid in baseline:
                        continue
                    detail = get('/v1/convai/conversations/'+cid)
                    if is_phone(detail):
                        pc = detail['metadata']['phone_call']
                        hr('#')
                        print('  >>> CHIAMATA IN ARRIVO  ', datetime.now().strftime('%H:%M:%S'))
                        print('      Da   :', pc.get('external_number') or pc.get('from') or 'n/d')
                        print('      A    :', pc.get('agent_number') or pc.get('to') or 'n/d')
                        print('      Tipo :', pc.get('type') or 'sip_trunk', '|  conv:', cid)
                        hr('#')
                        active = cid; printed_turns = 0
                        break
                    else:
                        baseline.add(cid)  # sessione web demo: ignora
            else:
                detail = get('/v1/convai/conversations/'+active)
                tr = detail.get('transcript', [])
                for t in tr[printed_turns:]:
                    role = t.get('role','?').upper()
                    msg  = (t.get('message') or '').strip()
                    if msg:
                        tag = 'AGENTE ' if role.startswith('A') else 'CHIAMANTE'
                        print(f'   {tag:>9} | {msg}')
                printed_turns = len(tr)
                md = detail.get('metadata',{})
                if detail.get('status') == 'done':
                    hr()
                    print('  CHIAMATA TERMINATA  durata',
                          md.get('call_duration_secs'),'s  | esito:', detail.get('analysis',{}).get('call_successful'))
                    print('  Audio entrata (turni chiamante trascritti):',
                          'OK' if any(t.get('role','').startswith('user') for t in tr) else 'NESSUNO -> verifica RTP in ingresso')
                    print('  Audio uscita  (turni agente):',
                          'OK' if any(t.get('role','').startswith('agent') for t in tr) else 'NESSUNO -> verifica RTP in uscita')
                    print('  Link trascrizione: https://elevenlabs.io/app/agents/agents/%s/history/%s'%(AGENT,active))
                    hr('#')
                    baseline.add(active); active=None; printed_turns=0
                    print('\n  In ascolto per un\'altra chiamata...\n')
            time.sleep(3)
        except urllib.error.URLError as e:
            print('  (rete) ', e, '- ritento tra 5s'); time.sleep(5)
        except KeyboardInterrupt:
            print('\n  Monitor chiuso.'); return

if __name__ == '__main__':
    preflight()
    watch()
