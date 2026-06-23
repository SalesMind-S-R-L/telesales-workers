# BRIEF RICERCA - Lead in target per Eureweb / AD Lab

## Chi e il cliente e cosa vende
Eureweb (Salo, BS) e una agenzia digital. La sua unit **AD Lab** vende **shooting foto/video INTERAMENTE generati con intelligenza artificiale** (contenuti AI high-ticket, prezzo interno da 15.000 EUR a salire - NON dire mai prezzi al telefono). I contenuti servono per social, campagne ADV, spot TV, affissioni: tutti i touchpoint.
Eureweb ha anche altri servizi (barter/cambio merce, digital audit a performance, e-commerce, programmatic, lead generation, drive to store): utili come contesto, ma il prodotto che vendiamo qui e lo shooting AI.

## CRITERIO DI SELEZIONE (da onboarding 11/6 + email Giulia Rizzi 15/6) - TASSATIVO
Selezionare SOLO aziende **attive in Italia** che **gia investono (o vogliono investire) in pubblicita e produzione contenuti**, con **presenza rilevante in: comunicazione, advertising, contenuti digitali, campagne video, social media, branded content**.
- Sia big advertiser noti, sia realta simili per posizionamento, dimensione, attivita di comunicazione.
- Aziende ENTERPRISE/grandi con budget allocati. NO PMI con budget basso, NO aziende senza attivita di comunicazione strutturata.
- Per multinazionali: puntare all'entita ITALIANA del gruppo.
- 6 settori target: Automotive, Food & Beverage, Retail & GDO, Fashion & Lifestyle, Finance & Insurance, Telecomunicazioni.

## COSA DEVI FARE
Per OGNI azienda della lista che ti viene passata, verifica con ricerca web l'evidenza CONCRETA che investe in adv/contenuti e classificala. POI proponi NUOVE aziende in target nel tuo settore (non in lista, non tra i clienti esclusi qui sotto).

Per ogni azienda raccogli (solo dati REALI e verificabili - niente invenzioni):
- evidenza concreta di investimento in adv/contenuti, con anno/segnale (es: "spot TV 2025", "campagne attive su Meta Ad Library", "canale YouTube con video frequenti", "shooting di collezione stagionali", "forte presenza social con contenuti video", "rebrand 2024", "nuova linea/lancio 2025", "nuovo CMO/direttore marketing")
- livello di investimento: Alto / Medio / Basso
- segnale di NUOVO investimento (rebrand, nuova linea, nuovo responsabile marketing, espansione, primo ingresso su un canale): si/no + dettaglio breve
- in_target: true/false (false se non investe in adv/contenuti o non e abbastanza grande)
- prio consigliata: A (grande advertiser molto attivo) / B (mid-large attivo) / C (piu piccolo ma con budget)

ANTI-ALLUCINAZIONE: se non riesci a verificare nulla per un'azienda, metti investimento "Basso", evidenza "non verificato", in_target valutalo con prudenza. NON inventare campagne, numeri, nomi. Cita brevemente la fonte/segnale.

## NUOVI LEAD da proporre
Proponi 12-20 NUOVE aziende in target nel tuo settore (non gia in lista, non tra i clienti esclusi). Per ciascuna: azienda, sede (citta IT), sito (dominio), evidenza investimento adv/contenuti, livello, nuovo_investimento, prio. Solo aziende che rispettano il criterio (gia attive in adv/contenuti).

## CLIENTI GIA EUREWEB - DA ESCLUDERE SEMPRE (non verificare, non proporre)
Automotive: Pirelli, Maserati, Kawasaki, MV Agusta, Peugeot, Citroen, Suzuki, Subaru, Kia, Mitsubishi, Chevrolet, Piaggio, NIU, Metzeler, Luna Rossa, Driver, MAK, Brixton, Biauto.
Fashion & Beauty: Armani, Fondazione Prada, Damiani, Citizen, Breil, Bulova, Frederique Constant, Golden Point, Golden Lady, Motivi, Carpisa, Arena, Iceberg, Salewa, UPIM, Acqua dell'Elba, Locman, Pompea, Camomilla, Clinians, Natura Verde, Geomar, Revita Care, Sodalis, ACBC, Vic Matie, Cafe Noir, Simonetta, Liabel, Sport Specialist, Cisalfa, Scarpe e Scarpe, Nicla, Ceradi Cupra.
Food: Coop, Mutti, Garofalo, Pernigotti, Carapelli, Caffarel, Amica Chips, Tennent's, Fileni, Frescobaldi, Pellini, Bofrost, Swiss Cheese, Recla, Witor's, L'Angelica, Fresco Pesce, Il Pescatore.
Interiors: Cassina, Poltrona Frau, Snaidero, Uno+Piu, Piscine Castiglione, Grandform, Edilkamin.
Tech: Samsung, Acer, Lenovo, Euronics, Media World, Energizer, Fujitsu, Sharp, Sennheiser, Olympia Splendid, Konica Minolta, iRobot, Olympus, Polti, Meliconi, Cerved.
Other: Henkel, GLS, Sisal, WEBUILD, Sant'Anna, Hangar, Tupperware, Einhell, Motul, Brico.io, Upower, Weber, MaxMeyer, Plan Hotel, MAM, GioStyle, Urban Fitness, Marka, Martini, North Sails.

## OUTPUT - scrivi un file JSON
Scrivi il risultato (SOLO JSON valido, niente altro testo) nel file che ti viene indicato nel prompt. Struttura:
{
  "settore": "<nome settore>",
  "verificate": [
    {"azienda":"...","in_target":true,"investimento":"Alto|Medio|Basso","evidenza":"...","nuovo_investimento":"si - <dettaglio> | no","prio":"A|B|C"}
  ],
  "nuovi_lead": [
    {"azienda":"...","settore":"<nome settore>","sede":"...","sito":"dominio.it","investimento":"Alto|Medio|Basso","evidenza":"...","nuovo_investimento":"si - <dettaglio> | no","prio":"A|B|C"}
  ]
}
Dopo aver scritto il file, restituisci SOLO un riassunto breve (2-3 righe): quante verificate, quante in_target, quante non in_target, quanti nuovi lead.
