# BRIEF - Decision maker MARKETING (massima qualita, verificato)

Per ogni azienda del chunk, identifica la PERSONA responsabile di marketing/comunicazione/brand
nell'ENTITA ITALIANA (il vero compratore per uno studio di contenuti/shooting).

Cerca (fonti, in ordine): LinkedIn (via ricerca Google: "<azienda> direttore marketing" / "responsabile marketing" / "CMO" / "head of marketing" site:linkedin.com/in), pagina Team/Press del sito ufficiale, comunicati stampa e news (Engage, ADC Group, Pambianco, Sole24Ore), interviste.

Raccogli, SOLO se verificabile:
- dm_nome: nome e cognome della persona
- dm_ruolo: ruolo esatto (es. Direttore Marketing, CMO, Responsabile Comunicazione, Brand Manager, Head of Digital)
- dm_linkedin: URL del profilo LinkedIn della persona (deve corrispondere ALLA persona giusta nell'azienda giusta)
- dm_email: email diretta SOLO se pubblicata su fonte ufficiale (altrimenti "")
- dm_cell: cellulare SOLO se pubblicato su fonte ufficiale (quasi sempre ""; mai inventato)
- dm_fonte: URL della fonte principale

REGOLE TASSATIVE (massima qualita = zero errori):
- Deve essere la persona del MARKETING dell'entita ITALIANA. Se trovi solo ruoli esteri (es. "marketing America"), NON usarli, lascia "".
- Verifica che la persona sia ATTUALE e davvero in quell'azienda (no ex dipendenti, no omonimi).
- Se non riesci a identificare con certezza il responsabile marketing, lascia i campi "" (meglio vuoto che sbagliato).
- Se il marketing non e una funzione dedicata (PMI), puoi indicare il titolare/AD come riferimento marketing, segnalandolo nel ruolo.
- Niente invenzioni di nomi, profili, email, numeri.

OUTPUT: scrivi SOLO JSON valido (array) nel file indicato:
[{"azienda":"..","dm_nome":"..","dm_ruolo":"..","dm_linkedin":"..","dm_email":"..","dm_cell":"..","dm_fonte":".."}]
Includi TUTTE le aziende del chunk. Poi restituisci un riassunto breve: quanti DM marketing identificati, quanti con LinkedIn, quanti con email/cellulare pubblici.
