from pathlib import Path

import pandas as pd

from exoplanets_research.experiments.candidates import (
    assign_rank,
    build_featured_candidates,
    build_ranked_candidates,
)
from exoplanets_research.habitability.scoring import score_candidates
from exoplanets_research.habitability.scoring_config import ScoringConfig, load_scoring_config
from exoplanets_research.paper.figures import plot_hz_model_overlap, write_markdown_table
from exoplanets_research.validation.baselines import (
    followup_readiness_baseline,
    hz_radius_baseline,
    rank_correlation_summary,
    top_k_jaccard,
)


def run_hz_model_comparison(manifest: dict, output_dir: Path) -> tuple[pd.DataFrame, list[Path]]:
    input_path = Path(manifest["input"])
    hz_models = manifest.get("hz_models", [])
    top_ks = manifest.get("top_k", [25])
    if not hz_models:
        return pd.DataFrame(), []

    rankings = {
        hz_model: assign_rank(build_ranked_candidates(input_path, hz_model=hz_model), "rank")
        for hz_model in hz_models
    }
    reference_model = hz_models[0]
    reference_names = rankings[reference_model]["pl_name"].tolist()
    rows = []
    for hz_model, ranked in rankings.items():
        row = {
            "hz_model": hz_model,
            "n_candidates": int(len(ranked)),
            "inside_hz_count": int(ranked["habitable_zone_status"].eq("inside").sum()),
        }
        candidate_names = ranked["pl_name"].tolist()
        for top_k in top_ks:
            row[f"top_{top_k}_overlap"] = round(top_k_jaccard(reference_names, candidate_names, k=int(top_k)), 3)
        rows.append(row)

    summary = pd.DataFrame(rows)
    csv_path = output_dir / "hz_model_comparison.csv"
    table_path = Path("paper/tables/hz_model_comparison.md")
    figure_path = Path("paper/figures/hz_model_overlap.png")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(csv_path, index=False)
    write_markdown_table(summary, table_path)
    plot_hz_model_overlap(summary, figure_path)
    return summary, [csv_path, table_path, figure_path]


def run_baseline_comparison(manifest: dict, output_dir: Path) -> tuple[pd.DataFrame, list[Path]]:
    input_path = Path(manifest["input"])
    hz_model = manifest["hz_models"][0]
    top_ks = manifest.get("top_k", [25])
    ranked = assign_rank(build_ranked_candidates(input_path, hz_model=hz_model), "ectp_rank")
    ectp_names = ranked["pl_name"].tolist()
    baseline_functions = {
        "hz_radius_baseline": hz_radius_baseline,
        "followup_readiness_baseline": followup_readiness_baseline,
    }
    rows = []
    for baseline_name, baseline_function in baseline_functions.items():
        baseline = assign_rank(baseline_function(ranked), "baseline_rank")
        merged = ranked[["pl_name", "ectp_rank"]].merge(
            baseline[["pl_name", "baseline_rank", "baseline_score"]],
            on="pl_name",
            how="inner",
        )
        correlations = rank_correlation_summary(merged, "ectp_rank", "baseline_rank")
        row = {
            "baseline": baseline_name,
            "n": int(correlations["n"]),
            "spearman_r": round(correlations["spearman_r"], 3),
            "kendall_tau": round(correlations["kendall_tau"], 3),
        }
        baseline_names = baseline["pl_name"].tolist()
        for top_k in top_ks:
            row[f"top_{top_k}_overlap"] = round(top_k_jaccard(ectp_names, baseline_names, k=int(top_k)), 3)
        rows.append(row)

    summary = pd.DataFrame(rows)
    csv_path = output_dir / "baseline_comparison.csv"
    table_path = Path("paper/tables/baseline_comparison.md")
    summary.to_csv(csv_path, index=False)
    write_markdown_table(summary, table_path)
    return summary, [csv_path, table_path]


def _scaled_scoring_config(base: ScoringConfig, *, profile_id: str, label: str, multipliers: dict[str, float]) -> ScoringConfig:
    weighted = {
        key: value * float(multipliers.get(key, 1.0))
        for key, value in base.weights.items()
    }
    total = sum(weighted.values())
    normalized = {key: value / total for key, value in weighted.items()}
    return ScoringConfig(
        id=profile_id,
        label=label,
        description=f"Sensitivity profile derived from {base.id}.",
        weights=normalized,
        penalties=base.penalties,
        confidence=base.confidence,
        non_claim=base.non_claim,
    )


def run_score_sensitivity(manifest: dict, output_dir: Path) -> tuple[pd.DataFrame, list[Path]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    input_path = Path(manifest["input"])
    hz_model = manifest["hz_models"][0]
    top_ks = manifest.get("top_k", [25])
    base_config = load_scoring_config(Path(manifest["score_profiles"][0]))
    featured = build_featured_candidates(input_path, hz_model=hz_model)
    sensitivity_profiles = [
        base_config,
        _scaled_scoring_config(
            base_config,
            profile_id="ectp_hz_emphasis",
            label="ECTP HZ-emphasis sensitivity",
            multipliers={"hz_position": 1.35, "planet_size": 1.10},
        ),
        _scaled_scoring_config(
            base_config,
            profile_id="ectp_followup_emphasis",
            label="ECTP follow-up-emphasis sensitivity",
            multipliers={"followup_readiness": 1.60, "data_quality": 1.20},
        ),
        _scaled_scoring_config(
            base_config,
            profile_id="ectp_data_quality_emphasis",
            label="ECTP data-quality-emphasis sensitivity",
            multipliers={"data_quality": 1.75, "stellar_context": 1.15},
        ),
    ]
    rankings = {
        config.id: assign_rank(score_candidates(featured, config=config), "rank")
        for config in sensitivity_profiles
    }
    reference = rankings[base_config.id]
    reference_names = reference["pl_name"].tolist()
    rows = []
    for config in sensitivity_profiles:
        ranked = rankings[config.id]
        merged = reference[["pl_name", "rank"]].rename(columns={"rank": "reference_rank"}).merge(
            ranked[["pl_name", "rank"]].rename(columns={"rank": "variant_rank"}),
            on="pl_name",
            how="inner",
        )
        correlations = rank_correlation_summary(merged, "reference_rank", "variant_rank")
        row = {
            "score_profile": config.id,
            "n": int(correlations["n"]),
            "spearman_r": round(correlations["spearman_r"], 3),
            "kendall_tau": round(correlations["kendall_tau"], 3),
        }
        variant_names = ranked["pl_name"].tolist()
        for top_k in top_ks:
            row[f"top_{top_k}_overlap"] = round(top_k_jaccard(reference_names, variant_names, k=int(top_k)), 3)
        rows.append(row)

    summary = pd.DataFrame(rows)
    csv_path = output_dir / "score_sensitivity.csv"
    table_path = Path("paper/tables/score_sensitivity.md")
    summary.to_csv(csv_path, index=False)
    write_markdown_table(summary, table_path)
    return summary, [csv_path, table_path]
