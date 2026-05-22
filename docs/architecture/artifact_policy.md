# Generated Artifact Policy

Generated on 2026-05-22 for the architecture cleanup roadmap.

## Purpose

The project must remain reproducible without turning Git into storage for every generated intermediate. This policy separates scientific record artifacts from reproducible working files.

## Artifact Classes

| Class | Examples | Git policy | Publication policy |
| --- | --- | --- | --- |
| Source inputs | `data/PS_2025.06.22_09.41.26.csv`, curated literature YAML | Track when the file is part of the reproducible snapshot and is below repository limits. | Cite source and include provenance. |
| Final scientific tables | `paper/tables/*.md`, `data/outputs/experiments/paper_v1/*.csv` | Track. | Include in release or manuscript supplement. |
| Final scientific figures | `paper/figures/*.png` | Track when deterministic and paper-facing. | Include in manuscript or release. |
| Summary outputs | `data/outputs/astrobiology_ranked_candidates.csv`, `data/outputs/astrobiology_rank_uncertainty.csv` | Track. | Include in release or archival package. |
| Provenance and inventories | `*.provenance.json`, `docs/validation/*inventory*.md` | Track. | Include with outputs. |
| Reproducible intermediates | Full Monte Carlo sample rows, caches, temporary experiment outputs | Do not track. | Attach to release, Zenodo, object storage, or regenerate from command. |
| External downloaded catalogs | `data/external/*` except README and `.gitkeep` | Do not track by default. | Cite source URL, date, checksum, and retrieval command. |

## Monte Carlo Sample Policy

Full uncertainty samples are reproducible intermediates. They can become large quickly because their size scales with:

```text
ranked candidates * uncertainty runs
```

The default paper run writes full sample rows to:

```text
data/outputs/experiments/paper_v1/intermediate/astrobiology_uncertainty_samples.csv
```

That path is ignored by Git. The tracked scientific output is the reduced rank-stability summary:

```text
data/outputs/astrobiology_rank_uncertainty.csv
```

## What Must Stay Tracked

Keep these classes in Git:

- scoring and experiment manifests;
- final ranked candidate CSV;
- uncertainty summary CSV;
- experiment comparison CSVs;
- paper tables and figures;
- provenance sidecars;
- validation reports and inventories;
- frontend JSON when it is the dashboard data contract.

## What Must Stay Out Of Git

Do not track:

- `data/outputs/astrobiology_uncertainty_samples.csv`;
- `data/outputs/experiments/*/intermediate/`;
- `data/external/*` except `README.md` and `.gitkeep`;
- frontend build output;
- paper build output;
- cache directories.

## Release Guidance

When a paper or preprint is prepared, publish heavy reproducible intermediates as release assets or as an archival dataset with a DOI. The release notes must include:

- commit SHA;
- exact reproduction command;
- input catalog identity;
- uncertainty run count and seed;
- checksums for large attached files.
