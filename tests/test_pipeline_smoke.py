import json

import pandas as pd

from exoplanets_research.pipeline import run_pipeline


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
