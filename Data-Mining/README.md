# Data Mining Notes

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
2. Open the `Data-Mining` folder in VS Code, not just the `main.tex` file:

   ```powershell
   code C:\percorso\Data-Mining
   ```

3. Open [main.tex](main.tex), the entry point for the notes.

## Compilation

The build task is defined in [.vscode/tasks.json](.vscode/tasks.json) and is the default VS Code build task.

Press:

```text
Ctrl+Shift+B
```

The task runs:

```powershell
latexmk -pdf -interaction=nonstopmode main.tex
```

The PDF is generated in the repository root as `main.pdf`, together with the LaTeX auxiliary files. These files are useful for local preview but are excluded from Git by [.gitignore](.gitignore).

You can also compile from the integrated terminal:

```powershell
latexmk -pdf -interaction=nonstopmode main.tex
```

To remove generated artifacts:

```powershell
latexmk -c
```

## PDF Preview

With LaTeX Workshop:

1. Open `main.tex`.
2. Press `Ctrl+Shift+B` to compile.
3. Open the **TEX** panel in the sidebar and choose the PDF viewer, or run **LaTeX Workshop: View LaTeX PDF** from the Command Palette (`Ctrl+Shift+P`).

The preview is updated after each successful compilation.

## Project Structure

```text
Data-Mining/
├── .vscode/
│   └── tasks.json              # Ctrl+Shift+B build task
├── assets/                     # Images and graphical resources
├── chapters/                   # Notes chapters (bilingual: it / en)
│   ├── en/
│   └── it/
├── config/
│   └── preamble.tex            # Packages and shared configuration
├── datasets/                   # Sample datasets
├── notebooks/                  # Interactive Jupyter notebooks & figure scripts
│   ├── README.md               # Guide to notebooks environment
│   ├── requirements.txt        # Python dependencies
│   ├── generate_dispensa_figures.py # Script for dispensa figures
│   └── *.ipynb                 # Interactive Jupyter notebooks
├── .gitignore                  # Unversioned artifacts
├── main.tex                    # Entry point
├── references.bib              # Bibliographic sources
└── README.md                   # This guide
```

## Python & Jupyter Notebooks

A dedicated environment is available in [notebooks/](notebooks/README.md) containing the interactive Jupyter lab notebooks for data understanding, EDA, feature engineering, and dimensionality reduction, as well as the vector figure generator for the lecture notes.

## Adding a Chapter

1. Create a new file in `chapters/`, for example `02-data-preprocessing.tex`.
2. Write its content using `\chapter{...}`.
3. Add it to `main.tex`:

   ```latex
   \include{chapters/02-data-preprocessing}
   ```

Common packages and environments should be added to [config/preamble.tex](config/preamble.tex), not to individual chapters.

### Figures and Graphs

Every image or graph must include:

1. A descriptive `\caption`.
2. A `\label` for internal navigation.
3. A sentence in the surrounding text that refers to the resource with
   `\autoref{...}`.

## Common Problems

### `latexmk` is not found

Close and reopen VS Code after installing MiKTeX. If the problem persists, verify that MiKTeX's `bin` directory is in the Windows `PATH`, then restart the integrated terminal.

### Missing LaTeX package

Open MiKTeX Console, run **Check for updates** and **Update now**, then try compiling again. Also check that automatic package installation is enabled.

### The PDF is not updated

Save the `.tex` file, run `Ctrl+Shift+B` again, and check the **OUTPUT** panel in LaTeX Workshop. Compilation errors are also reported in the integrated terminal.
