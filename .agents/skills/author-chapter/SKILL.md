---
name: author-chapter
description: Guida alla redazione, strutturazione, standardizzazione grafica e compilazione di nuovi capitoli LaTeX per le dispense universitarie del repository.
---

# Skill: Redazione e Standardizzazione di Nuovi Capitoli LaTeX

Questa skill guida la stesura e l'integrazione di un nuovo capitolo nelle dispense del repository, garantendo coerenza stilistica, rigore matematico e assenza di errori di compilazione.

---

## Fasi Operative

### Fase 1: Analisi del Materiale Sorgente
1. Ricevi il contenuto (slide, trascrizioni, appunti) relativo alla lezione o modulo didattico.
2. Identifica i macro-temi e organizza la scaletta logica in sezioni e sottosezioni.
3. Seleziona i concetti chiave che beneficiano di un diagramma TikZ o di una tabella comparativa riassuntiva.

### Fase 2: Redazione del File LaTeX
Crea il nuovo file in `<Subject>/chapters/it/<numero>-<nome-descrittivo>.tex`.

Rispetta la struttura standardizzata:
```latex
\chapter{Titolo Accademico del Capitolo}
\label{ch:titolo-descrittivo}

\section{Introduzione e Motivazione}
\label{sec:titolo-intro}
% Nessun testo orfano prima di questa sezione!
In questo capitolo vengono esaminati i fondamenti di...
```

Linee guida di stile per il corpo del testo:
- **Formalismo Matematico**: definisci sempre insiemi, vettori e dimensioni con chiarezza ($X = \langle x_1, \dots, x_n \rangle \in \mathbb{R}^n$).
- **Figure TikZ**: usa la palette `navy`, `darkgreen`, `crimson`, `codebackground` con nodi `rounded corners`. Posiziona sempre le etichette a lato degli archi o con sfondo per non nascondere le frecce.
- **Confinamento Float**: usa sempre `\begin{figure}[H]` e `\begin{table}[H]`, e anteponi `\FloatBarrier` ad ogni `\section` e `\subsection` affinché nessuna figura o tabella oltrepassi il proprio paragrafo.
- **Tabelle**: usa `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), font `\small` e layout compatto racchiuso ove opportuno in `\resizebox{\columnwidth}{!}{...}`.
- **Box e Teoremi**: usa gli ambienti `definition`, `theorem`, `example` per evidenziare i passaggi teorici cardine.

### Fase 3: Integrazione nei File Principali
1. **`main_it.tex`**: aggiungi `\include{chapters/it/<nome-file>}` nella sequenza logica dei capitoli.
2. **`references.bib`**: inserisci le voci bibliografiche pertinenti citate nel testo con `\cite{...}`.
3. **`README.md`**: aggiungi il nuovo capitolo con titolo ed estremi nella panoramica dei contenuti del corso.

### Fase 4: Verifica della Compilazione
Esegui la compilazione tramite PowerShell:
```powershell
.\scripts\build.ps1 -Subject "<Subject>" -Force
```
- Controlla il log e assicurati che non vi siano errori bloccanti né warning critici su referenze mancanti o package non definiti.
- Se si verificano errori, correggili immediatamente e riesegui la compilazione.

### Fase 5: Consegna e Revisione
- Presenta all'utente una sintesi strutturata dei contenuti aggiunti, evidenziando le sezioni principali e i diagrammi realizzati.
- **Attendi sempre conferma esplicita prima di proporre o eseguire il commit Git.**
