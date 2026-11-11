# Appunti di Algorithm Engineering -- Parte II

> 📍 *Parte dell'hub documentale unificato degli appunti universitari: [Visualizza Hub Principale](../README.md)*

Appunti universitari in LaTeX per la seconda parte del corso di **Algorithm Engineering** (Anno Accademico 2026/2027), incentrata su algoritmi di compressione dati, trasformata di Burrows-Wheeler, strutture dati succinte e FM-Index.

## Compilazione

Dalla radice del repository è possibile compilare la dispensa con lo script unificato PowerShell:

```powershell
# Compila la dispensa in italiano
.\scripts\build.ps1 -Subject "Algorithm-Engineering-II"
```

Il file PDF compilato verrà automaticamente collocato in `pdf/Algorithm-Engineering-II-IT.pdf`.

Oppure direttamente all'interno della cartella `Algorithm-Engineering-II` con `latexmk`:

```powershell
latexmk -pdf -interaction=nonstopmode main_it.tex
```

## Struttura della Cartella e Indice dei Capitoli

- **Capitolo 1:** Fondamenti di Compressione Dati e Teoria dell'Informazione (`01-fondamenti-compressione-teoria-informazione-shannon`)
- **Capitolo 2:** Compressori Statistici, Codifica di Huffman e Forma Canonica (`02-compressori-statistici-codifica-huffman-forma-canonica`)
- **Capitolo 3:** Codifica Aritmetica (*Arithmetic Coding*) (`03-codifica-aritmetica`)
- **Capitolo 4:** Esercitazioni di Compressione Statistica: Huffman e Codifica Aritmetica (`04-esercitazioni-compressione-statistica-huffman-aritmetica`)
- **Capitolo 5:** Compressione Statistica Avanzata: Codifica Aritmetica Dinamica, Huffman Canonico e Codici Ottimi Non-Huffman (`05-compressione-statistica-avanzata-modelli-dinamici-ottimalita-huffman`)

```text
Algorithm-Engineering-II/
├── assets/                 # Figure, grafici vettoriali e schemi TikZ
├── chapters/
│   └── it/                 # Capitoli in italiano (.tex)
├── config/
│   └── preamble_it.tex     # Preambolo e configurazione pacchetti
├── main_it.tex             # Entry point principale per la compilazione
├── main.tex                # Entry point per editor VS Code
├── references.bib          # Bibliografia
└── README.md               # Scheda descrittiva del modulo
```

## Linee Guida per i Capitoli e le Figure

1. Ogni capitolo è un file autonomo collocato in `chapters/it/` e incluso in `main_it.tex` tramite `\include{chapters/it/...}`.
2. Figure ed equazioni devono avere `\caption` descrittive e `\label` per la navigazione interna, richiamate nel testo con `\autoref{...}`.
3. Configurazioni globali, pacchetti e macro matematiche vanno collocati esclusivamente in `config/preamble_it.tex`.
