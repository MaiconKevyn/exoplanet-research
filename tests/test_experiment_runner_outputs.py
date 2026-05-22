import pandas as pd

from exoplanets_research.experiments import run_ablation


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
    monkeypatch.setattr(run_ablation, "build_ranked_candidates", fake_build_ranked_candidates)

    hz_summary, hz_outputs = run_ablation.run_hz_model_comparison(manifest, tmp_path / "outputs")
    baseline_summary, baseline_outputs = run_ablation.run_baseline_comparison(manifest, tmp_path / "outputs")

    assert list(hz_summary["hz_model"]) == ["simple_luminosity_baseline", "kopparapu_conservative_earth_mass"]
    assert hz_summary.loc[1, "top_2_overlap"] == 1.0
    assert baseline_summary.loc[0, "baseline"] == "hz_radius_baseline"
    for path in [*hz_outputs, *baseline_outputs]:
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

    summary, outputs = run_ablation.run_external_validation(manifest, tmp_path / "outputs")

    assert summary.loc[0, "target_hosts"] == 1
    assert summary.loc[0, "matched_candidates"] == 1
    for path in outputs:
        assert path.exists()
