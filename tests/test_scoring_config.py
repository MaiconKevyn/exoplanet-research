from pathlib import Path

from exoplanets_research.habitability.scoring_config import load_scoring_config


def test_load_scoring_config_has_normalized_weights():
    config = load_scoring_config(Path("configs/scoring/ectp_v1.yml"))

    assert config.id == "ectp_v1"
    assert round(sum(config.weights.values()), 8) == 1.0
    assert config.penalties["max_missing_data"] == 0.25
    assert "No biosignature inference" in config.non_claim
