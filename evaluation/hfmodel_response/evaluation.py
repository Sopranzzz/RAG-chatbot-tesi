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

hypothesis = """Un "code smell" (in italiano "odore di codice") è un termine utilizzato nel campo 
dello sviluppo software per descrivere una porzione di codice che sembra suggerire la presenza 
di un problema di progettazione o di qualità, sebbene non sia necessariamente un bug in sé.
L'espressione "code smell" è stata resa popolare dal libro "Refactoring: Improving the 
Design of Existing Code" di Martin Fowler.
Un code smell non è sempre sinonimo di errore di programmazione, 
ma può indicare che il codice potrebbe essere disorganizzato, difficile da comprendere o manutenere, 
o che potrebbe essere soggetto a bug in futuro.
Alcuni esempi di code smells includono:
Duplicated code (codice duplicato)
Long method (metodi molto lunghi)
Large class (classi molto grandi)"""

score = rouge_scorer.get_scores(
    hyps=hypothesis,
    refs=reference,
)

print(score[0]["rouge-l"]["f"])