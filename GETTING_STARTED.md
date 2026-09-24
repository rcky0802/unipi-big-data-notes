# 🛠️ Guida Rapida all'Uso e alla Contribuzione

Guida rapida per compilare le dispense in PDF, modificare gli appunti o aggiungere una nuova materia.

---

## 📋 1. Requisito Unico di Sistema

Per garantire la perfetta riproducibilità su qualsiasi sistema operativo (Windows, macOS, Linux) e azzerare i problemi di pacchetti mancanti, **questo progetto utilizza esclusivamente Docker**. Non è necessario installare distribuzioni LaTeX pesanti (MiKTeX/TeX Live) o ambienti Python locali.

- **Docker Desktop** (o Docker Engine): [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)  
  *Assicurati che Docker Desktop sia avviato prima di compilare.*
- **Editor consigliato**: **Visual Studio Code** ([code.visualstudio.com](https://code.visualstudio.com/)) oppure **Visual Studio** (*Apri cartella*).

---

## 🚀 2. Apertura del Progetto

Apri sempre la **cartella radice (`Note`)** nell'editor (non una singola sottocartella), per abilitare i task unificati di compilazione:

```powershell
git clone <url-repository>
cd Note
code .
```

> **Sviluppo con Dev Containers (opzionale):**  
> Se usi l'estensione **Dev Containers** in VS Code / Cursor, premi `F1` e seleziona **"Dev Containers: Reopen in Container"**. L'editor si collegherà direttamente all'interno dell'ambiente con TeX Live, Python 3 e LaTeX Workshop già attivi.

---

## 🗂️ 3. Struttura del Repository

Il progetto è organizzato come monorepo multi-materia bilingue:

```text
Note/
├── Dockerfile                  # Ambiente riproducibile (TeX Live + Python 3 + Data Science)
├── docker-compose.yml          # Profili di compilazione isolata
├── pdf/                        # Dispense PDF centralizzate (IT ed EN)
├── <Nome-Materia>/             # es. Algorithm-Engineering, Data-Mining, Information-Retrieval
│   ├── assets/                 # Immagini, grafici vettoriali e slide
│   ├── chapters/
│   │   ├── it/                 # Capitoli in italiano (.tex)
│   │   └── en/                 # Capitoli in inglese speculari (.tex)
│   ├── config/                 # Preamboli bilingue (preamble_it.tex, preamble_en.tex)
│   ├── main_it.tex / main_en.tex # Entry point di compilazione
│   ├── references.bib          # Bibliografia BibTeX
│   └── README.md               # Scheda descrittiva della materia
├── .vscode/tasks.json          # Task unificati per VS Code (Ctrl + Shift + B)
├── tasks.vs.json               # Task unificati per Visual Studio
├── build.ps1                   # Motore di Smart Build differenziale su Docker
├── clean.ps1                   # Pulizia dei file ausiliari LaTeX
└── README.md                   # Hub principale con link ai PDF
```

---

## ⚡ 4. Compilazione dei PDF

Tutte le modalità di compilazione usano Docker sotto il cofano, garantendo compilazioni differenziali veloci (**Smart Build**).

### Metodo A: Da VS Code (Scelta Rapida)
Premi **`Ctrl + Shift + B`** per accedere al menu dei task:
- **Smart Build (Compila solo modificate IT + EN)** *(Default)*: compila in pochi secondi solo le materie e le lingue con modifiche effettive.
- **Compila solo Italiano (IT)**: compila solo le dispense in italiano con modifiche.
- **Compila solo Inglese (EN)**: compila solo le dispense in inglese con modifiche.
- **Scegli Materia e Lingua**: seleziona interattivamente la materia e la lingua.
- **Forza Compilazione Totale (Force All)**: ricompila tutti i documenti da zero.
- **Aggiorna Figure Data-Mining (Python)**: rigenera i grafici vettoriali dai dati reali.
- **Pulisci File Temporanei LaTeX (Clean All)**: elimina i file ausiliari (`.aux`, `.log`, `.toc`, ecc.).

### Metodo B: Da Visual Studio ("Apri cartella")
Clic destro sulla cartella o dal menu Compila:
- **Smart Build (Compila solo modificate IT + EN)**
- **Compila solo Italiano (IT)**
- **Compila solo Inglese (EN)**
- **Forza Compilazione Totale (Force All)**

### Metodo C: Da Terminale (PowerShell)
Dalla radice del progetto:

```powershell
# Smart Build differenziale (compila solo le dispense modificate)
.\build.ps1

# Compila solo una specifica lingua
.\build.ps1 -Lang IT
.\build.ps1 -Lang EN

# Compila solo una specifica materia
.\build.ps1 -Subject "Data-Mining" -Lang IT

# Selezione interattiva con menu a terminale
.\build.ps1 -Interactive

# Pulizia dei file temporanei
.\clean.ps1
```

### Metodo D: Tramite Docker Compose Diretto (qualsiasi OS / shell Linux)

```bash
# Compilazione totale e copia in pdf/
docker compose run --rm build

# Genera solo le figure del capitolo 2 di Data Mining
docker compose run --rm figures

# Shell interattiva nel container
docker compose run --rm app

# Pulizia dei file ausiliari
docker compose run --rm clean
```

Tutti i PDF finali vengono automaticamente sincronizzati in [`pdf/<Materia>-<Lingua>.pdf`](./pdf/) e nelle rispettive cartelle.

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
| `Il daemon di Docker non e' in esecuzione` | Docker Desktop non è avviato | Avvia Docker Desktop e attendi che l'icona diventi verde. |
| `docker non trovato` | Docker non è installato nel PATH | Installa Docker Desktop da [docker.com](https://www.docker.com/products/docker-desktop). |
| Errore `ExecutionPolicy` | Policy di esecuzione script Windows | Esegui una tantum: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Errori su file obsoleti | Cache ausiliaria non allineata (`.aux`, `.toc`) | Esegui `.\clean.ps1` e ricompila con `.\build.ps1 -Force`. |
