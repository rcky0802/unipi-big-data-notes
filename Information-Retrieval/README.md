# Information Retrieval Notes

> 📍 *Parte dell'hub documentale unificato degli appunti universitari: [Visualizza Hub Principale](../README.md)*

University notes in LaTeX, organized into separate chapters and compiled directly from Visual Studio Code (Academic Year 2026/2027).

## Prerequisites

Install the following tools:

1. [Visual Studio Code](https://code.visualstudio.com/)
2. A LaTeX distribution, preferably [MiKTeX](https://miktex.org/download)
3. `latexmk`, usually included with MiKTeX
4. The VS Code extension [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)

During the first compilation, allow MiKTeX to install missing packages automatically. Alternatively, open **MiKTeX Console**, run the updates, and verify that automatic package installation is enabled.

## Opening the Project

1. Clone or download the repository.
2. Open the repository root folder in VS Code:

   ```powershell
   code C:\path\to\Note
   ```

3. Or open `Information-Retrieval` directly:

   ```powershell
   code C:\path\to\Note\Information-Retrieval
   ```

4. Open [main.tex](main.tex) (or [main_it.tex](main_it.tex) / [main_en.tex](main_en.tex)), the entry point for the notes.

## Compilation

You can compile using the repository unified build script from PowerShell:

```powershell
.\scripts\build.ps1 -Subject "Information-Retrieval"
```

To compile only the Italian version:

```powershell
.\scripts\build.ps1 -Subject "Information-Retrieval" -Lang IT
```

To compile only the English version:

```powershell
.\scripts\build.ps1 -Subject "Information-Retrieval" -Lang EN
```

Or from within the `Information-Retrieval` folder with `latexmk`:

```powershell
latexmk -pdf -interaction=nonstopmode main_it.tex
latexmk -pdf -interaction=nonstopmode main_en.tex
```

To remove generated auxiliary artifacts:

```powershell
latexmk -c
```

## Chapters Overview

- **Chapter 1: Introduction and Architecture of Information Retrieval**
  - IR definitions, motivations, IR vs. Data Retrieval (SQL/DBMS).
  - The two fundamental goals: Effectiveness vs. Efficiency (pipelining, hazards, memory hierarchy, SIMD, parallel computing).
  - Language properties (Zipf's law, Heaps' law), text preprocessing pipeline.
  - Inverted Index structure, dictionary + posting lists, Merge Intersection algorithm.
  - Index compression: Binary Interpolative Coding (recursive median range partitioning), LZ77 dictionary coding.
  - Neural Information Retrieval: Interaction-based (Cross-Encoders) vs. Representation-based (Bi-Encoders).
  - Embedding families: Dense single-vector, Dense multi-vector (ColBERT late interaction / MaxSim), Sparse single-vector (SPLADE).
  - $k$-Approximate Nearest Neighbor Search ($k$-ANN, MIPS, TusKANNy).

- **Chapter 2: Evaluation of Information Retrieval Systems**

- **Chapter 3: Efficiency on Modern CPU Architectures** *(Italian only)*
  - Memory hierarchy (L1/L2/L3/RAM), cache lines, spatial/temporal locality, hardware prefetchers.
  - Sequential scan vs. pointer-chasing benchmark (Rust) and cache-line-aware jumping.
  - 5-stage pipelining, latency vs. throughput, superscalar execution and execution ports.
  - Structural hazards, RAW data hazards and dependency-chain interleaving.
  - Control hazards, speculative execution, branch misprediction cost and branchless techniques.
  - Evaluating search quality: efficiency, side services, intrinsic effectiveness.
  - Measuring User Happiness: CTR, zero-click searches, conversions, retention, Dwell Time, paradigm shifts with LLMs.
  - The Cranfield Paradigm (Cyril Cleverdon), benchmark test collections (corpus, queries, qrels).
  - Combinatorial scale challenges, crowdsourcing trade-offs, TREC infrastructure.
  - The Pooling technique, unjudged document assumptions, and pooling bias.
  - Information need vs. surface query.
  - Unranked evaluation (contingency table, Precision, Recall, $F_1$-score harmonic mean, weighted $F_\beta$).
  - Ranked evaluation (Precision@k, Recall@k, Average Precision, MAP macro-averaging, MRR for known-item search).
  - Graded relevance evaluation: Cumulative Gain, Discounted Cumulative Gain (standard vs. exponential), Ideal DCG, and Normalized Discounted Cumulative Gain (NDCG) with full step-by-step numerical traces.

