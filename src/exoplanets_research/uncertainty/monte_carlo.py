from __future__ import annotations

import numpy as np
import pandas as pd

from exoplanets_research.habitability.features import add_habitability_features
from exoplanets_research.habitability.habitable_zone import add_habitable_zone_columns
from exoplanets_research.habitability.scoring import score_candidates
from exoplanets_research.habitability.scoring_config import ScoringConfig


UNCERTAINTY_COLUMNS = ["pl_orbsmax", "pl_rade", "pl_masse", "st_teff", "st_rad", "st_lum"]
NON_NEGATIVE_COLUMNS = {"pl_orbsmax", "pl_rade", "pl_masse", "st_teff", "st_rad"}


def sample_asymmetric_normal(
    value: float,
    err_plus: float | None,
    err_minus: float | None,
    *,
    rng,
) -> float:
    if pd.isna(value):
        return value
    sigma_plus = abs(float(err_plus)) if not pd.isna(err_plus) else 0.0
    sigma_minus = abs(float(err_minus)) if not pd.isna(err_minus) else sigma_plus
    sigma = max(sigma_plus, sigma_minus)
    if sigma == 0:
        return float(value)
    return float(rng.normal(float(value), sigma))


def sample_catalog_measurements(df: pd.DataFrame, *, rng: np.random.Generator) -> pd.DataFrame:
    sampled = df.copy()
    for column in UNCERTAINTY_COLUMNS:
        if column not in sampled.columns:
            continue
        err_plus = f"{column}err1"
        err_minus = f"{column}err2"
        if err_plus not in sampled.columns and err_minus not in sampled.columns:
            continue
        sampled[column] = sampled.apply(
            lambda row: sample_asymmetric_normal(
                row.get(column),
                row.get(err_plus, pd.NA),
                row.get(err_minus, pd.NA),
                rng=rng,
            ),
            axis=1,
        )
        if column in NON_NEGATIVE_COLUMNS:
            sampled[column] = sampled[column].clip(lower=0)
    return sampled


def summarize_rank_uncertainty(samples: pd.DataFrame, *, top_k: int = 10) -> pd.DataFrame:
    ranked = samples.copy()
    ranked["rank"] = ranked.groupby("run_id")["score_total"].rank(method="first", ascending=False)
    summary = (
        ranked.groupby("pl_name")
        .agg(
            score_mean=("score_total", "mean"),
            score_std=("score_total", "std"),
            rank_median=("rank", "median"),
            rank_p05=("rank", lambda values: values.quantile(0.05)),
            rank_p95=("rank", lambda values: values.quantile(0.95)),
            top_probability=("rank", lambda values: (values <= top_k).mean()),
        )
        .reset_index()
    )
    summary = summary.rename(columns={"top_probability": f"top{top_k}_probability"})
    return summary.sort_values(["rank_median", "score_mean"], ascending=[True, False]).reset_index(drop=True)


def generate_uncertainty_samples(
    canonical: pd.DataFrame,
    *,
    runs: int,
    seed: int,
    hz_model: str,
    scoring_config: ScoringConfig | None = None,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    samples = []
    for run_id in range(runs):
        sampled = sample_catalog_measurements(canonical, rng=rng)
        hz = add_habitable_zone_columns(sampled, model=hz_model)
        hz = hz[hz["hz_inner"].notna() & hz["pl_orbsmax"].notna()].copy()
        featured = add_habitability_features(hz)
        scored = score_candidates(featured, config=scoring_config)
        scored["run_id"] = run_id
        scored["uncertainty_seed"] = seed
        samples.append(scored)
    if not samples:
        return pd.DataFrame()
    return pd.concat(samples, ignore_index=True)
