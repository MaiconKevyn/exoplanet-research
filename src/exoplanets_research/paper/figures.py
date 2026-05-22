from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_score_distribution(ranked: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 4.5))
    sns.histplot(ranked["score_total"].dropna(), bins=40, color="#1f5f74")
    plt.xlabel("ECTP score")
    plt.ylabel("Candidate count")
    plt.title("Distribution of evidence-calibrated target scores")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_subscore_heatmap(ranked: pd.DataFrame, output_path: Path, *, top_n: int = 25) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "score_hz_position",
        "score_planet_size",
        "score_stellar_context",
        "score_data_quality",
        "score_followup_readiness",
    ]
    data = ranked.head(top_n).set_index("pl_name")[columns]
    plt.figure(figsize=(9, max(5, top_n * 0.26)))
    sns.heatmap(data, vmin=0, vmax=1, cmap="viridis", cbar_kws={"label": "Sub-score"})
    plt.xlabel("Evidence dimension")
    plt.ylabel("Candidate")
    plt.title(f"Top {top_n} candidate evidence decomposition")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_rank_uncertainty(uncertainty: pd.DataFrame, output_path: Path, *, top_n: int = 25) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = uncertainty.head(top_n).copy()
    lower_error = (data["rank_median"] - data["rank_p05"]).clip(lower=0)
    upper_error = (data["rank_p95"] - data["rank_median"]).clip(lower=0)
    plt.figure(figsize=(8, max(5, top_n * 0.26)))
    plt.errorbar(
        data["rank_median"],
        data["pl_name"],
        xerr=[lower_error, upper_error],
        fmt="o",
        color="#1f5f74",
        ecolor="#8ecae6",
    )
    plt.gca().invert_xaxis()
    plt.xlabel("Rank interval")
    plt.ylabel("Candidate")
    plt.title(f"Top {top_n} rank stability under catalog uncertainty")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_hz_model_overlap(experiment_summary: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = experiment_summary.copy()
    if "top_k_overlap" not in data.columns:
        overlap_columns = [column for column in data.columns if column.startswith("top_") and column.endswith("_overlap")]
        data["top_k_overlap"] = data[overlap_columns[0]]
    plt.figure(figsize=(8, 4.5))
    sns.barplot(data=data, x="hz_model", y="top_k_overlap", color="#2f725b")
    plt.ylim(0, 1)
    plt.xlabel("HZ model")
    plt.ylabel("Top-k overlap")
    plt.title("Candidate overlap across habitable-zone model families")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()
