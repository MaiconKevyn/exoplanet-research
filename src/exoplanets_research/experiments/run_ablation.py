import argparse
from pathlib import Path

import pandas as pd
import yaml

from exoplanets_research.paper.figures import (
    plot_score_distribution,
    plot_subscore_heatmap,
    write_top_candidate_table,
)


def load_experiment_manifest(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def write_paper_artifacts(manifest: dict) -> list[Path]:
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
        from exoplanets_research.paper.figures import plot_rank_uncertainty

        uncertainty = pd.read_csv(uncertainty_path, low_memory=False)
        rank_figure = Path("paper/figures/rank_uncertainty_top25.png")
        plot_rank_uncertainty(uncertainty, rank_figure, top_n=25)
        outputs.append(rank_figure)

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
    artifacts = write_paper_artifacts(manifest)
    print(f"experiment_id: {manifest['id']}")
    print(f"output_dir: {output_dir}")
    for artifact in artifacts:
        print(f"artifact: {artifact}")


if __name__ == "__main__":
    main()
