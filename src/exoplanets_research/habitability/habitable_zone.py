import math

import pandas as pd


HZ_MODEL = "simple_luminosity_kasting_like_baseline"


def luminosity_from_log_luminosity(st_lum: float) -> float:
    return 10**st_lum


def simple_habitable_zone_from_log_luminosity(st_lum: float) -> tuple[float, float]:
    luminosity = luminosity_from_log_luminosity(st_lum)
    inner = math.sqrt(luminosity / 1.1)
    outer = math.sqrt(luminosity / 0.53)
    return inner, outer


def add_habitable_zone_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    if "st_lum" not in result.columns:
        result["st_lum"] = pd.NA
    if "pl_orbsmax" not in result.columns:
        result["pl_orbsmax"] = pd.NA

    result["hz_inner"] = float("nan")
    result["hz_outer"] = float("nan")
    result["hz_model"] = pd.NA
    result["habitable_zone_status"] = "unknown"

    valid_luminosity = result["st_lum"].notna()
    for index, st_lum in result.loc[valid_luminosity, "st_lum"].items():
        inner, outer = simple_habitable_zone_from_log_luminosity(float(st_lum))
        result.at[index, "hz_inner"] = inner
        result.at[index, "hz_outer"] = outer
        result.at[index, "hz_model"] = HZ_MODEL

    valid_orbit = result["pl_orbsmax"].notna() & result["hz_inner"].notna() & result["hz_outer"].notna()
    inside = valid_orbit & (result["pl_orbsmax"] >= result["hz_inner"]) & (result["pl_orbsmax"] <= result["hz_outer"])
    outside = valid_orbit & ~inside
    result.loc[inside, "habitable_zone_status"] = "inside"
    result.loc[outside, "habitable_zone_status"] = "outside"
    return result
