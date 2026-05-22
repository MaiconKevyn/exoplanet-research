# Paper Readiness Audit

Generated on 2026-05-22 for `docs/superpowers/plans/2026-05-22-scientific-paper-roadmap.md`.

## Success Criteria

| Requirement | Evidence | Status |
| --- | --- | --- |
| Versioned scoring configurations replace a fixed score. | `configs/scoring/ectp_v1.yml`; `score_profile_id` and score-weight columns in `data/outputs/astrobiology_ranked_candidates.csv`; `--score-profile` in `src/exoplanets_research/pipeline.py`. | Complete |
| At least three HZ model outputs exist. | `data/outputs/experiments/paper_v1/hz_model_comparison.csv` lists `simple_luminosity_baseline`, `kopparapu_conservative_earth_mass`, and `kopparapu_optimistic_earth_mass`. | Complete |
| Every ranked candidate has uncertainty columns. | `data/outputs/astrobiology_ranked_candidates.csv` has non-null `score_mean`, `score_std`, `rank_median`, `rank_p05`, `rank_p95`, and `top10_probability` for 4,236 rows. | Complete |
| One command reproduces paper tables and figures. | `paper/reproduce.sh` runs tests, the full pipeline with `--paper-artifacts`, and the experiment runner. | Complete |
| Top-ranked candidates are compared against at least two baselines. | `data/outputs/experiments/paper_v1/baseline_comparison.csv` includes `hz_radius_baseline` and `followup_readiness_baseline`. | Complete |
| External validation includes mission-facing host-star overlap. | `data/outputs/experiments/paper_v1/external_validation_summary.csv` reports HWO ExEP overlap from `DI_STARS_EXEP`. | Complete |
| Results include rank-correlation and top-k metrics. | `baseline_comparison.csv`, `hz_model_comparison.csv`, and `score_sensitivity.csv` include Spearman/Kendall or top-k overlap metrics. | Complete |
| Limitations state why catalog-only ranking cannot infer biosignatures. | `README.md`, `paper/manuscript.md`, and `docs/validation/validation_report.md`. | Complete |
| CI runs tests, pipeline smoke, and conservative-language checks. | `.github/workflows/ci.yml`; latest GitHub run for commit `5383164` passed. | Complete |
| Repo has license, citation, paper package, and reproducibility command. | `LICENSE`, `CITATION.cff`, `paper/`, `paper/reproduce.sh`. | Complete |

## Paper-Readiness Checklist

| Requirement | Evidence | Status |
| --- | --- | --- |
| A reader can reproduce the main table without manual editing. | `paper/reproduce.sh` regenerates `paper/tables/top_candidates.md`. | Complete |
| A reader can reproduce every figure without manual plotting. | `paper/reproduce.sh` regenerates `paper/figures/score_distribution.png`, `paper/figures/subscore_heatmap_top25.png`, `paper/figures/rank_uncertainty_top25.png`, and `paper/figures/hz_model_overlap.png`. | Complete |
| Every score column has a definition. | `docs/research/scientific_method_contract.md` includes output field definitions. | Complete |
| Every model name maps to a cited method. | `docs/research/scientific_method_contract.md` maps each HZ model to `BaselineInventory2026` or `Kopparapu2014`; `paper/references.bib` contains those entries. | Complete |
| Every uncertainty column has a sampling rule. | `docs/research/scientific_method_contract.md` documents Monte Carlo sampling rules. | Complete |
| Every external validation table has source URL, download date, and checksum. | `data/outputs/experiments/paper_v1/external_validation_summary.csv` and `paper/tables/external_validation_summary.md`. | Complete |
| Every major limitation is visible in README and manuscript. | `README.md` Scientific Limitations; `paper/manuscript.md` Discussion. | Complete |
| Every abstract claim is supported by a result table or command. | HZ comparison, baseline comparison, score sensitivity, uncertainty, and external validation tables under `paper/tables/`; reproduction command in `paper/reproduce.sh`. | Complete |
| Dashboard and README avoid biosignature/life-detection claims. | Conservative-language audit in `docs/validation/validation_report.md`; CI conservative-language check passed. | Complete |
| CI passes on GitHub. | Latest branch CI passed for commit `5383164`. | Complete |

## Residual Engineering Notes

- Full Monte Carlo sample rows now belong under `data/outputs/experiments/paper_v1/intermediate/` and are ignored by Git. The tracked uncertainty artifact is `data/outputs/astrobiology_rank_uncertainty.csv`.
- GitHub Actions reports a Node.js 20 action-runtime deprecation warning for upstream actions. The workflow still passes, but the actions should be updated when GitHub publishes Node 24-compatible versions.
