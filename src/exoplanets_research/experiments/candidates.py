from pathlib import Path

import pandas as pd

from exoplanets_research.data.archive import load_planetary_systems_csv
from exoplanets_research.data.cleaning import select_best_planet_records
from exoplanets_research.habitability.features import add_habitability_features
from exoplanets_research.habitability.habitable_zone import add_habitable_zone_columns
from exoplanets_research.habitability.scoring import score_candidates


def build_featured_candidates(input_path: Path, *, hz_model: str) -> pd.DataFrame:
    raw = load_planetary_systems_csv(input_path)
    canonical = select_best_planet_records(raw)
    hz = add_habitable_zone_columns(canonical, model=hz_model)
    hz = hz[hz["hz_inner"].notna() & hz["pl_orbsmax"].notna()].copy()
    return add_habitability_features(hz)


def build_ranked_candidates(input_path: Path, *, hz_model: str) -> pd.DataFrame:
    return score_candidates(build_featured_candidates(input_path, hz_model=hz_model)).reset_index(drop=True)


def assign_rank(df: pd.DataFrame, column: str) -> pd.DataFrame:
    result = df.copy().reset_index(drop=True)
    result[column] = result.index + 1
    return result
