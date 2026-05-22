import pandas as pd

from exoplanets_research.habitability.hz_models import calculate_hz_bounds

HZ_MODEL = "simple_luminosity_baseline"


def luminosity_from_log_luminosity(st_lum: float) -> float:
    return 10**st_lum


def simple_habitable_zone_from_log_luminosity(st_lum: float) -> tuple[float, float]:
    bounds = calculate_hz_bounds(st_lum=st_lum, st_teff=None, model="simple_luminosity_baseline")
    return bounds.inner_au, bounds.outer_au


def add_habitable_zone_columns(df: pd.DataFrame, *, model: str = HZ_MODEL) -> pd.DataFrame:
    result = df.copy()
    if "st_lum" not in result.columns:
        result["st_lum"] = pd.NA
    if "st_teff" not in result.columns:
        result["st_teff"] = pd.NA
    if "pl_orbsmax" not in result.columns:
        result["pl_orbsmax"] = pd.NA

    result["hz_inner"] = float("nan")
    result["hz_outer"] = float("nan")
    result["hz_model"] = pd.NA
    result["hz_inner_limit"] = pd.NA
    result["hz_outer_limit"] = pd.NA
    result["habitable_zone_status"] = "unknown"

    valid_luminosity = result["st_lum"].notna()
    for index, row in result.loc[valid_luminosity].iterrows():
        bounds = calculate_hz_bounds(st_lum=row.get("st_lum"), st_teff=row.get("st_teff"), model=model)
        result.at[index, "hz_inner"] = bounds.inner_au
        result.at[index, "hz_outer"] = bounds.outer_au
        result.at[index, "hz_model"] = bounds.model
        result.at[index, "hz_inner_limit"] = bounds.inner_limit
        result.at[index, "hz_outer_limit"] = bounds.outer_limit

    valid_orbit = result["pl_orbsmax"].notna() & result["hz_inner"].notna() & result["hz_outer"].notna()
    inside = valid_orbit & (result["pl_orbsmax"] >= result["hz_inner"]) & (result["pl_orbsmax"] <= result["hz_outer"])
    outside = valid_orbit & ~inside
    result.loc[inside, "habitable_zone_status"] = "inside"
    result.loc[outside, "habitable_zone_status"] = "outside"
    return result
