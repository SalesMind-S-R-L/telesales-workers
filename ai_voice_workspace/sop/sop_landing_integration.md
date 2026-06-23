# SOP — Lead landing page + ElevenLabs outbound

## Quando applicare
Quando si vuole un flusso `lead inserisce numero su landing → l'AI chiama subito` (es. `chiamami.html` di Telesales con Marco Ferretti).

## Architettura

```
[Landing HTML]
   form: nome + telefono
        │
        ▼
   submit → fetch("/api/start-call", {body: {nome, telefono}})
        │
        ▼
[Cloudflare Worker / Apps Script API]
        │
        ▼
   POST /v1/convai/conversations/outbound  (ElevenLabs)
        │
        ▼
[Marco Ferretti chiama il numero]
        │
        ▼
   post_call_webhook → sheet lead + email recap
```

## Componenti

### 1. Landing HTML (file: `telesales-website-deploy/chiamami.html`)
- Form con nome + telefono
- Telesales gold logo top-left (no pulse "Live · Adesso")
- Validazione client-side numero italiano (+39 / 3xx mobile o 0xxx fisso)
- Submit con loading state
- On success: messaggio "Marco ti sta chiamando, rispondi al telefono"

```html
<form id="callForm">
  <input name="nome" placeholder="Nome" required>
  <input name="phone" placeholder="+39 ..." required pattern="^[+0-9 ]+$">
  <button type="submit">Chiamami</button>
</form>
<script>
document.getElementById('callForm').addEventListener('submit', async e => {
  e.preventDefault();
  const f = new FormData(e.target);
  const r = await fetch('/api/start-call', {
    method: 'POST',
    headers: {'content-type':'application/json'},
    body: JSON.stringify({nome: f.get('nome'), phone: f.get('phone')})
  });
  if (r.ok) showMsg('Marco ti sta chiamando, rispondi al telefono');
});
</script>
```

### 2. Endpoint server (Cloudflare Worker / Apps Script web app / Node)

```js
async function startCall(req) {
  const {nome, phone} = await req.json();
  const r = await fetch('https://api.elevenlabs.io/v1/convai/conversations/outbound', {
    method: 'POST',
    headers: {
      'xi-api-key': ENV.ELEVENLABS_API_KEY,
      'content-type': 'application/json'
    },
    body: JSON.stringify({
      agent_id: 'agent_9201krn8z6ptevxsmx3g5e6vy69b',  // Marco Ferretti Spiegazione
      agent_phone_number_id: 'phnum_1501kr3sx76sfxeap503jqy1m7j9',
      to_number: normalizePhone(phone),
      conversation_initiation_client_data: {
        dynamic_variables: {
          nome_contatto: nome,
          source: 'landing_chiamami',
          submitted_at: new Date().toISOString()
        }
      }
    })
  });
  return new Response(JSON.stringify(await r.json()), {status: r.status});
}
```

### 3. Deploy GitHub Pages (multi-account)

Stack attuale Telesales:
- Repo `telesales-website` (account principale)
- Repo `SalesMind-srl/chiamami` (deploy white-label)
- Repo `marco-chiama`

Tool: `gh` CLI con multi-account. Per push:
```bash
gh auth switch -u SalesMind-srl
git push origin main
# poi torna account principale
gh auth switch -u simocors
```

### 4. Post-call: email recap solo per chiamate positive

Sull'agente Marco Ferretti il post-call webhook punta a Apps Script `apps_script_marco_ferretti.gs`:
```js
function handlePostCall_(d) {
  var esito = deduceEsito_(d);
  if (esito === 'Appuntamento' || esito === 'Email') {
    sendNotifEmails_(d);  // a admintelesales@gmail.com + lead.email
  }
}
```

Vedi `/Users/simocors/Desktop/telesales/demo_mik/apps_script_marco_ferretti.gs` per implementazione completa.

## Voce/agent settings per agente "spiegazione aziendale"

L'agente per landing è diverso dall'outbound HoReCa: deve essere "demo style", più lungo, più ricco.

- `max_duration_seconds`: 300 (5 min)
- Modello TTS: `eleven_v3_conversational`
- Settings: stability 0.3, similarity 0.7, expressive_mode true, speed 1.0
- Audio tags: `[warm]` apertura, `[happy]` durante, `[cheerful]` chiusura
- KB: documento azienda + 9 prodotti Telesales

**Importante per SIP**: la voce custom dell'agente landing potrebbe usare `pcm_44100` — incompatibile con SIP outbound. Soluzione: clonare la voce a `pcm_16000` come "SIP version" e usare quella per agenti SIP.

## Gotchas

- **CORS** sull'endpoint server (Cloudflare Worker): aggiungi `Access-Control-Allow-Origin` per il dominio della landing
- **Rate limit**: limita le chiamate da landing a 1 ogni 60s per IP (evita spam)
- **Validazione numero**: server-side, no client-only — controlla che sia +39/0xxx
- **Privacy**: avviso GDPR sulla landing prima del form ("Il numero verrà usato per la chiamata immediata")
- **Test su numero personale prima**: una chiamata Marco Ferretti costa ~10c
