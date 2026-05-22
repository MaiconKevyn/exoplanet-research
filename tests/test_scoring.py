import pandas as pd

from exoplanets_research.data.cleaning import select_best_planet_records
from exoplanets_research.habitability.features import add_habitability_features
from exoplanets_research.habitability.habitable_zone import add_habitable_zone_columns
from exoplanets_research.habitability.scoring import score_candidates


def test_select_best_planet_records_prefers_default_record():
    df = pd.DataFrame(
        [
            {"pl_name": "TOI-700 d", "default_flag": 0, "pl_rade": 1.2, "pl_masse": None, "pl_orbsmax": 0.16, "st_teff": 3480, "st_rad": 0.42, "st_lum": -1.7},
            {"pl_name": "TOI-700 d", "default_flag": 1, "pl_rade": 1.1, "pl_masse": 1.7, "pl_orbsmax": 0.163, "st_teff": 3459, "st_rad": 0.42, "st_lum": -1.65},
            {"pl_name": "Kepler-442 b", "default_flag": 1, "pl_rade": 1.34, "pl_masse": 2.3, "pl_orbsmax": 0.409, "st_teff": 4402, "st_rad": 0.6, "st_lum": -0.7},
        ]
    )

    result = select_best_planet_records(df)

    toi = result[result["pl_name"] == "TOI-700 d"].iloc[0]
    assert len(result) == 2
    assert toi["default_flag"] == 1
    assert toi["duplicate_record_count"] == 2
    assert toi["selected_record_reason"] == "default_flag"


def test_scoring_outputs_subscores_and_conservative_caveat():
    df = pd.DataFrame(
        [
            {
                "pl_name": "Kepler-442 b",
                "hostname": "Kepler-442",
                "default_flag": 1,
                "pl_rade": 1.34,
                "pl_masse": 2.3,
                "pl_orbsmax": 0.409,
                "st_teff": 4402,
                "st_rad": 0.6,
                "st_lum": -0.65,
                "sy_dist": 370.0,
            }
        ]
    )

    scored = score_candidates(add_habitability_features(add_habitable_zone_columns(df)))
    row = scored.iloc[0]

    assert row["interpretation_label"] == "habitability_followup_candidate"
    assert "No biosignature inference is made" in row["interpretation_caveat"]
    assert row["score_total"] > 0.5
    assert 0 <= row["score_hz_position"] <= 1
    assert 0 <= row["score_data_quality"] <= 1
    assert row["score_profile_id"] == "ectp_v1"
    assert row["score_weight_hz_position"] == 0.35


def test_known_candidates_survive_deduplication_and_scoring():
    raw = pd.read_csv("data/processed_exoplanet_data.csv", low_memory=False)
    canonical = select_best_planet_records(raw)
    scored = score_candidates(add_habitability_features(add_habitable_zone_columns(canonical)))
    names = set(scored["pl_name"])

    assert {"Kepler-442 b", "Kepler-22 b", "TRAPPIST-1 e", "TOI-700 d"}.issubset(names)
