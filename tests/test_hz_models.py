import math

import pandas as pd

from exoplanets_research.habitability.hz_models import calculate_hz_bounds, supported_hz_models


def test_supported_hz_models_include_baseline_and_kopparapu_profiles():
    assert {
        "simple_luminosity_baseline",
        "kopparapu_conservative_earth_mass",
        "kopparapu_optimistic_earth_mass",
    }.issubset(set(supported_hz_models()))


def test_simple_luminosity_baseline_preserves_current_solar_case():
    bounds = calculate_hz_bounds(st_lum=0.0, st_teff=5778, model="simple_luminosity_baseline")

    assert math.isclose(bounds.inner_au, math.sqrt(1 / 1.1), rel_tol=1e-12)
    assert math.isclose(bounds.outer_au, math.sqrt(1 / 0.53), rel_tol=1e-12)
    assert bounds.model == "simple_luminosity_baseline"


def test_kopparapu_conservative_returns_solar_like_bounds():
    bounds = calculate_hz_bounds(st_lum=0.0, st_teff=5780, model="kopparapu_conservative_earth_mass")

    assert 0.90 <= bounds.inner_au <= 1.05
    assert 1.55 <= bounds.outer_au <= 1.80
    assert bounds.inner_limit == "runaway_greenhouse"
    assert bounds.outer_limit == "maximum_greenhouse"


def test_invalid_or_missing_inputs_return_unknown_bounds():
    bounds = calculate_hz_bounds(st_lum=pd.NA, st_teff=5780, model="kopparapu_conservative_earth_mass")

    assert pd.isna(bounds.inner_au)
    assert pd.isna(bounds.outer_au)
    assert bounds.model == "kopparapu_conservative_earth_mass"
