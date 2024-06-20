
# Compilazione automatica preferenze GPS del MIUR

Script python per la compilazione automatica delle 150 preferenze GPS del MIUR.
Ultima modifica: 2023-07.

Il MIUR espone una piattaforma per consentire ai docenti di esprimere le proprie preferenze per l'assegnazione delle cattedre.
Tale piattaforma prevede che il docente compili manualmente questa lista, per un massimo di 150 preferenze.
Ho personalmente visto svolgere questa attività ed il grande tedio che ne deriva, poichè ogni singola entry richiede diversi click e passaggi manuali all'utente,

Ho creato così questa piccola utility che grazie alla libreria Selenium effettua il crawling della pagina, compilando automaticamente le preferenze in base ai valori preimpostati nello script.

### Prerequisiti
Prima di avviare lo script è necessario aver configurato l'ambiente python ed aver installato la libreria selenium

### Setup
All'interno dello script sono presenti 3 liste: `SOURCE_TIPI_CONTRATTI`, `SOURCE_CLASSI_CONCORSO`, `SOURCE_SCUOLE`.
Queste 3 liste vanno valorizzate con le proprie preferenze. I valori inseriti sono i valori che possono essere selezionati dalle varie tendine della piattaforma.

Il criterio con cui vengono create le entry (tipologia contrattuale + classe di concorso + scuola) viene definito dall'ordine dei foreach definiti nel corpo dello script.
