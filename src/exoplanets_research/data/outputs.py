from pathlib import Path

import pandas as pd


UNCERTAINTY_SUMMARY_COLUMNS = ["score_mean", "score_std", "rank_median", "rank_p05", "rank_p95", "top10_probability"]


def write_frontend_json(csv_path: Path, frontend_root: Path) -> Path:
    frontend_root.mkdir(parents=True, exist_ok=True)
    output_path = frontend_root / "astrobiology_ranked_candidates.json"
    df = pd.read_csv(csv_path, low_memory=False)
    df.to_json(output_path, orient="records", indent=2)
    return output_path


def attach_uncertainty_summary(ranked: pd.DataFrame, summary: pd.DataFrame | None = None) -> pd.DataFrame:
    result = ranked.copy()
    for column in UNCERTAINTY_SUMMARY_COLUMNS:
        if column not in result.columns:
            result[column] = pd.NA
    if summary is None or summary.empty:
        return result
    return result.drop(columns=UNCERTAINTY_SUMMARY_COLUMNS, errors="ignore").merge(
        summary[["pl_name", *UNCERTAINTY_SUMMARY_COLUMNS]],
        on="pl_name",
        how="left",
    )
