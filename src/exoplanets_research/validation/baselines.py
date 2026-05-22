import pandas as pd
from scipy.stats import kendalltau, spearmanr


def top_k_jaccard(left: list[str], right: list[str], *, k: int) -> float:
    left_set = set(left[:k])
    right_set = set(right[:k])
    if not left_set and not right_set:
        return 1.0
    return len(left_set & right_set) / len(left_set | right_set)


def rank_correlation_summary(df: pd.DataFrame, left_rank: str, right_rank: str) -> dict[str, float]:
    clean = df[[left_rank, right_rank]].dropna()
    if len(clean) < 2:
        return {"spearman_r": float("nan"), "kendall_tau": float("nan"), "n": float(len(clean))}
    spearman = spearmanr(clean[left_rank], clean[right_rank]).statistic
    kendall = kendalltau(clean[left_rank], clean[right_rank]).statistic
    return {"spearman_r": float(spearman), "kendall_tau": float(kendall), "n": float(len(clean))}


def hz_radius_baseline(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["baseline_score"] = (
        (result["habitable_zone_status"].eq("inside").astype(float) * 0.7)
        + (result["pl_rade"].between(0.5, 1.5).fillna(False).astype(float) * 0.3)
    )
    return result.sort_values(["baseline_score", "pl_name"], ascending=[False, True]).reset_index(drop=True)


def followup_readiness_baseline(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    readiness = result.get("followup_readiness_score", pd.Series(0.0, index=result.index)).fillna(0).astype(float)
    data_quality = result.get("score_data_quality", pd.Series(0.0, index=result.index)).fillna(0).astype(float)
    if "sy_dist" not in result.columns:
        result["sy_dist"] = float("inf")
    result["baseline_score"] = (0.6 * readiness) + (0.4 * data_quality)
    return result.sort_values(["baseline_score", "sy_dist", "pl_name"], ascending=[False, True, True]).reset_index(drop=True)
