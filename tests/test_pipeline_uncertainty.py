import pandas as pd

from exoplanets_research.pipeline import run_pipeline


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
