# 🛠️ Guida Rapida all'Uso e alla Contribuzione

Guida rapida per compilare le dispense in PDF, modificare gli appunti o aggiungere una nuova materia.

---

## 📋 1. Requisito Unico di Sistema

Per garantire la perfetta riproducibilità su qualsiasi sistema operativo (Windows, macOS, Linux) e azzerare i problemi di pacchetti mancanti, **questo progetto utilizza preferibilmente Docker**. Non è necessario installare distribuzioni LaTeX pesanti (MiKTeX/TeX Live) o ambienti Python locali.

- **Docker Desktop** (o Docker Engine): [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)  
  *Assicurati che Docker Desktop sia avviato prima di compilare tramite container.*
- **Editor consigliato**: **Visual Studio Code** ([code.visualstudio.com](https://code.visualstudio.com/)) oppure **Visual Studio** (*Apri cartella*).
- *(Opzionale)* Una distribuzione LaTeX locale con `latexmk` (es. MiKTeX su Windows) se si preferisce compilare senza Docker.

---

## 🚀 2. Apertura del Progetto

Apri sempre la **cartella radice del repository** nell'editor (non una singola sottocartella), per abilitare i task unificati di compilazione:

```powershell
git clone <url-repository>
cd unipi-big-data-notes
code .
```

> **Sviluppo con Dev Containers (opzionale):**  
> Se usi l'estensione **Dev Containers** in VS Code, premi `F1` e seleziona **"Dev Containers: Reopen in Container"**. L'editor si collegherà direttamente all'interno dell'ambiente con TeX Live, Python 3 e LaTeX Workshop già attivi.

---

## 🗂️ 3. Struttura del Repository

Il progetto è organizzato come monorepo modulare con dispense in lingua italiana:

```text
unipi-big-data-notes/
├── Dockerfile                  # Ambiente riproducibile (TeX Live + Python 3 + Data Science)
├── docker-compose.yml          # Profili di compilazione isolata
├── pdf/                        # Dispense PDF centralizzate in italiano
├── <Nome-Materia>/             # es. Algorithm-Engineering, Computational-Mathematics, Data-Mining, Information-Retrieval
│   ├── assets/                 # Immagini, schemi TikZ e grafici vettoriali
│   ├── chapters/
│   │   └── it/                 # Capitoli in italiano (.tex) con nomi kebab-case
│   ├── config/
│   │   └── preamble_it.tex     # Preambolo e configurazione pacchetti condivisa
│   ├── main_it.tex             # Entry point principale di compilazione
│   ├── main.tex                # Entry point per editor VS Code / LaTeX Workshop
│   ├── references.bib          # Bibliografia BibTeX
│   └── README.md               # Scheda descrittiva della materia
├── .vscode/tasks.json          # Task unificati per VS Code (Ctrl + Shift + B)
├── tasks.vs.json               # Task unificati per Visual Studio
├── scripts/                    # Script PowerShell e CMD unificati
│   ├── build.ps1               # Motore di Smart Build differenziale
│   ├── clean.ps1               # Pulizia dei file ausiliari LaTeX
│   ├── start-jupyter.ps1       # Avvio rapido Jupyter Lab in Docker
│   └── start-jupyter.cmd       # Launcher con doppio clic per Windows
└── README.md                   # Hub principale con link ai PDF
```

---

## ⚡ 4. Compilazione dei PDF

Tutte le modalità di compilazione usano lo script intelligente `scripts/build.ps1`, che garantisce compilazioni differenziali veloci (**Smart Build** rilevando i file effettivamente modificati).

### Metodo A: Da VS Code (Scelta Rapida)
Premi **`Ctrl + Shift + B`** per accedere al menu dei task:
- **Smart Build (Compila solo modificate)** *(Default)*: compila in pochi secondi solo le materie con modifiche effettive.
- **Scegli Materia da Compilare**: seleziona dal menu a tendina quale materia compilare.
- **Forza Compilazione Totale (Force All)**: ricompila tutti i documenti da zero.
- **Aggiorna Figure Data-Mining (Python)**: rigenera i grafici vettoriali dai dati reali.
- **Pulisci File Temporanei LaTeX (Clean All)**: elimina i file ausiliari (`.aux`, `.log`, `.toc`, ecc.).
- **Avvia Jupyter Lab (Docker)**: avvia il server Jupyter e apre il browser.

### Metodo B: Da Visual Studio ("Apri cartella")
Clic destro sulla cartella o dal menu Compila:
- **Smart Build (Compila solo modificate)**
- **Compila solo Italiano (IT)**
- **Forza Compilazione Totale (Force All)**
- **Pulisci File Temporanei LaTeX (Clean All)**

### Metodo C: Da Terminale (PowerShell)
Dalla radice del progetto:

```powershell
# Smart Build differenziale (compila solo le dispense modificate)
.\scripts\build.ps1

# Compila solo una specifica materia
.\scripts\build.ps1 -Subject "Data-Mining"

# Forza la ricompilazione totale di tutte le materie
.\scripts\build.ps1 -All -Force

# Selezione interattiva con menu a terminale
.\scripts\build.ps1 -Interactive

# Pulizia dei file temporanei
.\scripts\clean.ps1

# Avvio rapido Jupyter Lab
.\scripts\start-jupyter.ps1
# oppure doppio clic su .\scripts\start-jupyter.cmd
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

Tutti i PDF finali vengono automaticamente sincronizzati in [`pdf/<Materia>-IT.pdf`](./pdf/).

---

## ✍️ 5. Linee Guida di Contribuzione

- **Nomenclatura File Capitoli:** I capitoli vanno collocati in `chapters/it/` con prefisso numerico a due cifre e descrizione in italiano in formato kebab-case (ad es. `01-introduzione-...tex`).
- **Standard LaTeX:** Utilizzare `main_it.tex` come documento principale. Configurazioni comuni, macro matematiche e stili di codice vanno definiti in `config/preamble_it.tex`.
- **Anonimato:** Non inserire nomi o riferimenti all'autore in codice, file o messaggi di commit.
- **Aggiungere una Nuova Materia:**  
  Crea una nuova cartella con la struttura standard sopra descritta. [`scripts/build.ps1`](./scripts/build.ps1) la rileverà automaticamente senza necessità di configurazioni aggiuntive. Aggiungi poi i link in [`README.md`](./README.md) e l'opzione in [`.vscode/tasks.json`](./.vscode/tasks.json).

---

## ❓ 6. Risoluzione Rapida Problemi

| Problema | Causa | Soluzione |
| :--- | :--- | :--- |
| `Il daemon di Docker non e' in esecuzione` | Docker Desktop non è avviato | Avvia Docker Desktop e attendi che l'icona diventi verde (se compili via Docker). |
| `docker non trovato` | Docker non è installato nel PATH | Installa Docker Desktop da [docker.com](https://www.docker.com/products/docker-desktop) oppure usa MiKTeX in locale. |
| Errore `ExecutionPolicy` | Policy di esecuzione script Windows | Esegui una tantum: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Errori su file obsoleti | Cache ausiliaria non allineata (`.aux`, `.toc`) | Esegui `.\scripts\clean.ps1` e ricompila con `.\scripts\build.ps1 -Force`. |
