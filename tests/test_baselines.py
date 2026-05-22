import pandas as pd

from exoplanets_research.validation.baselines import rank_correlation_summary, top_k_jaccard


def test_top_k_jaccard_measures_overlap():
    left = ["A", "B", "C"]
    right = ["B", "C", "D"]

    assert top_k_jaccard(left, right, k=3) == 0.5


def test_rank_correlation_summary_handles_identical_rankings():
    df = pd.DataFrame(
        {
            "pl_name": ["A", "B", "C"],
            "rank_a": [1, 2, 3],
            "rank_b": [1, 2, 3],
        }
    )

    summary = rank_correlation_summary(df, "rank_a", "rank_b")

    assert summary["spearman_r"] == 1.0
