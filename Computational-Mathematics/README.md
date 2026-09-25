# Computational Mathematics for Learning and Data Analysis Notes

> 📍 *Parte dell'hub documentale unificato degli appunti universitari: [Visualizza Hub Principale](../README.md)*

Appunti universitari in LaTeX per il corso di **Computational Mathematics for Learning and Data Analysis** (Anno Accademico 2026/2027), strutturati in capitoli bilingue modulari e compilabili sia tramite Docker sia in ambiente locale.

## Prerequisiti

Per la compilazione locale sono consigliati:
1. [Visual Studio Code](https://code.visualstudio.com/) con estensione [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
2. Una distribuzione LaTeX (es. [MiKTeX](https://miktex.org/download) su Windows con `latexmk`)
3. Oppure semplicemente [Docker Desktop](https://www.docker.com/products/docker-desktop) sfruttando il container unificato del repository.

## Compilazione

Dalla radice del repository è possibile compilare la dispensa con lo script unificato PowerShell:

```powershell
# Compila entrambe le edizioni (Italiano e Inglese)
.\scripts\build.ps1 -Subject "Computational-Mathematics"

# Compila solo l'edizione Italiana
.\scripts\build.ps1 -Subject "Computational-Mathematics" -Lang IT

# Compila solo l'edizione Inglese
.\scripts\build.ps1 -Subject "Computational-Mathematics" -Lang EN
```

Oppure direttamente all'interno della cartella `Computational-Mathematics` con `latexmk`:

```powershell
latexmk -pdf -interaction=nonstopmode main_it.tex
latexmk -pdf -interaction=nonstopmode main_en.tex
```

## Struttura della Cartella

```text
Computational-Mathematics/
├── assets/                 # Figure, grafici vettoriali e schemi
├── chapters/
│   ├── it/                 # Capitoli in italiano (.tex)
│   │   └── 01-fondamenti-algebra-lineare-svd.tex
│   └── en/                 # Capitoli in inglese speculari (.tex)
│       └── 01-foundations-linear-algebra-svd.tex
├── config/                 # Preamboli bilingue
│   ├── preamble_it.tex
│   └── preamble_en.tex
├── main_it.tex             # Entry point compilazione italiano
├── main_en.tex             # Entry point compilazione inglese
├── main.tex                # Entry point per editor VS Code
├── references.bib          # Bibliografia
└── README.md               # Scheda descrittiva
```
