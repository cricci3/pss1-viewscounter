# Assignment 1 - Processo e Sviluppo del Software

## Git URL
https://gitlab.com/bicoccaprojects/2023_assignment1_viewscounter

## Membri
- Ficara Damiano (919386)
- Ricci Claudio (918956)
- Toli Emilio (920337)

## Note
Questo README si pone l'obiettivo di documentare il lavoro svolto fino alla prima consegna. Verranno quindi descritti gli stages di: Build, Verify, Unit-test, Integration-test, Package e Release.

## Introduzione
Il primo Assignment del corso di Processo e Sviluppo del Software si pone come obiettivo la realizzazione di una Pipeline CI/CD che automatizzi il processo di manutenzione di un'applicazione seguendo l'insieme di pratiche DEVOPS, mirando ad abbreviare il ciclo di vita di sviluppo di un sistema e soprattutto fornendo una consegna continua di software qualitativamente elevato.

## Applicazione
L'obiettivo principale dell'assignment non è l'implementazione dell'applicazione in sé. Pertanto, è stata scelta la realizzazione di un sistema estremamente semplice denominato "Views Counter". Questo sistema fa uso del database Firebase per tenere traccia del numero di visualizzazioni effettuate da ciascun utente all'interno del sistema.

All'avvio dell'applicazione, agli utenti viene richiesto di specificare il proprio nome. L'applicazione verifica quindi se tale nome è già presente nel database. Nel caso affermativo, il sistema incrementa il conteggio delle visualizzazioni associate a quell'utente e restituisce il valore aggiornato. Se, invece, si tratta della prima volta in cui quel nome viene inserito, il sistema restituisce un valore iniziale di 1.

## Stages
Di seguito vengono elencate le fasi da implementare necessarie allo svolgimento dell'assignment:
- Build
- Verify
- Unit-test
- Integration-test
- Package
- Release
- Deploy

### Prerequisiti
In questa sezione, vengono forniti alcuni prerequisiti che vengono eseguiti prima dell'avvio dello script con le fasi elencate in precedenza:
- La pipeline utilizza l'immagine Docker Python più recente come base, definita come segue: `image: python:latest`.
- Viene definita una variabile globale denominata `PIP_CACHE_DIR`, il cui percorso è impostato su `"$CI_PROJECT_DIR/.cache/pip"`.\\
L'utilizzo della cache in una pipeline riveste un ruolo fondamentale nel migliorare l'efficienza, la velocità e la coerenza del processo di sviluppo del software. Tale pratica consente di ottimizzare l'uso delle risorse e garantisce un flusso di lavoro più agevole.
- Inoltre, viene attivato un ambiente virtuale per isolare tutte le operazioni Python all'interno del progetto. Questo ambiente consente di installare e gestire le dipendenze specifiche per il progetto senza interferire con il sistema globale.

### Build
La compilazione del progetto avviene mediante il comando seguente:\\
`pip install -r requirements.txt`\\
Questo metodo consente di semplificare il processo di installazione delle librerie esterne richieste per l'esecuzione dell'applicazione. Al posto di elencare manualmente tutte le librerie e le rispettive versioni, vengono specificate nel file di testo "requirements.txt" le librerie necessarie. Se a fianco del nome della libreria non è specificata nessuna versione, significa che si prende quella più recente.

### Verify
La fase di "verify" nella pipeline di sviluppo utilizza due comandi per eseguire controlli di qualità del codice e identificare possibili problematiche di sicurezza prima di procedere ulteriormente nello sviluppo dell'applicazione. Al momento della prima scadenza dell'assignment, non è ancora stato scritto nella pipeline il comando di `bandit`, quindi il solo comando eseguito è:
- `prospector`, il quale esegue l'analisi statica del codice alla ricerca di possibili problemi di stile, conformità alle linee guida di codifica, e altre metriche di qualità del codice.

### Unit-test
Un test di unità ha lo scopo di verificare il corretto funzionamento di una singola unità di codice, come un metodo, una funzione o una classe, in modo indipendente dal resto del sistema. In questo contesto, è stato creato un file denominato *test_unit.py* contenente una funzione di test. Questa funzione verifica il collegamento al database, restituendo `True` se la connessione è attiva.\\
Per eseguire il test di unità all'interno di una pipeline, è possibile utilizzare il seguente comando:\\
`pytest tests/test_unit.py`\\
Questo comando fa uso della libreria di testing pytest per eseguire il test specifico contenuto nel file *test_unit.py*. Il risultato dell'esecuzione fornirà un responso sul corretto funzionamento del collegamento al database. Se il test restituisce `True`, indica che il collegamento è attivo, confermando il successo del test e la validità della connessione al database.


### Integration-test
Un integration test è una fase necessaria per avere la garanzia che le componenti di un'applicazione non generino problemi nel momento in cui vengono integrate assieme, garantendo che le componenti siano in grado di comunicare tra loro in maniera corretta.
Inserendo questo stage nella pipeline i test vengono eseguiti ad ogni modifica del codice sorgente, in modo da garantire la qualità del software.
Entrando nel contesto, l'integration test esegue due principali controlli: il primo, dopo aver inizializzato Firebase, ottiene il valore dell'utente di prova e verifica se esso sia uguale ad un valore predefinito, ossia 10 ed in tal caso il test passerà correttamente. 

Il secondo test, sempre dopo aver inizializzato l'istanza di Firebase, imposta il valore del contatore dell'utente "damiano" con il valore '5' verificando, poi, che l'incremento funzioni correttamente richiamando la funzione "firebase.increment_counter('damiano')" che restituisce "true" in caso di riuscita dell'operazione.
L'ultima operazione consiste nel verificare che il contatore sia stato incrementato correttamente e che quindi abbia valore '6'.

### Package-test
Il package test è un processo importante per la preparazione del software alla distribuzione, infatti, il codice sorgente viene convertito in pacchetti al fine di distribuire agevolmente applicazioni oppure librerie.
E' possibile generare due tipi di pacchetti grazie al comando `python setup.py sdist bdist_wheel`: "sdist" che contiene il codice sorgente del progetto, mentre "bdist_wheel" permette di installare il software su sistemi Python senza doverlo compilare. 

Infine la sezione "artifacts" permette di specificare che la directory indicata (nel caso specifico `dist/`) può essere archiviata ed utilizzata per la distribuzione in pacchetti, oppure per l'utilizzo negli stage successivi della pipeline. 

### Release-test
Il release-test è una fase che ha lo scopo di verificare la qualità e la conformità ai requisiti del software prima del rilascio agli utenti finali.
In particolare, nella pipeline, sono presenti le seguenti specifiche:

- `source venv/bin/activate`: è l'istruzione che permette di attivare l'ambiente virtuale, con l'intenzione di evitare conflitti con gli altri progetti

- ` echo "[pypi]" > ~/.pypirc` : permette la creazione del file pypirc, che è utilizzato per la lettura del nome utente e della password necessari per l'autenticazione a PiPI, al fine di effettuare l'upload dei pacchetti Python.

- `echo "username = __token__" >> ~/.pypirc` : è l'istruzione utilizzata per impostare lo username nel file pypirc (impostato come "token").

- `echo "password = $TWINE_TOKEN" >> ~/.pypirc`: rappresenta l'istruzione per l'impostazione della password nel file pypirc (fornita dalla variabile $TWINE_TOKEN).

- `cat ~/.pypirc` : è l'istruzione che consente di stampare il contenuto del file per fini di debug

- `twine upload dist/*` : questa istruzione permette di caricare su PyPI i pacchetti generati nella fase di Package, i quali sono stati caricati nella directory `dist/`










