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

- **Corpo Principale (`01`–`36`, moduli teorici):** Introduzione al KDD, Data Understanding, Data Preparation, Prossimità e Clustering, Analisi delle Associazioni e Pattern Sequenziali, Serie Temporali, Classificazione, Ensemble, $K$-NN, Regole, Shapelets, Coordinated Behavior, Responsible Data Analytics, Explainable AI, Federated Learning.
- **Appendice A (`appendice-a-esercizi.tex`):** Esercizi svolti e simulazioni algoritmiche (Sequential Pattern Mining, K-Means, GSP, DTW, $K$-NN, Decision Tree Training, CNN/Tomek Links, Network Science, Clustering Eterogeneo e Multi-Vista).
- **Appendice B (`appendice-b-codici-python.tex`):** Laboratori e codici Python (Data Understanding/Preparation, Validazione Clustering, Time Series, Pattern Mining/SNA, Clustering Eterogeneo, Topic Modeling BERTopic, Machine Learning/Dati Sbilanciati, Shapelets, XAI & Privacy).

```text
Data-Mining/
├── assets/                 # Immagini, figure e schemi grafici
├── chapters/
│   └── it/                 # Capitoli in italiano (.tex)
├── config/
│   └── preamble_it.tex     # Preambolo e configurazione pacchetti
├── datasets/               # Dataset di esempio per le esercitazioni
├── scripts/                # Script Python e dataset per la generazione delle figure
│   ├── requirements.txt    # Dipendenze Python
│   ├── datasets/           # Dataset usati dagli script (es. iris.csv)
│   └── generate_dispensa_figures.py # Script generazione figure
├── main_it.tex             # Entry point principale per la compilazione
├── main.tex                # Entry point per editor VS Code
├── references.bib          # Bibliografia
└── README.md               # Scheda descrittiva del corso
```

## Ambiente Python & Generazione Figure

All'interno della cartella `scripts/` è disponibile lo script Python dedicato alla generazione delle figure vettoriali statiche incluse nella dispensa (`Data-Mining/assets/figures/it/`). La generazione va eseguita esplicitamente con `python3 Data-Mining/scripts/generate_dispensa_figures.py` oppure tramite `docker compose run --rm figures`.

## Linee Guida per i Capitoli e le Figure

1. Ogni capitolo è un file autonomo incluso in `main_it.tex` tramite `\include{chapters/it/...}`.
2. Figure ed equazioni devono avere `\caption` descrittive e `\label` per la navigazione interna, richiamate nel testo con `\autoref{...}`.
3. Configurazioni globali, pacchetti e macro matematiche vanno collocati esclusivamente in `config/preamble_it.tex`.
