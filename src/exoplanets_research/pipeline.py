import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from exoplanets_research.config import DATA_DIR, FRONTEND_DATA_DIR
from exoplanets_research.data.archive import load_planetary_systems_csv
from exoplanets_research.data.cleaning import select_best_planet_records
from exoplanets_research.habitability.features import add_habitability_features
from exoplanets_research.habitability.habitable_zone import add_habitable_zone_columns
from exoplanets_research.habitability.scoring import score_candidates
from exoplanets_research.literature.catalog import load_sources


DEFAULT_INPUT = DATA_DIR / "PS_2025.06.22_09.41.26.csv"


def _write_provenance(path: Path, *, input_file: Path, row_count: int, stage: str) -> None:
    payload = {
        "source": "NASA Exoplanet Archive",
        "input_file": str(input_file),
        "row_count": row_count,
        "stage": stage,
        "generated_by": "src/exoplanets_research/pipeline.py",
        "generated_at_utc": datetime.now(UTC).isoformat(),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_frontend_json(csv_path: Path, frontend_root: Path) -> Path:
    frontend_root.mkdir(parents=True, exist_ok=True)
    output_path = frontend_root / "astrobiology_ranked_candidates.json"
    df = pd.read_csv(csv_path, low_memory=False)
    df.to_json(output_path, orient="records", indent=2)
    return output_path


def run_pipeline(
    *,
    input_path: Path = DEFAULT_INPUT,
    output_root: Path = DATA_DIR,
    frontend_root: Path = FRONTEND_DATA_DIR,
    stage: str = "all",
) -> dict[str, Path]:
    input_path = Path(input_path)
    output_root = Path(output_root)
    frontend_root = Path(frontend_root)
    processed_dir = output_root / "processed"
    outputs_dir = output_root / "outputs"
    processed_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, Path] = {}

    if stage == "literature":
        load_sources(DATA_DIR / "literature" / "astrobiology_sources.yml")
        return outputs

    raw = load_planetary_systems_csv(input_path)
    canonical = select_best_planet_records(raw)
    canonical_path = processed_dir / "canonical_exoplanets.csv"
    canonical.to_csv(canonical_path, index=False)
    canonical_provenance = processed_dir / "canonical_exoplanets.provenance.json"
    _write_provenance(canonical_provenance, input_file=input_path, row_count=len(canonical), stage="canonical")
    outputs["canonical"] = canonical_path
    outputs["canonical_provenance"] = canonical_provenance

    if stage == "canonical":
        return outputs

    hz = add_habitable_zone_columns(canonical)
    hz = hz[hz["hz_inner"].notna() & hz["pl_orbsmax"].notna()].copy()
    hz_path = processed_dir / "habitable_zone_exoplanets.csv"
    hz.to_csv(hz_path, index=False)
    outputs["habitable_zone"] = hz_path

    featured = add_habitability_features(hz)
    ranked = score_candidates(featured)
    ranked_path = outputs_dir / "astrobiology_ranked_candidates.csv"
    ranked.to_csv(ranked_path, index=False)
    ranked_provenance = outputs_dir / "astrobiology_ranked_candidates.provenance.json"
    _write_provenance(ranked_provenance, input_file=input_path, row_count=len(ranked), stage="score")
    outputs["ranked"] = ranked_path
    outputs["ranked_provenance"] = ranked_provenance

    if stage in {"score", "all", "export-frontend"}:
        outputs["frontend_json"] = _write_frontend_json(ranked_path, frontend_root)

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the astrobiology research pipeline.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--stage", choices=["all", "literature", "canonical", "score", "export-frontend"], default="all")
    args = parser.parse_args()

    outputs = run_pipeline(input_path=args.input, stage=args.stage)
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
