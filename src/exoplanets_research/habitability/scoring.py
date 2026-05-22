import pandas as pd

from exoplanets_research.habitability.features import CRITICAL_SCORING_FIELDS
from exoplanets_research.habitability.scoring_config import ScoringConfig, load_scoring_config


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


def _evidence_confidence(row: pd.Series, config: ScoringConfig) -> str:
    data_quality = float(row["score_data_quality"])
    if (
        row.get("habitable_zone_status") == "inside"
        and data_quality >= config.confidence["moderate_min_data_quality"]
    ):
        return "moderate_catalog_confidence"
    if data_quality >= config.confidence["limited_min_data_quality"]:
        return "limited_catalog_confidence"
    return "low_catalog_confidence"


def score_candidates(df: pd.DataFrame, *, config: ScoringConfig | None = None) -> pd.DataFrame:
    config = config or load_scoring_config()
    result = df.copy()
    for column in CRITICAL_SCORING_FIELDS + ["followup_readiness_score"]:
        if column not in result.columns:
            result[column] = pd.NA

    result["score_hz_position"] = result.apply(_score_hz_position, axis=1)
    result["score_planet_size"] = result["pl_rade"].apply(_score_planet_size)
    result["score_stellar_context"] = result["st_teff"].apply(_score_stellar_context)
    result["score_data_quality"] = result.apply(_score_data_quality, axis=1)
    result["score_followup_readiness"] = result["followup_readiness_score"].fillna(0).astype(float)
    result["penalty_missing_data"] = result.apply(
        lambda row: min(config.penalties["max_missing_data"], config.penalties["missing_field"] * _missing_count(row)),
        axis=1,
    )
    result["score_total"] = (
        (config.weights["hz_position"] * result["score_hz_position"])
        + (config.weights["planet_size"] * result["score_planet_size"])
        + (config.weights["stellar_context"] * result["score_stellar_context"])
        + (config.weights["data_quality"] * result["score_data_quality"])
        + (config.weights["followup_readiness"] * result["score_followup_readiness"])
        - result["penalty_missing_data"]
    ).clip(lower=0, upper=1)
    result["evidence_confidence"] = result.apply(lambda row: _evidence_confidence(row, config), axis=1)
    result["interpretation_label"] = "habitability_followup_candidate"
    result["interpretation_caveat"] = config.non_claim
    result["score_profile_id"] = config.id
    result["score_profile_label"] = config.label
    result["score_weight_hz_position"] = config.weights["hz_position"]
    result["score_weight_planet_size"] = config.weights["planet_size"]
    result["score_weight_stellar_context"] = config.weights["stellar_context"]
    result["score_weight_data_quality"] = config.weights["data_quality"]
    result["score_weight_followup_readiness"] = config.weights["followup_readiness"]
    return result.sort_values(["score_total", "pl_name"], ascending=[False, True]).reset_index(drop=True)
