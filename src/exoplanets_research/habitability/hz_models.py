from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Literal

import pandas as pd


HZModelName = Literal[
    "simple_luminosity_baseline",
    "kopparapu_conservative_earth_mass",
    "kopparapu_optimistic_earth_mass",
]


@dataclass(frozen=True)
class HZBounds:
    model: str
    inner_au: float
    outer_au: float
    inner_limit: str
    outer_limit: str


def supported_hz_models() -> list[str]:
    return [
        "simple_luminosity_baseline",
        "kopparapu_conservative_earth_mass",
        "kopparapu_optimistic_earth_mass",
    ]


def _is_missing(value: object) -> bool:
    return bool(pd.isna(value))


def _luminosity_from_log10(st_lum: float) -> float:
    return 10 ** float(st_lum)


def _nan_bounds(model: str, inner_limit: str, outer_limit: str) -> HZBounds:
    return HZBounds(
        model=model,
        inner_au=float("nan"),
        outer_au=float("nan"),
        inner_limit=inner_limit,
        outer_limit=outer_limit,
    )


def _simple_luminosity_baseline(st_lum: float) -> HZBounds:
    luminosity = _luminosity_from_log10(st_lum)
    return HZBounds(
        model="simple_luminosity_baseline",
        inner_au=sqrt(luminosity / 1.1),
        outer_au=sqrt(luminosity / 0.53),
        inner_limit="simple_inner_flux",
        outer_limit="simple_outer_flux",
    )


def _kopparapu_seff(st_teff: float, limit: str) -> float:
    # Coefficients from Kopparapu et al. 2014 for 1 Earth-mass HZ boundaries.
    coefficients = {
        "recent_venus": (1.776, 2.136e-4, 2.533e-8, -1.332e-11, -3.097e-15),
        "runaway_greenhouse": (1.107, 1.332e-4, 1.58e-8, -8.308e-12, -1.931e-15),
        "maximum_greenhouse": (0.356, 6.171e-5, 1.698e-9, -3.198e-12, -5.575e-16),
        "early_mars": (0.32, 5.547e-5, 1.526e-9, -2.874e-12, -5.011e-16),
    }
    seff_sun, a, b, c, d = coefficients[limit]
    t_star = float(st_teff) - 5780.0
    return seff_sun + (a * t_star) + (b * t_star**2) + (c * t_star**3) + (d * t_star**4)


def _kopparapu(st_lum: float, st_teff: float, *, model: str, inner_limit: str, outer_limit: str) -> HZBounds:
    if st_teff < 2600 or st_teff > 7200:
        return _nan_bounds(model, inner_limit, outer_limit)
    luminosity = _luminosity_from_log10(st_lum)
    inner_flux = _kopparapu_seff(st_teff, inner_limit)
    outer_flux = _kopparapu_seff(st_teff, outer_limit)
    if inner_flux <= 0 or outer_flux <= 0:
        return _nan_bounds(model, inner_limit, outer_limit)
    return HZBounds(
        model=model,
        inner_au=sqrt(luminosity / inner_flux),
        outer_au=sqrt(luminosity / outer_flux),
        inner_limit=inner_limit,
        outer_limit=outer_limit,
    )


def calculate_hz_bounds(
    st_lum: float,
    st_teff: float | None,
    model: HZModelName = "simple_luminosity_baseline",
) -> HZBounds:
    if model not in supported_hz_models():
        raise ValueError(f"Unsupported HZ model: {model}")
    if _is_missing(st_lum):
        if model == "kopparapu_optimistic_earth_mass":
            return _nan_bounds(model, "recent_venus", "early_mars")
        if model == "kopparapu_conservative_earth_mass":
            return _nan_bounds(model, "runaway_greenhouse", "maximum_greenhouse")
        return _nan_bounds(model, "simple_inner_flux", "simple_outer_flux")
    if model == "simple_luminosity_baseline":
        return _simple_luminosity_baseline(float(st_lum))
    if _is_missing(st_teff):
        if model == "kopparapu_optimistic_earth_mass":
            return _nan_bounds(model, "recent_venus", "early_mars")
        return _nan_bounds(model, "runaway_greenhouse", "maximum_greenhouse")
    if model == "kopparapu_conservative_earth_mass":
        return _kopparapu(
            float(st_lum),
            float(st_teff),
            model=model,
            inner_limit="runaway_greenhouse",
            outer_limit="maximum_greenhouse",
        )
    return _kopparapu(
        float(st_lum),
        float(st_teff),
        model=model,
        inner_limit="recent_venus",
        outer_limit="early_mars",
    )
