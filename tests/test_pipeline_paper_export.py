from pathlib import Path

import pandas as pd

from exoplanets_research.pipeline import run_pipeline


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
