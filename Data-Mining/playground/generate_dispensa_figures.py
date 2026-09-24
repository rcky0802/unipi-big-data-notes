"""Script to generate realistic, high-quality vector PDF figures for the Data Mining notes.

Generates bilingual figures:
- `Data-Mining/assets/figures/it/` for Italian notes (main_it.tex)
- `Data-Mining/assets/figures/en/` for English notes (main_en.tex)

Figures produced per language:
1. `iris_conditional_boxplot.pdf`: Conditional boxplot of Petal Length by species with true quartiles & jittered points.
2. `iris_scatterplot_real.pdf`: Real 2D scatter plot (Petal Length vs Petal Width) of all 150 instances with annotations.
3. `iris_splom_real.pdf`: Real 4x4 Scatter Plot Matrix (SPLOM) with true KDE diagonals.
4. `iris_parallel_coordinates.pdf`: Real Parallel Coordinates of all 150 instances normalized [0, 1].
5. `iris_radar_plot.pdf`: Real Radar plot comparing normalized mean profiles across the 3 species.
6. `iris_correlation_heatmaps.pdf`: Real Pearson and Spearman correlation heatmaps.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_PATH = SCRIPT_DIR / "datasets" / "iris.csv"
ASSETS_DIR = SCRIPT_DIR.parent / "assets" / "figures"

# Academic styling for LaTeX integration
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "figure.titlesize": 13,
        "figure.autolayout": False,
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "grid.color": "#e0e0e0",
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
    }
)

PALETTE = {
    "setosa": "#1F77B4",      # Blue
    "versicolor": "#FF7F0E",  # Orange
    "virginica": "#2CA02C",   # Green
}

STRINGS: Dict[str, Dict[str, str]] = {
    "it": {
        "species_label": "Specie",
        "median_fmt": "Mediana: {med:.2f} cm",
        "samples_label": "campioni",
        "atypical_point": "Punto atipico per Versicolor\n(PL=4.8, PW=1.8)",
        "setosa_separation": "Separazione netta\nSetosa (PL < 2.5 cm)",
        "legend_species": "Specie",
        "normalized_value": "Valore Normalizzato [0, 1]",
        "mean_prefix": "Media",
        "pearson_title": "Correlazione Lineare di Pearson ($r$)",
        "spearman_title": "Correlazione di Rango di Spearman ($\\rho_s$)",
        "cbar_label": "Coefficiente",
        "sepal_length": "Sepal Length",
        "sepal_width": "Sepal Width",
        "petal_length": "Petal Length",
        "petal_width": "Petal Width",
        "sepal_l_short": "Sepal L.",
        "sepal_w_short": "Sepal W.",
        "petal_l_short": "Petal L.",
        "petal_w_short": "Petal W.",
        # Chapter 3: Data Preparation figures
        "precip_title_monthly": "Deviazione Standard Precipitazioni Mensili",
        "precip_title_yearly": "Deviazione Standard Precipitazioni Annuali",
        "precip_xlabel_monthly": "Std Dev Precipitazioni Mensili (cm)",
        "precip_xlabel_yearly": "Std Dev Precipitazioni Annuali (cm)",
        "precip_ylabel": "Numero di Località Terrestri",
        "pca_scree_title": "Varianza Spiegata per Componente Principale (Scree Plot)",
        "pca_scree_xlabel": "Componente Principale",
        "pca_scree_ylabel": "Varianza Spiegata (%)",
        "pca_cum_label": "Varianza Cumulata",
        "pca_proj_title": "Proiezione PCA 2D (Iris Dataset)",
        "pca_proj_xlabel": "Prima Componente Principale (PC1 - {v1:.1f}%)",
        "pca_proj_ylabel": "Seconda Componente Principale (PC2 - {v2:.1f}%)",
        # Sampling Tradeoff figure
        "sampling_tradeoff_title": "Trade-off sulla Dimensione del Campionamento",
        "sampling_pop_title": "Popolazione Originaria ($N = 8000$)",
        "sampling_small_title": "Campione Sotto-dimensionato ($n = 500$)",
        "sampling_rep_title": "Campione Rappresentativo ($n = 2000$)",
        "sampling_small_note": "Perdita di continuità geometrica\ne cluster disgregati",
        "sampling_rep_note": "Silhouette e topologia\npreservate con tempi ridotti",
    },
    "en": {
        "species_label": "Species",
        "median_fmt": "Median: {med:.2f} cm",
        "samples_label": "samples",
        "atypical_point": "Atypical point for Versicolor\n(PL=4.8, PW=1.8)",
        "setosa_separation": "Clear separation\nSetosa (PL < 2.5 cm)",
        "legend_species": "Species",
        "normalized_value": "Normalized Value [0, 1]",
        "mean_prefix": "Mean",
        "pearson_title": "Pearson Linear Correlation ($r$)",
        "spearman_title": "Spearman Rank Correlation ($\\rho_s$)",
        "cbar_label": "Coefficient",
        "sepal_length": "Sepal Length",
        "sepal_width": "Sepal Width",
        "petal_length": "Petal Length",
        "petal_width": "Petal Width",
        "sepal_l_short": "Sepal L.",
        "sepal_w_short": "Sepal W.",
        "petal_l_short": "Petal L.",
        "petal_w_short": "Petal W.",
        # Chapter 3: Data Preparation figures
        "precip_title_monthly": "Standard Deviation of Monthly Precipitation",
        "precip_title_yearly": "Standard Deviation of Yearly Precipitation",
        "precip_xlabel_monthly": "Monthly Precipitation Std Dev (cm)",
        "precip_xlabel_yearly": "Yearly Precipitation Std Dev (cm)",
        "precip_ylabel": "Number of Land Locations",
        "pca_scree_title": "Explained Variance by Principal Component (Scree Plot)",
        "pca_scree_xlabel": "Principal Component",
        "pca_scree_ylabel": "Explained Variance (%)",
        "pca_cum_label": "Cumulative Variance",
        "pca_proj_title": "2D PCA Projection (Iris Dataset)",
        "pca_proj_xlabel": "First Principal Component (PC1 - {v1:.1f}%)",
        "pca_proj_ylabel": "Second Principal Component (PC2 - {v2:.1f}%)",
        # Sampling Tradeoff figure
        "sampling_tradeoff_title": "Sample Size Trade-off in Data Reduction",
        "sampling_pop_title": "Original Population ($N = 8000$)",
        "sampling_small_title": "Undersized Sample ($n = 500$)",
        "sampling_rep_title": "Representative Sample ($n = 2000$)",
        "sampling_small_note": "Loss of geometric continuity\nand fragmented clusters",
        "sampling_rep_note": "Contours and topology\npreserved with low cost",
    },
}


def load_data() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Missing {DATASET_PATH}")
    return pd.read_csv(DATASET_PATH)


def generate_conditional_boxplot(df: pd.DataFrame, lang: str, out_dir: Path) -> None:
    """Figure 1: Real Conditional Box Plot of Petal Length by Species."""
    t = STRINGS[lang]
    fig, ax = plt.subplots(figsize=(7.5, 3.8))

    species_order = ["setosa", "versicolor", "virginica"]
    species_labels = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]

    sns.boxplot(
        data=df,
        y="species",
        x="petal_length",
        hue="species",
        legend=False,
        order=species_order,
        palette=PALETTE,
        width=0.48,
        ax=ax,
        fliersize=4.5,
        flierprops=dict(marker="o", markerfacecolor="red", markeredgecolor="black", alpha=0.8),
        boxprops=dict(alpha=0.85, edgecolor="#222222", linewidth=1.1),
        whiskerprops=dict(color="#222222", linewidth=1.1),
        capprops=dict(color="#222222", linewidth=1.1),
        medianprops=dict(color="black", linewidth=2.0),
    )

    sns.stripplot(
        data=df,
        y="species",
        x="petal_length",
        order=species_order,
        color="black",
        alpha=0.35,
        size=4,
        jitter=0.18,
        ax=ax,
    )

    medians = df.groupby("species")["petal_length"].median()
    for i, sp in enumerate(species_order):
        med = medians[sp]
        ax.text(
            med,
            i - 0.32,
            t["median_fmt"].format(med=med),
            horizontalalignment="center",
            fontsize=8.5,
            fontweight="bold",
            color="#222222",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor="#cccccc"),
        )

    ax.set_yticks(range(len(species_labels)))
    ax.set_yticklabels(species_labels, fontweight="bold")
    ax.set_xlabel("Petal Length (cm)", fontweight="bold")
    ax.set_ylabel(t["species_label"], fontweight="bold")
    ax.set_xlim(0.5, 7.5)
    ax.grid(axis="x", linestyle="--", alpha=0.7)

    out_path = out_dir / "iris_conditional_boxplot.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_real_scatterplot(df: pd.DataFrame, lang: str, out_dir: Path) -> None:
    """Figure 2: Real 2D Scatter Plot of Petal Length vs Petal Width."""
    t = STRINGS[lang]
    fig, ax = plt.subplots(figsize=(7.5, 5.0))

    markers = {"setosa": "o", "versicolor": "s", "virginica": "D"}
    species_labels = {
        "setosa": f"Iris-setosa (50 {t['samples_label']})",
        "versicolor": f"Iris-versicolor (50 {t['samples_label']})",
        "virginica": f"Iris-virginica (50 {t['samples_label']})",
    }

    for sp in ["setosa", "versicolor", "virginica"]:
        sub = df[df["species"] == sp]
        ax.scatter(
            sub["petal_length"],
            sub["petal_width"],
            label=species_labels[sp],
            color=PALETTE[sp],
            marker=markers[sp],
            s=48,
            alpha=0.85,
            edgecolors="black",
            linewidth=0.6,
        )

    atypical_versicolor = df[(df["species"] == "versicolor") & (df["petal_width"] >= 1.7)].iloc[0]
    ax.annotate(
        t["atypical_point"],
        xy=(atypical_versicolor["petal_length"], atypical_versicolor["petal_width"]),
        xytext=(3.0, 2.15),
        arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.2),
        fontsize=8.5,
        fontweight="bold",
        color="#c0392b",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fdf2e9", edgecolor="#e67e22"),
    )

    ax.axvline(x=2.5, color="#7f8c8d", linestyle=":", linewidth=1.3)
    ax.text(2.35, 1.2, t["setosa_separation"], rotation=90, fontsize=8, color="#555555", va="center")

    ax.set_xlabel("Petal Length (cm)", fontweight="bold")
    ax.set_ylabel("Petal Width (cm)", fontweight="bold")
    ax.set_xlim(0.5, 7.5)
    ax.set_ylim(-0.1, 2.8)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="lower right", framealpha=0.92, edgecolor="#cccccc")

    out_path = out_dir / "iris_scatterplot_real.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_real_splom(df: pd.DataFrame, lang: str, out_dir: Path) -> None:
    """Figure 3: Real 4x4 Scatter Plot Matrix (SPLOM) with true KDE diagonals."""
    t = STRINGS[lang]
    feature_labels = {
        "sepal_length": f"{t['sepal_l_short']} (cm)",
        "sepal_width": f"{t['sepal_w_short']} (cm)",
        "petal_length": f"{t['petal_l_short']} (cm)",
        "petal_width": f"{t['petal_w_short']} (cm)",
    }
    df_renamed = df.rename(columns=feature_labels)

    g = sns.pairplot(
        df_renamed,
        hue="species",
        palette=PALETTE,
        markers=["o", "s", "D"],
        diag_kind="kde",
        plot_kws={"alpha": 0.75, "s": 26, "edgecolor": "none"},
        diag_kws={"fill": True, "alpha": 0.35, "linewidth": 1.2},
        height=1.85,
        aspect=1.0,
    )
    g._legend.set_title(t["legend_species"])
    g._legend.set_bbox_to_anchor((0.98, 0.55))

    out_path = out_dir / "iris_splom_real.pdf"
    g.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_parallel_coordinates(df: pd.DataFrame, lang: str, out_dir: Path) -> None:
    """Figure 4: Real Parallel Coordinates for all 150 observations."""
    t = STRINGS[lang]
    fig, ax = plt.subplots(figsize=(8.0, 4.4))

    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    feature_names = [t["sepal_length"], t["sepal_width"], t["petal_length"], t["petal_width"]]

    scaler = MinMaxScaler()
    df_norm = df.copy()
    df_norm[features] = scaler.fit_transform(df[features])

    x_coords = np.arange(len(features))

    for x in x_coords:
        ax.axvline(x=x, color="#666666", linestyle="-", linewidth=1.2)

    for sp in ["setosa", "versicolor", "virginica"]:
        sub = df_norm[df_norm["species"] == sp]
        for _, row in sub.iterrows():
            y_vals = [row[f] for f in features]
            ax.plot(x_coords, y_vals, color=PALETTE[sp], alpha=0.35, linewidth=1.1)

    for sp, label in [("setosa", "Iris-setosa"), ("versicolor", "Iris-versicolor"), ("virginica", "Iris-virginica")]:
        sub = df_norm[df_norm["species"] == sp]
        mean_vals = [sub[f].mean() for f in features]
        ax.plot(x_coords, mean_vals, color=PALETTE[sp], linewidth=2.8, marker="o", markersize=6, label=f"{t['mean_prefix']} {label}")

    ax.set_xticks(x_coords)
    ax.set_xticklabels(feature_names, fontweight="bold", fontsize=10.5)
    ax.set_ylabel(t["normalized_value"], fontweight="bold")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    ax.legend(loc="upper right", framealpha=0.92, edgecolor="#cccccc")

    out_path = out_dir / "iris_parallel_coordinates.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_radar_plot(df: pd.DataFrame, lang: str, out_dir: Path) -> None:
    """Figure 5: Real Radar Plot comparing mean normalized profiles."""
    t = STRINGS[lang]
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    feature_names = [f"{t['sepal_l_short']}\nLength", f"{t['sepal_w_short']}\nWidth", f"{t['petal_l_short']}\nLength", f"{t['petal_w_short']}\nWidth"]

    scaler = MinMaxScaler()
    df_norm = df.copy()
    df_norm[features] = scaler.fit_transform(df[features])

    mean_profiles = df_norm.groupby("species")[features].mean()

    num_vars = len(features)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
    species_labels = {"setosa": "Iris-setosa", "versicolor": "Iris-versicolor", "virginica": "Iris-virginica"}

    for sp in ["setosa", "versicolor", "virginica"]:
        values = mean_profiles.loc[sp].tolist()
        values += values[:1]
        ax.plot(angles, values, color=PALETTE[sp], linewidth=2.2, label=species_labels[sp])
        ax.fill(angles, values, color=PALETTE[sp], alpha=0.18)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(feature_names, fontweight="bold", fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8, color="#555555")
    ax.grid(color="#cccccc", linestyle="--")
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), framealpha=0.92, edgecolor="#cccccc")

    out_path = out_dir / "iris_radar_plot.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_correlation_heatmaps(df: pd.DataFrame, lang: str, out_dir: Path) -> None:
    """Figure 6: Real Pearson and Spearman correlation heatmaps."""
    t = STRINGS[lang]
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    display_names = [t["sepal_l_short"], t["sepal_w_short"], t["petal_l_short"], t["petal_w_short"]]

    data = df[features].copy()
    data.columns = display_names

    pearson_corr = data.corr(method="pearson")
    spearman_corr = data.corr(method="spearman")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.8))

    # Pearson
    sns.heatmap(
        pearson_corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        cbar=False,
        square=True,
        ax=ax1,
        annot_kws={"size": 9.5, "weight": "bold"},
        linewidths=0.5,
        linecolor="white",
    )
    ax1.set_title(t["pearson_title"], fontweight="bold", fontsize=11)

    # Spearman
    sns.heatmap(
        spearman_corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        cbar=True,
        cbar_kws={"shrink": 0.82, "label": t["cbar_label"]},
        square=True,
        ax=ax2,
        annot_kws={"size": 9.5, "weight": "bold"},
        linewidths=0.5,
        linecolor="white",
    )
    ax2.set_title(t["spearman_title"], fontweight="bold", fontsize=11)

    plt.tight_layout()
    out_path = out_dir / "iris_correlation_heatmaps.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_precipitation_aggregation(lang: str, out_dir: Path) -> None:
    """Figure 7: Aggregation effect on variability (Precipitation in Australia)."""
    t = STRINGS[lang]
    rng = np.random.RandomState(42)

    # Simulate realistic monthly and yearly precipitation std dev across locations (cm)
    # Monthly precipitation std dev has higher spread and values
    monthly_std = rng.gamma(shape=2.5, scale=1.6, size=1200) + 0.5
    # Yearly aggregated precipitation std dev is compressed towards zero with much lower variability
    yearly_std = rng.gamma(shape=1.2, scale=0.7, size=1200) * 0.45 + 0.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)

    # Monthly Histogram
    ax1.hist(monthly_std, bins=50, color="#1F77B4", edgecolor="#114477", alpha=0.85)
    ax1.set_title(t["precip_title_monthly"], fontweight="bold", fontsize=11)
    ax1.set_xlabel(t["precip_xlabel_monthly"], fontsize=10)
    ax1.set_ylabel(t["precip_ylabel"], fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.set_xlim(0, 18)

    # Yearly Histogram
    ax2.hist(yearly_std, bins=50, color="#FF7F0E", edgecolor="#AA5500", alpha=0.85)
    ax2.set_title(t["precip_title_yearly"], fontweight="bold", fontsize=11)
    ax2.set_xlabel(t["precip_xlabel_yearly"], fontsize=10)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.set_xlim(0, 18)

    plt.tight_layout()
    out_path = out_dir / "precipitation_aggregation.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_pca_scree_plot(df: pd.DataFrame, lang: str, out_dir: Path) -> None:
    """Figure 8: PCA Scree plot showing individual and cumulative explained variance."""
    t = STRINGS[lang]
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    x = StandardScaler().fit_transform(df[features])

    pca = PCA()
    pca.fit(x)
    var_exp = pca.explained_variance_ratio_ * 100
    cum_var = np.cumsum(var_exp)

    fig, ax = plt.subplots(figsize=(7.5, 4.0))

    components = [f"PC{i+1}" for i in range(len(var_exp))]
    bars = ax.bar(components, var_exp, color="#2B5B84", edgecolor="#183652", width=0.55, alpha=0.85, label=t["pca_scree_ylabel"])
    line = ax.plot(components, cum_var, color="#D95F02", marker="o", linewidth=2.2, markersize=6, label=t["pca_cum_label"])

    for bar, pct in zip(bars, var_exp):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 1.2, f"{pct:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    for i, cum in enumerate(cum_var):
        ax.text(i, cum + 2.0, f"{cum:.1f}%", ha="center", va="bottom", fontsize=9, color="#D95F02", fontweight="bold")

    ax.set_title(t["pca_scree_title"], fontweight="bold", fontsize=12)
    ax.set_xlabel(t["pca_scree_xlabel"], fontsize=10.5)
    ax.set_ylabel(t["pca_scree_ylabel"], fontsize=10.5)
    ax.set_ylim(0, 110)
    ax.legend(loc="center right", frameon=True)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    out_path = out_dir / "pca_scree_plot.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_pca_2d_projection(df: pd.DataFrame, lang: str, out_dir: Path) -> None:
    """Figure 9: Real 2D projection on first 2 Principal Components."""
    t = STRINGS[lang]
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    x = StandardScaler().fit_transform(df[features])

    pca = PCA(n_components=2)
    coords = pca.fit_transform(x)
    var_exp = pca.explained_variance_ratio_ * 100

    proj_df = pd.DataFrame(coords, columns=["PC1", "PC2"])
    proj_df["species"] = df["species"]

    fig, ax = plt.subplots(figsize=(7.8, 5.0))

    markers = {"setosa": "o", "versicolor": "s", "virginica": "^"}
    for sp in ["setosa", "versicolor", "virginica"]:
        sub = proj_df[proj_df["species"] == sp]
        ax.scatter(
            sub["PC1"],
            sub["PC2"],
            label=sp.capitalize(),
            color=PALETTE[sp],
            marker=markers[sp],
            s=50,
            alpha=0.85,
            edgecolors="black",
            linewidth=0.5,
        )

    ax.set_title(t["pca_proj_title"], fontweight="bold", fontsize=12)
    ax.set_xlabel(t["pca_proj_xlabel"].format(v1=var_exp[0]), fontsize=10.5)
    ax.set_ylabel(t["pca_proj_ylabel"].format(v2=var_exp[1]), fontsize=10.5)
    ax.axhline(0, color="gray", linestyle=":", linewidth=0.8)
    ax.axvline(0, color="gray", linestyle=":", linewidth=0.8)
    ax.legend(title=t["legend_species"], frameon=True, loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    out_path = out_dir / "pca_2d_projection.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_sampling_tradeoff(lang: str, out_dir: Path) -> None:
    """Figure 3.x: Sample Size Trade-off (8000 vs 500 vs 2000 points).
    
    Demonstrates:
    - Left: Full population of 8000 points with two intertwined spiral/crescent clusters and a dense core.
    - Center: Undersized sample (500 points) where continuous geometric structures break up and become sparse.
    - Right: Representative sample (2000 points) where silhouettes and cluster topologies are clearly preserved.
    """
    t = STRINGS[lang]
    rng = np.random.default_rng(42)
    N = 8000

    # Cluster 1: Outer crescent / arc (3600 points)
    theta1 = rng.uniform(0, np.pi * 1.3, 3600)
    r1 = 2.8 + rng.normal(0, 0.22, 3600)
    x1 = r1 * np.cos(theta1)
    y1 = r1 * np.sin(theta1)

    # Cluster 2: Inner crescent / arc (3400 points)
    theta2 = rng.uniform(np.pi * 0.7, np.pi * 2.0, 3400)
    r2 = 1.4 + rng.normal(0, 0.18, 3400)
    x2 = r2 * np.cos(theta2) + 0.6
    y2 = r2 * np.sin(theta2) - 0.3

    # Cluster 3: Dense central minor cluster (1000 points)
    x3 = rng.normal(-0.2, 0.28, 1000)
    y3 = rng.normal(0.4, 0.28, 1000)

    X_pop = np.vstack([
        np.column_stack([x1, y1]),
        np.column_stack([x2, y2]),
        np.column_stack([x3, y3])
    ])

    # Subsamples
    idx_500 = rng.choice(N, size=500, replace=False)
    idx_2000 = rng.choice(N, size=2000, replace=False)

    X_500 = X_pop[idx_500]
    X_2000 = X_pop[idx_2000]

    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.2), sharex=True, sharey=True)

    # Subplot 1: Population N=8000
    axes[0].scatter(X_pop[:, 0], X_pop[:, 1], s=3.0, alpha=0.35, color="#1f77b4", edgecolors="none")
    axes[0].set_title(t["sampling_pop_title"], fontweight="bold", fontsize=11.5, pad=10)
    axes[0].text(0.05, 0.06, "$N = 8000$\nCost: $100\\%$", transform=axes[0].transAxes,
                 fontsize=9.5, bbox=dict(boxstyle="round,pad=0.3", facecolor="#f0f4f8", edgecolor="#b0c4de", alpha=0.9))

    # Subplot 2: Undersized n=500
    axes[1].scatter(X_500[:, 0], X_500[:, 1], s=10.0, alpha=0.65, color="#d9534f", edgecolors="none")
    axes[1].set_title(t["sampling_small_title"], fontweight="bold", fontsize=11.5, pad=10)
    axes[1].text(0.05, 0.06, f"$n = 500$ (6.25%)\n{t['sampling_small_note']}", transform=axes[1].transAxes,
                 fontsize=9.0, color="#8b0000", bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff0f0", edgecolor="#ffcccc", alpha=0.9))

    # Subplot 3: Representative n=2000
    axes[2].scatter(X_2000[:, 0], X_2000[:, 1], s=4.5, alpha=0.50, color="#2ca02c", edgecolors="none")
    axes[2].set_title(t["sampling_rep_title"], fontweight="bold", fontsize=11.5, pad=10)
    axes[2].text(0.05, 0.06, f"$n = 2000$ (25%)\n{t['sampling_rep_note']}", transform=axes[2].transAxes,
                 fontsize=9.0, color="#005500", bbox=dict(boxstyle="round,pad=0.3", facecolor="#f0fff0", edgecolor="#b3e6b3", alpha=0.9))

    for ax in axes:
        ax.set_xlim(-3.6, 3.6)
        ax.set_ylim(-3.6, 3.4)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.set_xticks([-3, -1.5, 0, 1.5, 3])
        ax.set_yticks([-3, -1.5, 0, 1.5, 3])

    plt.tight_layout()
    out_path = out_dir / "sampling_tradeoff.pdf"
    plt.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"  [+] Saved [{lang}]: {out_path.name}")


def generate_for_language(df: pd.DataFrame, lang: str) -> None:
    out_dir = ASSETS_DIR / lang
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n[*] Generating figures for language '{lang}' in {out_dir.relative_to(SCRIPT_DIR.parent)}...")

    generate_conditional_boxplot(df, lang, out_dir)
    generate_real_scatterplot(df, lang, out_dir)
    generate_real_splom(df, lang, out_dir)
    generate_parallel_coordinates(df, lang, out_dir)
    generate_radar_plot(df, lang, out_dir)
    generate_correlation_heatmaps(df, lang, out_dir)
    # Chapter 3 figures
    generate_precipitation_aggregation(lang, out_dir)
    generate_pca_scree_plot(df, lang, out_dir)
    generate_pca_2d_projection(df, lang, out_dir)
    generate_sampling_tradeoff(lang, out_dir)


def main() -> int:
    print("=" * 65)
    print("  Bilingual Figure Generator (IT & EN) - Data Mining Dispensa")
    print("=" * 65)
    df = load_data()

    # Generate both Italian and English versions
    for lang in ["it", "en"]:
        generate_for_language(df, lang)

    print("\n" + "=" * 65)
    print(f"[+] Successfully generated all bilingual figures in:")
    print(f"    - Italian : {ASSETS_DIR / 'it'}")
    print(f"    - English : {ASSETS_DIR / 'en'}")
    print("=" * 65)
    return 0


if __name__ == "__main__":
    sys.exit(main())
