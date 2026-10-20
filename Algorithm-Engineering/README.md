# Appunti di Algorithm Engineering

> 📍 *Parte dell'hub documentale unificato degli appunti universitari: [Visualizza Hub Principale](../README.md)*

Appunti universitari in LaTeX per il corso di **Algorithm Engineering** (Anno Accademico 2026/2027), strutturati in capitoli modulari e compilabili sia tramite Docker sia in ambiente locale.

## Prerequisiti

Per la compilazione locale sono consigliati:
1. [Visual Studio Code](https://code.visualstudio.com/) con estensione [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
2. Una distribuzione LaTeX (es. [MiKTeX](https://miktex.org/download) su Windows con `latexmk`)
3. Oppure semplicemente [Docker Desktop](https://www.docker.com/products/docker-desktop) sfruttando il container unificato del repository.

## Compilazione

Dalla radice del repository è possibile compilare la dispensa con lo script unificato PowerShell:

```powershell
# Compila la dispensa in italiano
.\scripts\build.ps1 -Subject "Algorithm-Engineering"
```

Oppure direttamente all'interno della cartella `Algorithm-Engineering` con `latexmk`:

```powershell
latexmk -pdf -interaction=nonstopmode main_it.tex
```

Per rimuovere i file ausiliari di compilazione:

```powershell
latexmk -c
```

## Struttura della Cartella e Indice dei Capitoli

- **Capitolo 1:** Progettazione di Algoritmi, Modelli Computazionali e Gerarchia di Memoria (`01`)
- **Capitolo 2:** Accesso a Passi, B-Tree e Impatto della Paginazione Virtuale (`02`)
- **Capitolo 3:** Permutazione, Ordinamento e Binary Merge Sort in Memoria Esterna (`03`)
- **Capitolo 4:** Multiway Merge Sort, Snow Plow e Disk Striping (`04`)
- **Capitolo 5:** Limiti Inferiori per l'Ordinamento, Quicksort Dual-Pivot e Bounded Quicksort (`05`)
- **Capitolo 6:** Statistiche d'Ordine, Trade-off Multi-Pivot e Analisi Formale del Caso Medio di Quicksort (`06`)
- **Capitolo 7:** Ordinamento Esterno (Distribution Sort), Over-Sampling e Fondamenti di Random Sampling (`07`)
- **Capitolo 8:** Algoritmi di Random Sampling su Data Stream (`08`)
- **Capitolo 9:** Strutture Dati Randomizzate: Il Problema del Dizionario e Skip List (`09`)
- **Capitolo 10:** Alberi di Ricerca Randomizzati: Treap, Operazioni Dinamiche e Applicazioni Geometriche (`10`)
- **Capitolo 11:** Algoritmi di Intersezione per Posting Lists nell'Information Retrieval (`11`)
- **Capitolo 12:** Ricerca per Interpolazione su Bucket e Ordinamento di Stringhe (Multi-Key Quicksort) (`12`)
- **Capitolo 13:** Strutture Dati e Algoritmi per Stringhe: Ternary Search Trees (TST) e Radix Sort (`13`)

```text
Algorithm-Engineering/
├── assets/                 # Figure, grafici vettoriali e schemi TikZ
├── chapters/
│   └── it/                 # Capitoli in italiano (.tex)
├── config/
│   └── preamble_it.tex     # Preambolo e configurazione pacchetti
├── main_it.tex             # Entry point principale per la compilazione
├── main.tex                # Entry point per editor VS Code
├── references.bib          # Bibliografia
└── README.md               # Scheda descrittiva del corso
```

## Linee Guida per i Capitoli e le Figure

1. Ogni capitolo è un file autonomo incluso in `main_it.tex` tramite `\include{chapters/it/...}`.
2. Figure ed equazioni devono avere `\caption` descrittive e `\label` per la navigazione interna, richiamate nel testo con `\autoref{...}`.
3. Configurazioni globali, pacchetti e macro matematiche vanno collocati esclusivamente in `config/preamble_it.tex`.
