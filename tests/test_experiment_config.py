from pathlib import Path

import yaml


def test_paper_v1_manifest_has_required_experiments():
    payload = yaml.safe_load(Path("configs/experiments/paper_v1.yml").read_text())

    assert payload["id"] == "paper_v1"
    assert "kopparapu_conservative_earth_mass" in payload["hz_models"]
    assert payload["uncertainty"]["runs"] >= 500
    assert 10 in payload["top_k"]
