import json
from datetime import UTC, datetime
from pathlib import Path


def write_provenance(path: Path, *, input_file: Path, row_count: int, stage: str, generated_by: str) -> None:
    payload = {
        "source": "NASA Exoplanet Archive",
        "input_file": str(input_file),
        "row_count": row_count,
        "stage": stage,
        "generated_by": generated_by,
        "generated_at_utc": datetime.now(UTC).isoformat(),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
