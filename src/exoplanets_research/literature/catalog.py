from collections import defaultdict
from pathlib import Path

import yaml

from exoplanets_research.literature.schema import validate_source


def load_sources(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or []

    if not isinstance(data, list):
        raise ValueError("Literature registry must be a YAML list.")

    for source in data:
        if not isinstance(source, dict):
            raise ValueError("Every literature source must be a mapping.")
        validate_source(source)

    return data


def group_sources_by_category(sources: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for source in sources:
        grouped[source["category"]].append(source)
    return dict(grouped)

