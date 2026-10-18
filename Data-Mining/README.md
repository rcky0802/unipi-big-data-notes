# Appunti di Data Mining

> 📍 *Parte dell'hub documentale unificato degli appunti universitari: [Visualizza Hub Principale](../README.md)*

Appunti universitari in LaTeX per il corso di **Data Mining** (Anno Accademico 2026/2027), strutturati in capitoli modulari e compilabili sia tramite Docker sia in ambiente locale.

## Prerequisiti

Per la compilazione locale sono consigliati:
1. [Visual Studio Code](https://code.visualstudio.com/) con estensione [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
2. Una distribuzione LaTeX (es. [MiKTeX](https://miktex.org/download) su Windows con `latexmk`)
3. Oppure semplicemente [Docker Desktop](https://www.docker.com/products/docker-desktop) sfruttando il container unificato del repository.

## Compilazione

Dalla radice del repository è possibile compilare la dispensa con lo script unificato PowerShell:

```powershell
# Compila la dispensa in italiano
.\scripts\build.ps1 -Subject "Data-Mining"
```

Oppure direttamente all'interno della cartella `Data-Mining` con `latexmk`:

```powershell
latexmk -pdf -interaction=nonstopmode main_it.tex
```

Per rimuovere i file ausiliari di compilazione:

```powershell
latexmk -c
```

## Struttura della Cartella e Indice dei Capitoli

- **Capitolo 1:** Introduzione al Data Mining e il Processo KDD (`01`)
- **Capitolo 2:** Data Understanding I: Tipologie di Dati, Attributi e Statistica Descrittiva (`02`)
- **Capitolo 3:** Data Understanding II: Analisi Multivariata, Correlazione e Rilevamento Outliers (`03`)
- **Capitolo 4:** Data Preparation & Cleaning: Riduzione, Discretizzazione e Trasformazione (`04`)
- **Capitolo 5:** Laboratorio Python: Data Understanding e Data Preparation (`05`)
- **Capitolo 6:** Misure di Prossimità, Teoria dell'Informazione e Cluster Analysis (`06`)
- **Capitolo 7:** Cluster Analysis: Algoritmi K-Means e Clustering Gerarchico (`07`)
- **Capitolo 8:** Cluster Analysis: Clustering Basato su Densità (DBSCAN) (`08`)
- **Capitolo 9:** Varianti di K-Means, Criterio BIC, Modelli Mistura ed EM (`09`)
- **Capitolo 10:** Validazione del Clustering: Misure, Teoria e Metodologie (`10`)
- **Capitolo 11:** Analisi delle Associazioni: Concetti di Base e Algoritmi (`11`)
- **Capitolo 12:** Sequential Pattern Mining: Modelli, Definizioni ed Esercizi (`12`)
- **Capitolo 13:** Mining di Regole di Associazione (FP-Growth), Simulazioni di Clustering e Pattern Sequenziali (GSP) (`13`)

```text
Data-Mining/
├── assets/                 # Immagini, figure e schemi grafici
├── chapters/
│   └── it/                 # Capitoli in italiano (.tex)
├── config/
│   └── preamble_it.tex     # Preambolo e configurazione pacchetti
├── datasets/               # Dataset di esempio per le esercitazioni
├── notebooks/              # Jupyter notebook interattivi e script figure
│   ├── README.md           # Guida all'ambiente dei notebook
│   ├── requirements.txt    # Dipendenze Python
│   ├── generate_dispensa_figures.py # Script generazione figure
│   └── *.ipynb             # Notebook interattivi
├── main_it.tex             # Entry point principale per la compilazione
├── main.tex                # Entry point per editor VS Code
├── references.bib          # Bibliografia
└── README.md               # Scheda descrittiva del corso
```

## Ambiente Python & Jupyter Notebooks

All'interno della cartella [notebooks/](notebooks/README.md) è disponibile l'ambiente dedicato contenente i Jupyter notebook per il data understanding, l'analisi esplorativa (EDA), la preparazione dati e gli algoritmi di clustering, oltre agli script di generazione per le figure vettoriali incluse nella dispensa.

## Linee Guida per i Capitoli e le Figure

1. Ogni capitolo è un file autonomo incluso in `main_it.tex` tramite `\include{chapters/it/...}`.
2. Figure ed equazioni devono avere `\caption` descrittive e `\label` per la navigazione interna, richiamate nel testo con `\autoref{...}`.
3. Configurazioni globali, pacchetti e macro matematiche vanno collocati esclusivamente in `config/preamble_it.tex`.
