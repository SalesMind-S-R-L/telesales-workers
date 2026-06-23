# TTS Voice Settings — ElevenLabs

## Modello TTS

**`eleven_v3_conversational`** — supporta audio tags, conversazione naturale.

## Settings consigliati per outbound HoReCa / B2C

| Parametro | Valore | Note |
|---|---|---|
| `stability` | 0.2 | Bassa = più variabilità emotiva. Alta = monotono |
| `similarity_boost` | 0.8 | Alta = voce fedele al clone. Bassa = libera |
| `style` / `speed` | 1.0 - 1.1 | 1.1 per energia maggiore |
| `expressive_mode` | `true` | OBBLIGATORIO se voce risulta triste/piatta |
| `optimize_streaming_latency` | 0 | Qualità prima della latenza |
| `use_speaker_boost` | true | (opzionale) |

**Diagnostica voce triste**:
- Se l'agente suona spento → controlla `expressive_mode=true`
- Se monotono → riduci stability a 0.15
- Se troppo enfatico → alza stability a 0.35
- Se non rispetta i tag → conferma modello `eleven_v3_conversational`

## LLM dell'agente

| Parametro | Valore | Note |
|---|---|---|
| Modello | `gemini-2.5-flash-lite` | Best price/quality per voice |
| Temperature | 0.7 | Naturalezza + coerenza |
| Max tokens output | ~150 | Frasi corte |

Alternative testate:
- `gpt-4o-mini` — più verboso, sconsigliato per voice
- `claude-haiku-4-5-20251001` — qualità alta ma latenza superiore

## Voci

### Voci custom (cloned)
Disponibili solo su piano Pro+. La migrazione 5/5/2026 al nuovo account ha mappato voci custom su premade — per averle identiche serve Pro + nuovo clone.

### Voci premade italiane consigliate
- Marco / Mario → italian male, brillante
- Sofia / Sara → italian female, calda
- Verifica sempre con preview prima di pubblicare

### Naming voce
La voce deve matchare il **nome dell'agente** (es. Marco Culligan = voce maschile italiana brillante, non triste).

## Audio tags supportati (eleven_v3_conversational)

| Tag | Quando usare |
|---|---|
| `[warm]` | Primo saluto, presentazione |
| `[happy]` | Conversazione, proposta |
| `[cheerful]` | Chiusura positiva |
| `[laughs]` | Battuta, momento leggero |
| `[serious]` | Obiezioni delicate (raro) |

**VIETATI**: `[excited]` (suona artificiale), `[slow]`/`[fast]`/`[pause]`/`[smile]` (non interpretati).

Regola posizione: il tag va all'INIZIO della frase, mai a metà.

## Velocità conversazione

`speed` di conversazione (non TTS):
- `1.1` per outbound commerciale (energia)
- `1.0` per demo/intervista
- `0.9` per chiamate delicate (assistenza, condoglianze)

## Latency optimization (solo se necessario)

Se serve abbassare latenza per call center high-volume:
- `optimize_streaming_latency: 2` (compromesso qualità)
- Riduzione `chunk_size` lato client
- Pre-warmup con frase di apertura corta

Default: lascia qualità massima.
