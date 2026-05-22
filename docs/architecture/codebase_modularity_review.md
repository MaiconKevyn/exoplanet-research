# Codebase Modularity Review

Generated on 2026-05-22 for the architecture cleanup roadmap.

## Purpose

This document defines the maintenance boundaries for the exoplanet research platform. It is a companion to the scientific architecture: the scientific architecture explains why the platform exists; this review explains where code should live and how future changes should be scoped.

## Data Flow

```text
NASA Exoplanet Archive snapshot
        |
        v
data/archive.py
        |
        v
data/cleaning.py
        |
        v
habitability/habitable_zone.py + habitability/hz_models.py
        |
        v
habitability/features.py
        |
        v
habitability/scoring.py + habitability/scoring_config.py
        |
        +--> uncertainty/monte_carlo.py
        |
        +--> validation/baselines.py + validation/external_targets.py
        |
        v
data outputs + provenance + paper artifacts + frontend JSON
```

## Module Ownership

| Module | Responsibility | Should not own |
| --- | --- | --- |
| `data/archive.py` | NASA archive CSV/TAP loading and archive metadata handling. | Scoring, plotting, validation, frontend export. |
| `data/cleaning.py` | Canonical row selection and duplicate policy. | HZ models, score weights, paper artifact writing. |
| `habitability/hz_models.py` | Named HZ model formulas and model metadata. | Candidate ranking or experiment orchestration. |
| `habitability/habitable_zone.py` | Stable HZ dataframe interface used by the pipeline. | External validation or paper figure generation. |
| `habitability/features.py` | Evidence feature engineering before scoring. | Score weighting policy and output IO. |
| `habitability/scoring.py` | Score calculation, sub-score fields, confidence labels, caveats. | Monte Carlo sampling, CLI parsing, file writing. |
| `habitability/scoring_config.py` | Versioned scoring profile loading and validation. | Runtime experiment summaries. |
| `uncertainty/monte_carlo.py` | Perturbation sampling and uncertainty summaries. | Baseline comparisons or table serialization. |
| `validation/baselines.py` | Baseline rankers and rank-comparison metrics. | Pipeline IO and external catalog downloads. |
| `validation/external_targets.py` | External mission target loading and host crossmatch. | Paper inventory text and CLI orchestration. |
| `experiments/*` | Paper-grade experiment orchestration and experiment artifact creation. | Core scientific formulas already owned by domain modules. |
| `paper/figures.py` | Plot generation only. | Markdown table serialization. |
| `paper/tables.py` | Paper table serialization and table-specific column selection. | Plotting or experiment execution. |
| `pipeline.py` | Public pipeline orchestration and CLI. | Low-level file writing details. |

## Public Entrypoints

| Entrypoint | Contract |
| --- | --- |
| `.venv/bin/python -m exoplanets_research.pipeline --stage all` | Regenerates the main processed data, ranking, provenance, and frontend JSON. |
| `.venv/bin/python -m exoplanets_research.pipeline --stage score` | Runs the scoring path and refreshes ranking artifacts. |
| `.venv/bin/python -m exoplanets_research.pipeline --paper-artifacts` | Exports paper tables and figures from current ranked outputs. |
| `.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml` | Runs HZ, baseline, sensitivity, external-validation, and paper-artifact experiment summaries. |
| `paper/reproduce.sh` | Runs the full paper reproduction gate. |
| `npm --prefix frontend run build` | Builds the dashboard against generated frontend data. |

## Versioned Artifacts

These artifacts are part of the scientific record and can be reviewed in Git:

- `configs/scoring/ectp_v1.yml`
- `configs/experiments/paper_v1.yml`
- `data/processed/canonical_exoplanets.csv`
- `data/processed/habitable_zone_exoplanets.csv`
- `data/outputs/astrobiology_ranked_candidates.csv`
- `data/outputs/astrobiology_rank_uncertainty.csv`
- `data/outputs/experiments/paper_v1/*.csv`
- `docs/validation/*.md`
- `paper/tables/*.md`
- `paper/figures/*.png`
- `frontend/src/data/astrobiology_ranked_candidates.json`

Sample-level Monte Carlo artifacts are reproducible intermediates. They should be governed by `docs/architecture/artifact_policy.md` once that policy is implemented.

## Current Maintenance Risks

| Risk | Current Evidence | Target Remediation |
| --- | --- | --- |
| Experiment runner concentration | `src/exoplanets_research/experiments/run_ablation.py` mixes manifest loading, ranking, comparisons, external validation, inventory, table writing, plotting, and CLI. | Split into `manifest.py`, `candidates.py`, `comparisons.py`, `external_validation.py`, and `artifacts.py`. |
| Pipeline side effects | `pipeline.py` writes provenance and frontend JSON directly and imports experiment helpers inside `run_pipeline`. | Move low-level writers to `data/outputs.py` and `io/provenance.py`. |
| Paper artifact coupling | `paper/figures.py` contains both plotting and Markdown table writing. | Move table logic to `paper/tables.py`. |
| Test concentration | `tests/test_pipeline_outputs.py` covers archive, provenance, uncertainty, profile overrides, and paper exports. | Split by behavior: archive, smoke, uncertainty, paper export. |
| Legacy script ambiguity | Exploratory scripts live under `src/` outside the package namespace. | Move to `scripts/legacy/` with a README. |
| Generated artifact pressure | Large sample-level outputs are versioned alongside summary outputs. | Define tracked versus reproducible-intermediate artifact classes. |

## Rules For Future Changes

1. Do not change scientific formulas in the same commit as file movement.
2. Preserve public CLI options unless a migration note and test update accompany the change.
3. Add tests at the module boundary where behavior is owned.
4. Keep generated paper tables and figures deterministic.
5. Treat catalog-only outputs as target-prioritization evidence, never biosignature detection.
6. Keep large reproducible intermediates out of Git unless there is an explicit publication reason.
7. Update this document when adding a new top-level module or changing module ownership.

## Post-Refactor Review

This section must be updated after completing the roadmap with:

- final Python line-count distribution;
- final test commands and results;
- final reproduction command result;
- any scientific-output changes, or a declaration that no formula/ranking semantics changed;
- remaining risks that should be handled after this cleanup.
