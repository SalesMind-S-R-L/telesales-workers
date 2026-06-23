Aggiungi al sito Telesales (telesales.it) una **sezione "Parla con Marco"**: un riquadro interattivo, identico per logica a quello che usiamo per la demo TelNet, dove il visitatore preme un pulsante, consente il microfono e **parla a voce dal vivo** con il nostro agente AI "Marco Ferretti — Spiegazione Aziendale" (presentazione dell'azienda). L'interfaccia è nera con barre audio oro che reagiscono alla voce reale (niente orb o marchi terzi).

## Contesto tecnico (importante)
- L'agente vive su ElevenLabs Conversational AI, è **pubblico**, ID: `agent_9201krn8z6ptevxsmx3g5e6vy69b`. Per girare nel browser basta l'ID, nessuna API key.
- Il componente usa l'SDK ufficiale `@elevenlabs/client` importato via CDN (ESM). Funziona solo in **HTTPS** e richiede il **permesso microfono** (il browser lo chiede al primo avvio).
- Il visualizzatore audio è guidato da `setInterval` (NON `requestAnimationFrame`, che Chrome sospende quando il tab è in background).
- **Il salvataggio delle conversazioni sul foglio Google NON lo fa il sito.** È gestito dal *post-call webhook* dell'agente lato ElevenLabs (come per TelNet). Il sito deve solo avviare la conversazione con l'agent ID giusto. Non aggiungere logica di salvataggio nel sito.
- Classi e ID del componente sono prefissati con `mv-` / `marco-` per non entrare in conflitto con gli stili esistenti del sito. Le variabili CSS sono scoperte (scoped) sul contenitore, non su `:root`.

## Cosa fare
Inserisci nella pagina (dove ha senso, es. dopo la hero o in una sezione "Provalo ora") il seguente blocco self-contained. Se il sito usa React/Next o componenti, incapsulalo in un componente client (lo `<script type="module">` va eseguito lato browser; in Next puoi usare un `<Script>` o un componente con `useEffect` che importa l'SDK). Mantieni il markup, le classi `mv-` e gli ID invariati. Adatta solo eventuali testi/colori se serve coerenza col resto del sito (di default è nero/oro Telesales e sta bene su qualsiasi sfondo).

```html
<!-- ===== SEZIONE: Parla con Marco (voce AI Telesales) ===== -->
<section class="mv-stage" id="marco-voice">
  <style>
    #marco-voice{
      --mv-gold:#D4AF37; --mv-gold-lite:#F5E7A8; --mv-gold-deep:#7A5E18;
      --mv-grad:linear-gradient(135deg,#F5E7A8 0%,#D4AF37 45%,#7A5E18 100%);
      --mv-green:#5EE08C; --mv-line:rgba(212,175,55,.16);
      --mv-t50:rgba(255,255,255,.52); --mv-t35:rgba(255,255,255,.35);
      --mv-font:"Plus Jakarta Sans",-apple-system,system-ui,sans-serif;
      position:relative; max-width:540px; margin:40px auto; padding:0 20px;
      font-family:var(--mv-font);
    }
    #marco-voice .mv-eyebrow{text-align:center;color:var(--mv-gold);font-size:12.5px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;margin-bottom:10px}
    #marco-voice .mv-title{text-align:center;color:#fff;font-size:clamp(24px,4vw,34px);font-weight:800;letter-spacing:-.02em;margin-bottom:22px}
    #marco-voice .mv-console{position:relative;border-radius:28px;padding:46px 34px 38px;text-align:center;
      background:linear-gradient(180deg,#0c0a06,#050402);border:1px solid var(--mv-line);overflow:hidden;
      box-shadow:0 40px 120px rgba(0,0,0,.7),inset 0 1px 0 rgba(255,255,255,.04);color:#fff}
    #marco-voice .mv-console::before{content:"";position:absolute;inset:0;pointer-events:none;
      background:radial-gradient(120% 80% at 50% -10%,rgba(212,175,55,.14),transparent 60%)}
    #marco-voice .mv-viz{position:relative;height:92px;display:flex;align-items:center;justify-content:center;gap:7px;margin-bottom:28px}
    #marco-voice .mv-viz span{width:7px;height:14px;border-radius:6px;background:linear-gradient(180deg,var(--mv-gold-lite),var(--mv-gold-deep));opacity:.4;transition:opacity .3s}
    #marco-voice .mv-console[data-state="idle"] .mv-viz span{height:14px;opacity:.28}
    #marco-voice .mv-console[data-state="connecting"] .mv-viz span{animation:mvBob 1s ease-in-out infinite;opacity:.55}
    #marco-voice .mv-console[data-state="listening"] .mv-viz span{animation:mvBob 1.4s ease-in-out infinite;opacity:.7}
    #marco-voice .mv-console[data-state="speaking"] .mv-viz span{animation:mvTalk .55s ease-in-out infinite;opacity:1}
    #marco-voice .mv-viz span:nth-child(1){animation-delay:0s}#marco-voice .mv-viz span:nth-child(2){animation-delay:.08s}
    #marco-voice .mv-viz span:nth-child(3){animation-delay:.16s}#marco-voice .mv-viz span:nth-child(4){animation-delay:.24s}
    #marco-voice .mv-viz span:nth-child(5){animation-delay:.32s}#marco-voice .mv-viz span:nth-child(6){animation-delay:.20s}
    #marco-voice .mv-viz span:nth-child(7){animation-delay:.12s}#marco-voice .mv-viz span:nth-child(8){animation-delay:.04s}
    @keyframes mvBob{0%,100%{height:14px}50%{height:34px}}
    @keyframes mvTalk{0%,100%{height:16px}50%{height:62px}}
    #marco-voice .mv-status{font-size:22px;font-weight:700;letter-spacing:-.01em;margin-bottom:8px}
    #marco-voice .mv-sub{color:var(--mv-t50);font-size:14px;max-width:340px;margin:0 auto 24px;min-height:20px}
    #marco-voice .mv-controls{display:flex;gap:12px;justify-content:center;align-items:center}
    #marco-voice .mv-b{display:inline-flex;align-items:center;gap:10px;border:none;cursor:pointer;font-family:var(--mv-font);font-weight:700;font-size:15.5px;border-radius:100px;padding:15px 28px;transition:transform .2s,box-shadow .2s}
    #marco-voice .mv-b svg{width:18px;height:18px}
    #marco-voice .mv-call{background:var(--mv-grad);color:#1a1400;box-shadow:0 14px 38px rgba(212,175,55,.3)}
    #marco-voice .mv-call:hover{transform:translateY(-2px);box-shadow:0 20px 50px rgba(212,175,55,.42)}
    #marco-voice .mv-end{background:rgba(255,80,80,.12);color:#ff8a8a;border:1px solid rgba(255,120,120,.3)}
    #marco-voice .mv-end:hover{background:rgba(255,80,80,.2)}
    #marco-voice .mv-b[hidden]{display:none}
    #marco-voice .mv-err{margin-top:14px;font-size:12.5px;color:#ff8a8a;min-height:16px}
    #marco-voice .mv-note{margin-top:14px;font-size:12px;color:var(--mv-t35)}
    #marco-voice .mv-note b{color:var(--mv-green);font-weight:600}
  </style>

  <div class="mv-eyebrow">Provalo ora</div>
  <div class="mv-title">Parla con Marco, la voce AI di Telesales</div>

  <div class="mv-console" id="marco-console" data-state="idle">
    <div class="mv-viz"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
    <div class="mv-status" id="marco-status">Parla con Marco di Telesales</div>
    <div class="mv-sub" id="marco-sub">Premi "Avvia la conversazione", consenti il microfono e chiedigli cosa fa Telesales.</div>
    <div class="mv-controls">
      <button class="mv-b mv-call" id="marco-start">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        Avvia la conversazione
      </button>
      <button class="mv-b mv-end" id="marco-end" hidden>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
        Termina
      </button>
    </div>
    <div class="mv-err" id="marco-err"></div>
    <div class="mv-note">Funziona dal browser · <b>serve il microfono</b></div>
  </div>

  <script type="module">
    import { Conversation } from 'https://cdn.jsdelivr.net/npm/@elevenlabs/client/+esm';

    const AGENT_ID = 'agent_9201krn8z6ptevxsmx3g5e6vy69b'; // Marco Ferretti — Spiegazione Aziendale (pubblico)
    const consoleEl = document.getElementById('marco-console');
    const statusEl  = document.getElementById('marco-status');
    const subEl     = document.getElementById('marco-sub');
    const startBtn  = document.getElementById('marco-start');
    const endBtn    = document.getElementById('marco-end');
    const errEl     = document.getElementById('marco-err');
    const bars      = Array.from(consoleEl.querySelectorAll('.mv-viz span'));

    let convo = null, vizTimer = null, mode = 'listening';
    const N = bars.length;
    const heights = new Array(N).fill(14);

    const TXT = {
      idle:       ['Parla con Marco di Telesales', 'Premi "Avvia la conversazione", consenti il microfono e chiedigli cosa fa Telesales.'],
      connecting: ['Connessione in corso…', 'Sto avviando la conversazione con Marco.'],
      listening:  ['Ti ascolto…', 'Chiedi pure: cosa fa Telesales, come funziona, risultati, prezzi.'],
      speaking:   ['Sto rispondendo…', 'Marco di Telesales ti sta parlando.'],
    };
    function setState(s){ consoleEl.dataset.state = s; const [a,b]=TXT[s]||TXT.idle; statusEl.textContent=a; subEl.textContent=b; }

    function freqData(){
      if(!convo) return null;
      try{
        const out = convo.getOutputByteFrequencyData ? convo.getOutputByteFrequencyData() : null;
        const inp = convo.getInputByteFrequencyData ? convo.getInputByteFrequencyData() : null;
        const oVol = convo.getOutputVolume ? convo.getOutputVolume() : 0;
        const iVol = convo.getInputVolume ? convo.getInputVolume() : 0;
        return (oVol >= iVol ? out : inp) || out || inp;
      }catch(e){ return null; }
    }
    function animate(){
      const data = freqData();
      const order = [3,2,1,0,1,2,3,4];
      for(let i=0;i<N;i++){
        let target = 14;
        if(data && data.length){
          const g = order[i]||0, span = 22, start = 6 + g*span;
          let sum=0,cnt=0;
          for(let k=start;k<start+span && k<data.length;k++){ sum+=data[k]; cnt++; }
          target = 12 + ((cnt?sum/cnt:0)/255)*64;
        }
        heights[i] += (target - heights[i]) * 0.35;
        bars[i].style.height = heights[i].toFixed(1) + 'px';
        bars[i].style.opacity = (0.45 + (heights[i]-12)/64 * 0.55).toFixed(2);
      }
    }
    function startViz(){ bars.forEach(b=>b.style.animation='none'); if(!vizTimer) vizTimer=setInterval(animate,33); }
    function stopViz(){ if(vizTimer){clearInterval(vizTimer);vizTimer=null;} bars.forEach(b=>{b.style.height='';b.style.opacity='';b.style.animation='';}); heights.fill(14); }

    async function start(){
      errEl.textContent=''; setState('connecting'); startBtn.hidden=true;
      try{
        await navigator.mediaDevices.getUserMedia({ audio:true });
        const c = await Conversation.startSession({
          agentId: AGENT_ID,
          connectionType: 'webrtc',
          onConnect: () => { setState('listening'); endBtn.hidden=false; },
          onDisconnect: () => cleanup(),
          onError: (e) => { errEl.textContent='Si è verificato un problema. Riprova.'; console.error(e); cleanup(); },
          onModeChange: (m) => { mode=(m&&(m.mode||m))||'listening'; if(consoleEl.dataset.state==='connecting') return; setState(mode==='speaking'?'speaking':'listening'); },
        });
        convo = c; startViz();
      }catch(e){
        console.error(e);
        errEl.textContent = (e&&e.name==='NotAllowedError')
          ? 'Microfono negato. Consenti l’accesso al microfono e riprova.'
          : 'Impossibile avviare la conversazione. Riprova tra un istante.';
        cleanup();
      }
    }
    async function end(){ const c=convo; convo=null; try{ if(c) await c.endSession(); }catch(e){} cleanup(); }
    function cleanup(){ convo=null; stopViz(); endBtn.hidden=true; startBtn.hidden=false; setState('idle'); }

    startBtn.addEventListener('click', start);
    endBtn.addEventListener('click', end);
    window.addEventListener('beforeunload', () => { try{ convo && convo.endSession(); }catch(e){} });
    setState('idle');
  </script>
</section>
<!-- ===== /SEZIONE Parla con Marco ===== -->
```

## Requisiti / note finali
- Assicurati che il font "Plus Jakarta Sans" sia caricato (se il sito non lo ha già, aggiungi nel <head>: `<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&display=swap" rel="stylesheet">`). In alternativa eredita il font del sito rimuovendo la riga `--mv-font`.
- Il sito deve essere servito in HTTPS (telesales.it lo è) perché il microfono funzioni.
- NON aggiungere chiavi API, webhook o logica di salvataggio nel sito: la raccolta dati e il salvataggio su foglio sono gestiti dal post-call webhook dell'agente su ElevenLabs.
- Se usi Next.js/React: metti `'use client'`, importa l'SDK dentro un `useEffect` (o usa un `<script type="module">` in una pagina statica), e aggancia i listener agli elementi via ref/id. La logica resta identica.
- Testa con il tab in primo piano e microfono consentito: deve connettersi, salutare ("Pronto! Sono Marco di Telesales…"), ascoltare e rispondere, con le barre che reagiscono alla voce. Il pulsante "Termina" chiude la conversazione.
