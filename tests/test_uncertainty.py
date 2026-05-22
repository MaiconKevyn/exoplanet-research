import pandas as pd

from exoplanets_research.uncertainty.monte_carlo import summarize_rank_uncertainty


def test_rank_uncertainty_summary_has_required_columns():
    samples = pd.DataFrame(
        [
            {"run_id": 0, "pl_name": "A b", "score_total": 0.8},
            {"run_id": 0, "pl_name": "B b", "score_total": 0.6},
            {"run_id": 1, "pl_name": "A b", "score_total": 0.7},
            {"run_id": 1, "pl_name": "B b", "score_total": 0.9},
        ]
    )

    summary = summarize_rank_uncertainty(samples, top_k=1)

    assert {"score_mean", "score_std", "rank_median", "rank_p05", "rank_p95", "top1_probability"}.issubset(
        summary.columns
    )
    assert set(summary["pl_name"]) == {"A b", "B b"}
