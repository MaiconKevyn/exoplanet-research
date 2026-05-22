from pathlib import Path

import pandas as pd
import yaml

from exoplanets_research.paper.figures import (
    plot_rank_uncertainty,
    plot_score_distribution,
    plot_subscore_heatmap,
)
from exoplanets_research.paper.tables import write_top_candidate_table


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
