import math

import pandas as pd

from exoplanets_research.habitability.habitable_zone import (
    add_habitable_zone_columns,
    simple_habitable_zone_from_log_luminosity,
)


def test_simple_habitable_zone_matches_existing_artifact():
    existing = pd.read_csv(
        "data/habitable_zone_calculated.csv",
        usecols=["st_lum", "hz_inner", "hz_outer"],
        low_memory=False,
    ).dropna().head(20)

    for row in existing.itertuples(index=False):
        inner, outer = simple_habitable_zone_from_log_luminosity(row.st_lum)
        assert math.isclose(inner, row.hz_inner, rel_tol=0, abs_tol=1e-8)
        assert math.isclose(outer, row.hz_outer, rel_tol=0, abs_tol=1e-8)


def test_add_habitable_zone_columns_labels_inside_and_outside_orbits():
    df = pd.DataFrame(
        [
            {"pl_name": "inside", "st_lum": 0.0, "pl_orbsmax": 1.0},
            {"pl_name": "outside", "st_lum": 0.0, "pl_orbsmax": 0.1},
            {"pl_name": "missing", "st_lum": None, "pl_orbsmax": 1.0},
        ]
    )

    result = add_habitable_zone_columns(df)

    assert result.loc[0, "habitable_zone_status"] == "inside"
    assert result.loc[1, "habitable_zone_status"] == "outside"
    assert result.loc[2, "habitable_zone_status"] == "unknown"
    assert set(result["hz_model"].dropna()) == {"simple_luminosity_kasting_like_baseline"}
