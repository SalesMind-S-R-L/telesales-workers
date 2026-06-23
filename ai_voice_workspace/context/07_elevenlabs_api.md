# ElevenLabs API — Reference operativa

## Account attuale (post-migrazione 2026-05-05)
- Email: `admin@telesales.it`
- API key: in `.env` come `ELEVENLABS_API_KEY=sk_...` (var name può variare, default `sk_9148f936...` per Culligan)
- Base URL: `https://api.elevenlabs.io`

12 agenti ricreati post-migrazione. Voci custom mappate su premade (per identiche serve Pro + nuovo clone).

## Endpoints chiave

### Agenti
```
GET    /v1/convai/agents                     # lista
GET    /v1/convai/agents/{id}                # dettaglio (prompt, tools, settings)
PATCH  /v1/convai/agents/{id}                # update prompt/settings/tools
```

Body PATCH per aggiornare prompt + tools:
```json
{
  "conversation_config": {
    "agent": {
      "prompt": {
        "prompt": "...",
        "built_in_tools": {
          "end_call": {"name":"end_call","description":"...",
                       "response_timeout_secs":20,
                       "params":{"system_tool_type":"end_call"}},
          "voicemail_detection": {"name":"voicemail_detection",
                                  "description":"...",
                                  "response_timeout_secs":20,
                                  "params":{"system_tool_type":"voicemail_detection",
                                            "voicemail_message":""}}
        }
      }
    },
    "conversation": {"max_duration_seconds": 180}
  }
}
```

### Chiamate outbound singole
```
POST   /v1/convai/conversations/outbound          # via convai (preferito per simple calls)
POST   /v1/convai/sip-trunk/outbound-call         # via SIP trunk diretto (Telnyx)
```

Payload:
```json
{
  "agent_id": "agent_...",
  "agent_phone_number_id": "phnum_...",
  "to_number": "+39...",
  "conversation_initiation_client_data": {
    "dynamic_variables": {
      "nome_azienda": "...",
      "nome_titolare": "...",
      "categoria": "hotel",
      "citta": "Bolzano",
      "indirizzo": "...",
      "note_extra": "...",
      "row_index": "12"
    }
  }
}
```

### Batch outbound
```
POST   /v1/convai/batch-calling/submit
GET    /v1/convai/batch-calling/{id}
GET    /v1/convai/batch-calling/workspace?limit=20
```

Payload batch:
```json
{
  "call_name": "Culligan-Bolzano-20260518-1731",
  "agent_id": "agent_...",
  "agent_phone_number_id": "phnum_...",
  "recipients": [
    {"phone_number": "+39...",
     "conversation_initiation_client_data": {"dynamic_variables": {...}}}
  ],
  "target_concurrency_limit": 1,
  "telephony_call_config": {"ringing_timeout_secs": 60}
}
```

**Regola d'oro**: `target_concurrency_limit=1` → sequenziale, no overlap, no SIP overload.

### Conversazioni
```
GET    /v1/convai/conversations?agent_id=...&page_size=100
GET    /v1/convai/conversations/{id}        # dettaglio: transcript + analysis
```

Campi rilevanti del dettaglio:
- `transcript` — turn-by-turn `[{role: "agent"|"user", message, time_in_call_secs}]`
- `analysis.transcript_summary` — riassunto generato
- `analysis.data_collection_results` — campi strutturati estratti (nome_contatto, telefono_diretto, email_contatto, appuntamento_preso, data_appuntamento, note_chiamata)
- `metadata.start_time_unix_secs` — timestamp inizio
- `metadata.call_duration_secs`
- `metadata.termination_reason`
- `conversation_initiation_client_data.dynamic_variables.nome_azienda` — per match con foglio

### Webhooks
```
GET    /v1/workspace/webhooks                # lista webhook workspace
PATCH  agents.platform_settings.workspace_overrides.webhooks.post_call_webhook_id
```

Configurazione consigliata sul webhook agente:
```json
{
  "post_call_webhook_id": "<webhook_id>",
  "events": ["transcript"],
  "transcript_format": "json",
  "send_audio": false
}
```

URL webhook punta a Apps Script web app (vedi `sop_postcall_webhook.md`).

## Errori comuni

| Errore | Causa | Fix |
|---|---|---|
| `486 User Busy` | SIP fail | Retry (vedi `sop_sip_retry.md`) |
| `pcm_44100 not supported on SIP` | Voice cloning sample rate | Clonare a 16000 Hz per agenti SIP |
| `dynamic_variable missing` | Variabile non popolata | Verifica payload `dynamic_variables` |
| `webhook 504 timeout` | Apps Script lento | Restituisci 200 subito e fai work async |

## Costi (riferimento maggio 2026)

- LLM: ~0.005 $/min (Gemini Flash Lite)
- TTS conversational v3: ~0.04 $/min
- SIP outbound (Telnyx): ~0.02 €/min Italia mobile
- Webhook: gratis

Costo medio chiamata HoReCa di 2 min: ~0.10-0.15 €
