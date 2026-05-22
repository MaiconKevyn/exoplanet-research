from pathlib import Path

from exoplanets_research.data.archive import build_pscomppars_tap_query, load_planetary_systems_csv


def test_load_planetary_systems_csv_handles_nasa_metadata_rows():
    df = load_planetary_systems_csv(Path("data/PS_2025.06.22_09.41.26.csv"))

    assert len(df) == 38500
    assert {"pl_name", "hostname", "pl_orbsmax", "st_lum"}.issubset(df.columns)


def test_build_pscomppars_tap_query_includes_required_fields():
    query = build_pscomppars_tap_query()

    assert "select" in query.lower()
    assert "pscomppars" in query.lower()
    for column in ["pl_name", "hostname", "pl_orbsmax", "pl_rade", "st_teff", "sy_dist"]:
        assert column in query
