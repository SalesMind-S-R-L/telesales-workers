# BRIEF - Recupero centralini verificati (massima copertura, 100% affidabili)

Per ogni azienda dell'elenco assegnato, trova il numero di telefono UFFICIALE della sede italiana.

FONTI (incrocia in questo ordine, entra solo se coerente su >=2 fonti oppure da fonte ufficiale del sito):
1. Pagina "Contatti" o "Chi siamo" del SITO UFFICIALE dell'azienda (URL fornito)
2. Registro imprese / Camera di Commercio / ufficiocamerale.it / visura.net
3. PagineGialle.it / PagineBianche.it / Kompass.it intestati alla ragione sociale e sede
4. Scheda Google Business ufficiale (google.com/maps cerca ragione sociale)
5. LinkedIn pagina aziendale (a volte riporta il numero)

OUTPUT: JSON array con struttura:
[{"azienda":"...", "tel":"...", "fonte":"URL1 | URL2", "note":"..."}]

REGOLE TASSATIVE:
- Numero SOLO se verificato su fonte reale. Nel dubbio, tel="" (vuoto meglio di sbagliato)
- MAI numeri verdi 800/numero verde spacciati per sede
- MAI customer care generici che non corrispondono alla sede italiana
- Per aziende digital-only (Satispay, Scalapay, Revolut, N26, ho.Mobile, Spotify, ManoMano): 
  quasi certamente non hanno numero pubblico (solo app/chat) → tel="" è corretto e onesto
- Formato: "030 522672" (nazionalecon spazio), mai +39, mai cifre attaccate
- Includi TUTTE le aziende del tuo elenco (anche quelle dove il risultato è "")
