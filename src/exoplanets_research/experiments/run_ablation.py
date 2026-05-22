import argparse
from pathlib import Path

import yaml


def load_experiment_manifest(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run paper-grade ECTP experiments.")
    parser.add_argument("--config", type=Path, default=Path("configs/experiments/paper_v1.yml"))
    args = parser.parse_args()
    manifest = load_experiment_manifest(args.config)
    output_dir = Path(manifest["outputs"]["directory"])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manifest_resolved.yml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    print(f"experiment_id: {manifest['id']}")
    print(f"output_dir: {output_dir}")


if __name__ == "__main__":
    main()
