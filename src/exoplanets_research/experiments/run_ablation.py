import argparse
from pathlib import Path

import yaml

from exoplanets_research.experiments.artifacts import unique_paths, write_paper_artifacts
from exoplanets_research.experiments.candidates import (
    assign_rank,
    build_featured_candidates,
    build_ranked_candidates,
)
from exoplanets_research.experiments.comparisons import (
    run_baseline_comparison,
    run_hz_model_comparison,
    run_score_sensitivity,
)
from exoplanets_research.experiments.external_validation import (
    run_external_validation,
    sha256_file,
    write_external_inventory,
)
from exoplanets_research.experiments.manifest import load_experiment_manifest


__all__ = [
    "assign_rank",
    "build_featured_candidates",
    "build_ranked_candidates",
    "load_experiment_manifest",
    "run_baseline_comparison",
    "run_external_validation",
    "run_hz_model_comparison",
    "run_score_sensitivity",
    "sha256_file",
    "unique_paths",
    "write_external_inventory",
    "write_paper_artifacts",
]


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
