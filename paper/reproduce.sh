#!/usr/bin/env bash
set -euo pipefail

UNCERTAINTY_RUNS="${UNCERTAINTY_RUNS:-500}"
UNCERTAINTY_SEED="${UNCERTAINTY_SEED:-42}"

.venv/bin/python -m pytest -q
.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv --hz-model simple_luminosity_baseline --score-profile configs/scoring/ectp_v1.yml --uncertainty-runs "${UNCERTAINTY_RUNS}" --uncertainty-seed "${UNCERTAINTY_SEED}" --paper-artifacts
.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml
