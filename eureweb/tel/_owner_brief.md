# BRIEF - Titolare, Responsabile acquisti, Cellulare (per master Eureweb)

Per ogni azienda del chunk assegnato, cerca da FONTI PUBBLICHE/UFFICIALI:

1) TITOLARE / LEGALE RAPPRESENTANTE: nome e cognome del titolare, legale rappresentante, AD/CEO o presidente.
   Fonti: registro imprese / ufficiocamerale / visura pubblica, pagina "Chi siamo"/"Governance"/"Team" del sito ufficiale, news affidabili (Sole24Ore, ANSA), LinkedIn (profilo leadership verificabile).
   Per le grandi SpA indica l'Amministratore Delegato (o Presidente) attuale.

2) RESPONSABILE ACQUISTI: nome e cognome del responsabile/direttore acquisti, procurement o supply chain,
   SOLO se pubblicamente verificabile (LinkedIn con ruolo esplicito, sito ufficiale). Se non trovi nulla di
   verificabile, lascia "" (per le grandi aziende sara quasi sempre vuoto: e corretto).

3) CELLULARE: numero di cellulare del titolare o del responsabile acquisti SOLO se PUBBLICATO su fonte
   ufficiale dell'azienda. NON usare directory, NON numeri personali a caso, NON dedurre. Quasi sempre vuoto.

REGOLE TASSATIVE (anti-invenzione):
- Solo nomi/numeri REALI e verificabili, con fonte (URL). Se non sei sicuro, lascia "".
- Mai inventare nomi plausibili. Mai attribuire un nome di un'azienda omonima.
- Formato cellulare: nazionale ("349 1234567"), mai +39.

OUTPUT: scrivi SOLO JSON valido (array) nel file indicato, con struttura:
[{"azienda":"..","titolare":"Nome Cognome","titolare_fonte":"URL","acquisti":"Nome Cognome o ''","acquisti_fonte":"URL o ''","cellulare":"'' o numero","cellulare_fonte":"'' o URL"}]
Includi TUTTE le aziende del chunk. Poi restituisci un riassunto breve: quanti titolari / quanti acquisti / quanti cellulari trovati.
