import pandas as pd

from exoplanets_research.validation.baselines import followup_readiness_baseline, rank_correlation_summary, top_k_jaccard


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


def test_followup_readiness_baseline_prioritizes_ready_nearby_targets():
    df = pd.DataFrame(
        {
            "pl_name": ["Distant b", "Nearby b"],
            "hostname": ["Distant", "Nearby"],
            "followup_readiness_score": [0.4, 0.9],
            "score_data_quality": [1.0, 0.8],
            "sy_dist": [300.0, 12.0],
        }
    )

    ranked = followup_readiness_baseline(df)

    assert ranked.loc[0, "pl_name"] == "Nearby b"
    assert ranked.loc[0, "baseline_score"] > ranked.loc[1, "baseline_score"]
