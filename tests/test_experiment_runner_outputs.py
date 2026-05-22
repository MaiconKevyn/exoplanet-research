from pathlib import Path

import pandas as pd

from exoplanets_research.experiments import comparisons, external_validation


def _ranked(names: list[str]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "pl_name": names,
            "hostname": [name.split()[0] for name in names],
            "score_total": [1.0 - index * 0.1 for index in range(len(names))],
            "habitable_zone_status": ["inside", "inside", "outside"][: len(names)],
            "pl_rade": [1.0, 1.4, 2.5][: len(names)],
        }
    )


def test_hz_and_baseline_comparison_write_outputs(tmp_path, monkeypatch):
    manifest = {
        "input": "unused.csv",
        "hz_models": ["simple_luminosity_baseline", "kopparapu_conservative_earth_mass"],
        "top_k": [2],
    }

    def fake_build_ranked_candidates(input_path, *, hz_model):
        if hz_model == "kopparapu_conservative_earth_mass":
            return _ranked(["B b", "A b", "C b"])
        return _ranked(["A b", "B b", "C b"])

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(comparisons, "build_ranked_candidates", fake_build_ranked_candidates)

    hz_summary, hz_outputs = comparisons.run_hz_model_comparison(manifest, tmp_path / "outputs")
    baseline_summary, baseline_outputs = comparisons.run_baseline_comparison(manifest, tmp_path / "outputs")

    assert list(hz_summary["hz_model"]) == ["simple_luminosity_baseline", "kopparapu_conservative_earth_mass"]
    assert hz_summary.loc[1, "top_2_overlap"] == 1.0
    assert set(baseline_summary["baseline"]) == {"hz_radius_baseline", "followup_readiness_baseline"}
    for path in [*hz_outputs, *baseline_outputs]:
        assert path.exists()


def test_score_sensitivity_writes_profile_comparisons(tmp_path, monkeypatch):
    manifest = {
        "input": "unused.csv",
        "hz_models": ["simple_luminosity_baseline"],
        "score_profiles": [str(Path(__file__).resolve().parents[1] / "configs/scoring/ectp_v1.yml")],
        "top_k": [2],
    }
    featured = pd.DataFrame(
        {
            "pl_name": ["A b", "B b", "C b"],
            "hostname": ["A", "B", "C"],
            "habitable_zone_status": ["inside", "inside", "outside"],
            "hz_center_offset": [0.1, 0.5, pd.NA],
            "pl_rade": [1.0, 1.4, 2.5],
            "pl_masse": [1.0, 2.0, pd.NA],
            "st_teff": [5778, 5000, 3000],
            "st_rad": [1.0, 0.8, 0.2],
            "st_lum": [0.0, -0.2, -2.0],
            "followup_readiness_score": [0.6, 0.9, 0.7],
        }
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(comparisons, "build_featured_candidates", lambda input_path, *, hz_model: featured)

    summary, outputs = comparisons.run_score_sensitivity(manifest, tmp_path / "outputs")

    assert {"ectp_v1", "ectp_hz_emphasis", "ectp_followup_emphasis", "ectp_data_quality_emphasis"} == set(
        summary["score_profile"]
    )
    for path in outputs:
        assert path.exists()


def test_external_validation_writes_crossmatch_outputs(tmp_path, monkeypatch):
    manifest = {
        "id": "test",
        "external_targets": {
            "target_list": "hwo_exep_2023",
            "table_name": "DI_STARS_EXEP",
            "path": "data/external/hwo_exep_2023.csv",
            "download": False,
        },
    }
    monkeypatch.chdir(tmp_path)
    ranked_path = tmp_path / "data/outputs/astrobiology_ranked_candidates.csv"
    target_path = tmp_path / "data/external/hwo_exep_2023.csv"
    ranked_path.parent.mkdir(parents=True)
    target_path.parent.mkdir(parents=True)
    _ranked(["A b", "B b", "C b"]).to_csv(ranked_path, index=False)
    pd.DataFrame({"hostname": ["B"], "target_list": ["hwo_exep_2023"]}).to_csv(target_path, index=False)

    summary, outputs = external_validation.run_external_validation(manifest, tmp_path / "outputs")

    assert summary.loc[0, "target_hosts"] == 1
    assert summary.loc[0, "matched_candidates"] == 1
    for path in outputs:
        assert path.exists()
