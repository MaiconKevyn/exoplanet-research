from dataclasses import dataclass
from pathlib import Path

import yaml

from exoplanets_research.config import PROJECT_ROOT


DEFAULT_SCORING_CONFIG_PATH = PROJECT_ROOT / "configs" / "scoring" / "ectp_v1.yml"


@dataclass(frozen=True)
class ScoringConfig:
    id: str
    label: str
    description: str
    weights: dict[str, float]
    penalties: dict[str, float]
    confidence: dict[str, float]
    non_claim: str


def load_scoring_config(path: Path = DEFAULT_SCORING_CONFIG_PATH) -> ScoringConfig:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    weights = {key: float(value) for key, value in payload["weights"].items()}
    total_weight = sum(weights.values())
    if round(total_weight, 8) != 1.0:
        raise ValueError(f"Scoring weights must sum to 1.0, got {total_weight}")
    return ScoringConfig(
        id=str(payload["id"]),
        label=str(payload["label"]),
        description=str(payload["description"]),
        weights=weights,
        penalties={key: float(value) for key, value in payload["penalties"].items()},
        confidence={key: float(value) for key, value in payload["confidence"].items()},
        non_claim=str(payload["non_claim"]),
    )
