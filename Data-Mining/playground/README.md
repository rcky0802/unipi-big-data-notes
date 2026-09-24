# Data Mining Python Playground 🐍📊

Benvenuto nel **Playground Python** del corso di **Data Mining** (Anno Accademico 2026/2027 - Università di Pisa).

Questo ambiente raccoglie script eseguibili, dataset giocattolo e pipeline di analisi a supporto delle dispense teoriche in LaTeX (in particolare il Capitolo 2: *Data Understanding* e il Capitolo 1: *Introduction to Data Mining*).

---

## 📁 Struttura della Cartella

```text
Data-Mining/playground/
├── README.md                     # Guida all'ambiente e documentazione script
├── requirements.txt              # Dipendenze scientifiche (NumPy, Pandas, SciPy, Scikit-learn, Matplotlib, Seaborn)
├── datasets/
│   ├── iris.csv                  # Dataset Iris classico (150 campioni, 4 feature continue, 3 classi)
│   └── customer_churn_toy.csv    # Dataset sintetico con valori mancanti, outlier e variabili categoriche
├── output/                       # Grafici e report generati automaticamente (ignorati da Git)
├── 00_environment_check.py       # Verifica dell'interprete Python e delle librerie installate
├── 01_data_understanding.py      # Statistica descrittiva univariata, multivariata e visualizzazione
├── 02_outlier_and_missing.py     # Diagnostica e gestione di valori mancanti (NaN/camuffati) e outlier (IQR, Z-Score)
└── 03_data_preprocessing.py      # Normalizzazione (Min-Max, Z-score), Discretizzazione ed Encoding categorico
```

---

## 🚀 Guida Rapida all'Installazione

Si consiglia di creare ed attivare un ambiente virtuale dedicato (`.venv`):

### Su Windows (PowerShell)

```powershell
# 1. Posizionarsi nella cartella del playground
cd Data-Mining\playground

# 2. Creare il virtual environment
python -m venv .venv

# 3. Attivare il virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Installare le librerie necessarie
pip install --upgrade pip
pip install -r requirements.txt

# 5. Verificare la corretta configurazione
python 00_environment_check.py
```

> **Nota per PowerShell:** Se l'esecuzione degli script è bloccata, abilitarla nella sessione corrente con:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### Su Linux / macOS (Bash / Zsh)

```bash
cd Data-Mining/playground
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 00_environment_check.py
```

---

## 🌐 Visualizzazione a Video: Dashboard Interattiva & Grafici Statici

Gli script ora supportano una doppia modalità di visualizzazione:
1. **Dashboard Interattiva a Video (Plotly)**: Aprendo automaticamente il browser predefinito, permette di ruotare grafici in 3D, fare zoom dinamico, visualizzare valori esatti al passaggio del cursore (*hover tooltips*) e filtrare le classi con un clic sulla legenda.
2. **Immagini Statiche ad Alta Risoluzione (PNG)**: Tutte le figure generate vengono contestualmente esportate nella cartella `Data-Mining/playground/output/`.

### Come avviare la visualizzazione interattiva

Basta eseguire lo script normalmente:

```powershell
python .\01_data_understanding.py
```

Al termine del calcolo:
* Si aprirà automaticamente a video nel tuo browser la dashboard interattiva [**`01_interactive_dashboard.html`**](output/01_interactive_dashboard.html).
* I file `.png` statici resteranno disponibili in [**`output/`**](output/).

### Opzioni da riga di comando

* `--no-browser`: Genera sia le immagini PNG sia la dashboard interattiva HTML senza aprire automaticamente il browser.
* `--static-only`: Genera esclusivamente le immagini PNG statiche (nessun file HTML).

---

## 📚 Panoramica degli Script e Corrispondenze Teoriche

### 1. `00_environment_check.py`
* **Scopo**: Esegue un controllo di fumo (*smoke test*) rapido. Verifica la versione di Python in uso e tenta l'import di ciascun package in `requirements.txt`, indicando esattamente lo stato di installazione o le istruzioni per configurare il virtualenv.

### 2. `01_data_understanding.py`
Corrisponde alla sezione **Statistica Descrittiva ed Esplorazione Univariata/Multivariata** del Capitolo 2:
* **Statistica Univariata**:
  * Tendenza centrale: Media campionaria ($\bar{x}$), Mediana ($Q_2$), Moda.
  * Dispersione: Varianza campionaria ($s^2$), Deviazione standard ($s$), Range ($Max - Min$), Range Interquartile ($IQR = Q_3 - Q_1$).
  * Sintesi a cinque numeri di Tukey ($Min, Q_1, Mediana, Q_3, Max$).
  * Asimmetria (*Skewness*): interpretazione di code a destra (*positive skew*) e code a sinistra (*negative skew*).
* **Statistica Multivariata**:
  * Matrice di Covarianza campionaria ($S_{ij} = \frac{1}{n-1}\sum (x_k - \bar{x})(y_k - \bar{y})$).
  * Matrice di Correlazione lineare di Pearson ($r_{xy} = \frac{S_{xy}}{S_x S_y}$).
  * Matrice di Correlazione di rango di Spearman ($\rho_s$).
* **Visualizzazioni generate in `output/`**:
  * `01_univariate_histograms.png`: Istogrammi e stima di densità KDE per ciascun attributo continuo.
  * `01_boxplots_by_species.png`: Box plot di Tukey raggruppati per classe.
  * `01_correlation_heatmaps.png`: Heatmap comparative di correlazione lineare (Pearson) e monotonica (Spearman).
  * `01_pairplot_scatter_matrix.png`: Matrice di scatter plot bivariata con separazione per classe.

### 3. `02_outlier_and_missing.py`
Corrisponde alla sezione **Gestione di Outlier e Valori Mancanti**:
* **Valori Mancanti**:
  * Individuazione di valori mancanti camuffati (sentinel values, ad es. `age = 999` o stringhe vuote).
  * Calcolo percentuale di incompletezza per attributo.
  * Strategie di imputazione: Mediana (per variabili numeriche asimmetriche), Moda (per variabili categoriche).
  * Inclusione di flag binari indicativi di imputazione (`age_was_missing`).
* **Rilevamento Outlier**:
  * **Regola di Tukey (IQR Fences)**: Outlier lievi in $[Q_1 - 1.5 \cdot IQR, Q_3 + 1.5 \cdot IQR]$ ed estremi con fattore $3.0$.
  * **Parametrica Z-Score**: Valutazione dei punti oltre la soglia $|z| > 3.0$.
* **Visualizzazioni e Artefatti**:
  * `02_missing_values_bar.png`: Grafico a barre del conteggio record mancanti.
  * `02_outlier_boxplots.png`: Boxplot con evidenziazione grafica dei punti anomali.
  * Generazione del dataset pulito `datasets/customer_churn_cleaned.csv`.

### 4. `03_data_preprocessing.py`
Corrisponde ai fondamenti di **Preprocessing e Trasformazione Dati**:
* **Scalatura delle Feature**:
  * Normalizzazione Min-Max nell'intervallo $[0, 1]$: $x' = \frac{x - x_{min}}{x_{max} - x_{min}}$.
  * Standardizzazione Z-score a media nulla e varianza unitaria: $z = \frac{x - \mu}{\sigma}$.
* **Discretizzazione (Binning)**:
  * Equal-Width: suddivisione dell'intervallo in $k$ bin di ampiezza costante $w = \frac{Max - Min}{k}$.
  * Equal-Frequency: suddivisione per quantili in modo che ogni intervallo contenga circa $N/k$ osservazioni.
* **Codifica delle Variabili Categoriche**:
  * *Ordinal Encoding* per attributi con ordinamento intrinseco (`High School` < `Bachelor` < `Master` < `PhD`).
  * *One-Hot Encoding* (*Dummy Encoding*) per attributi nominali privi di ordine (`gender`, `churn`).
* **Visualizzazioni**:
  * `03_scaling_comparison.png`: Confronto delle distribuzioni prima e dopo Min-Max e Standardizzazione.
  * `03_discretization_comparison.png`: Distribuzione delle frequenze nei bin Equal-Width vs Equal-Frequency.
