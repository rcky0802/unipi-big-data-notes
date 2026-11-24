# Appunti di Algorithm Engineering -- Parte II

> 📍 *Parte dell'hub documentale unificato degli appunti universitari: [Visualizza Hub Principale](../README.md)*

Appunti universitari in LaTeX per la seconda parte del corso di **Algorithm Engineering** (Anno Accademico 2026/2027), incentrata su algoritmi di compressione dati, trasformata di Burrows-Wheeler, strutture dati succinte e FM-Index.

## Prerequisiti

Per la compilazione locale sono consigliati:
1. [Visual Studio Code](https://code.visualstudio.com/) con estensione [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
2. Una distribuzione LaTeX (es. [MiKTeX](https://miktex.org/download) o TeX Live con `latexmk`)
3. Oppure semplicemente [Docker Desktop](https://www.docker.com/products/docker-desktop) sfruttando il container unificato del repository.

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

Per rimuovere i file ausiliari di compilazione:

```powershell
latexmk -c
```

## Struttura della Cartella e Indice dei Capitoli

- **Capitolo 1:** Fondamenti di Compressione Dati e Teoria dell'Informazione (`01-fondamenti-compressione-teoria-informazione-shannon`)
- **Capitolo 2:** Compressori Statistici, Codifica di Huffman e Forma Canonica (`02-compressori-statistici-codifica-huffman-forma-canonica`)
- **Capitolo 3:** Codifica Aritmetica (*Arithmetic Coding*) (`03-codifica-aritmetica`)
- **Capitolo 4:** Esercitazioni di Compressione Statistica: Huffman e Codifica Aritmetica (`04-esercitazioni-compressione-statistica-huffman-aritmetica`)
- **Capitolo 5:** Compressione Statistica Avanzata: Codifica Aritmetica Dinamica, Huffman Canonico e Codici Ottimi Non-Huffman (`05-compressione-statistica-avanzata-modelli-dinamici-ottimalita-huffman`)
- **Capitolo 6:** Compressori Dizionari e Sintattici: Famiglia Lempel-Ziv, GZIP, LZ78 ed LZW (`06-compressori-lempel-ziv-gzip-lz78-lzw`)
- **Capitolo 7:** Codifica di Interi (*Integer Coding*) e Codici Compatti: Elias, Rice, PForDelta e VByte (`07-codifica-interi-codici-compatti-elias-rice-pfordelta-vbyte`)
- **Capitolo 8:** Variante LZSS e Codifica Interpolativa (*Interpolative Coding*) (`08-lzss-interpolative-coding`)
- **Capitolo 9:** Codifica di Elias-Fano e Strutture Quasi-Succinte (`09-codifica-elias-fano-quasi-succinct`)
- **Appendice A:** Esercizi Svolti su Compressori Lempel-Ziv (LZ77, LZ78, LZW) e Codifica di Interi (Delta, PForDelta, Rice) (`appendice-esercizi-svolti-lz-integer-coding`)

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
