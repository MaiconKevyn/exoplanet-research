# Development Guide

## Scope

This guide is for contributors changing code, tests, generated artifacts, or documentation. The scientific reproduction path remains documented in `paper/reproduce.sh`; this file focuses on day-to-day engineering workflow.

## Local Environment

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
npm --prefix frontend install
```

The project expects Python 3.11 or newer. The frontend uses Vite 7 and should run with Node.js `^20.19.0` or `>=22.12.0`.

## Common Commands

| Purpose | Command |
| --- | --- |
| Run all Python tests | `.venv/bin/python -m pytest -q` |
| Run the main pipeline | `.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv` |
| Run a fast paper smoke reproduction | `UNCERTAINTY_RUNS=25 paper/reproduce.sh` |
| Run paper experiment summaries | `.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml` |
| Build dashboard | `npm --prefix frontend run build` |
| Check unsafe overclaim language | `rg -n "life[ ]found|alien[ ]life|proof[ ]of[ ]life|confirmed[ ]life|biosignature[ ]detected" README.md docs paper frontend/src src tests` |

## Module Boundaries

Use `docs/architecture/codebase_modularity_review.md` as the source of truth for module ownership. In short:

- data loading and canonical selection belong under `src/exoplanets_research/data/`;
- HZ models, features, score configs, and scoring belong under `src/exoplanets_research/habitability/`;
- uncertainty sampling belongs under `src/exoplanets_research/uncertainty/`;
- baseline and external target validation belong under `src/exoplanets_research/validation/`;
- paper experiment orchestration belongs under `src/exoplanets_research/experiments/`;
- paper plots belong in `src/exoplanets_research/paper/figures.py`;
- paper tables belong in `src/exoplanets_research/paper/tables.py`;
- the public pipeline should remain a thin orchestration layer.

## Testing Rules

Place tests next to the behavior they protect:

- archive ingestion: `tests/test_archive.py`;
- HZ and scoring contracts: `tests/test_habitable_zone.py`, `tests/test_hz_models.py`, `tests/test_scoring.py`, `tests/test_scoring_config.py`;
- pipeline smoke and IO contracts: `tests/test_pipeline_smoke.py`;
- uncertainty pipeline behavior: `tests/test_pipeline_uncertainty.py`;
- paper export path: `tests/test_pipeline_paper_export.py`;
- experiment summaries: `tests/test_experiment_runner_outputs.py`;
- paper tables/figures: `tests/test_paper_tables.py`, `tests/test_paper_figures.py`.

When moving code without changing behavior, keep existing asserts intact and only update imports or fixture placement.

## Artifact Rules

Use `docs/architecture/artifact_policy.md` before adding generated files.

Tracked by default:

- final ranked CSVs;
- uncertainty summary CSVs;
- experiment comparison CSVs;
- paper tables and figures;
- provenance and validation reports;
- dashboard JSON used by the checked-in frontend.

Ignored by default:

- full Monte Carlo sample rows;
- `data/outputs/experiments/*/intermediate/`;
- downloaded external catalogs under `data/external/`;
- frontend build output;
- paper build output;
- cache directories.

## Commit Rules

Use small commits with one reviewable idea:

- `docs: ...` for documentation and policy updates;
- `refactor: ...` for behavior-preserving code movement;
- `test: ...` for test-only changes;
- `chore: ...` for repository organization.

Do not combine scientific formula changes with file movement. If rankings, scores, or paper tables change semantically, update `docs/validation/validation_report.md` in the same commit.
