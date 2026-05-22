# Validation Report

Generated on 2026-05-22 for the ECTP scientific-paper roadmap implementation.

## Summary

The repository now implements the first paper-oriented version of Evidence-Calibrated Target Prioritization (ECTP). The system preserves the original conservative interpretation boundary while adding versioned scoring profiles, corrected Kopparapu 1 Earth-mass habitable-zone coefficients, multiple habitable-zone model comparisons, Monte Carlo rank-stability outputs, external HWO ExEP target validation, experiment manifests, paper artifact generation, CI metadata, citation metadata, and a manuscript/reproduction package.

The scientific interpretation remains deliberately conservative: outputs rank follow-up candidates for observation and modeling. They do not infer biosignatures from catalog-only data.

## Commands Run

Pipeline and paper reproduction:

```bash
bash paper/reproduce.sh
```

The reproduction script ran:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv --uncertainty-runs 25 --uncertainty-seed 42
.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml
```

Frontend build:

```bash
npm --prefix frontend run build
```

Conservative-language audit:

```bash
rg -n "life[ ]found|alien[ ]life|proof[ ]of[ ]life|confirmed[ ]life|biosignature[ ]detected" README.md docs paper frontend/src src tests
```

Data-size review:

```bash
du -h data/*.csv data/processed/*.csv data/outputs/*.csv frontend/src/data/*.json paper/figures/* paper/tables/* 2>/dev/null | sort -h
```

## Test Results

Command:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
28 passed in 4.10s
```

Covered behavior:

- Literature registry schema validation.
- HZ formula parity against the existing simple baseline artifact.
- HZ status labels for inside, outside, and unknown cases.
- Kopparapu conservative and optimistic HZ model availability.
- Kopparapu cool-star bounds and out-of-domain temperature handling for the published 2600-7200 K validity range.
- Duplicate handling that prefers `default_flag == 1`.
- Versioned scoring profile loading and normalized weights.
- Scoring sub-scores, total score, confidence label, score-profile metadata, and conservative caveat.
- Known-candidate visibility after de-duplication and scoring.
- NASA metadata-row CSV loading.
- PSCompPars TAP query construction.
- Pipeline CSV, provenance, frontend JSON, uncertainty samples, and rank-uncertainty output generation.
- Baseline ranking metrics.
- External target host-star crossmatch hooks.
- Paper experiment output generation for HZ comparison, baseline comparison, and external target crossmatch summaries.
- Paper table generation.
- Experiment manifest validation.

## Data Provenance Checks

Generated outputs:

| Artifact | Rows | Columns | Notes |
| --- | ---: | ---: | --- |
| `data/processed/canonical_exoplanets.csv` | 5,921 | 290 | One selected row per `pl_name`, with duplicate metadata. |
| `data/processed/habitable_zone_exoplanets.csv` | 4,236 | 296 | Canonical rows with orbit and luminosity sufficient for HZ calculation. |
| `data/outputs/astrobiology_ranked_candidates.csv` | 4,236 | 321 | ECTP-ranked candidates with sub-scores, profile metadata, caveats, and HZ model fields. |
| `data/outputs/astrobiology_uncertainty_samples.csv` | 105,900 | 5 | 25 Monte Carlo runs, reduced to rank-stability essentials. |
| `data/outputs/astrobiology_rank_uncertainty.csv` | 4,236 | 7 | Score mean/std, rank quantiles, and top-10 probability. |
| `data/outputs/experiments/paper_v1/hz_model_comparison.csv` | 3 | 6 | Model-level top-k overlap and HZ candidate counts. |
| `data/outputs/experiments/paper_v1/baseline_comparison.csv` | 1 | 7 | ECTP versus HZ-radius baseline overlap and rank correlation. |
| `data/outputs/experiments/paper_v1/external_validation_summary.csv` | 1 | 7 | HWO ExEP host crossmatch summary. |
| `data/outputs/experiments/paper_v1/external_validation.csv` | 4,236 | 7 | Ranked candidates annotated with external target flags. |
| `frontend/src/data/astrobiology_ranked_candidates.json` | 4,236 | n/a | Dashboard export. |

Provenance sidecars:

| Sidecar | Row count | Stage | Generator |
| --- | ---: | --- | --- |
| `data/processed/canonical_exoplanets.provenance.json` | 5,921 | `canonical` | `src/exoplanets_research/pipeline.py` |
| `data/outputs/astrobiology_ranked_candidates.provenance.json` | 4,236 | `score` | `src/exoplanets_research/pipeline.py` |

## Current Top Ranked Candidates

| Rank | Planet | Host | Total | HZ model | Score profile | Confidence |
| ---: | --- | --- | ---: | --- | --- | --- |
| 1 | Kepler-442 b | Kepler-442 | 0.815 | `simple_luminosity_baseline` | `ectp_v1` | limited_catalog_confidence |
| 2 | LP 890-9 c | LP 890-9 | 0.793 | `simple_luminosity_baseline` | `ectp_v1` | moderate_catalog_confidence |
| 3 | TRAPPIST-1 e | TRAPPIST-1 | 0.761 | `simple_luminosity_baseline` | `ectp_v1` | moderate_catalog_confidence |
| 4 | TOI-700 d | TOI-700 | 0.742 | `simple_luminosity_baseline` | `ectp_v1` | limited_catalog_confidence |
| 5 | Kepler-705 b | Kepler-705 | 0.725 | `simple_luminosity_baseline` | `ectp_v1` | limited_catalog_confidence |

## Current Rank-Stability Smoke Results

The current reproduction script runs 25 Monte Carlo samples as a smoke-grade rank-stability gate. The experiment manifest keeps the paper target at 500 runs, but the generated repository artifact is intentionally smaller for routine validation.

| Planet | Score mean | Score std | Median rank | Rank p05 | Rank p95 | Top-10 probability |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| LP 890-9 c | 0.793 | 0.011 | 2.0 | 1.0 | 3.0 | 1.00 |
| TRAPPIST-1 e | 0.730 | 0.123 | 2.0 | 1.0 | 805.2 | 0.80 |
| TOI-700 d | 0.731 | 0.041 | 5.0 | 1.4 | 10.0 | 0.96 |
| Kepler-1704 b | 0.679 | 0.034 | 8.0 | 4.2 | 28.2 | 0.68 |
| Kepler-1544 b | 0.679 | 0.049 | 9.0 | 4.0 | 85.4 | 0.60 |

## HZ Model and Baseline Comparisons

The experiment runner now recomputes rankings across the manifest's HZ model family and writes paper-facing comparison tables. Relative to the default simple luminosity baseline, the Kopparapu conservative and optimistic models materially change the top-ranked set, which is scientifically useful because it exposes sensitivity to climate-model assumptions instead of hiding it inside a single score.

| HZ model | Candidates | Inside HZ | Top-10 overlap | Top-25 overlap | Top-50 overlap |
| --- | ---: | ---: | ---: | ---: | ---: |
| `simple_luminosity_baseline` | 4,236 | 84 | 1.000 | 1.000 | 1.000 |
| `kopparapu_conservative_earth_mass` | 4,188 | 127 | 0.111 | 0.429 | 0.613 |
| `kopparapu_optimistic_earth_mass` | 4,188 | 196 | 0.111 | 0.316 | 0.449 |

The simple HZ-radius baseline has weak-to-moderate agreement with ECTP, which supports the claim that ECTP is not merely re-labeling the widest HZ/radius filter.

| Baseline | n | Spearman r | Kendall tau | Top-10 overlap | Top-25 overlap | Top-50 overlap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hz_radius_baseline` | 4,236 | 0.304 | 0.217 | 0.250 | 0.111 | 0.111 |

## External Mission-Target Validation

The experiment runner downloads the NASA Exoplanet Archive HWO ExEP Precursor Science Stars TAP table `DI_STARS_EXEP` when the local file is absent, then performs a conservative host-name crossmatch against the ranked candidate table. HPIC is documented in the external inventory as the next large-catalog ingestion target, but it is not included in the default automated run until a stable tabular ingestion contract is added.

| Target list | Source table | Target hosts | Ranked candidates | Matched candidates | Matched top 25 | Matched top 50 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `hwo_exep_2023` | `DI_STARS_EXEP` | 164 | 4,236 | 16 | 0 | 1 |

## Paper Artifacts

Generated artifacts:

- `paper/tables/top_candidates.md`
- `paper/figures/score_distribution.png`
- `paper/figures/subscore_heatmap_top25.png`
- `paper/figures/rank_uncertainty_top25.png`
- `paper/tables/hz_model_comparison.md`
- `paper/tables/baseline_comparison.md`
- `paper/tables/external_validation_summary.md`
- `paper/figures/hz_model_overlap.png`
- `docs/validation/external_data_inventory.md`
- `data/outputs/experiments/paper_v1/hz_model_comparison.csv`
- `data/outputs/experiments/paper_v1/baseline_comparison.csv`
- `data/outputs/experiments/paper_v1/external_validation.csv`
- `data/outputs/experiments/paper_v1/external_validation_summary.csv`
- `data/outputs/experiments/paper_v1/manifest_resolved.yml`
- `data/outputs/experiments/paper_v1/paper_artifacts.yml`

## Frontend Build

Command:

```bash
npm --prefix frontend run build
```

Result:

```text
vite v7.0.0 building for production...
617 modules transformed.
built in 5.82s
```

Warnings:

- Browserslist/caniuse-lite data is stale.
- The JavaScript bundle is large because the dashboard imports large static JSON artifacts.

## Conservative Language Check

Result:

```text
No matches.
```

## Scientific Limitations

- The default reproduction output still uses `simple_luminosity_baseline`; Kopparapu model comparison is now generated, but manuscript submission should still decide which HZ family is the primary analysis.
- The current routine Monte Carlo output uses 25 smoke runs. The `paper_v1` manifest targets 500 runs for a paper-grade run.
- HWO ExEP validation is automated and inventoried. HPIC remains a future expansion because it is distributed as a larger downloadable package rather than the current default TAP table.
- The ranking uses catalog-level fields and cannot infer atmospheric biosignatures.
- Disequilibrium, oxygen context, atmospheric retrievals, surface spectra, stellar activity, and photochemical false positives remain future evidence classes.
- Static JSON makes the current dashboard easy to reproduce but creates a large bundle; a future version should lazy-load candidate data.

## Conclusion

The current implementation is validated as a reproducible, literature-grounded candidate-prioritization platform with a paper-oriented scaffold. It now has the core infrastructure required for a scientific manuscript: method contract, corrected HZ model families, versioned scoring, uncertainty outputs, baseline metrics, automated HWO ExEP validation, paper artifacts, CI, citation metadata, and a reproducibility script. The remaining scientific work before submission is to run the full 500-sample experiment matrix, add HPIC-scale ingestion if required by the manuscript framing, and complete the manuscript results/discussion sections from the generated artifacts.
