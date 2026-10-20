# LaTeX Lecture Notes Standard & Editorial Guidelines

Questa regola definisce gli standard editoriali, tipografici e strutturali per tutti i documenti LaTeX delle dispense nel repository `unipi-big-data-notes` (Information Retrieval, Algorithm Engineering, Data Mining, Computational Mathematics).

---

## 1. Struttura dei Capitoli e Sezionamento

### 1.1 Divieto di Introduzioni Orfane a Livello di Capitolo
* **Regola tassativa**: Non inserire mai testo descrittivo, abstract o paragrafi introduttivi tra `\chapter{...}\label{...}` e la prima `\section{...}`.
* **Motivazione**: Mantenere perfetta uniformità strutturale e consistenza nell'indice generale del documento.
* **Corretta impostazione**:
  ```latex
  \chapter{Titolo del Capitolo}
  \label{ch:titolo-capitolo}

  \section{Introduzione e Panoramica}
  \label{sec:introduzione-panoramica}
  Questo capitolo tratta...
  ```

### 1.2 Gerarchia di Sezionamento
* Articolare i contenuti rispettando la gerarchia:
  1. `\chapter{...}` (o `\part{...}` / `\chapter{...}` ove previsto dal corso)
  2. `\section{...}`
  3. `\subsection{...}`
  4. `\subsubsection{...}` o `\paragraph{...}`
* Ogni sezione e sottosezione deve possedere una label univoca e descrittiva (`sec:...`, `subsec:...`).

---

## 2. Standard Grafici e Diagrammi TikZ

* **Palette Colori Ufficiale**:
  - `navy`: elementi primari, nodi principali, frecce di controllo o bordi formali.
  - `darkgreen`: stati di successo, match positivi, pesi ottimali, partizioni valide.
  - `crimson`: stati di errore, divergenze, pruning, valori limite o scarti.
  - `codebackground`: riempimento di box informativi, blocchi di codice o nodi di sfondo neutro.
* **Stile dei Nodi ed Ergonomia Grafica**:
  - Utilizzare `rounded corners` e spessori di linea armonici (`line width=0.8pt` o `thick`).
  - Font leggibili e proporzionati all'interno dei nodi (`\small`, `\footnotesize`).
* **Frecce ed Etichette TikZ**:
  - Garantire una spaziatura sufficiente tra i nodi (lunghezza degli archi adeguata) per una lettura pulita.
  - Le etichette lungo gli archi (es. simboli $<$, $=$, $>$) non devono **mai coprire o sovrapporsi al tratto o alla punta della freccia**: posizionarle a lato (`above left`, `above right`, `left`, `right`) oppure specificare un background opaco (`fill=white, inner sep=1.5pt`).
* **Confinamento nei Paragrafi e Posizionamento Rigido**:
  - **Regola di non scavalcamento**: nessuna figura o tabella appartenente alla sezione/sottosezione $X.Y$ può scivolare nella sezione $X.Y+1$.
  - Usare sempre il posizionatore rigido `[H]` (dal package `float`): `\begin{figure}[H] \centering ... \end{figure}`.
  - Inserire `\FloatBarrier` (dal package `placeins`) immediatamente prima di ogni `\section{...}` e `\subsection{...}` per confinare deterministicamente i float nel loro ambito di pertinenza.
  - Aggiungere sempre `\caption{...}` esplicativa e `\label{fig:...}`.

---

## 3. Tabelle e Impaginazione Dati

* Le tabelle devono essere posizionate in modo rigido tramite `\begin{table}[H] \centering ... \end{table}`, con font compatto (`\small` o `\footnotesize`).
* Per tabelle larghe o con testo lungo, utilizzare `tabularx` con colonne a larghezza automatica `X` o racchiudere in `\resizebox{\columnwidth}{!}{...}` se a singola colonna.
* Utilizzare `booktabs` per la spaziatura orizzontale (`\toprule`, `\midrule`, `\bottomrule`), evitando linee verticali continue.
* Se necessario regolare lo spazio intercolonna, usare `\setlength{\tabcolsep}{...}` localmente all'interno del gruppo `table`.

---

## 4. Notazione Matematica e Formalizzazione

* **Uniformità delle Variabili**:
  - $n$: numero di elementi, punti, campioni o lunghezza di una sequenza.
  - $m$: lunghezza di una seconda sequenza o numero di vincoli/attributi.
  - $k$: numero di cluster, rango di troncamento o cardinalità del top-$k$.
  - $d$: dimensionalità dello spazio vettoriale o funzione di distanza ($d(x, y)$).
* **Definizioni e Teoremi**:
  - Utilizzare gli ambienti dedicati (`\begin{definition}`, `\begin{theorem}`, `\begin{example}`, ecc.) per evidenziare le formalizzazioni teoriche e le proprietà matematiche.
* **Formule Matematiche Fuori Testo**:
  - Usare `\begin{equation}` con `\label{eq:...}` per equazioni richiamate nel testo.
  - Usare `\begin{align*}` per passaggi algebrici ed equivalenze multilinea senza numerazione ridondante.

---

## 5. Riferimenti Bibliografici e File Principali

* Ogni nuovo capitolo deve essere registrato nel rispettivo `main_it.tex` (tramite `\include{chapters/it/...}`).
* Aggiornare sempre la bibliografia `references.bib` con le citazioni rilevanti usate nel capitolo.
* Aggiornare il `README.md` del corso corrispondente per riflettere l'indice aggiornato degli argomenti.

---

## 6. Verifica della Compilazione e Workflow di Lavoro

* **Verifica Obbligatoria del Build**:
  Prima di presentare il lavoro all'utente, compilare sempre il documento modificato usando lo script dedicato:
  ```powershell
  .\scripts\build.ps1 -Subject "<Subject>" -Force
  ```
  Accertarsi che la compilazione termini con **0 errori** (exit code 0).
* **Policy sui Commit**:
  Non eseguire mai `git commit` o modifiche al versioning senza l'esplicita e preventiva richiesta/conferma dell'utente.
