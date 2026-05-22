import pandas as pd

from exoplanets_research.paper.figures import plot_score_distribution


def test_plot_score_distribution(tmp_path):
    ranked = pd.DataFrame(
        {
            "pl_name": ["A b", "B b"],
            "hostname": ["A", "B"],
            "score_total": [0.9, 0.8],
            "evidence_confidence": ["moderate_catalog_confidence", "limited_catalog_confidence"],
        }
    )
    output = tmp_path / "score_distribution.png"

    plot_score_distribution(ranked, output)

    assert output.exists()
    assert output.stat().st_size > 0
