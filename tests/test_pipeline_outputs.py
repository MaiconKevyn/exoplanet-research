import json
from pathlib import Path

import pandas as pd

from exoplanets_research.data.archive import build_pscomppars_tap_query, load_planetary_systems_csv
from exoplanets_research.pipeline import run_pipeline


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


def test_pipeline_writes_ranked_outputs_with_provenance(tmp_path):
    df = pd.DataFrame(
        [
            {"pl_name": "A b", "hostname": "A", "default_flag": 1, "pl_orbsmax": 1.0, "pl_rade": 1.0, "pl_masse": 1.0, "st_teff": 5778, "st_rad": 1.0, "st_lum": 0.0, "sy_dist": 10.0},
            {"pl_name": "A b", "hostname": "A", "default_flag": 0, "pl_orbsmax": 1.1, "pl_rade": 1.1, "pl_masse": None, "st_teff": 5778, "st_rad": 1.0, "st_lum": 0.0, "sy_dist": 10.0},
            {"pl_name": "B b", "hostname": "B", "default_flag": 1, "pl_orbsmax": 0.03, "pl_rade": 3.0, "pl_masse": None, "st_teff": 2500, "st_rad": None, "st_lum": -3.0, "sy_dist": 30.0},
        ]
    )
    input_path = tmp_path / "input.csv"
    output_root = tmp_path / "out"
    frontend_root = tmp_path / "frontend"
    df.to_csv(input_path, index=False)

    outputs = run_pipeline(input_path=input_path, output_root=output_root, frontend_root=frontend_root, stage="all")

    ranked_path = outputs["ranked"]
    provenance_path = outputs["ranked_provenance"]
    frontend_path = outputs["frontend_json"]

    ranked = pd.read_csv(ranked_path)
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))

    assert list(ranked["pl_name"]) == ["A b", "B b"]
    assert ranked.loc[0, "score_total"] >= ranked.loc[1, "score_total"]
    assert {"score_mean", "score_std", "rank_median", "rank_p05", "rank_p95", "top10_probability"}.issubset(
        ranked.columns
    )
    assert provenance["row_count"] == 2
    assert provenance["generated_by"] == "src/exoplanets_research/pipeline.py"
    assert frontend_path.exists()


def test_pipeline_writes_uncertainty_outputs(tmp_path):
    df = pd.DataFrame(
        [
            {
                "pl_name": "A b",
                "hostname": "A",
                "default_flag": 1,
                "pl_orbsmax": 1.0,
                "pl_orbsmaxerr1": 0.01,
                "pl_orbsmaxerr2": -0.01,
                "pl_rade": 1.0,
                "pl_radeerr1": 0.01,
                "pl_radeerr2": -0.01,
                "pl_masse": 1.0,
                "st_teff": 5778,
                "st_tefferr1": 10,
                "st_tefferr2": -10,
                "st_rad": 1.0,
                "st_lum": 0.0,
                "st_lumerr1": 0.01,
                "st_lumerr2": -0.01,
                "sy_dist": 10.0,
            },
            {
                "pl_name": "B b",
                "hostname": "B",
                "default_flag": 1,
                "pl_orbsmax": 0.03,
                "pl_orbsmaxerr1": 0.001,
                "pl_orbsmaxerr2": -0.001,
                "pl_rade": 3.0,
                "pl_radeerr1": 0.1,
                "pl_radeerr2": -0.1,
                "pl_masse": None,
                "st_teff": 2500,
                "st_tefferr1": 20,
                "st_tefferr2": -20,
                "st_rad": None,
                "st_lum": -3.0,
                "st_lumerr1": 0.01,
                "st_lumerr2": -0.01,
                "sy_dist": 30.0,
            },
        ]
    )
    input_path = tmp_path / "input.csv"
    output_root = tmp_path / "out"
    frontend_root = tmp_path / "frontend"
    df.to_csv(input_path, index=False)

    outputs = run_pipeline(
        input_path=input_path,
        output_root=output_root,
        frontend_root=frontend_root,
        stage="all",
        uncertainty_runs=2,
        uncertainty_seed=7,
    )

    samples = pd.read_csv(outputs["uncertainty_samples"])
    summary = pd.read_csv(outputs["rank_uncertainty"])
    ranked = pd.read_csv(outputs["ranked"])

    assert set(samples["run_id"]) == {0, 1}
    assert {"score_mean", "rank_median", "rank_p05", "rank_p95", "top10_probability"}.issubset(summary.columns)
    assert ranked["score_mean"].notna().all()
    assert ranked["top10_probability"].notna().all()


def test_pipeline_accepts_score_profile_override(tmp_path):
    df = pd.DataFrame(
        [
            {
                "pl_name": "A b",
                "hostname": "A",
                "default_flag": 1,
                "pl_orbsmax": 1.0,
                "pl_rade": 1.0,
                "pl_masse": 1.0,
                "st_teff": 5778,
                "st_rad": 1.0,
                "st_lum": 0.0,
                "sy_dist": 10.0,
            }
        ]
    )
    input_path = tmp_path / "input.csv"
    output_root = tmp_path / "out"
    frontend_root = tmp_path / "frontend"
    score_profile = tmp_path / "score.yml"
    df.to_csv(input_path, index=False)
    score_profile.write_text(
        """
id: test_profile
label: Test Profile
description: Test score profile.
weights:
  hz_position: 0.20
  planet_size: 0.20
  stellar_context: 0.20
  data_quality: 0.20
  followup_readiness: 0.20
penalties:
  missing_field: 0.05
  max_missing_data: 0.25
confidence:
  moderate_min_data_quality: 0.85
  limited_min_data_quality: 0.60
non_claim: No biosignature inference is made; this ranking prioritizes candidates for further observation and modeling.
""",
        encoding="utf-8",
    )

    outputs = run_pipeline(
        input_path=input_path,
        output_root=output_root,
        frontend_root=frontend_root,
        stage="all",
        score_profile=score_profile,
    )

    ranked = pd.read_csv(outputs["ranked"])
    assert ranked.loc[0, "score_profile_id"] == "test_profile"
    assert ranked.loc[0, "score_weight_hz_position"] == 0.20


def test_pipeline_can_export_paper_artifacts(tmp_path, monkeypatch):
    df = pd.DataFrame(
        [
            {
                "pl_name": "A b",
                "hostname": "A",
                "default_flag": 1,
                "pl_orbsmax": 1.0,
                "pl_rade": 1.0,
                "pl_masse": 1.0,
                "st_teff": 5778,
                "st_rad": 1.0,
                "st_lum": 0.0,
                "sy_dist": 10.0,
            },
            {
                "pl_name": "B b",
                "hostname": "B",
                "default_flag": 1,
                "pl_orbsmax": 1.2,
                "pl_rade": 1.2,
                "pl_masse": 2.0,
                "st_teff": 5600,
                "st_rad": 1.0,
                "st_lum": 0.0,
                "sy_dist": 20.0,
            },
        ]
    )
    monkeypatch.chdir(tmp_path)
    input_path = tmp_path / "input.csv"
    experiment_config = tmp_path / "configs/experiments/paper_v1.yml"
    input_path.write_text(df.to_csv(index=False), encoding="utf-8")
    experiment_config.parent.mkdir(parents=True)
    experiment_config.write_text(
        """
id: test_paper
outputs:
  directory: data/outputs/experiments/test_paper
""",
        encoding="utf-8",
    )

    outputs = run_pipeline(
        input_path=input_path,
        output_root=Path("data"),
        frontend_root=Path("frontend"),
        stage="all",
        paper_artifacts=True,
        experiment_config=experiment_config,
    )

    assert any(name.startswith("paper_artifact_") for name in outputs)
    assert Path("paper/tables/top_candidates.md").exists()
    assert Path("data/outputs/experiments/test_paper/paper_artifacts.yml").exists()
