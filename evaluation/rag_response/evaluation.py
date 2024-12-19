from rouge import Rouge

rouge_scorer = Rouge()

reference = """Nella programmazione, un code smell identifica una caratteristica del codice 
di un programma che indica la possibile presenza di un problema più serio. 
Determinare cosa sia un code smell è soggettivo, e varia da linguaggio, 
sviluppatore e metodologia di sviluppo. Il termine è stato reso popolare 
da Kent Beck (l'ideatore dell'extreme programming) alla fine degli anni 1990. 
Una lista dettagliata dei code smells e delle contromisure è disponibile al 
seguente indirizzo: https://refactoring.guru/refactoring/catalog.
Alcuni esempi di code smell includono: metodi troppo lunghi, classi grandi, commenti eccessivi,
codice duplicato, codice morto, Ossessione dei tipi primitivi, Lunga lista di parametri, Data Clumps"""

hypothesis = """Un code smell è un termine utilizzato in programmazione per descrivere una 
caratteristica del codice di un programma che potrebbe indicare la presenza di un problema più serio. 
L'identificazione di un code smell aiuta gli sviluppatori a riconoscere e affrontare i problemi 
potenzialmente nascosti nel codice, migliorandone la qualità, la leggibilità e la manutenibilità. 
Va notato che la percezione di ciò che costituisce un code smell può variare 
in base al linguaggio di programmazione, allo sviluppatore e alla metodologia di sviluppo adottata. 
Il termine "code smell" è stato reso popolare da Kent Beck, 
l'ideatore dell'extreme programming, alla fine degli anni '90.
Ecco alcuni esempi comuni di code smell e le relative contromisure:
Commenti eccessivi: Un metodo contiene molti commenti esplicativi. 
Contromisura: estrarre i metodi ed usare nomi che aiutino la comprensione.
Codice duplicato: Esistono più pezzi di codice sostanzialmente identici. 
Contromisura: Raggruppare il codice duplicato in un unico metodo o classe, utilizzando l'ereditarietà o la composizione, se appropriato.
Codice morto: Classi, metodi o campi che non sono utilizzati. 
Contromisura: Rimuovere o segnare per la rimozione del codice morto.
Per una lista dettagliata di code smells e delle relative contromisure, consultare il seguente indirizzo:
https://refactoring.guru/refactoring/catalog"""

score = rouge_scorer.get_scores(
    hyps=hypothesis,
    refs=reference,
)

print(score[0]["rouge-l"]["f"])