# 🛠️ Guida Rapida all'Uso e alla Contribuzione Locale

Questa guida è pensata per chiunque cloni o scarichi il repository in locale e desideri **compilare le dispense in PDF**, **modificare gli appunti esistenti** oppure **aggiungere una nuova materia**.

---

## 📋 1. Requisiti di Sistema

Per compilare e modificare correttamente i documenti LaTeX del progetto sono necessari:

| Strumento | Descrizione | Come installarlo |
| :--- | :--- | :--- |
| **Visual Studio Code** | Editor consigliato con supporto task integrato | [code.visualstudio.com](https://code.visualstudio.com/) |
| **MiKTeX** (o TeX Live) | Distribuzione LaTeX con compilatore `latexmk` | `winget install MiKTeX.MiKTeX` oppure [miktex.org](https://miktex.org/download) |
| **LaTeX Workshop** *(estensione)* | Estensione VS Code per evidenziazione sintassi e preview PDF | ID: `James-Yu.latex-workshop` nel Marketplace di VS Code |

> [!IMPORTANT]
> **Installazione di MiKTeX:**  
> Durante l'installazione guidata di MiKTeX, imposta l'opzione **"Install missing packages on-the-fly"** su **`Yes`**. In questo modo MiKTeX scaricherà automaticamente tutti i pacchetti aggiuntivi necessari durante la prima compilazione.

---

## 🚀 2. Clonare e Aprire il Progetto

1. Clona il repository sul tuo computer:
   ```bash
   git clone https://github.com/rcky0802/<nome-repository>.git
   cd <nome-repository>
   ```
2. **Apri la cartella radice (`Note`) in VS Code**, e non una singola sottocartella:
   ```powershell
   code .
   ```
   *Aprire la radice consente a VS Code di caricare i task unificati di compilazione presenti in `.vscode/tasks.json`.*

---

## 🗂️ 3. Organizzazione delle Cartelle

Il repository è organizzato come monorepo multi-materia:

```text
Note/
├── pdf/                        # Tutte le dispense PDF aggiornate e pronte al download
├── Algorithm-Engineering/      # Archivio materia: Algorithm Engineering
│   ├── assets/                 # Immagini, grafici e diagrammi
│   ├── chapters/               # Singoli capitoli in formato .tex
│   ├── config/preamble.tex     # Pacchetti, layout e macro matematiche
│   ├── main.tex                # Entry point per la compilazione
│   ├── references.bib          # Bibliografia BibTeX
│   └── README.md               # Guida specifica della materia
├── Data-Mining/                # Archivio materia: Data Mining
│   ├── assets/                 # Immagini, grafici e diagrammi
│   ├── chapters/               # Singoli capitoli in formato .tex
│   ├── config/preamble.tex     # Pacchetti, layout e macro matematiche
│   ├── main.tex                # Entry point per la compilazione
│   ├── references.bib          # Bibliografia BibTeX
│   └── README.md               # Guida specifica della materia
├── .vscode/
│   └── tasks.json              # Task di compilazione per VS Code
├── .editorconfig               # Regole di formattazione editor
├── .gitattributes              # Gestione fine riga e file binari
├── .gitignore                  # Esclusione automatica file ausiliari LaTeX
├── build.ps1                   # Script di build intelligente con rilevamento modifiche
├── clean.ps1                   # Pulizia dei file ausiliari di compilazione
├── GETTING_STARTED.md          # Questa guida
└── README.md                   # Landing page principale del progetto
```

---

## ⚡ 4. Comandi di Compilazione in PDF

Il progetto include un motore di compilazione intelligente ([`build.ps1`](./build.ps1)) che rileva automaticamente le modifiche ai sorgenti ed evita ricompilazioni inutili.

### Modalità A: Da Visual Studio Code (Scelta Rapida)

Premi in qualsiasi momento:

```text
Ctrl + Shift + B
```

Si aprirà il menu dei task preconfigurati:
- **`Smart Build (Compila solo modificate)`** *(predefinito)*: compila **solo** le materie in cui hai modificato file `.tex`, `.bib` o immagini. Se una materia è già aggiornata, viene saltata all'istante.
- **`Scegli Materia da Compilare (Interattivo VS Code)`**: mostra un menu a tendina per scegliere quale materia compilare singolarmente.
- **`Forza Compilazione di Tutte le Materie (Force All)`**: ricompila tutte le materie da zero ignorando la cache.
- **`Pulisci File Temporanei LaTeX (Clean All)`**: elimina tutti i file ausiliari generati da LaTeX (`.aux`, `.log`, `.synctex.gz`, `.toc`, ecc.).

---

### Modalità B: Da Terminale PowerShell

Puoi lanciare lo script direttamente dal terminale PowerShell alla radice del progetto:

```powershell
# 1. Smart Build (compila in automatico solo le dispense modificate IT ed EN)
.\build.ps1

# 2. Compila solo in italiano o solo in inglese
.\build.ps1 -Lang IT
.\build.ps1 -Lang EN

# 3. Selezione interattiva con menu a terminale
.\build.ps1 -Interactive

# 4. Compila solo una specifica materia
.\build.ps1 -Subject "Algorithm-Engineering" -Lang IT
.\build.ps1 -Subject "Data-Mining" -Lang EN

# 5. Forza la compilazione totale di tutte le materie e lingue
.\build.ps1 -All -Force

# 6. Pulizia dei file ausiliari di compilazione
.\clean.ps1
```

---

## 📥 5. Dove Trovare i PDF Generati

Una volta completata la compilazione, i PDF sono disponibili in due posizioni:
1. **Nell'archivio centralizzato con suffisso lingua:**
   - [`pdf/Algorithm-Engineering-IT.pdf`](./pdf/Algorithm-Engineering-IT.pdf) / [`pdf/Algorithm-Engineering-EN.pdf`](./pdf/Algorithm-Engineering-EN.pdf)
   - [`pdf/Data-Mining-IT.pdf`](./pdf/Data-Mining-IT.pdf) / [`pdf/Data-Mining-EN.pdf`](./pdf/Data-Mining-EN.pdf)
2. **Nella cartella locale della materia:**
   - [`<Nome-Materia>/main_it.pdf`](./Algorithm-Engineering/main_it.pdf) (Italiano)
   - [`<Nome-Materia>/main_en.pdf`](./Algorithm-Engineering/main_en.pdf) (Inglese)

---

## ✍️ 6. Come Modificare gli Appunti Esistenti

Tutte le materie seguono una struttura bilingue modulare speculare:

```text
Materia/
├── chapters/
│   ├── it/                 # Capitoli in italiano (.tex)
│   └── en/                 # Capitoli in inglese (.tex, identici e speculari)
├── assets/                 # Immagini, grafici TikZ, screenshot condivisi
├── config/
│   ├── preamble_it.tex     # Preambolo italiano (babel italian, teoremi IT)
│   └── preamble_en.tex     # Preambolo inglese (babel english, teoremi EN)
├── references.bib          # Fonti bibliografiche BibTeX condivise
├── main_it.tex             # Entry point versione italiana
└── main_en.tex             # Entry point versione inglese
```

### Modificare un Capitolo
1. Apri il file del capitolo corrispondente all'interno di `chapters/it/` o `chapters/en/`. Ricorda di mantenere speculari e allineate entrambe le versioni.
2. Apporta le modifiche utilizzando la sintassi standard LaTeX:
   - Sezioni e paragrafi: `\section{...}`, `\subsection{...}`
   - Ambienti matematici ed enunciati:
     ```latex
     \begin{definition}[Titolo Definizione]
       Testo della definizione...
     \end{definition}
     ```
   - Figure e immagini:
     ```latex
     \begin{figure}[htbp]
       \centering
       \includegraphics[width=0.8\textwidth]{assets/nome-immagine.png}
       \caption{Descrizione dettagliata della figura.}
       \label{fig:mio-grafico}
     \end{figure}
     ```
   - Riferimenti incrociati nel testo: `Come illustrato in \autoref{fig:mio-grafico}...`
3. Salva il file e premi `Ctrl + Shift + B`: lo Smart Build rileverà la modifica e aggiornerà il PDF in pochi secondi.

### Aggiungere un Riferimento Bibliografico
1. Apri `references.bib` della materia.
2. Inserisci la nuova voce in formato BibTeX:
   ```bibtex
   @book{tan2018,
     author    = {Pang-Ning Tan and Michael Steinbach and Anuj Karpatne and Vipin Kumar},
     title     = {Introduction to Data Mining},
     edition   = {2nd},
     publisher = {Pearson},
     year      = {2018}
   }
   ```
3. Cita la fonte all'interno dei capitoli con `\cite{tan2018}`.

---

## ➕ 7. Come Aggiungere una Nuova Materia

Il sistema è progettato per essere scalabile a qualsiasi nuovo esame o corso:

1. **Crea la nuova cartella** alla radice di `Note/` (es. `Machine-Learning/`).
2. **Crea la struttura di base:**
   - `main.tex`: documento radice con `\documentclass{report}`, `\input{config/preamble}`, titoli e i vari `\include{chapters/...}`.
   - `chapters/`: cartella contenente i singoli file `.tex` dei capitoli.
   - `config/preamble.tex`: preambolo con pacchetti e definizioni.
   - `assets/`: cartella per immagini e grafici.
   - `references.bib`: file per le citazioni.
   - `README.md`: scheda descrittiva della materia.
3. **Compilazione automatica:**  
   Non devi configurare alcuno script! Eseguendo `.\build.ps1` o premendo `Ctrl+Shift+B`, lo script rileverà la nuova cartella contenente `main.tex`, la compilerà e salverà il PDF corrispondente in `pdf/Machine-Learning.pdf`.
4. Aggiungi la nuova materia nella tabella di [`README.md`](./README.md).

---

## ❓ 8. Risoluzione dei Problemi Comuni (Troubleshooting)

### 🔴 `latexmk non trovato` o `exit code: 1` al build
- **Causa:** MiKTeX non è ancora installato, oppure non è stato aggiunto al `PATH` di sistema.
- **Soluzione:**
  1. Installa MiKTeX eseguendo da PowerShell: `winget install MiKTeX.MiKTeX`.
  2. Riavvia completamente Visual Studio Code per permettere l'aggiornamento del `PATH`.
  3. Lo script [`build.ps1`](./build.ps1) include un meccanismo di auto-discovery che controlla anche i percorsi standard (`%LOCALAPPDATA%\Programs\MiKTeX\...`).

### 🔴 Errore sui permessi degli script PowerShell (`ExecutionPolicy`)
- **Causa:** Le policy di sicurezza di Windows impediscono l'esecuzione di script non firmati.
- **Soluzione:**
  Esegui una tantum in una finestra PowerShell con privilegi di amministratore:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
  *(In alternativa, i task VS Code sono già preconfigurati con il parametro `-ExecutionPolicy Bypass`)*.

### 🔴 Errori di compilazione dopo modifiche strutturali
- **Causa:** File ausiliari obsoleti (`.aux`, `.toc`, `.bbl`) non allineati.
- **Soluzione:**
  Esegui lo script di pulizia:
  ```powershell
  .\clean.ps1
  ```
  Quindi ricompila con `Ctrl + Shift + B` o `.\build.ps1 -Force`.
