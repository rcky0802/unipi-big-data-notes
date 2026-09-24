"""Data Mining Playground - Data Preprocessing & Transformations.

This script implements fundamental data transformation techniques:
1. Normalization & Standardization:
   - Min-Max Normalization (mapping features to [0, 1]).
   - Z-score Standardization (mean = 0, standard deviation = 1).
2. Discretization (Binning):
   - Equal-Width Binning (dividing range into k equal intervals).
   - Equal-Frequency (Quantile) Binning (k intervals with roughly equal samples).
3. Categorical Encoding:
   - Ordinal Encoding (preserving natural rank for ordinal attributes).
   - One-Hot Encoding (for nominal attributes without implicit ordering).
4. Visual comparison before and after transformation saved to `output/`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Tuple

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder, StandardScaler
except ImportError as err:
    print(f"[-] Missing required dependency: {err.name}")
    print("[-] Please install required packages first: pip install -r requirements.txt")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
CLEANED_DATA_PATH = SCRIPT_DIR / "datasets" / "customer_churn_cleaned.csv"
RAW_DATA_PATH = SCRIPT_DIR / "datasets" / "customer_churn_toy.csv"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    """Load cleaned dataset if available; otherwise load raw and fill minimal nulls."""
    if CLEANED_DATA_PATH.exists():
        df = pd.read_csv(CLEANED_DATA_PATH)
    else:
        df = pd.read_csv(RAW_DATA_PATH)
        df["age"] = df["age"].replace(999, np.nan).fillna(df["age"].median())
        df["gender"] = df["gender"].fillna("Unknown")
        df["education_level"] = df["education_level"].fillna("Bachelor")
        df["monthly_charges"] = df["monthly_charges"].fillna(df["monthly_charges"].median())
    return df


def demonstrate_scaling(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Compare Min-Max Normalization vs Z-Score Standardization on numerical features."""
    print("=" * 70)
    print("1. FEATURE SCALING: MIN-MAX vs Z-SCORE STANDARDIZATION")
    print("=" * 70)

    numeric_cols = ["age", "tenure_months", "monthly_charges", "total_charges"]
    data = df[numeric_cols].copy()

    # 1. Min-Max Scaling [0, 1]
    min_max_scaler = MinMaxScaler(feature_range=(0, 1))
    min_max_scaled = pd.DataFrame(
        min_max_scaler.fit_transform(data),
        columns=[f"{col}_minmax" for col in numeric_cols],
    )

    # 2. Z-Score Standardization (mean=0, std=1)
    std_scaler = StandardScaler()
    std_scaled = pd.DataFrame(
        std_scaler.fit_transform(data),
        columns=[f"{col}_zscore" for col in numeric_cols],
    )

    print("[*] Original Statistics (Raw):")
    print(data.describe().round(2).T[["mean", "std", "min", "50%", "max"]].to_string())

    print("\n[*] Min-Max Scaled Statistics (Range [0, 1]):")
    print(min_max_scaled.describe().round(3).T[["mean", "std", "min", "50%", "max"]].to_string())

    print("\n[*] Z-Score Standardized Statistics (Mean ~ 0, Std ~ 1):")
    print(std_scaled.describe().round(3).T[["mean", "std", "min", "50%", "max"]].to_string())

    return min_max_scaled, std_scaled


def demonstrate_discretization(df: pd.DataFrame) -> pd.DataFrame:
    """Compare Equal-Width Binning and Equal-Frequency Binning on continuous attributes."""
    print("\n" + "=" * 70)
    print("2. DISCRETIZATION: EQUAL-WIDTH vs EQUAL-FREQUENCY")
    print("=" * 70)

    target_feature = "age"
    k_bins = 4
    labels = ["Group_1_Young", "Group_2_Adult", "Group_3_MiddleAged", "Group_4_Senior"]

    discretized_df = pd.DataFrame()
    discretized_df["age_raw"] = df[target_feature]

    # Equal-Width Binning: splits range into k equal width intervals
    discretized_df["age_equal_width"] = pd.cut(df[target_feature], bins=k_bins, labels=labels)
    # Equal-Frequency (Quantile) Binning: splits into quantiles so each bin has ~N/k rows
    discretized_df["age_equal_freq"] = pd.qcut(df[target_feature], q=k_bins, labels=labels)

    print(f"[*] Discretizing '{target_feature}' into {k_bins} bins:\n")
    print("Equal-Width Distribution:")
    print(discretized_df["age_equal_width"].value_counts(sort=False).to_string())

    print("\nEqual-Frequency (Quantile) Distribution:")
    print(discretized_df["age_equal_freq"].value_counts(sort=False).to_string())

    return discretized_df


def demonstrate_categorical_encoding(df: pd.DataFrame) -> pd.DataFrame:
    """Encode ordinal attributes with rank mapping and nominal attributes with one-hot."""
    print("\n" + "=" * 70)
    print("3. CATEGORICAL ATTRIBUTE ENCODING")
    print("=" * 70)

    encoded_df = df.copy()

    # Ordinal feature: Education Level has natural progression
    education_order = ["High School", "Bachelor", "Master", "PhD"]
    ord_encoder = OrdinalEncoder(categories=[education_order])
    encoded_df["education_ordinal"] = ord_encoder.fit_transform(encoded_df[["education_level"]])

    print("[*] Ordinal Encoding for 'education_level':")
    for category, code in zip(education_order, range(len(education_order))):
        print(f"    {category:<12} -> {code}")

    # Nominal feature: Gender and Churn (One-Hot Encoding with drop_first=True for binary)
    print("\n[*] One-Hot Encoding for 'gender' and 'churn':")
    one_hot = pd.get_dummies(encoded_df[["gender", "churn"]], prefix=["gender", "churn"], drop_first=True, dtype=int)
    encoded_df = pd.concat([encoded_df, one_hot], axis=1)

    preview_cols = ["customer_id", "education_level", "education_ordinal", "gender", "gender_Male", "churn", "churn_Yes"]
    valid_preview = [c for c in preview_cols if c in encoded_df.columns]
    print(encoded_df[valid_preview].head(6).to_string(index=False))

    return encoded_df


def plot_scaling_and_binning_effects(df: pd.DataFrame, min_max_scaled: pd.DataFrame, std_scaled: pd.DataFrame, disc_df: pd.DataFrame) -> None:
    """Plot visualizations of transformations."""
    print("\n" + "=" * 70)
    print("4. GENERATING PREPROCESSING VISUALIZATIONS")
    print("=" * 70)

    sns.set_theme(style="whitegrid")

    # Figure 1: Comparison of scaling transformations on Monthly Charges
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    raw_col = df["monthly_charges"]
    mm_col = min_max_scaled["monthly_charges_minmax"]
    z_col = std_scaled["monthly_charges_zscore"]

    sns.histplot(raw_col, kde=True, ax=axes[0], color="#2ca02c", bins=10)
    axes[0].set_title("Original (Raw $)", fontweight="bold")

    sns.histplot(mm_col, kde=True, ax=axes[1], color="#1f77b4", bins=10)
    axes[1].set_title("Min-Max Normalized [0, 1]", fontweight="bold")

    sns.histplot(z_col, kde=True, ax=axes[2], color="#ff7f0e", bins=10)
    axes[2].set_title("Z-Score Standardized (μ=0, σ=1)", fontweight="bold")

    plt.suptitle("Impact of Scaling on Distribution (Shape Preserved, Range Transformed)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig1_path = OUTPUT_DIR / "03_scaling_comparison.png"
    plt.savefig(fig1_path, dpi=200)
    plt.close()
    print(f"  [+] Saved scaling comparison to: {fig1_path.name}")

    # Figure 2: Equal-Width vs Equal-Frequency Binning
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    disc_df["age_equal_width"].value_counts(sort=False).plot(kind="bar", ax=axes[0], color="#4c72b0")
    axes[0].set_title("Equal-Width Discretization (Intervals equal)", fontweight="bold")
    axes[0].tick_params(axis="x", rotation=25)

    disc_df["age_equal_freq"].value_counts(sort=False).plot(kind="bar", ax=axes[1], color="#55a868")
    axes[1].set_title("Equal-Frequency Discretization (Frequencies equal)", fontweight="bold")
    axes[1].tick_params(axis="x", rotation=25)

    plt.tight_layout()
    fig2_path = OUTPUT_DIR / "03_discretization_comparison.png"
    plt.savefig(fig2_path, dpi=200)
    plt.close()
    print(f"  [+] Saved discretization comparison to: {fig2_path.name}")


def build_interactive_dashboard(
    df: pd.DataFrame,
    min_max_scaled: pd.DataFrame,
    std_scaled: pd.DataFrame,
    disc_df: pd.DataFrame,
    open_browser: bool = True,
) -> Path:
    """Generate interactive Plotly dashboard for scaling, discretization, and feature engineering."""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import webbrowser
    except ImportError:
        print("[-] Plotly not available.")
        return None

    print("\n" + "=" * 70)
    print("5. GENERATING INTERACTIVE WEB DASHBOARD (PLOTLY)")
    print("=" * 70)

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "1. Effetto della Scalatura su Monthly Charges",
            "2. Discretizzazione Equal-Width vs Equal-Frequency",
            "3. Spazio delle Feature Normalizzate (Min-Max [0, 1])",
            "4. Distribuzione Standardizzata Z-Score (Media=0, Std=1)",
        ),
        specs=[
            [{"type": "xy"}, {"type": "xy"}],
            [{"type": "xy"}, {"type": "xy"}],
        ],
        vertical_spacing=0.14,
        horizontal_spacing=0.09,
    )

    # 1. Overlay histograms comparing Scaling on monthly_charges
    fig.add_trace(
        go.Histogram(
            x=min_max_scaled["monthly_charges_minmax"],
            name="Min-Max [0, 1]",
            opacity=0.6,
            marker_color="#1f77b4",
            nbinsx=10,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Histogram(
            x=std_scaled["monthly_charges_zscore"],
            name="Z-Score (Std)",
            opacity=0.5,
            marker_color="#ff7f0e",
            nbinsx=10,
        ),
        row=1,
        col=1,
    )
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(title_text="Valore Scalato", row=1, col=1)
    fig.update_yaxes(title_text="Frequenza", row=1, col=1)

    # 2. Equal-Width vs Equal-Frequency Bar Charts
    ew_counts = disc_df["age_equal_width"].value_counts(sort=False)
    ef_counts = disc_df["age_equal_freq"].value_counts(sort=False)

    fig.add_trace(
        go.Bar(
            x=[str(x) for x in ew_counts.index],
            y=ew_counts.values,
            name="Equal-Width",
            marker_color="#4c72b0",
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Bar(
            x=[str(x) for x in ef_counts.index],
            y=ef_counts.values,
            name="Equal-Frequency",
            marker_color="#55a868",
        ),
        row=1,
        col=2,
    )
    fig.update_xaxes(title_text="Bin Età", row=1, col=2)
    fig.update_yaxes(title_text="Numero Osservazioni", row=1, col=2)

    # 3. 2D Scatter in Min-Max space: Age vs Monthly Charges colored by Churn
    churn_colors = {"Yes": "#EF553B", "No": "#636EFA"}
    for ch in ["No", "Yes"]:
        mask = df["churn"] == ch
        fig.add_trace(
            go.Scatter(
                x=min_max_scaled.loc[mask, "age_minmax"],
                y=min_max_scaled.loc[mask, "monthly_charges_minmax"],
                mode="markers",
                name=f"Churn: {ch} (Norm)",
                marker=dict(size=9, color=churn_colors.get(ch), opacity=0.85),
                hovertext=[
                    f"Customer #{cid}<br>Age (norm): {a:.2f}<br>Monthly (norm): {mc:.2f}"
                    for cid, a, mc in zip(
                        df.loc[mask, "customer_id"],
                        min_max_scaled.loc[mask, "age_minmax"],
                        min_max_scaled.loc[mask, "monthly_charges_minmax"],
                    )
                ],
                hoverinfo="text",
                legendgroup=f"churn_{ch}",
            ),
            row=2,
            col=1,
        )
    fig.update_xaxes(title_text="Age (Min-Max Scaled [0, 1])", row=2, col=1)
    fig.update_yaxes(title_text="Monthly Charges (Min-Max Scaled [0, 1])", row=2, col=1)

    # 4. Box plots of all Z-Score features (demonstrating mean ~0 and std ~1)
    for col in std_scaled.columns:
        fig.add_trace(
            go.Box(
                y=std_scaled[col],
                name=col.replace("_zscore", ""),
                boxpoints="outliers",
                showlegend=False,
            ),
            row=2,
            col=2,
        )
    fig.update_yaxes(title_text="Z-Score", row=2, col=2)

    fig.update_layout(
        title_text="<b>Data Mining Playground — Trasformazioni, Normalizzazione & Discretizzazione</b>",
        title_font_size=15,
        template="plotly_white",
        height=860,
        margin=dict(l=40, r=40, t=80, b=40),
    )

    html_file = OUTPUT_DIR / "03_interactive_preprocessing.html"
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

    parser = argparse.ArgumentParser(description="Data Preprocessing & Transformations")
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

    df = load_dataset()
    min_max_df, std_df = demonstrate_scaling(df)
    disc_df = demonstrate_discretization(df)
    encoded_df = demonstrate_categorical_encoding(df)

    # 1. Genera immagini statiche PNG
    plot_scaling_and_binning_effects(df, min_max_df, std_df, disc_df)

    # 2. Genera dashboard interattiva HTML (Plotly)
    if not args.static_only:
        build_interactive_dashboard(df, min_max_df, std_df, disc_df, open_browser=not args.no_browser)

    processed_csv = SCRIPT_DIR / "datasets" / "customer_churn_preprocessed.csv"
    encoded_df.to_csv(processed_csv, index=False)
    print(f"\n[+] Saved fully preprocessed dataset to: {processed_csv.name}")

    print("=" * 70)
    print("[*] Data Preprocessing pipeline complete.")
    print("    - Immagini statiche salvate in: playground/output/*.png")
    print("    - Dashboard interattiva salvata in: playground/output/03_interactive_preprocessing.html")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
