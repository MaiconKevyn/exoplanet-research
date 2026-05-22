import argparse
import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import yaml

from exoplanets_research.data.archive import load_planetary_systems_csv
from exoplanets_research.data.cleaning import select_best_planet_records
from exoplanets_research.habitability.features import add_habitability_features
from exoplanets_research.habitability.habitable_zone import add_habitable_zone_columns
from exoplanets_research.habitability.scoring import score_candidates
from exoplanets_research.habitability.scoring_config import ScoringConfig, load_scoring_config
from exoplanets_research.paper.figures import (
    plot_hz_model_overlap,
    plot_rank_uncertainty,
    plot_score_distribution,
    plot_subscore_heatmap,
    write_markdown_table,
    write_top_candidate_table,
)
from exoplanets_research.validation.baselines import (
    followup_readiness_baseline,
    hz_radius_baseline,
    rank_correlation_summary,
    top_k_jaccard,
)
from exoplanets_research.validation.external_targets import (
    HWO_EXEP_TABLE,
    add_host_target_flags,
    download_mission_star_table,
    load_external_targets,
)


def load_experiment_manifest(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def build_featured_candidates(input_path: Path, *, hz_model: str) -> pd.DataFrame:
    raw = load_planetary_systems_csv(input_path)
    canonical = select_best_planet_records(raw)
    hz = add_habitable_zone_columns(canonical, model=hz_model)
    hz = hz[hz["hz_inner"].notna() & hz["pl_orbsmax"].notna()].copy()
    return add_habitability_features(hz)


def build_ranked_candidates(input_path: Path, *, hz_model: str) -> pd.DataFrame:
    return score_candidates(build_featured_candidates(input_path, hz_model=hz_model)).reset_index(drop=True)


def assign_rank(df: pd.DataFrame, column: str) -> pd.DataFrame:
    result = df.copy().reset_index(drop=True)
    result[column] = result.index + 1
    return result


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    unique = []
    for path in paths:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_external_validation(manifest: dict, output_dir: Path) -> tuple[pd.DataFrame, list[Path]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ranked_path = Path("data/outputs/astrobiology_ranked_candidates.csv")
    if not ranked_path.exists():
        return pd.DataFrame(), []
    external_config = manifest.get("external_targets", {})
    target_path = Path(external_config.get("path", "data/external/hwo_exep_2023.csv"))
    if not target_path.exists() and external_config.get("download", True):
        download_mission_star_table(
            target_path,
            table_name=external_config.get("table_name", HWO_EXEP_TABLE),
            target_list=external_config.get("target_list", "hwo_exep_2023"),
        )

    if not target_path.exists():
        return pd.DataFrame(), []

    ranked = pd.read_csv(ranked_path, low_memory=False)
    targets = load_external_targets(target_path, target_list=external_config.get("target_list", "hwo_exep_2023"))
    annotated = add_host_target_flags(ranked, targets)
    matched = annotated[annotated["external_target_match"] == True].copy()  # noqa: E712
    matched.insert(0, "ectp_rank", matched.index + 1)
    summary = pd.DataFrame(
        [
            {
                "target_list": external_config.get("target_list", "hwo_exep_2023"),
                "source_table": external_config.get("table_name", HWO_EXEP_TABLE),
                "target_hosts": int(targets["hostname"].nunique()),
                "ranked_candidates": int(len(ranked)),
                "matched_candidates": int(len(matched)),
                "matched_top_25": int(matched["ectp_rank"].le(25).sum()) if not matched.empty else 0,
                "matched_top_50": int(matched["ectp_rank"].le(50).sum()) if not matched.empty else 0,
            }
        ]
    )
    validation_path = output_dir / "external_validation.csv"
    summary_path = output_dir / "external_validation_summary.csv"
    table_path = Path("paper/tables/external_validation_summary.md")
    validation_columns = [
        "pl_name",
        "hostname",
        "score_total",
        "evidence_confidence",
        "hz_model",
        "external_target_match",
        "external_target_lists",
    ]
    annotated.loc[:, [column for column in validation_columns if column in annotated.columns]].to_csv(
        validation_path,
        index=False,
    )
    summary.to_csv(summary_path, index=False)
    write_markdown_table(summary, table_path)
    return summary, [validation_path, summary_path, table_path]


def write_external_inventory(manifest: dict, output_path: Path) -> Path:
    external_config = manifest.get("external_targets", {})
    target_path = Path(external_config.get("path", "data/external/hwo_exep_2023.csv"))
    rows = "not downloaded"
    checksum = "not downloaded"
    if target_path.exists():
        rows = str(len(pd.read_csv(target_path, low_memory=False)))
        checksum = sha256_file(target_path)
    generated_at = datetime.now(UTC).date().isoformat()
    source_url = external_config.get("source_url", "https://exoplanetarchive.ipac.caltech.edu/docs/MissionStellar.html")
    tap_url = external_config.get("tap_url", "https://exoplanetarchive.ipac.caltech.edu/TAP/sync")
    text = f"""# External Data Inventory

Generated for experiment `{manifest["id"]}`.

| Dataset | Access | Source URL | Download date | Local path | Rows | SHA-256 | Processing command | Scientific role |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| HWO ExEP Precursor Science Stars | NASA Exoplanet Archive TAP table `{external_config.get("table_name", HWO_EXEP_TABLE)}` via `{tap_url}` | {source_url} | {generated_at} | `{target_path}` | {rows} | `{checksum}` | `.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml` | Mission-facing stellar target list used to test whether ECTP prioritizes known direct-imaging target hosts. |
| HWO Preliminary Input Catalog | NASA Exoplanet Archive `.tgz` package, DOI listed by NASA as `10.26133/NEA39` | {source_url} | Not downloaded | Not vendored | n/a | n/a | Planned HPIC ingestion step | Future large-scale expansion target; excluded from the default automated run until a stable tabular ingestion contract is added. |

The HWO ExEP crossmatch is host-name based and therefore conservative: it measures overlap with known stellar target hosts, not biological evidence.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path


def write_paper_artifacts(manifest: dict, extra_outputs: list[Path] | None = None) -> list[Path]:
    ranked_path = Path("data/outputs/astrobiology_ranked_candidates.csv")
    if not ranked_path.exists():
        return []
    ranked = pd.read_csv(ranked_path, low_memory=False)
    outputs = [
        Path("paper/tables/top_candidates.md"),
        Path("paper/figures/score_distribution.png"),
        Path("paper/figures/subscore_heatmap_top25.png"),
    ]
    write_top_candidate_table(ranked, outputs[0], top_n=25)
    plot_score_distribution(ranked, outputs[1])
    plot_subscore_heatmap(ranked, outputs[2], top_n=25)

    uncertainty_path = Path("data/outputs/astrobiology_rank_uncertainty.csv")
    if uncertainty_path.exists():
        uncertainty = pd.read_csv(uncertainty_path, low_memory=False)
        rank_figure = Path("paper/figures/rank_uncertainty_top25.png")
        plot_rank_uncertainty(uncertainty, rank_figure, top_n=25)
        outputs.append(rank_figure)

    outputs = unique_paths([*(extra_outputs or []), *outputs])
    summary_path = Path(manifest["outputs"]["directory"]) / "paper_artifacts.yml"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        yaml.safe_dump({"paper_artifacts": [str(path) for path in outputs]}, sort_keys=False),
        encoding="utf-8",
    )
    outputs.append(summary_path)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run paper-grade ECTP experiments.")
    parser.add_argument("--config", type=Path, default=Path("configs/experiments/paper_v1.yml"))
    args = parser.parse_args()
    manifest = load_experiment_manifest(args.config)
    output_dir = Path(manifest["outputs"]["directory"])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manifest_resolved.yml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    hz_summary, hz_artifacts = run_hz_model_comparison(manifest, output_dir)
    baseline_summary, baseline_artifacts = run_baseline_comparison(manifest, output_dir)
    sensitivity_summary, sensitivity_artifacts = run_score_sensitivity(manifest, output_dir)
    external_summary, external_artifacts = run_external_validation(manifest, output_dir)
    inventory = write_external_inventory(manifest, Path("docs/validation/external_data_inventory.md"))
    artifacts = write_paper_artifacts(
        manifest,
        [*hz_artifacts, *baseline_artifacts, *sensitivity_artifacts, *external_artifacts, inventory],
    )
    print(f"experiment_id: {manifest['id']}")
    print(f"output_dir: {output_dir}")
    print(f"hz_models_compared: {len(hz_summary)}")
    print(f"baselines_compared: {len(baseline_summary)}")
    print(f"score_sensitivity_profiles: {len(sensitivity_summary)}")
    print(f"external_validations: {len(external_summary)}")
    for artifact in artifacts:
        print(f"artifact: {artifact}")


if __name__ == "__main__":
    main()
