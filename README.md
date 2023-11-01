# Assignment 1 - Processo e Sviluppo del Software

## Git URL
https://gitlab.com/bicoccaprojects/2023_assignment1_viewscounter

## Membri
- Ficara Damiano (919386)
- Ricci Claudio (918956)
- Toli Emilio (920337)

## Note
Questo README ha lo scopo di fornire una documentazione completa delle decisioni prese durante lo sviluppo della pipeline, spaziando attraverso tutte le sue fasi: Build, Verify, Unit-test, Integration-test, Package e Release.

Inoltre, verranno fornite giustificazioni e commenti approfonditi per ciascuna di queste scelte.

## Introduzione
Il primo Assignment del corso di Processo e Sviluppo del Software si pone come obiettivo la realizzazione di una Pipeline CI/CD che automatizzi il processo di manutenzione di un'applicazione seguendo l'insieme di pratiche DEVOPS, mirando ad abbreviare il ciclo di vita di sviluppo di un sistema e soprattutto fornendo una consegna continua di software qualitativamente elevato.

La decisione di sviluppare l'applicazione in Python è stata presa con l'obiettivo di semplificare lo sviluppo della pipeline CI/CD. Rispetto ad altri linguaggi, come Java, Python offre un'esperienza di sviluppo più agevole in questo contesto. Mentre Java richiederebbe l'utilizzo di strumenti e librerie specifiche per la gestione dei processi di CI/CD, Python offre una serie di vantaggi che consentono di implementare e gestire la pipeline in modo più diretto ed efficiente.

## Applicazione
L'obiettivo principale dell'assignment non è l'implementazione dell'applicazione in sé. Pertanto, è stata scelta la realizzazione di un sistema estremamente semplice denominato "**Views Counter**". Questo sistema fa uso del database _Firebase_ per tenere traccia del numero di visualizzazioni effettuate da ciascun utente all'interno del sistema.

All'avvio dell'applicazione, agli utenti viene richiesto di specificare il proprio nome e, in seguito, l'applicazione verifica se tale nome è già presente nel database:
- in caso affermativo, il sistema incrementa il conteggio delle visualizzazioni associate a quell'utente e restituisce il valore aggiornato.
- se, invece, si tratta della prima volta in cui quel nome viene inserito, il sistema restituisce un valore iniziale di 1.

## Stages
Di seguito vengono elencate le fasi che sono state implementate per lo svolgimento dell'assignment:
1. **Build**
2. **Verify**
3. **Unit-test**
4. **Integration-test**
5. **Package**
6. **Release**
7. **Docs**


### Prerequisiti
In questa sezione, vengono spiegati alcuni prerequisiti che vengono eseguiti prima dell'avvio dello script con le fasi elencate in precedenza:
- La pipeline utilizza l'immagine Docker Python più recente come base, definita come segue: `image: python:latest`.\
L'immagine Docker Python assicura che tutte le fasi della pipeline utilizzino un ambiente coerente, eliminando problemi di compatibilità tra ambienti di sviluppo e produzione. Inoltre, le immagini Docker Python sono in genere rapide da avviare, ottimizzando i tempi di build e test all'interno della pipeline.
- Viene definita una variabile globale denominata `PIP_CACHE_DIR`, il cui percorso è impostato su `"$CI_PROJECT_DIR/.cache/pip"`.\
L'utilizzo della cache in una pipeline riveste un ruolo fondamentale nel migliorare l'efficienza, la velocità e la coerenza del processo di sviluppo del software. Tale pratica consente di ottimizzare l'uso delle risorse e garantisce un flusso di lavoro più agevole.
- Inoltre, viene eseguito uno stage di "before_script" che si occupa di effettuare alcune azioni necessarie a far eseguire con successo gli stages successivi:
    - `pip --version` seguito da `pip install --upgrade pip` che si occupano di verificare e aggiornare la versione di `pip`;
    - Inoltre, viene creato e poi attivato un ambiente virtuale per isolare tutte le operazioni Python all'interno del progetto con `python -m venv venv` e `source venv/bin/activate`. L'ambiente virtuale consente di installare e gestire le dipendenze specifiche per il progetto senza interferire con il sistema globale.

Alcuni stages contengono un comando che indica che lo stage in questione, e quindi la pipeline, deve essere eseguita solo quando ci si trova sul branch `main`. In questo modo ci siamo assicurati di non far partire la pipeline, e quindi di perdere minuti di utilizzo, durante l'esecuzione di modifiche su branch diversi dal principale.

### 1. Build
La compilazione del progetto viene eseguita attraverso il seguente comando: `pip install -r requirements.txt`.

Questa scelta è motivata da diverse ragioni che contribuiscono alla semplificazione del processo di installazione delle librerie esterne necessarie per l'esecuzione dell'applicazione. In questo modo, la specifica delle librerie e delle relative versioni richieste è concentrata in un file esterno denominato "requirements.txt". Questo approccio centralizzato semplifica notevolmente la gestione delle dipendenze, consentendo di elencare in modo chiaro e ordinato tutte le librerie necessarie per l'applicazione. Inoltre, l'utilizzo di un file di requisiti esterno permette di aggiungere o modificare librerie senza la necessità di apportare modifiche alla pipeline stessa. In altre parole, se si desidera inserire una nuova libreria o aggiornare una versione, è sufficiente aggiornare il file "requirements.txt". Questo aumenta l'agilità nello sviluppo, poiché non è richiesta alcuna modifica al processo di build della pipeline.

In definitiva, l'uso del file "requirements.txt" per la gestione delle dipendenze promuove l'efficienza, l'agilità, la tracciabilità e la riduzione degli errori nel processo di CI/CD, offrendo un approccio robusto per gestire le librerie necessarie all'esecuzione dell'applicazione.

### 2. Verify
La fase di "verify" nella pipeline di sviluppo, come da specifiche dell'assignment, utilizza due comandi per eseguire controlli di qualità del codice e identificare possibili problematiche di sicurezza prima di procedere ulteriormente nello sviluppo dell'applicazione. 

Dato che questi due comandi sono indipendenti l'uno dall'altro, si è scelto di scrivere lo scritp di questo stage in modo che esegua due jobs in parallelo per migliorare le prestazioni della pipeline. I due jobs eseguono `prospector` e `bandit`, in particolare:
- "prospector", esegue l'analisi statica del codice alla ricerca di possibili problemi di stile, conformità alle linee guida di codifica, e altre metriche di qualità del codice. In sostanza, garantisce la conformità alle migliori pratiche di sviluppo, assicurando che il codice sia di alta qualità, privo di errori e pronto per il rilascio, migliorando significativamente l'efficienza e la qualità.
- "bandit" esegue due analisi separate della sicurezza del codice Python per due diverse parti del progetto: "application" (frontend) e "database" (gestione del database). Questa analisi include l'esecuzione del comando `bandit` due volte, una per ciascuna parte del progetto. Utilizzando l'opzione `-r`, Bandit esegue l'analisi in modalità ricorsiva, esaminando tutto il contenuto delle directory specificate, inclusi tutti i file Python presenti al loro interno.

### 3. Unit-test
Un test di unità ha lo scopo di verificare il corretto funzionamento di una singola unità di codice, come un metodo, una funzione o una classe, in modo indipendente dal resto del sistema.\
In questo contesto, è stato creato un file denominato *test_unit.py* contenente una funzione di test. Questa funzione verifica il collegamento al database, restituendo `True` se la connessione è attiva.

Per eseguire il test di unità all'interno della pipeline, è stato utilizzato il seguente comando: `pytest tests/test_unit.py`.\
Questo comando fa uso della libreria di testing _pytest_ per eseguire il test specifico contenuto nel file *test_unit.py*.

`pytest`è un framework di testing per Python che abbiamo utilizzato per la scrittura e l'esecuzione dei test unitari e dei test di integrazione. Questo framework è in grado di rilevare automaticamente i file di test all'interno del progetto. I file di test sono stati denominati secondo una convenzione di denominazione specifica, devono iniziare con "test_", così che `pytest` li identificherà e li eseguirà quando richiamto.

Il risultato dell'esecuzione fornirà un responso sul corretto funzionamento del collegamento al database. Se il test restituisce `True`, indica che il collegamento è attivo, confermando il successo del test e la validità della connessione al database.

### 4. Integration-test
Un integration test è una fase necessaria per avere la garanzia che le componenti di un'applicazione non generino problemi nel momento in cui vengono integrate assieme, garantendo che le componenti siano in grado di comunicare tra loro in maniera corretta.
Inserendo questo stage nella pipeline i test vengono eseguiti ad ogni modifica del codice sorgente, in modo da garantire la qualità del software.

Entrando nel contesto della pipeline, l'integration test viene eseguito tramite il seguente comando: `pytest tests/test_integration.py`.\
Questo test esegue due principali controlli:
    1. Dopo aver inizializzato _Firebase_, ottiene il valore dell'utente di prova e verifica se esso sia uguale ad un valore predefinito, ossia 10 ed in tal caso il test passerà correttamente. 
    2. Il secondo test, sempre dopo aver inizializzato l'istanza di _Firebase_, imposta il valore del contatore dell'utente "damiano" con il valore '5' verificando, poi, che l'incremento funzioni correttamente richiamando la funzione `firebase.increment_counter('damiano')` che restituisce `true` in caso di riuscita dell'operazione.\
L'ultima operazione di questo test consiste nel verificare che il contatore sia stato incrementato correttamente e che quindi abbia valore '6'.

### 5. Package
Durante la fase di Package, il codice sorgente viene trasformato in pacchetti, agevolando così la distribuzione di applicazioni e librerie. I pacchetti sono archivi che includono il codice sorgente e i file necessari all'installazione del software su vari sistemi e ambienti. Questo processo è fondamentale per semplificare la distribuzione e garantire che il software funzioni su diverse piattaforme.

Nella pipeline questo stage è uno dei più critichi ed esegue diverse operazioni per preparare il codice alla distribuzione. Il comando principale eseguito è `python setup.py sdist bdist_wheel`.\ Utilizziamo il file `setup.py` per creare pacchetti sorgente e pacchetti `bdist_wheel`. Questo file di configurazione definisce le informazioni relative al progetto Python, come il nome, la versione, l'autore, la descrizione e le dipendenze. Questo file è utilizzato insieme al framework `setuptools`.
    - `sdist` rappresenta il pacchetto sorgente, contenente il codice sorgente e altri file necessari per l'installazione.
    - `bdist_wheel` è un formato di pacchetto binario ottimizzato per la distribuzione su PyPI, che semplifica l'installazione su diverse piattaforme. La pubblicazione su PyPI (pypi.org/) mette a disposizione del pubblico il software Python, facilitando la condivisione e la collaborazione tra sviluppatori.

Ma prima di poter eseguire il comando appena descritto è necessario effettuare i seguenti comandi:
- `git config user.email $GIT_EMAIL` e `git config user.name $GIT_NAME` che configurano l'utente Git con l'indirizzo email e il nome specificati nelle variabili d'ambiente `$GIT_EMAIL` e `$GIT_NAME`.
- `git remote add gitlab_origin $GITLAB_REMOTE_URL` che aggiunge un'origine Git denominata "gitlab_origin" con l'URL specificato nella variabile `$GITLAB_REMOTE_URL`.
- `python increment_version.py patch` che esegue lo scritp del file _increment_version_ che si occupa di aggiornare il numero di versione del progetto nel file _setup.py_. E per questo, successivamente, è necessario eseguire `git add setup.py` per aggiungere questo file alle modifiche su cui si eseguirà il comando di _commit_.
- `git commit -m "incremento versione"` per eseguire il _commit_.
- `git push gitlab_origin HEAD:main -o ci.skip` che esegue il push delle modifiche al repository remoto e utilizza l'opzione `-o ci.skip` per impedire l'attivazione di una pipeline CI/CD in risposta a questo push.

Infine, l'esecuzione di questo stage produrrà dei pacchetti (artifacts) che vengono archiviati nella directory "dist/".

**Problemi riscontrati in questo stage**
Durante questa fase, è importante prestare attenzione a un aspetto chiave. Il file `setup.py` contiene la versione dell'applicazione, e ogni volta che eseguiamo la pipeline, è necessario aggiornare la versione prima di consentire una seconda esecuzione. Questo passo è fondamentale poiché l'obiettivo è pubblicare l'applicazione su PyPI. Pertanto, per garantire una corretta esecuzione di questa fase, è essenziale verificare che non esista già un'applicazione con lo stesso nome su PyPI e che la versione sia aggiornata ad ogni esecuzione. A questo fine, si è deciso di creare uno scritp _increment_version.py_ che si occupa di aggiornare in modo automatico la versione del progetto.


### 6. Release
Questa fase della pipeline è strettamente correlata alla fase precedente di "Package" in quanto, se nella fase di "Package" abbiamo preparato i pacchetti dell'applicazione, in questa fase li pubblichiamo su PyPI.
I passi eseguiti da questo stage sono quattro:
- `echo "[pypi]" > ~/.pypirc`, in questo passaggio viene creato un file di configurazione necessario per l'interazione con PyPI. Questo file conterrà le informazioni di autenticazione richieste per l'upload dei pacchetti Python su PyPI.
- `echo "username = __token__" >> ~/.pypirc`, qui, all'interno del file _.pypirc_, specificiamo che l'username per l'autenticazione su PyPI è "token". Questo indica che l'autenticazione avviene tramite un token API anziché un nome utente e una password tradizionali.
- `echo "password = $TWINE_TOKEN" >> ~/.pypirc`, inseriamo il valore del token API come password nel file _.pypirc_. Il valore del token è recuperato da una variabile globale, $TWINE_TOKEN, definita nelle impostazioni di GitLab. 
- `twine upload dist/*`, questa istruzione permette di caricare su PyPI i pacchetti generati nella fase di "Package" nella directory `dist/`. Viene utilizzato "Twine", che è uno strumento di Python per facilitare l'upload di pacchetti verso repository di pacchetti come PyPI

**Scelte architetturali di questo stage**
Per eseguire questa fase, è stato necessario creare un account su PyPI. Al fine di rendere la pipeline più professionale e garantire la sicurezza dell'autenticazione, abbiamo optato per una configurazione basata su token API. PyPI consente a ciascun utente di generare un token API personale, eliminando la necessità di condividere le proprie informazioni di account. Questo approccio migliora la sicurezza e semplifica il processo di pubblicazione sul repository PyPI.

### 7. Docs
Il progetto di sviluppo di software non è completo senza una documentazione adeguata. La documentazione fornisce agli sviluppatori, agli utenti e agli altri membri del team tutte le informazioni necessarie per comprendere, utilizzare ed estendere il software. Questa fase è dedicata a garantire che la documentazione sia sempre allineata con il codice sorgente e pronta per essere distribuita.

Questa fase della pipeline è composta da diverse azioni:
- `pip install mkdocs` la pipeline installa lo strumento MkDocs, uno strumento di generazione di documentazione che consente di creare facilmente documentazione basata su Markdown. Questo strumento sarà utilizzato per costruire la documentazione del progetto.
- `mkdocs build --clean` utilizzato per generare la documentazione del progetto. Questo comando elabora i file Markdown presenti nel repository e crea una versione formattata della documentazione pronta per la distribuzione. L'opzione `--clean` assicura che la cartella di output sia ripulita da vecchi file inutili, garantendo che la nuova documentazione sia fresca e aggiornata.
- Nella sezione degli artifacts, vengono specificati i file o le directory che devono essere conservati per un uso futuro. In particolare, viene conservato il file _mkdocs.yaml_, che è il file di configurazione principale di MkDocs. Questo file contiene le impostazioni e le informazioni necessarie per generare la documentazione.
