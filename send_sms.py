#!/usr/bin/env python3
"""
Invia SMS via Telnyx da numero Telesales.
Il destinatario riceve il messaggio con mittente "Telesales".

Uso:
  python3 send_sms.py +393939764799 "Messaggio qui"
  python3 send_sms.py 3939764799 "Messaggio"   (normalizza automaticamente)
"""
import sys, re, requests, os

TELNYX_KEY  = os.environ.get('TELNYX_KEY', '')
FROM_NUMBER = '+17852084549'  # US number con profilo "Telesales Italia SMS"

def norm(p):
    p = re.sub(r'[^\d+]', '', str(p).strip())
    if p.startswith('+'): return p
    if p.startswith('39') and len(p) >= 11: return '+' + p
    return '+39' + p

def send_sms(to, text):
    to = norm(to)
    resp = requests.post(
        'https://api.telnyx.com/v2/messages',
        headers={'Authorization': f'Bearer {TELNYX_KEY}', 'Content-Type': 'application/json'},
        json={'from': FROM_NUMBER, 'to': to, 'text': text},
        timeout=20
    )
    d = resp.json().get('data', {})
    status = d.get('to', [{}])[0].get('status', '?') if d.get('to') else resp.text[:100]
    msg_id  = d.get('id', '?')
    print(f'SMS → {to} | status: {status} | id: {msg_id}')
    return resp.status_code == 200

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Uso: python3 send_sms.py <numero> "<messaggio>"')
        sys.exit(1)
    send_sms(sys.argv[1], sys.argv[2])
