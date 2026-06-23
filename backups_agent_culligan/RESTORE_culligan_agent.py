#!/usr/bin/env python3
"""
ROLLBACK Culligan AI agent to a previous backup.

Usage:
    python3 RESTORE_culligan_agent.py                          # restore latest
    python3 RESTORE_culligan_agent.py culligan_agent_XXX.json  # restore specific
"""
import sys, json, urllib.request, glob, os

AGENT_ID = "agent_5101kreejrz1e98rfzjrf3brhd50"
API_KEY = "sk_9148f936dc1c67e88b13f7b400333cb87813613682f70726"
BACKUP_DIR = "/Users/simocors/Desktop/telesales/backups_agent_culligan"

if len(sys.argv) > 1:
    backup_file = sys.argv[1]
    if not backup_file.startswith("/"):
        backup_file = os.path.join(BACKUP_DIR, backup_file)
else:
    files = sorted(glob.glob(f"{BACKUP_DIR}/culligan_agent_*.json"), reverse=True)
    if not files:
        print("Nessun backup trovato")
        sys.exit(1)
    backup_file = files[0]
    print(f"Usando ultimo backup: {os.path.basename(backup_file)}")

backup = json.load(open(backup_file))
cc = backup['conversation_config']

# Restore TUTTI i campi modificabili
payload = {
    'conversation_config': {
        'agent': {
            'prompt': {
                'prompt': cc['agent']['prompt']['prompt'],
                'llm': cc['agent']['prompt'].get('llm'),
                'temperature': cc['agent']['prompt'].get('temperature'),
                'max_tokens': cc['agent']['prompt'].get('max_tokens'),
            },
            'first_message': cc['agent'].get('first_message', ''),
            'language': cc['agent'].get('language', 'it'),
        },
        'tts': {
            'model_id': cc['tts'].get('model_id'),
            'voice_id': cc['tts'].get('voice_id'),
            'stability': cc['tts'].get('stability'),
            'similarity_boost': cc['tts'].get('similarity_boost'),
            'speed': cc['tts'].get('speed'),
            'optimize_streaming_latency': cc['tts'].get('optimize_streaming_latency'),
            'expressive_mode': cc['tts'].get('expressive_mode'),
        },
        'turn': {
            'turn_timeout': cc['turn'].get('turn_timeout'),
            'mode': cc['turn'].get('mode'),
        },
        'asr': {
            'provider': cc['asr'].get('provider'),
            'quality': cc['asr'].get('quality'),
        },
    }
}

# Confirm
print(f"\nSto per ripristinare:")
print(f"  prompt: {len(cc['agent']['prompt']['prompt'])} chars")
print(f"  voice: {cc['tts'].get('voice_id')}")
print(f"  stability: {cc['tts'].get('stability')}")
print(f"  turn_timeout: {cc['turn'].get('turn_timeout')}")
ans = input("\nProcedere? (s/N): ")
if ans.lower() != 's':
    print("Annullato.")
    sys.exit(0)

req = urllib.request.Request(
    f'https://api.elevenlabs.io/v1/convai/agents/{AGENT_ID}',
    data=json.dumps(payload).encode(),
    headers={'xi-api-key': API_KEY, 'Content-Type': 'application/json'},
    method='PATCH'
)
resp = json.load(urllib.request.urlopen(req, timeout=30))
print(f"\n✓ RESTORE OK — agent_id: {resp.get('agent_id')}")
print(f"  prompt ora: {len(resp['conversation_config']['agent']['prompt']['prompt'])} chars")
