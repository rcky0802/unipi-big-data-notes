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

## Struttura della Cartella e Indice dei Capitoli

### Sezione 0: Introduzione Generale ai Modelli Computazionali
- **Capitolo 0:** Introduzione Generale ai Modelli Computazionali (`00`)

### Parte I: Algebra Lineare Numerica e Analisi dei Dati
- **Capitolo 1:** Richiami di Algebra Lineare: Vettori, Operazioni e Norme (file `A01`)
- **Capitolo 2:** Prodotto tra Matrici, Complessità Computazionale e Ortogonalità (file `A02`)
- **Capitolo 3:** Matrici Ortonormali, Autovalori e Forme Quadratiche (file `A03`)
- **Capitolo 4:** Decomposizione ai Valori Singolari (SVD) (file `A04`)
- **Capitolo 5:** SVD: Norme Matriciali e Applicazioni (Eckart-Young, Compressione e PCA) (file `A05`)
- **Capitolo 6:** Fattorizzazione QR e Riflessioni di Householder (Full/Thin QR, Riflettori elementari, Stabilità numerica ed Esempio $3 \times 3$) (file `A06`)

### Parte II: Ottimizzazione Continua e Machine Learning
- **Capitolo 7:** Problemi Semplici di Ottimizzazione (file `B02`)
- **Capitolo 8:** Ottimizzazione Multivariata Lineare e Quadratica (file `B03`)
- **Capitolo 9:** Ottimizzazione Quadratica Non Omogenea (GMQ) (file `B04`)
- **Capitolo 10:** Analisi di Convergenza e Complessità del Metodo del Gradiente (file `B05`)

```text
Computational-Mathematics/
├── assets/                 # Figure, grafici vettoriali e schemi
├── chapters/
│   ├── it/                 # Capitoli in italiano (.tex)
│   └── en/                 # Capitoli in inglese speculari (.tex)
├── config/                 # Preamboli bilingue
│   ├── preamble_it.tex
│   └── preamble_en.tex
├── main_it.tex             # Entry point compilazione italiano
├── main_en.tex             # Entry point compilazione inglese
├── main.tex                # Entry point per editor VS Code
├── references.bib          # Bibliografia
└── README.md               # Scheda descrittiva
```
