import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from exoplanets_research.paper.figures import write_markdown_table
from exoplanets_research.validation.external_targets import (
    HWO_EXEP_TABLE,
    add_host_target_flags,
    download_mission_star_table,
    load_external_targets,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_external_validation(manifest: dict, output_dir: Path) -> tuple[pd.DataFrame, list[Path]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ranked_path = Path("data/outputs/astrobiology_ranked_candidates.csv")
    if not ranked_path.exists():
        return pd.DataFrame(), []
    external_config = manifest.get("external_targets", {})
    target_path = Path(external_config.get("path", "data/external/hwo_exep_2023.csv"))
    if not target_path.exists() and external_config.get("download", True):
        download_mission_star_table(
            target_path,
            table_name=external_config.get("table_name", HWO_EXEP_TABLE),
            target_list=external_config.get("target_list", "hwo_exep_2023"),
        )

    if not target_path.exists():
        return pd.DataFrame(), []

    ranked = pd.read_csv(ranked_path, low_memory=False)
    targets = load_external_targets(target_path, target_list=external_config.get("target_list", "hwo_exep_2023"))
    annotated = add_host_target_flags(ranked, targets)
    matched = annotated[annotated["external_target_match"] == True].copy()  # noqa: E712
    matched.insert(0, "ectp_rank", matched.index + 1)
    source_url = external_config.get("source_url", "https://exoplanetarchive.ipac.caltech.edu/docs/MissionStellar.html")
    download_date = datetime.now(UTC).date().isoformat()
    checksum = sha256_file(target_path)
    summary = pd.DataFrame(
        [
            {
                "target_list": external_config.get("target_list", "hwo_exep_2023"),
                "source_table": external_config.get("table_name", HWO_EXEP_TABLE),
                "source_url": source_url,
                "download_date": download_date,
                "sha256": checksum,
                "target_hosts": int(targets["hostname"].nunique()),
                "ranked_candidates": int(len(ranked)),
                "matched_candidates": int(len(matched)),
                "matched_top_25": int(matched["ectp_rank"].le(25).sum()) if not matched.empty else 0,
                "matched_top_50": int(matched["ectp_rank"].le(50).sum()) if not matched.empty else 0,
            }
        ]
    )
    validation_path = output_dir / "external_validation.csv"
    summary_path = output_dir / "external_validation_summary.csv"
    table_path = Path("paper/tables/external_validation_summary.md")
    validation_columns = [
        "pl_name",
        "hostname",
        "score_total",
        "evidence_confidence",
        "hz_model",
        "external_target_match",
        "external_target_lists",
    ]
    annotated.loc[:, [column for column in validation_columns if column in annotated.columns]].to_csv(
        validation_path,
        index=False,
    )
    summary.to_csv(summary_path, index=False)
    write_markdown_table(summary, table_path)
    return summary, [validation_path, summary_path, table_path]


def write_external_inventory(manifest: dict, output_path: Path) -> Path:
    external_config = manifest.get("external_targets", {})
    target_path = Path(external_config.get("path", "data/external/hwo_exep_2023.csv"))
    rows = "not downloaded"
    checksum = "not downloaded"
    if target_path.exists():
        rows = str(len(pd.read_csv(target_path, low_memory=False)))
        checksum = sha256_file(target_path)
    generated_at = datetime.now(UTC).date().isoformat()
    source_url = external_config.get("source_url", "https://exoplanetarchive.ipac.caltech.edu/docs/MissionStellar.html")
    tap_url = external_config.get("tap_url", "https://exoplanetarchive.ipac.caltech.edu/TAP/sync")
    text = f"""# External Data Inventory

Generated for experiment `{manifest["id"]}`.

| Dataset | Access | Source URL | Download date | Local path | Rows | SHA-256 | Processing command | Scientific role |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| HWO ExEP Precursor Science Stars | NASA Exoplanet Archive TAP table `{external_config.get("table_name", HWO_EXEP_TABLE)}` via `{tap_url}` | {source_url} | {generated_at} | `{target_path}` | {rows} | `{checksum}` | `.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml` | Mission-facing stellar target list used to test whether ECTP prioritizes known direct-imaging target hosts. |
| HWO Preliminary Input Catalog | NASA Exoplanet Archive `.tgz` package, DOI listed by NASA as `10.26133/NEA39` | {source_url} | Not downloaded | Not vendored | n/a | n/a | Planned HPIC ingestion step | Future large-scale expansion target; excluded from the default automated run until a stable tabular ingestion contract is added. |

The HWO ExEP crossmatch is host-name based and therefore conservative: it measures overlap with known stellar target hosts, not biological evidence.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path
