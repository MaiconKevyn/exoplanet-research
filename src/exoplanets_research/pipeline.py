import argparse
from pathlib import Path

from exoplanets_research.config import DATA_DIR, FRONTEND_DATA_DIR
from exoplanets_research.data.archive import load_planetary_systems_csv
from exoplanets_research.data.cleaning import select_best_planet_records
from exoplanets_research.data.outputs import attach_uncertainty_summary, write_frontend_json
from exoplanets_research.experiments.artifacts import write_paper_artifacts
from exoplanets_research.experiments.manifest import load_experiment_manifest
from exoplanets_research.habitability.features import add_habitability_features
from exoplanets_research.habitability.habitable_zone import HZ_MODEL, add_habitable_zone_columns
from exoplanets_research.habitability.scoring import score_candidates
from exoplanets_research.habitability.scoring_config import DEFAULT_SCORING_CONFIG_PATH, load_scoring_config
from exoplanets_research.io.provenance import write_provenance
from exoplanets_research.literature.catalog import load_sources
from exoplanets_research.uncertainty.monte_carlo import generate_uncertainty_samples, summarize_rank_uncertainty


DEFAULT_INPUT = DATA_DIR / "PS_2025.06.22_09.41.26.csv"
DEFAULT_EXPERIMENT_CONFIG = Path("configs/experiments/paper_v1.yml")
PIPELINE_GENERATOR = "src/exoplanets_research/pipeline.py"


def run_pipeline(
    *,
    input_path: Path = DEFAULT_INPUT,
    output_root: Path = DATA_DIR,
    frontend_root: Path = FRONTEND_DATA_DIR,
    stage: str = "all",
    hz_model: str = HZ_MODEL,
    score_profile: Path = DEFAULT_SCORING_CONFIG_PATH,
    uncertainty_runs: int = 0,
    uncertainty_seed: int = 42,
    paper_artifacts: bool = False,
    experiment_config: Path = DEFAULT_EXPERIMENT_CONFIG,
) -> dict[str, Path]:
    input_path = Path(input_path)
    output_root = Path(output_root)
    frontend_root = Path(frontend_root)
    processed_dir = output_root / "processed"
    outputs_dir = output_root / "outputs"
    processed_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, Path] = {}

    if stage == "literature":
        load_sources(DATA_DIR / "literature" / "astrobiology_sources.yml")
        return outputs

    raw = load_planetary_systems_csv(input_path)
    canonical = select_best_planet_records(raw)
    canonical_path = processed_dir / "canonical_exoplanets.csv"
    canonical.to_csv(canonical_path, index=False)
    canonical_provenance = processed_dir / "canonical_exoplanets.provenance.json"
    write_provenance(
        canonical_provenance,
        input_file=input_path,
        row_count=len(canonical),
        stage="canonical",
        generated_by=PIPELINE_GENERATOR,
    )
    outputs["canonical"] = canonical_path
    outputs["canonical_provenance"] = canonical_provenance

    if stage == "canonical":
        return outputs

    scoring_config = load_scoring_config(Path(score_profile))
    hz = add_habitable_zone_columns(canonical, model=hz_model)
    hz = hz[hz["hz_inner"].notna() & hz["pl_orbsmax"].notna()].copy()
    hz_path = processed_dir / "habitable_zone_exoplanets.csv"
    hz.to_csv(hz_path, index=False)
    outputs["habitable_zone"] = hz_path

    featured = add_habitability_features(hz)
    ranked = score_candidates(featured, config=scoring_config)
    uncertainty_summary = None

    if uncertainty_runs > 0 and stage in {"score", "all", "export-frontend"}:
        uncertainty_samples = generate_uncertainty_samples(
            canonical,
            runs=uncertainty_runs,
            seed=uncertainty_seed,
            hz_model=hz_model,
            scoring_config=scoring_config,
        )
        uncertainty_samples_path = outputs_dir / "astrobiology_uncertainty_samples.csv"
        uncertainty_samples.to_csv(uncertainty_samples_path, index=False)
        uncertainty_summary = summarize_rank_uncertainty(uncertainty_samples, top_k=10)
        uncertainty_summary_path = outputs_dir / "astrobiology_rank_uncertainty.csv"
        uncertainty_summary.to_csv(uncertainty_summary_path, index=False)
        outputs["uncertainty_samples"] = uncertainty_samples_path
        outputs["rank_uncertainty"] = uncertainty_summary_path

    ranked = attach_uncertainty_summary(ranked, uncertainty_summary)
    ranked_path = outputs_dir / "astrobiology_ranked_candidates.csv"
    ranked.to_csv(ranked_path, index=False)
    ranked_provenance = outputs_dir / "astrobiology_ranked_candidates.provenance.json"
    write_provenance(
        ranked_provenance,
        input_file=input_path,
        row_count=len(ranked),
        stage="score",
        generated_by=PIPELINE_GENERATOR,
    )
    outputs["ranked"] = ranked_path
    outputs["ranked_provenance"] = ranked_provenance

    if stage in {"score", "all", "export-frontend"}:
        outputs["frontend_json"] = write_frontend_json(ranked_path, frontend_root)

    if paper_artifacts and stage in {"score", "all", "export-frontend"}:
        manifest = load_experiment_manifest(Path(experiment_config))
        for index, artifact in enumerate(write_paper_artifacts(manifest)):
            outputs[f"paper_artifact_{index}"] = artifact

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the astrobiology research pipeline.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--stage", choices=["all", "literature", "canonical", "score", "export-frontend"], default="all")
    parser.add_argument("--hz-model", default=HZ_MODEL)
    parser.add_argument("--score-profile", type=Path, default=DEFAULT_SCORING_CONFIG_PATH)
    parser.add_argument("--uncertainty-runs", type=int, default=0)
    parser.add_argument("--uncertainty-seed", type=int, default=42)
    parser.add_argument("--paper-artifacts", action="store_true")
    parser.add_argument("--experiment-config", type=Path, default=DEFAULT_EXPERIMENT_CONFIG)
    args = parser.parse_args()

    outputs = run_pipeline(
        input_path=args.input,
        stage=args.stage,
        hz_model=args.hz_model,
        score_profile=args.score_profile,
        uncertainty_runs=args.uncertainty_runs,
        uncertainty_seed=args.uncertainty_seed,
        paper_artifacts=args.paper_artifacts,
        experiment_config=args.experiment_config,
    )
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
