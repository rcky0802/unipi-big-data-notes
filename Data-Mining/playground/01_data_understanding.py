"""Data Mining Playground - Chapter 2: Data Understanding & Exploration.

This script implements concepts from Chapter 2 ("Data Understanding"):
1. Dataset inspection (attributes, types, scales of measurement).
2. Univariate descriptive statistics:
   - Measures of central tendency: Mean, Median, Mode.
   - Measures of dispersion: Range, Variance, Standard Deviation, IQR.
   - Five-number summary (Min, Q1, Median, Q3, Max).
   - Distribution shape: Skewness (asimmetria).
3. Multivariate statistics:
   - Sample Covariance matrix.
   - Pearson Linear Correlation coefficient matrix.
   - Spearman Rank Correlation coefficient matrix.
4. Statistical Visualization:
   - Histograms & KDE distributions.
   - Boxplots with Tukey whiskers.
   - Correlation heatmaps.
   - Scatter plots / Pairwise relationships.

All generated plots are saved automatically to `playground/output/`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Verify dependencies before importing
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from scipy import stats
except ImportError as err:
    print(f"[-] Missing required dependency: {err.name}")
    print("[-] Please install required packages first:")
    print("    pip install -r requirements.txt")
    sys.exit(1)

# Ensure script runs from anywhere and finds datasets/output folders
SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_PATH = SCRIPT_DIR / "datasets" / "iris.csv"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    """Load the Iris dataset from CSV, or fall back to sklearn."""
    if DATASET_PATH.exists():
        print(f"[*] Loading dataset from local CSV: {DATASET_PATH.name}")
        df = pd.read_csv(DATASET_PATH)
    else:
        print("[*] Local dataset not found; loading Iris from sklearn.datasets...")
        from sklearn.datasets import load_iris

        iris = load_iris(as_frame=True)
        df = iris.frame
        df.rename(
            columns={
                "sepal length (cm)": "sepal_length",
                "sepal width (cm)": "sepal_width",
                "petal length (cm)": "petal_length",
                "petal width (cm)": "petal_width",
                "target": "species",
            },
            inplace=True,
        )
        species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}
        df["species"] = df["species"].map(species_map)
    return df


def inspect_dataset(df: pd.DataFrame) -> None:
    """Print structural dataset properties (shape, columns, dtypes)."""
    print("\n" + "=" * 70)
    print("1. DATASET OVERVIEW & METADATA")
    print("=" * 70)
    print(f"Shape : {df.shape[0]} rows x {df.shape[1]} columns")
    print("\nAttribute Types & Scales:")
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]) or isinstance(dtype, pd.CategoricalDtype):
            scale = "Nominal (Categorical)"
        else:
            scale = "Ratio (Continuous Numeric)"
        print(f"  - {col:<15} : dtype={str(dtype):<10} | Scale: {scale}")

    print("\nFirst 5 Records:")
    print(df.head().to_string(index=False))


def compute_univariate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute central tendency, dispersion, five-number summary, and skewness."""
    print("\n" + "=" * 70)
    print("2. UNIVARIATE DESCRIPTIVE STATISTICS")
    print("=" * 70)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    stats_records = []

    for col in numeric_cols:
        series = df[col].dropna()
        n = len(series)
        mean_val = series.mean()
        median_val = series.median()
        # Mode might have multiple values; take the first
        mode_val = series.mode().iloc[0] if not series.mode().empty else np.nan
        std_val = series.std(ddof=1)
        var_val = series.var(ddof=1)
        min_val = series.min()
        q1_val = series.quantile(0.25)
        q3_val = series.quantile(0.75)
        max_val = series.max()
        iqr_val = q3_val - q1_val
        range_val = max_val - min_val
        skewness_val = series.skew()

        stats_records.append(
            {
                "Feature": col,
                "Count": n,
                "Mean": round(mean_val, 3),
                "Median": round(median_val, 3),
                "Mode": round(mode_val, 3),
                "StdDev": round(std_val, 3),
                "Variance": round(var_val, 3),
                "Min": round(min_val, 3),
                "Q1 (25%)": round(q1_val, 3),
                "Q3 (75%)": round(q3_val, 3),
                "Max": round(max_val, 3),
                "IQR": round(iqr_val, 3),
                "Range": round(range_val, 3),
                "Skewness": round(skewness_val, 3),
            }
        )

    summary_df = pd.DataFrame(stats_records).set_index("Feature")
    print(summary_df.to_string())

    print("\nInterpretation of Skewness:")
    for col in numeric_cols:
        sk = summary_df.loc[col, "Skewness"]
        if abs(sk) < 0.2:
            direction = "Approximately Symmetric"
        elif sk > 0:
            direction = "Right-skewed (positive asymmetry, tail to the right)"
        else:
            direction = "Left-skewed (negative asymmetry, tail to the left)"
        print(f"  - {col:<15}: skew = {sk:+0.3f} -> {direction}")

    return summary_df


def compute_multivariate_statistics(df: pd.DataFrame) -> None:
    """Compute Covariance, Pearson correlation, and Spearman rank correlation."""
    print("\n" + "=" * 70)
    print("3. MULTIVARIATE STATISTICS: COVARIANCE & CORRELATION")
    print("=" * 70)

    numeric_df = df.select_dtypes(include=[np.number])

    print("[*] Sample Covariance Matrix (S_ij = (1/(n-1)) * sum((x_k - x_bar)(y_k - y_bar))):")
    cov_matrix = numeric_df.cov()
    print(cov_matrix.round(4).to_string())

    print("\n[*] Pearson Linear Correlation Matrix (r_xy = S_xy / (S_x * S_y)):")
    pearson_matrix = numeric_df.corr(method="pearson")
    print(pearson_matrix.round(4).to_string())

    print("\n[*] Spearman Rank Correlation Matrix (rho_s):")
    spearman_matrix = numeric_df.corr(method="spearman")
    print(spearman_matrix.round(4).to_string())


def plot_exploratory_visualizations(df: pd.DataFrame) -> None:
    """Generate and save statistical figures (histograms, boxplots, pairplot, heatmaps)."""
    print("\n" + "=" * 70)
    print("4. GENERATING STATISTICAL VISUALIZATIONS")
    print("=" * 70)
    sns.set_theme(style="whitegrid", palette="muted")
    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)

    # 1. Univariate Distributions (Histograms + KDE)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        sns.histplot(data=df, x=col, kde=True, ax=axes[i], color="#1f77b4", bins=12)
        axes[i].set_title(f"Distribution of {col}", fontsize=12, fontweight="bold")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frequency")
    plt.tight_layout()
    hist_path = OUTPUT_DIR / "01_univariate_histograms.png"
    plt.savefig(hist_path, dpi=200)
    plt.close()
    print(f"  [+] Saved histograms to: {hist_path.name}")

    # 2. Box Plots (Univariate & Grouped by Species)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        sns.boxplot(data=df, x="species", y=col, hue="species", ax=axes[i], palette="Set2", legend=False)
        axes[i].set_title(f"{col} by Species (Tukey Boxplot)", fontsize=11, fontweight="bold")
    plt.tight_layout()
    box_path = OUTPUT_DIR / "01_boxplots_by_species.png"
    plt.savefig(box_path, dpi=200)
    plt.close()
    print(f"  [+] Saved grouped boxplots to: {box_path.name}")

    # 3. Correlation Heatmaps (Pearson vs Spearman)
    numeric_df = df[numeric_cols]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    sns.heatmap(
        numeric_df.corr(method="pearson"),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        ax=ax1,
        square=True,
    )
    ax1.set_title("Pearson Linear Correlation (r)", fontsize=12, fontweight="bold")

    sns.heatmap(
        numeric_df.corr(method="spearman"),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        ax=ax2,
        square=True,
    )
    ax2.set_title("Spearman Rank Correlation (rho)", fontsize=12, fontweight="bold")
    plt.tight_layout()
    corr_path = OUTPUT_DIR / "01_correlation_heatmaps.png"
    plt.savefig(corr_path, dpi=200)
    plt.close()
    print(f"  [+] Saved correlation heatmaps to: {corr_path.name}")

    # 4. Pairplot (Bivariate Scatter Matrix)
    pairplot = sns.pairplot(df, hue="species", markers=["o", "s", "D"], palette="Dark2")
    pairplot.fig.subplots_adjust(top=0.94)
    pairplot.fig.suptitle("Iris Pairplot (Scatter Matrix by Class)", fontsize=13, fontweight="bold")
    pairplot_path = OUTPUT_DIR / "01_pairplot_scatter_matrix.png"
    pairplot.savefig(pairplot_path, dpi=200)
    plt.close()
    print(f"  [+] Saved pairplot to: {pairplot_path.name}")

    print(f"\n[+] All visual artifacts successfully stored in:\n    {OUTPUT_DIR}")


def build_interactive_dashboard(df: pd.DataFrame, open_browser: bool = True) -> Path:
    """Build a rich, multi-view interactive HTML dashboard using Plotly and open it."""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import webbrowser
    except ImportError:
        print("[-] Plotly not available. Install it with: pip install plotly")
        return None

    print("\n" + "=" * 70)
    print("5. GENERATING INTERACTIVE WEB DASHBOARD (PLOTLY)")
    print("=" * 70)

    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "1. Distribuzione & Box Plot (Hover per 5-Number Summary & Punti)",
            "2. Matrice di Correlazione Lineare di Pearson",
            "3. Scatter Plot Bivariato (Petal Length vs Petal Width)",
            "4. Scatter Plot 3D con Rotazione 360° (Sepal L., Petal L., Petal W.)",
        ),
        specs=[
            [{"type": "xy"}, {"type": "heatmap"}],
            [{"type": "xy"}, {"type": "scene"}],
        ],
        vertical_spacing=0.14,
        horizontal_spacing=0.09,
    )

    species_list = df["species"].unique()
    palette = {"setosa": "#636EFA", "versicolor": "#EF553B", "virginica": "#00CC96"}

    # 1. Box Plot with all points jittered
    for sp in species_list:
        sub = df[df["species"] == sp]
        fig.add_trace(
            go.Box(
                y=sub["petal_length"],
                name=f"{sp}",
                boxpoints="all",
                jitter=0.25,
                pointpos=-1.6,
                marker=dict(color=palette.get(sp, "#1f77b4")),
                showlegend=True,
                legendgroup=sp,
            ),
            row=1,
            col=1,
        )
    fig.update_xaxes(title_text="Specie", row=1, col=1)
    fig.update_yaxes(title_text="Petal Length (cm)", row=1, col=1)

    # 2. Correlation Heatmap
    corr = df[numeric_cols].corr(method="pearson").round(3)
    fig.add_trace(
        go.Heatmap(
            z=corr.values,
            x=numeric_cols,
            y=numeric_cols,
            colorscale="Blues",
            zmin=-1,
            zmax=1,
            text=corr.values,
            texttemplate="%{text:.2f}",
            textfont={"size": 11},
            hoverinfo="x+y+z",
            showscale=False,
        ),
        row=1,
        col=2,
    )

    # 3. 2D Scatter Plot
    for sp in species_list:
        sub = df[df["species"] == sp]
        fig.add_trace(
            go.Scatter(
                x=sub["petal_length"],
                y=sub["petal_width"],
                mode="markers",
                name=f"{sp}",
                marker=dict(size=9, color=palette.get(sp), opacity=0.85),
                hovertext=[
                    f"Specie: {sp}<br>Sepal Length: {sl} cm<br>Sepal Width: {sw} cm"
                    for sl, sw in zip(sub["sepal_length"], sub["sepal_width"])
                ],
                hoverinfo="text+x+y",
                showlegend=False,
                legendgroup=sp,
            ),
            row=2,
            col=1,
        )
    fig.update_xaxes(title_text="Petal Length (cm)", row=2, col=1)
    fig.update_yaxes(title_text="Petal Width (cm)", row=2, col=1)

    # 4. 3D Scatter Plot (Interactive 360-degree rotation)
    for sp in species_list:
        sub = df[df["species"] == sp]
        fig.add_trace(
            go.Scatter3d(
                x=sub["sepal_length"],
                y=sub["petal_length"],
                z=sub["petal_width"],
                mode="markers",
                name=f"{sp}",
                marker=dict(size=4.5, color=palette.get(sp), opacity=0.9),
                hovertext=[f"Specie: {sp}<br>Sepal W: {sw} cm" for sw in sub["sepal_width"]],
                hoverinfo="text+x+y+z",
                showlegend=False,
                legendgroup=sp,
            ),
            row=2,
            col=2,
        )

    fig.update_layout(
        title_text="<b>Data Mining Playground — Dashboard Interattiva (Capitolo 2: Data Understanding)</b>",
        title_font_size=15,
        template="plotly_white",
        height=860,
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(title_text="Specie (clicca per filtrare/isolare)"),
    )

    html_file = OUTPUT_DIR / "01_interactive_dashboard.html"
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

    parser = argparse.ArgumentParser(description="Chapter 2: Data Understanding & Statistical Exploration")
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
    inspect_dataset(df)
    compute_univariate_statistics(df)
    compute_multivariate_statistics(df)

    # 1. Genera e salva tutte le immagini statiche PNG
    plot_exploratory_visualizations(df)

    # 2. Genera la visualizzazione interattiva a video (Plotly)
    if not args.static_only:
        build_interactive_dashboard(df, open_browser=not args.no_browser)

    print("\n" + "=" * 70)
    print("[*] Chapter 2 Data Understanding run complete.")
    print("    - Immagini statiche salvate in: playground/output/*.png")
    print("    - Dashboard interattiva salvata in: playground/output/01_interactive_dashboard.html")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
