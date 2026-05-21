import pandas as pd


CRITICAL_SCORING_FIELDS = ["pl_orbsmax", "pl_rade", "pl_masse", "st_teff", "st_rad", "st_lum"]


def _radius_class(radius: float | None) -> str:
    if pd.isna(radius):
        return "unknown"
    if 0.5 <= float(radius) <= 1.5:
        return "terrestrial_size"
    if 1.5 < float(radius) <= 2.5:
        return "super_earth_or_mini_neptune"
    return "large_or_poor_rocky_candidate"


def _stellar_temperature_class(st_teff: float | None) -> str:
    if pd.isna(st_teff):
        return "unknown"
    value = float(st_teff)
    if 5200 <= value <= 6000:
        return "g_type_like"
    if 3700 <= value < 5200:
        return "k_type_like"
    if 2400 <= value < 3700:
        return "m_type_like"
    return "outside_preferred_range"


def _hz_center_offset(row: pd.Series) -> float | None:
    required = ["pl_orbsmax", "hz_inner", "hz_outer"]
    if any(pd.isna(row.get(column)) for column in required):
        return pd.NA
    inner = float(row["hz_inner"])
    outer = float(row["hz_outer"])
    if outer <= inner:
        return pd.NA
    center = (inner + outer) / 2
    half_width = (outer - inner) / 2
    return abs(float(row["pl_orbsmax"]) - center) / half_width


def _missing_critical_fields(row: pd.Series) -> str:
    missing = [column for column in CRITICAL_SCORING_FIELDS if pd.isna(row.get(column))]
    return ";".join(missing)


def _followup_readiness(row: pd.Series) -> float:
    score = 0.0
    distance = row.get("sy_dist")
    if not pd.isna(distance):
        distance = float(distance)
        if distance <= 50:
            score += 0.4
        elif distance <= 100:
            score += 0.3
        elif distance <= 250:
            score += 0.2
        else:
            score += 0.1

    radius = row.get("pl_rade")
    if not pd.isna(radius) and float(radius) <= 2.5:
        score += 0.2
    if not pd.isna(row.get("st_teff")):
        score += 0.15
    if not pd.isna(row.get("pl_orbsmax")):
        score += 0.15
    if not pd.isna(row.get("st_lum")):
        score += 0.1
    return min(score, 1.0)


def add_habitability_features(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for column in CRITICAL_SCORING_FIELDS + ["pl_insol", "sy_dist", "hz_inner", "hz_outer"]:
        if column not in result.columns:
            result[column] = pd.NA

    result["radius_class"] = result["pl_rade"].apply(_radius_class)
    result["stellar_temperature_class"] = result["st_teff"].apply(_stellar_temperature_class)
    result["mass_radius_data_quality"] = result[["pl_masse", "pl_rade"]].notna().sum(axis=1) / 2
    result["hz_center_offset"] = result.apply(_hz_center_offset, axis=1)
    result["insolation_available"] = result["pl_insol"].notna()
    result["stellar_context_available"] = result[["st_teff", "st_rad", "st_lum"]].notna().all(axis=1)
    result["followup_readiness_score"] = result.apply(_followup_readiness, axis=1)
    result["missing_critical_fields"] = result.apply(_missing_critical_fields, axis=1)
    return result

