"""Data Mining Playground - Chapter 2: Outlier Detection & Missing Values.

This script implements:
1. Missing Value Analysis:
   - Detection of explicit NaNs and disguised values (e.g., 999, -1, empty strings).
   - Missingness inspection per feature (count, percentage).
   - Imputation methods: Mean, Median (robust), Mode (categorical), and Missingness Indicators.
2. Outlier Detection:
   - Tukey's Fences / IQR Rule (Mild: [Q1 - 1.5*IQR, Q3 + 1.5*IQR], Extreme: [Q1 - 3*IQR, Q3 + 3*IQR]).
   - Parametric Z-Score Rule (|z| > 3.0).
3. Comparative reporting and visualization saved to `playground/output/`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
except ImportError as err:
    print(f"[-] Missing required dependency: {err.name}")
    print("[-] Please install required packages first: pip install -r requirements.txt")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_PATH = SCRIPT_DIR / "datasets" / "customer_churn_toy.csv"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_dataset() -> pd.DataFrame:
    """Load dataset containing real-world dirty data (NaNs, disguised values)."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    return df


def clean_disguised_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Identify and replace sentinel/disguised missing values (e.g., age=999) with np.nan."""
    print("=" * 70)
    print("1. DISGUISED MISSING VALUES IDENTIFICATION")
    print("=" * 70)
    df_cleaned = df.copy()

    # In our dataset, age 999 is a disguised missing value
    disguised_age = df_cleaned["age"] == 999
    if disguised_age.any():
        count = disguised_age.sum()
        print(f"[*] Detected {count} record(s) with disguised missing age (age = 999). Replacing with NaN.")
        df_cleaned.loc[disguised_age, "age"] = np.nan

    # Check for empty or whitespace strings
    for col in df_cleaned.select_dtypes(include=["object", "str"]).columns:
        empty_mask = df_cleaned[col].astype(str).str.strip().isin(["", "nan", "None", "NULL"])
        if empty_mask.any():
            print(f"[*] Detected empty string in '{col}'. Replacing with NaN.")
            df_cleaned.loc[empty_mask, col] = np.nan

    return df_cleaned


def analyze_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Report null counts and percentages per attribute."""
    print("\n" + "=" * 70)
    print("2. MISSING VALUES DIAGNOSTICS")
    print("=" * 70)

    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df)) * 100
    missing_report = pd.DataFrame(
        {
            "Missing Count": null_counts,
            "Missing (%)": null_pct.round(2),
            "Dtype": df.dtypes,
        }
    )
    print(missing_report[missing_report["Missing Count"] > 0].to_string())
    return missing_report


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Perform robust imputation (Median for skewed numeric, Mode for categorical)."""
    print("\n" + "=" * 70)
    print("3. MISSING VALUES IMPUTATION")
    print("=" * 70)

    df_imputed = df.copy()

    # 1. Impute age with median (more robust than mean when outliers might exist)
    age_median = df_imputed["age"].median()
    print(f"[*] Imputing 'age' NaN values with median = {age_median:.1f}")
    df_imputed["age_was_missing"] = df_imputed["age"].isnull().astype(int)
    df_imputed["age"] = df_imputed["age"].fillna(age_median)

    # 2. Impute monthly_charges with median
    if "monthly_charges" in df_imputed.columns:
        mc_median = df_imputed["monthly_charges"].median()
        print(f"[*] Imputing 'monthly_charges' with median = {mc_median:.2f}")
        df_imputed["monthly_charges"] = df_imputed["monthly_charges"].fillna(mc_median)

    # 3. Impute categorical columns with Mode
    for cat_col in ["gender", "education_level"]:
        if cat_col in df_imputed.columns and df_imputed[cat_col].isnull().any():
            mode_val = df_imputed[cat_col].mode().iloc[0]
            print(f"[*] Imputing categorical '{cat_col}' with mode = '{mode_val}'")
            df_imputed[cat_col] = df_imputed[cat_col].fillna(mode_val)

    remaining_nulls = df_imputed.isnull().sum().sum()
    print(f"[+] Total remaining NaNs after imputation: {remaining_nulls}")
    return df_imputed


def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> Tuple[pd.Series, float, float]:
    """Detect outliers using Tukey's IQR rule.
    Lower fence: Q1 - k * IQR
    Upper fence: Q3 + k * IQR
    """
    clean_series = series.dropna()
    q1 = clean_series.quantile(0.25)
    q3 = clean_series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr
    outlier_mask = (series < lower_bound) | (series > upper_bound)
    return outlier_mask, lower_bound, upper_bound


def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> Tuple[pd.Series, float]:
    """Detect outliers using parametric Z-score: |(x - mean) / std| > threshold."""
    clean_series = series.dropna()
    mean = clean_series.mean()
    std = clean_series.std(ddof=1)
    if std == 0:
        return pd.Series([False] * len(series), index=series.index), 0.0
    z_scores = (series - mean) / std
    outlier_mask = z_scores.abs() > threshold
    return outlier_mask, threshold


def analyze_outliers(df: pd.DataFrame) -> None:
    """Analyze outliers across numeric features using both IQR and Z-score."""
    print("\n" + "=" * 70)
    print("4. OUTLIER DETECTION (TUKEY IQR vs Z-SCORE)")
    print("=" * 70)

    numeric_cols = ["age", "tenure_months", "monthly_charges", "total_charges"]
    available_cols = [c for c in numeric_cols if c in df.columns]

    for col in available_cols:
        series = df[col]
        # IQR Mild (k=1.5)
        mask_mild, low_mild, high_mild = detect_outliers_iqr(series, k=1.5)
        # IQR Extreme (k=3.0)
        mask_ext, low_ext, high_ext = detect_outliers_iqr(series, k=3.0)
        # Z-score (3.0)
        mask_z, z_thresh = detect_outliers_zscore(series, threshold=3.0)

        print(f"\nFeature: '{col}' (N = {len(series)})")
        print(f"  - IQR Fences [k=1.5]  : [{low_mild:.2f}, {high_mild:.2f}] -> {mask_mild.sum()} outliers")
        print(f"  - IQR Fences [k=3.0]  : [{low_ext:.2f}, {high_ext:.2f}] -> {mask_ext.sum()} extreme outliers")
        print(f"  - Z-Score [|z| > 3.0] : {mask_z.sum()} outliers")

        if mask_mild.any():
            outlier_vals = series[mask_mild].tolist()
            print(f"    Sample outlier values: {outlier_vals[:5]}")


def generate_visual_diagnostics(df_raw: pd.DataFrame, df_imputed: pd.DataFrame) -> None:
    """Generate diagnostic plots for missing data and outlier distribution."""
    print("\n" + "=" * 70)
    print("5. SAVING DIAGNOSTIC FIGURES")
    print("=" * 70)

    sns.set_theme(style="whitegrid")

    # Figure 1: Missing Values Barplot
    fig, ax = plt.subplots(figsize=(8, 4))
    null_counts = df_raw.isnull().sum()
    null_counts = null_counts[null_counts > 0]
    if not null_counts.empty:
        null_counts.plot(kind="bar", color="#d62728", ax=ax)
        ax.set_title("Missing Values Count per Feature (Raw Data)", fontsize=12, fontweight="bold")
        ax.set_ylabel("Count")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plot1_path = OUTPUT_DIR / "02_missing_values_bar.png"
        plt.savefig(plot1_path, dpi=200)
        plt.close()
        print(f"  [+] Saved missing values plot: {plot1_path.name}")

    # Figure 2: Boxplots of Numerical Attributes after imputation
    num_cols = ["age", "tenure_months", "monthly_charges", "total_charges"]
    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    for i, col in enumerate(num_cols):
        sns.boxplot(y=df_imputed[col], ax=axes[i], color="#aec7e8", flierprops={"markerfacecolor": "red", "markersize": 6})
        axes[i].set_title(col, fontweight="bold")
    plt.suptitle("Boxplots of Features Post-Imputation (Outliers in Red)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plot2_path = OUTPUT_DIR / "02_outlier_boxplots.png"
    plt.savefig(plot2_path, dpi=200)
    plt.close()
    print(f"  [+] Saved boxplots: {plot2_path.name}")


def build_interactive_dashboard(df_raw: pd.DataFrame, df_imputed: pd.DataFrame, open_browser: bool = True) -> Path:
    """Generate interactive Plotly dashboard for missing data and outlier diagnostics."""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import webbrowser
    except ImportError:
        print("[-] Plotly not available.")
        return None

    print("\n" + "=" * 70)
    print("6. GENERATING INTERACTIVE WEB DASHBOARD (PLOTLY)")
    print("=" * 70)

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "1. Valori Mancanti per Attributo (Dati Grezzi)",
            "2. Box Plot Interattivo con Rilevamento Outlier (Tukey)",
            "3. Relazione Bivariata: Tenure vs Total Charges",
            "4. Distribuzione 'Age' (Prima e Dopo Imputazione Mediana)",
        ),
        specs=[
            [{"type": "xy"}, {"type": "xy"}],
            [{"type": "xy"}, {"type": "xy"}],
        ],
        vertical_spacing=0.14,
        horizontal_spacing=0.09,
    )

    # 1. Missing Values Bar Chart
    null_counts = df_raw.isnull().sum()
    null_counts = null_counts[null_counts > 0]
    if not null_counts.empty:
        null_pct = (null_counts / len(df_raw)) * 100
        fig.add_trace(
            go.Bar(
                x=null_counts.index,
                y=null_counts.values,
                name="Valori Nulli",
                marker_color="#EF553B",
                hovertext=[f"{count} righe ({pct:.1f}%)" for count, pct in zip(null_counts.values, null_pct.values)],
                hoverinfo="text+x",
                showlegend=False,
            ),
            row=1,
            col=1,
        )
        fig.update_yaxes(title_text="Conteggio Nulli", row=1, col=1)

    # 2. Box plots of numeric features
    num_cols = ["age", "tenure_months", "monthly_charges", "total_charges"]
    colors = ["#636EFA", "#00CC96", "#AB63FA", "#FFA15A"]
    for i, col in enumerate(num_cols):
        fig.add_trace(
            go.Box(
                y=df_imputed[col],
                name=col,
                boxpoints="outliers",
                marker_color=colors[i % len(colors)],
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    # 3. Scatter Plot: Tenure vs Total Charges colored by Churn
    churn_colors = {"Yes": "#EF553B", "No": "#636EFA"}
    for ch in ["No", "Yes"]:
        sub = df_imputed[df_imputed["churn"] == ch]
        fig.add_trace(
            go.Scatter(
                x=sub["tenure_months"],
                y=sub["total_charges"],
                mode="markers",
                name=f"Churn: {ch}",
                marker=dict(size=sub["monthly_charges"] / 8, color=churn_colors.get(ch), opacity=0.85),
                hovertext=[
                    f"ID: {cid}<br>Tenure: {tm}m<br>Monthly: ${mc}<br>Total: ${tc}"
                    for cid, tm, mc, tc in zip(sub["customer_id"], sub["tenure_months"], sub["monthly_charges"], sub["total_charges"])
                ],
                hoverinfo="text",
                legendgroup="churn",
            ),
            row=2,
            col=1,
        )
    fig.update_xaxes(title_text="Tenure (mesi)", row=2, col=1)
    fig.update_yaxes(title_text="Total Charges ($)", row=2, col=1)

    # 4. Age Distribution Before vs After Imputation
    fig.add_trace(
        go.Histogram(
            x=df_raw["age"],
            name="Age (Grezzo con NaN)",
            opacity=0.6,
            marker_color="#AB63FA",
            xbins=dict(start=15, end=80, size=5),
        ),
        row=2,
        col=2,
    )
    fig.add_trace(
        go.Histogram(
            x=df_imputed["age"],
            name="Age (Imputato)",
            opacity=0.5,
            marker_color="#00CC96",
            xbins=dict(start=15, end=80, size=5),
        ),
        row=2,
        col=2,
    )
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(title_text="Età (anni)", row=2, col=2)
    fig.update_yaxes(title_text="Frequenza", row=2, col=2)

    fig.update_layout(
        title_text="<b>Data Mining Playground — Diagnostica Valori Mancanti & Outlier</b>",
        title_font_size=15,
        template="plotly_white",
        height=860,
        margin=dict(l=40, r=40, t=80, b=40),
    )

    html_file = OUTPUT_DIR / "02_interactive_outliers.html"
    fig.write_html(str(html_file), include_plotlyjs=True)
    print(f"  [+] Generata dashboard interattiva HTML in: {html_file.name}")

    if open_browser:
        print(f"  [+] Apertura automatica nel browser predefinito...")
        try:
            webbrowser.open(html_file.resolve().as_uri())
        except Exception as e:
            print(f"  [-] Impossibile aprire automaticamente il browser: {e}")

    return html_file


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Chapter 2: Outlier Detection & Missing Values")
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Non aprire automaticamente la dashboard interattiva nel browser",
    )
    parser.add_argument(
        "--static-only",
        action="store_true",
        help="Genera solo le immagini statiche PNG senza la dashboard interattiva HTML",
    )
    args = parser.parse_args()

    df_raw = load_raw_dataset()
    df_clean_sentinels = clean_disguised_missing(df_raw)
    analyze_missing_values(df_clean_sentinels)
    df_imputed = impute_missing_values(df_clean_sentinels)
    analyze_outliers(df_imputed)

    # 1. Genera immagini statiche PNG
    generate_visual_diagnostics(df_clean_sentinels, df_imputed)

    # 2. Genera dashboard interattiva HTML (Plotly)
    if not args.static_only:
        build_interactive_dashboard(df_clean_sentinels, df_imputed, open_browser=not args.no_browser)

    # Salva dataset pulito
    out_csv = SCRIPT_DIR / "datasets" / "customer_churn_cleaned.csv"
    df_imputed.to_csv(out_csv, index=False)
    print(f"\n[+] Saved cleaned & imputed dataset to: {out_csv.name}")

    print("=" * 70)
    print("[*] Outlier & Missing values pipeline complete.")
    print("    - Immagini statiche salvate in: playground/output/*.png")
    print("    - Dashboard interattiva salvata in: playground/output/02_interactive_outliers.html")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
