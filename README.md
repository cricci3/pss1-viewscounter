# Assignment 1 - Processo e Sviluppo del Software

## Membri
- Ficara Damiano (919386)
- Ricci Claudio (918956)
- Toli Emilio ()

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
In questa sezione vengono elencati alcuni prerequisiti che vengono runnati prima dello script con stages elencati sopra.
- Per eseguire la pipeline, viene usata come immagine python la seguente
`image: python:latest`
- Viene definita una variabile globale 'PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"' per definire il path della cache. L'uso della cache in una pipeline è una pratica cruciale per migliorare l'efficienza, la velocità e la coerenza del processo di sviluppo del software. Aiuta a ottimizzare le risorse e a garantire un flusso di lavoro più agevole.
- attivazione dell'ambiente virtuale per isolere tutte le operazioni Python all'interno del progetto, consentendo di installare e gestire le dipendenze specifiche senza interferire con il sistema globale.

### Build
La compilazione del progetto avviene mediante il comando seguente:
'pip install -r requirements.txt'
Questo metodo consente di semplificare il processo di installazione delle librerie esterne richieste per l'esecuzione dell'applicazione. Al posto di elencare manualmente tutte le librerie e le rispettive versioni, vengono specificate nel file di testo "requirements.txt" le librerie necessarie. Se a fianco del nome della libreria non è specificata nessuna versione, significa che si prende quella più recente.

### Verify
La fase di "verify" nella pipeline di sviluppo utilizza due comandi per eseguire controlli di qualità del codice e identificare possibili problematiche di sicurezza prima di procedere ulteriormente nello sviluppo dell'applicazione. I comandi eseguiti sono:
- 'prospector', il quale esegue l'analisi statica del codice alla ricerca di possibili problemi di stile, conformità alle linee guida di codifica, e altre metriche di qualità del codice.
- 'bandit' strumento di analisi statica progettato specificamente per la ricerca di vulnerabilità di sicurezza nel codice Python. Esegue un controllo approfondito del codice alla ricerca di possibili debolezze e vulnerabilità, segnalando qualsiasi potenziale problema di sicurezza che richiede attenzione.



