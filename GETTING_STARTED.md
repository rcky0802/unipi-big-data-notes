# 🛠️ Guida Rapida all'Uso e alla Contribuzione

Guida rapida per compilare le dispense in PDF, modificare gli appunti o aggiungere una nuova materia.

---

## 📋 1. Requisiti di Sistema

- **Visual Studio Code** ([code.visualstudio.com](https://code.visualstudio.com/))
- **MiKTeX** (`winget install MiKTeX.MiKTeX` o [miktex.org](https://miktex.org/download))  
  *Durante l'installazione, imposta **"Install missing packages on-the-fly"** su **`Yes`**.*
- **LaTeX Workshop** (estensione VS Code: `James-Yu.latex-workshop`)

---

## 🚀 2. Apertura del Progetto

Apri sempre la **cartella radice (`Note`)** in VS Code (non una singola sottocartella), per abilitare i task unificati di compilazione:

```powershell
git clone <url-repository>
cd Note
code .
```

---

## 🗂️ 3. Struttura del Repository

Il progetto è organizzato come monorepo multi-materia bilingue:

```text
Note/
├── pdf/                        # Dispense PDF centralizzate (IT ed EN)
├── <Nome-Materia>/             # es. Algorithm-Engineering, Data-Mining, Information-Retrieval
│   ├── assets/                 # Immagini, grafici TikZ e slide
│   ├── chapters/
│   │   ├── it/                 # Capitoli in italiano (.tex)
│   │   └── en/                 # Capitoli in inglese speculari (.tex)
│   ├── config/                 # Preamboli bilingue (preamble_it.tex, preamble_en.tex)
│   ├── main_it.tex / main_en.tex # Entry point di compilazione
│   ├── references.bib          # Bibliografia BibTeX
│   └── README.md               # Scheda descrittiva della materia
├── .vscode/tasks.json          # Menu task per VS Code
├── build.ps1                   # Motore di compilazione intelligente
├── clean.ps1                   # Pulizia dei file ausiliari LaTeX
└── README.md                   # Hub principale con link ai PDF
```

---

## ⚡ 4. Compilazione dei PDF

### Metodo A: Da VS Code (Scelta Rapida)
Premi **`Ctrl + Shift + B`** per accedere al menu dei task:
- **Smart Build** *(Default)*: compila in pochi secondi solo le materie con file modificati.
- **Scegli Materia e Lingua**: seleziona interattivamente cosa compilare.
- **Forza Compilazione Totale**: ricompila tutti i documenti da zero.
- **Pulisci File Temporanei**: elimina i file ausiliari (`.aux`, `.log`, `.toc`, ecc.).

### Metodo B: Da Terminale PowerShell
Dalla radice del progetto:

```powershell
# Compilazione intelligente (solo modificate IT + EN)
.\build.ps1

# Compila solo una specifica lingua o materia
.\build.ps1 -Lang IT
.\build.ps1 -Subject "Information-Retrieval" -Lang EN

# Selezione interattiva con menu a terminale
.\build.ps1 -Interactive

# Pulizia dei file temporanei
.\clean.ps1
```

I PDF generati vengono salvati in `pdf/<Materia>-<Lingua>.pdf` e nella cartella della materia.

---

## ✍️ 5. Linee Guida di Contribuzione

- **Parità Bilingue:** Ogni modifica o nuovo capitolo deve essere inserito sia in `chapters/it/` sia in `chapters/en/`, mantenendo struttura e formule matematiche sincronizzate.
- **Anonimato:** Non inserire nomi o riferimenti all'autore in codice, file o messaggi di commit.
- **Aggiungere una Nuova Materia:**  
  Crea una nuova cartella con la struttura standard sopra descritta. [`build.ps1`](./build.ps1) la rileverà automaticamente senza necessità di configurazioni aggiuntive. Aggiungi poi i link in [`README.md`](./README.md) e l'opzione in [`.vscode/tasks.json`](./.vscode/tasks.json).

---

## ❓ 6. Risoluzione Rapida Problemi

| Problema | Causa | Soluzione |
| :--- | :--- | :--- |
| `latexmk non trovato` | MiKTeX non installato o PATH non aggiornato | Installa MiKTeX con `winget install MiKTeX.MiKTeX` e riavvia VS Code. |
| Errore `ExecutionPolicy` | Policy di esecuzione script Windows | Esegui una tantum: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Errori su file obsoleti | Cache ausiliaria non allineata (`.aux`, `.toc`) | Esegui `.\clean.ps1` e ricompila con `.\build.ps1 -Force`. |
