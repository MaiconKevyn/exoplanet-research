import pandas as pd

from exoplanets_research.habitability.features import CRITICAL_SCORING_FIELDS


def _score_hz_position(row: pd.Series) -> float:
    if row.get("habitable_zone_status") != "inside" or pd.isna(row.get("hz_center_offset")):
        return 0.0
    offset = min(float(row["hz_center_offset"]), 1.0)
    return max(0.0, 1.0 - (0.5 * offset))


def _score_planet_size(radius: float | None) -> float:
    if pd.isna(radius):
        return 0.0
    radius = float(radius)
    if 0.5 <= radius <= 1.5:
        return 1.0
    if 1.5 < radius <= 2.5:
        return 0.5
    return 0.0


def _score_stellar_context(st_teff: float | None) -> float:
    if pd.isna(st_teff):
        return 0.0
    st_teff = float(st_teff)
    if 5200 <= st_teff <= 6000:
        return 1.0
    if 3700 <= st_teff < 5200:
        return 0.75
    if 2400 <= st_teff < 3700:
        return 0.25
    return 0.0


def _score_data_quality(row: pd.Series) -> float:
    present = sum(not pd.isna(row.get(column)) for column in CRITICAL_SCORING_FIELDS)
    return present / len(CRITICAL_SCORING_FIELDS)


def _missing_count(row: pd.Series) -> int:
    return sum(pd.isna(row.get(column)) for column in CRITICAL_SCORING_FIELDS)


def _evidence_confidence(row: pd.Series) -> str:
    data_quality = float(row["score_data_quality"])
    if row.get("habitable_zone_status") == "inside" and data_quality >= 0.85:
        return "moderate_catalog_confidence"
    if data_quality >= 0.6:
        return "limited_catalog_confidence"
    return "low_catalog_confidence"


def score_candidates(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for column in CRITICAL_SCORING_FIELDS + ["followup_readiness_score"]:
        if column not in result.columns:
            result[column] = pd.NA

    result["score_hz_position"] = result.apply(_score_hz_position, axis=1)
    result["score_planet_size"] = result["pl_rade"].apply(_score_planet_size)
    result["score_stellar_context"] = result["st_teff"].apply(_score_stellar_context)
    result["score_data_quality"] = result.apply(_score_data_quality, axis=1)
    result["score_followup_readiness"] = result["followup_readiness_score"].fillna(0).astype(float)
    result["penalty_missing_data"] = result.apply(lambda row: min(0.25, 0.05 * _missing_count(row)), axis=1)
    result["score_total"] = (
        (0.35 * result["score_hz_position"])
        + (0.20 * result["score_planet_size"])
        + (0.15 * result["score_stellar_context"])
        + (0.15 * result["score_data_quality"])
        + (0.15 * result["score_followup_readiness"])
        - result["penalty_missing_data"]
    ).clip(lower=0, upper=1)
    result["evidence_confidence"] = result.apply(_evidence_confidence, axis=1)
    result["interpretation_label"] = "habitability_followup_candidate"
    result["interpretation_caveat"] = (
        "No biosignature inference is made; this ranking prioritizes candidates "
        "for further observation and modeling."
    )
    return result.sort_values(["score_total", "pl_name"], ascending=[False, True]).reset_index(drop=True)

