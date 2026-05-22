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

Sample-level Monte Carlo artifacts are reproducible intermediates governed by `docs/architecture/artifact_policy.md`.

## Maintenance Risks Reviewed

| Risk | Current Evidence | Target Remediation |
| --- | --- | --- |
| Experiment runner concentration | Resolved: `run_ablation.py` is now a CLI facade and the logic lives in focused `experiments/*` modules. | Keep new experiment behavior in the owning module instead of expanding the CLI facade. |
| Pipeline side effects | Resolved: provenance, frontend JSON, uncertainty summary attachment, and paper artifact hooks are separated from core orchestration. | Keep `pipeline.py` focused on execution order and public CLI arguments. |
| Paper artifact coupling | Resolved: Markdown tables live in `paper/tables.py`; plots remain in `paper/figures.py`. | Keep serialization and plotting changes separate. |
| Test concentration | Resolved: pipeline tests are split into archive, smoke, uncertainty, and paper export files. | Add future tests to the behavior-specific file. |
| Legacy script ambiguity | Resolved: exploratory scripts now live under `scripts/legacy/` with a local README. | Do not add production code under `scripts/legacy/`. |
| Generated artifact pressure | Resolved for Monte Carlo samples: full sample rows are ignored under experiment `intermediate/`; summaries stay tracked. | Use `docs/architecture/artifact_policy.md` for future generated artifacts. |

## Rules For Future Changes

1. Do not change scientific formulas in the same commit as file movement.
2. Preserve public CLI options unless a migration note and test update accompany the change.
3. Add tests at the module boundary where behavior is owned.
4. Keep generated paper tables and figures deterministic.
5. Treat catalog-only outputs as target-prioritization evidence, never biosignature detection.
6. Keep large reproducible intermediates out of Git unless there is an explicit publication reason.
7. Update this document when adding a new top-level module or changing module ownership.

## Post-Refactor Review

Completed on 2026-05-22.

Final largest Python modules after cleanup:

| File | Lines | Review note |
| --- | ---: | --- |
| `src/exoplanets_research/experiments/comparisons.py` | 173 | Largest remaining module; owns three related experiment comparisons and can be split later if new comparison families are added. |
| `src/exoplanets_research/pipeline.py` | 163 | Acceptable as public orchestration and CLI surface. Low-level writers have been extracted. |
| `src/exoplanets_research/habitability/hz_models.py` | 126 | Scientific model formulas remain centralized and tested. |
| `src/exoplanets_research/experiments/external_validation.py` | 110 | Owns external target validation and inventory generation. |
| `src/exoplanets_research/uncertainty/monte_carlo.py` | 96 | Owns uncertainty sampling and summary. |

Validation evidence:

- `find src tests -name "*.py" -print0 | xargs -0 wc -l | sort -n` completed; total Python lines: 2,275.
- `find src/exoplanets_research -name "*.py" -print0 | xargs -0 .venv/bin/python -m py_compile` completed with no import or syntax failures.
- `.venv/bin/python -m pytest -q` passed with 34 tests after the cleanup.
- `npm --prefix frontend run build` passed; Vite still warns that the static dashboard bundle is large.

Scientific-output status:

- No scoring formula, HZ formula, or ranking semantics were intentionally changed during this cleanup.
- The artifact contract changed for full Monte Carlo samples: `data/outputs/astrobiology_uncertainty_samples.csv` was removed from Git tracking, and reproducible full samples now write to `data/outputs/experiments/paper_v1/intermediate/astrobiology_uncertainty_samples.csv`.
- Tracked scientific summaries, paper tables, figures, manifests, provenance, and frontend JSON remain the reviewable scientific record.

Remaining engineering risks:

- `experiments/comparisons.py` should be split further if additional comparison families are added.
- The frontend bundle remains large because it embeds static candidate JSON; a future dashboard should lazy-load or paginate candidate data.
- GitHub Actions still depends on upstream action runtime versions outside this repository's code.
