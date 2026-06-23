export const meta = {
  name: 'culligan-list-curation',
  description: 'Cura liste Culligan: classifica 602 aziende ambigue HoReCa vs non-target + go-list/kill-list per segmento',
  phases: [
    { title: 'Classifica', detail: '11 agenti classificano le aziende ambigue HoReCa-vero vs non-target' },
    { title: 'Strategia', detail: 'sintesi go-list/kill-list per citta x categoria x telefono' },
  ],
}

const DIR = '/Users/simocors/Desktop/telesales/fri_run/listanalysis'
const N_ALTRO = 11

const CLS_SCHEMA = {
  type: 'object',
  properties: {
    aziende: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          nome: { type: 'string' },
          is_horeca: { type: 'boolean', description: 'true se e un locale HoReCa che serve acqua/bevande agli ospiti (bar, ristorante, pizzeria, hotel, b&b, gelateria, pasticceria, agriturismo, osteria, trattoria, pub, enoteca, braceria, caffe). false se NON e un target acqua: scuola, ente, castello/museo, negozio, ufficio, nome di persona puro, azienda generica S.r.l./S.a.s. senza ristorazione, catena fast food corporate.' },
          cat_vera: { type: 'string', enum: ['bar/caffe','ristorante','pizzeria','hotel/bb','gelateria','pasticceria','agriturismo','altro_horeca','NON_TARGET'] },
          motivo: { type: 'string', description: 'breve motivo se NON_TARGET, altrimenti vuoto' },
        },
        required: ['nome', 'is_horeca', 'cat_vera', 'motivo'],
      },
    },
  },
  required: ['aziende'],
}

phase('Classifica')
const idx = Array.from({ length: N_ALTRO }, (_, i) => i)
const cls = await parallel(idx.map((i) => () =>
  agent(
    `Sei un esperto del settore HoReCa italiano (Alto Adige/Trentino). Devi classificare aziende per una campagna Culligan (trattamento acqua: vende sistemi acqua alla spina a locali che servono acqua/bevande agli ospiti).\n\n` +
    `STEP 1: leggi il file ${DIR}/altro_${i}.json con Read. Contiene ~60 nomi di aziende con citta.\n` +
    `STEP 2: per OGNI azienda decidi se e un TARGET HoReCa valido (locale che serve acqua/bevande: bar, ristorante, pizzeria, hotel, b&b, garni, pension, gelateria, pasticceria, agriturismo, osteria, trattoria, pub, enoteca, braceria, caffe, gasthaus, stube, ethnic restaurant) oppure NON_TARGET (scuola/istituto, ente pubblico, castello/museo/venue eventi, negozio, ufficio, studio, nome di persona puro senza attivita ristorativa evidente, azienda S.r.l./S.a.s. generica, catena fast-food corporate tipo McDonald's/Burger King).\n` +
    `Nel dubbio su un nome che SEMBRA un locale (es. "Anatolia", "Cibus", "City Chicken", "Da Zio Alfonso", "Braceria X") → is_horeca=true, cat_vera best-guess.\n` +
    `Restituisci array "aziende" con una entry per ogni nome del file.`,
    { label: `cls-${i + 1}`, phase: 'Classifica', schema: CLS_SCHEMA, agentType: 'Explore' }
  )
))

const allCls = cls.filter(Boolean).flatMap(r => r.aziende)
const nonTarget = allCls.filter(a => !a.is_horeca)
log(`Classificate ${allCls.length} aziende ambigue · NON_TARGET trovati: ${nonTarget.length}`)

phase('Strategia')
const STRAT_SCHEMA = {
  type: 'object',
  properties: {
    sintesi: { type: 'string', description: 'la conclusione strategica sulle liste in 3-4 frasi' },
    segmenti_KILL: { type: 'array', items: { type: 'object', properties: { segmento: { type: 'string' }, motivo: { type: 'string' }, aziende_da_non_chiamare: { type: 'number' } }, required: ['segmento', 'motivo', 'aziende_da_non_chiamare'] }, description: 'segmenti citta x categoria da SMETTERE di chiamare (bassa resa)' },
    segmenti_GO: { type: 'array', items: { type: 'object', properties: { segmento: { type: 'string' }, perche: { type: 'string' }, priorita: { type: 'number' } }, required: ['segmento', 'perche', 'priorita'] }, description: 'segmenti su cui concentrare le chiamate, ordinati per priorita (1=max)' },
    profilo_vincente: { type: 'string', description: 'il profilo azienda con piu probabilita di appuntamento, basato su engagement+app+forense' },
    regole_go_list: { type: 'array', items: { type: 'string' }, description: 'regole operative per costruire la lista di chiamata di domani' },
    quante_aziende_go: { type: 'number', description: 'stima aziende nella go-list pulita' },
  },
  required: ['sintesi', 'segmenti_KILL', 'segmenti_GO', 'profilo_vincente', 'regole_go_list', 'quante_aziende_go'],
}

const segData = await agent(
  `Sei un direttore vendite che cura le liste di una campagna AI voice Culligan HoReCa in Alto Adige/Trentino. Obiettivo: chiamare SOLO liste/segmenti che possono produrre appuntamenti, smettere quelli morti.\n\n` +
  `DATI A DISPOSIZIONE — leggi il file ${DIR}/segments.json con Read: 41 segmenti (citta x categoria) con tot aziende, called, eng (engaged=dialogo reale/email/appuntamento), app (appuntamenti), nonint (non interessati), esausti (3 call a vuoto).\n\n` +
  `AZIENDE NON_TARGET gia identificate da escludere dalle liste (${nonTarget.length}): ` + JSON.stringify(nonTarget.map(a => a.nome)) + `\n\n` +
  `CONTESTO FORENSE (gia accertato su 97 chiamate): decisore raggiunto solo 29%; close reale 0/13; audio caduto 22.7%; obiezione "acqua di montagna" strutturale in zona; hotel/bb agganciano al 50% ma non convertono (rimandano a email/stagione); i 5 appuntamenti storici sono tutti di Bolzano; Merano e' German-heavy (problema lingua); Trento+Lavis 225 aziende mai chiamate; cellulare e fisso agganciano simile (~30%).\n\n` +
  `Produci la strategia liste: quali segmenti KILLARE (citta x cat a bassa resa), quali GO (ordinati per priorita), il profilo azienda vincente, e le regole operative per costruire la go-list di domani. Sii concreto e numerico.`,
  { label: 'strategia-liste', phase: 'Strategia', schema: STRAT_SCHEMA }
)

return { aziende_classificate: allCls.length, non_target: nonTarget, strategia: segData }
