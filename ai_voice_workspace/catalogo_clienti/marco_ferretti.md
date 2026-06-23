# Cliente — Marco Ferretti (Telesales)

## Stack
**Doppio**: ElevenLabs (production) + Deepgram (test parallelo).

## ElevenLabs

### Agenti
- **Marco Ferretti — Spiegazione Aziendale** (`agent_9201krn8z6ptevxsmx3g5e6vy69b`) — usato per landing `chiamami.html`, lead chiama, Marco spiega Telesales in 2-3 min e raccoglie email+telefono
- **Marco Ferretti — Browser Demo (white-label)** (`agent_1501krkcp8e0e8yb8p3zpfsv2drn`) — versione white-label per demo browser
- **Marco Ferretti 2.0 — Demo & Sales** (`agent_5301kpdv4sd9e15vcz4qpm8e7vrn`) — versione full sales con 9 prodotti

### Settings agente Spiegazione
- max_duration_seconds: 300
- Modello LLM: gemini-2.5-flash-lite (temp 0.7)
- TTS: eleven_v3_conversational, stability 0.2, similarity 0.8, speed 1.1, expressive_mode TRUE
- Phone ID: `phnum_1501kr3sx76sfxeap503jqy1m7j9` (Telnyx Italia)
- Webhook post-call: `apps_script_marco_ferretti.gs` → email recap solo per positivi

### Audio tags rules
- `[warm]` SOLO primo turno (apertura)
- `[happy]` durante
- `[cheerful]` chiusura
- MAI `[excited]` (suona artificiale)
- Tag SEMPRE all'inizio della frase, mai a metà

### Anti-esclamativo (regola CRITICA)
VIETATO aprire con: "Perfetto!", "Ottima scelta!", "Ottimo!", "Bene!", "Certo!", "Esatto!", "Assolutamente!", "Wow!"
Eccezione: "Certo," (basso, senza esclamativo).

### Chiusure
- Positiva: "Ottimo. Niccolò ti può sentire lunedì o martedì. Mi dai il tuo cellulare diretto e la tua email migliore? Ti mando intanto il materiale sui 9 prodotti."
- Richiamare: "Perfetto. Mi lasci email e cellulare? Ti mando riepilogo e Niccolò ti sente quando vuoi tu."
- Negativa: "Rispetto. Ti lascio il sito telesales.it, se cambi idea ci trovi sempre. Buona giornata."

### Tripla conferma appuntamento (importante)
Quando fissi appuntamento, DICHIARA SEMPRE che il lead riceverà:
1. WhatsApp di conferma con data/ora/link call
2. Email di riepilogo + materiale prodotti
3. Invito calendar (Google Cal / iCal)

Frase tipo: "Perfetto [nome], ti riassumo: [giorno] alle [ora] hai call con Niccolò Pratesi. Tra cinque minuti ti arriva un WhatsApp di conferma sul cellulare e una email con il riepilogo e i materiali. Trovi anche l'invito sul tuo calendario."

## Deepgram (parallel test)

### Asset
- Voice: `aura-2-elio-it`
- Voice Cribis test: `aura-2-cesare-it`
- Project ID: `b4d78343`
- API key: `.env.deepgram`
- Audio I/O: `sounddevice` (Python)
- Script: `smart_batch_caller.py` con tag Marco AI

### Note
Setup parallelo per testare Deepgram vs ElevenLabs su stesso flow. Da valutare quale ha:
- Latenza minore (Deepgram tipicamente ~200ms minore)
- Qualità voce italiana migliore (ElevenLabs vince su naturalezza, Deepgram su clarity)
- Costo per minuto inferiore (dipende dal piano)

## Landing chiamami.html

- Repo: `telesales-website-deploy/chiamami.html`
- Deploy multi-repo:
  - `telesales-website` (principale)
  - `SalesMind-srl/chiamami` (white-label SalesMind)
  - `marco-chiama` (vanity)
- Logo Telesales gold top-left (no pulse "Live · Adesso")
- Vedi `sop/sop_landing_integration.md` per setup completo

## Tone of voice

Imprenditore milanese smart, ENERGICO. Velocità alta, ritmo, frizzante. Sorriso sempre. Frasi corte (4-12 parole). Mai cupo, mai monotono, mai da call center.

Reference: prompt `agent_9201krn8z6ptevxsmx3g5e6vy69b` (19.7k chars) — il prompt più rifinito del workspace.
