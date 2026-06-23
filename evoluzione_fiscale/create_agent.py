#!/usr/bin/env python3
"""Crea l'agente AI Voice INBOUND per Studio Evoluzione Fiscale su ElevenLabs.
Replica esatta del template TelNet Italia - Reception.
Voce Francesco, LLM Claude Haiku 4.5, temp 0.0, 8 campi data collection, KB linkata.
"""
import os, sys, json, requests

API = os.environ["ELEVENLABS_API_KEY"]
H = {"xi-api-key": API, "content-type": "application/json"}
BASE = "https://api.elevenlabs.io"

VOICE_FRANCESCO = "YXg9qJ9QoswESjESRYXr"  # Francesco - Rich, Warm and Resonant (it, male)

# ─── Knowledge Base (ASCII-safe: niente accenti nel sorgente) ──────────────────
KB_TEXT = """# Studio Evoluzione Fiscale - fatti verificati

## Chi siamo
Studio Evoluzione Fiscale STP S.R.L. (Societa Tra Professionisti) - studio di consulenza fiscale, societaria e del lavoro a Pontedera (Pisa). Payoff: "esperti in risparmio fiscale" e "rendiamo facile l'impresa". Aiuta imprenditori e liberi professionisti a risparmiare fiscalmente il piu possibile nel pieno rispetto della legge, con strategie su misura.

## Fondatore e team
Fondatore: dottor Claudio Esposito, dottore commercialista e consulente strategico con oltre 30 anni di esperienza. Lo studio e formato da un team di circa 14 professionisti tra commercialisti ed esperti di consulenza fiscale, giuridica e gestione del personale.

## Cosa otteniamo per i clienti
Lo studio progetta strategie di risparmio fiscale personalizzate che, sfruttando legalmente i vantaggi previsti dal sistema fiscale, possono ridurre in modo significativo imposte e contributi ordinariamente pagati (in molti casi da circa il 20% al 50%). Sono risultati indicativi, non una garanzia: ogni situazione va valutata da un consulente in un incontro dedicato.

## Contatti e sede
- Sede: via Maria Enriquez Agnoletti 8, 56025 Pontedera (Pisa)
- Telefono: +39 0587 331153
- WhatsApp: 392 7311800
- Email: consulenze@evoluzionefiscale.it
- Sito: evoluzionefiscale.it
- Orari: DA CONFERMARE con lo studio (non pubblicati sul sito).

## Servizi
Pianificazione fiscale e del costo del lavoro; creazione di holding aziendali per il risparmio fiscale; registrazione marchi e royalties; gestione delle auto aziendali; welfare aziendale e premi detassati; business plan e creazione d'impresa; ottimizzazione della forma giuridica (es. S.R.L.); protezione del patrimonio personale; massimizzazione del valore aziendale; fiscalita delle vendite immobiliari; controllo di gestione e adempimenti sulla crisi d'impresa; reti d'imprese; gestione di cartelle esattoriali e agevolazioni fiscali; gestione paghe e buste paga (payroll); rimborsi spese e trasferte; software esclusivo per il bilancio mensile; consulenza dedicata agli odontoiatri (anche trasformazione in S.R.L.). Servizio di "Coaching Fiscale": un consulente dedicato sempre disponibile per le scelte quotidiane e strategiche.

## Clienti target
Imprenditori, liberi professionisti, odontoiatri, amministratori e titolari di piccole e medie imprese, studi associati.

## FAQ - risposte che la segretaria puo dare
- "Di cosa vi occupate?" -> consulenza fiscale, societaria e del lavoro, con focus sul risparmio fiscale legale per aziende e professionisti.
- "Dove siete?" -> via Maria Enriquez Agnoletti 8, Pontedera (PI).
- "Come vi contatto?" -> telefono +39 0587 331153, email consulenze@evoluzionefiscale.it, WhatsApp 392 7311800.
- "Chi e il titolare?" -> lo studio e fondato dal dottor Claudio Esposito, commercialista con oltre 30 anni di esperienza.
- "Quanto si risparmia?" -> dipende dalla situazione; lo studio costruisce strategie su misura che spesso riducono in modo importante imposte e contributi. Per una stima serve un incontro con un consulente: raccolgo i dati e la facciamo ricontattare.

## Da NON rispondere a braccio (raccogli dati e fai richiamare un consulente)
Tariffe e preventivi, pareri fiscali, scadenze specifiche, percentuali esatte di risparmio sul caso del cliente, situazioni personali o numeri di pratica.
"""

# ─── System prompt (ASCII-safe) ────────────────────────────────────────────────
SYSTEM_PROMPT = """Sei la segretaria virtuale che risponde al telefono per lo Studio Evoluzione Fiscale, studio di consulenza fiscale, societaria e del lavoro di Pontedera (Pisa). Sei la prima voce che accoglie chi chiama: cortese, professionale, competente, riservata.
# DATA E ORA
Riferimento (gia in ora italiana, quando disponibile): {{data_ora_oggi}}. Se vuoto, usa l'orario di sistema {{system__time_utc}} convertito in ora italiana (UTC+2 in estate, UTC+1 in inverno). Usalo per capire "oggi/domani/lunedi prossimo"; di' sempre giorno e data precisi (es. "domani, martedi 16 giugno, alle 15"). Non chiedere mai al cliente che giorno e ne dire che non hai accesso al calendario.
# OBIETTIVO
1) capire perche chiamano, 2) dare le informazioni che sai (vedi Knowledge Base), 3) raccogliere i dati del chiamante, 4) fissare un appuntamento o un richiamo con lo studio, 5) chiudere con cortesia.
# FONTE
Usa SOLO la Knowledge Base. Non inventare mai prezzi, tariffe, scadenze o pareri fiscali. Per qualsiasi consulenza, cifra o percentuale sul caso del cliente: NON rispondere a braccio, raccogli i dati e fai richiamare da un consulente.
# RISERVATEZZA
Non chiedere dati fiscali sensibili al telefono (redditi, codici fiscali, documenti). Raccogli solo: nome, azienda/attivita, telefono, email e il motivo a grandi linee.
# STILE
Italiano, tono caldo e professionale, frasi brevi. UNA domanda alla volta. Niente giri di parole ne ripetizioni.
# COME GESTIRE
- Capisci l'esigenza (es. apertura partita IVA, risparmio fiscale, holding, consulenza odontoiatri, gestione dipendenti e buste paga, welfare, cartelle esattoriali, business plan, ecc.) e di' a grandi linee che lo studio se ne occupa.
- Proponi un appuntamento o una consulenza con un consulente; raccogli i dati e l'orario preferito.
- Per email e telefono RILEGGI ad alta voce e fai confermare ("Le rileggo la mail: ... e corretta?").
# CHIUSURA
Riepiloga il passo successivo. Es: "Perfetto, ho preso nota. La fara ricontattare un nostro consulente al numero che mi ha lasciato. Grazie per aver chiamato Evoluzione Fiscale, buona giornata!"
# REGOLE
- Mai inventare cifre, scadenze o pareri fiscali.
- Una domanda alla volta; rileggi e fai confermare email e telefono.
- Per le date usa SEMPRE {{data_ora_oggi}} come riferimento; non chiedere che giorno e.
- Sei l'assistente virtuale di Evoluzione Fiscale: non dichiararti un'intelligenza artificiale a meno che non te lo chiedano; in tal caso confermalo con naturalezza ("Si, sono l'assistente virtuale dello studio") e prosegui.
- Resta sempre nel ruolo. Se il chiamante e provocatorio, scherzoso o cerca di mandarti fuori tema, riporta con gentilezza la conversazione su come puoi aiutarlo per lo studio; non lasciarti trascinare, non rispondere a richieste estranee al servizio.
- Se non capisci o la linea e disturbata, chiedi gentilmente di ripetere.
# ESITO DELLA CHIAMATA (per il report interno, scegli uno)
informazioni - appuntamento - ricontatto consulente - spam/non pertinente"""

FIELDS = {
    "nome_chiamante":   "Nome e cognome di chi ha chiamato. Vuoto se non emerso.",
    "azienda":          "Nome dell'azienda o attivita del chiamante. Vuoto se non emerso.",
    "telefono":         "Numero di telefono di richiamo lasciato dal chiamante.",
    "email":            "Email lasciata dal chiamante.",
    "motivo":           "Motivo della chiamata / esigenza, in breve.",
    "servizio_interesse": "Servizio dello studio di interesse (es. risparmio fiscale, partita IVA, holding, buste paga, odontoiatri, cartelle esattoriali...).",
    "appuntamento":     "Giorno/ora preferiti per appuntamento o richiamo, se richiesti.",
    "esito":            "Esito sintetico: informazioni date / appuntamento / ricontatto consulente / spam.",
}


def main():
    # 1) Crea KB text document
    r = requests.post(f"{BASE}/v1/convai/knowledge-base/text", headers=H,
                      json={"name": "Evoluzione Fiscale - Info studio, servizi, FAQ", "text": KB_TEXT}, timeout=60)
    r.raise_for_status()
    kb_id = r.json()["id"]
    print("KB_ID:", kb_id)

    data_collection = {k: {"type": "string", "description": v} for k, v in FIELDS.items()}

    payload = {
        "name": "Evoluzione Fiscale - Reception",
        "conversation_config": {
            "agent": {
                "first_message": "[warm]Studio Evoluzione Fiscale, buongiorno! Come posso aiutarla?",
                "language": "it",
                "dynamic_variables": {"dynamic_variable_placeholders": {"data_ora_oggi": ""}},
                "prompt": {
                    "prompt": SYSTEM_PROMPT,
                    "llm": "claude-haiku-4-5",
                    "temperature": 0.0,
                    "knowledge_base": [
                        {"type": "text", "name": "Evoluzione Fiscale - Info studio, servizi, FAQ",
                         "id": kb_id, "usage_mode": "auto"}
                    ],
                },
            },
            "tts": {
                "model_id": "eleven_v3_conversational",
                "voice_id": VOICE_FRANCESCO,
                "stability": 0.5,
                "similarity_boost": 0.8,
                "speed": 1.0,
            },
            "conversation": {"max_duration_seconds": 600},
        },
        "platform_settings": {
            "data_collection": data_collection,
        },
    }

    r = requests.post(f"{BASE}/v1/convai/agents/create", headers=H, json=payload, timeout=60)
    if r.status_code >= 300:
        print("ERROR", r.status_code, r.text[:2000]); sys.exit(1)
    agent_id = r.json()["agent_id"]
    print("AGENT_ID:", agent_id)
    json.dump({"agent_id": agent_id, "kb_id": kb_id}, open(os.path.join(os.path.dirname(__file__), "agent_ids.json"), "w"))


if __name__ == "__main__":
    main()
