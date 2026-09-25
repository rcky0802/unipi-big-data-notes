# Data Mining: Notebooks e Script Didattici

Questa cartella raccoglie l'intero ambiente didattico Python e Jupyter per il corso di **Data Mining**.

## Struttura della Cartella

- **`1_basics_and_understanding.ipynb`**: Notebook Jupyter interattivo per il Capitolo 2 (*Data Understanding, EDA, calcolo statistiche descrittive, IQR, Boxplot, Scatter Matrix, correlazioni e gestione missing values*).
- **`2_feature_engineering_and_data_representation.ipynb`**: Notebook Jupyter interattivo per il Capitolo 3 (*Data Preparation, PCA, Scree Plot, discretizzazione, binarizzazione, One-Hot Encoding, scaling e t-SNE*).
- **`generate_dispensa_figures.py`**: Script Python per generare le figure vettoriali ad alta risoluzione (PDF) incluse nelle dispense LaTeX (`Data-Mining/assets/figures/it/` ed `en/`).
- **`data_notebook/`**: Cartella contenente i dataset (`data/`) e le immagini di supporto (`images/`) impiegati dai notebook Jupyter.
- **`datasets/`**: Cartella con i dataset (ad es. `iris.csv`) utilizzati da `generate_dispensa_figures.py`.
- **`requirements.txt`**: Elenco delle dipendenze scientifiche Python (`numpy`, `pandas`, `scipy`, `matplotlib`, `seaborn`, `scikit-learn`, `jupyterlab`).

## Come Avviare Jupyter Lab

### Tramite Docker (Consigliato)
Dalla radice del progetto, eseguire:
```bash
docker compose up jupyter
```
oppure utilizzare lo script rapido con doppio clic `start-jupyter.cmd` (o `start-jupyter.ps1` da PowerShell).

Una volta avviato il container, aprire nel browser:
```text
http://localhost:8888/lab/tree/notebooks/1_basics_and_understanding.ipynb
```

## Come Rigenerare le Figure della Dispensa
Dalla radice del progetto:
```bash
docker compose run --rm figures
```
oppure in locale (con le dipendenze installate):
```bash
python Data-Mining/notebooks/generate_dispensa_figures.py
```
