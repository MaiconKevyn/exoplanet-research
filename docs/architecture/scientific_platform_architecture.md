# Scientific Platform Architecture

## Purpose

This architecture converts the repository from a static habitability analysis into a literature-grounded astrobiology research platform. The platform ranks exoplanets for follow-up observation and modeling while preserving evidence, uncertainty, provenance, and conservative interpretation.

## Non-Negotiable Rules

1. Every output row must be traceable to source data and scoring assumptions.
2. Every score must expose sub-scores and missing-data penalties.
3. Duplicate planet records must be handled before ranking.
4. Biosignature language must be probabilistic and evidence-based.
5. Validation must include known exoplanet sanity checks and pipeline reproducibility.

## C4-Style Architecture

### Context

The platform sits between three external knowledge sources and two user-facing outputs:

```text
NASA Exoplanet Archive CSV/TAP
          +
Astrobiology literature and platform registry
          +
Mission and observatory context
          |
          v
Python evidence pipeline
          |
          +--> CSV/JSON scientific artifacts
          +--> React dashboard and validation reports
```

### Containers

| Container | Responsibility |
| --- | --- |
| Python package `exoplanets_research` | Ingest archive data, de-duplicate planet records, engineer features, compute scores, quantify uncertainty, validate outputs, and export artifacts. |
| Literature registry | Store papers, strategies, platforms, and architecture implications in machine-readable YAML. |
| Data artifacts | Persist canonical data, HZ calculations, ranked candidates, and provenance sidecars. |
| Validation suite | Prove schema validity, HZ parity, known-candidate visibility, scoring policy, and pipeline outputs. |
| React dashboard | Present ranked candidates, evidence breakdowns, literature traceability, and caveats. |

### Components

| Component | File | Interface |
| --- | --- | --- |
| Archive ingestion | `src/exoplanets_research/data/archive.py` | `load_planetary_systems_csv`, `build_pscomppars_tap_query` |
| Record cleaning | `src/exoplanets_research/data/cleaning.py` | `select_best_planet_records` |
| Artifact writers | `src/exoplanets_research/data/outputs.py`, `src/exoplanets_research/io/provenance.py` | `write_frontend_json`, `attach_uncertainty_summary`, `write_provenance` |
| Literature catalog | `src/exoplanets_research/literature/catalog.py` | `load_sources`, `group_sources_by_category` |
| HZ models | `src/exoplanets_research/habitability/hz_models.py`, `src/exoplanets_research/habitability/habitable_zone.py` | `compute_hz_bounds`, `add_habitable_zone_columns` |
| Feature engineering | `src/exoplanets_research/habitability/features.py` | `add_habitability_features` |
| Evidence scoring | `src/exoplanets_research/habitability/scoring.py` | `score_candidates` |
| Uncertainty modeling | `src/exoplanets_research/uncertainty/monte_carlo.py` | `generate_uncertainty_samples`, `summarize_rank_uncertainty` |
| Experiment comparisons | `src/exoplanets_research/experiments/comparisons.py` | `run_hz_model_comparison`, `run_baseline_comparison`, `run_score_sensitivity` |
| Experiment artifacts | `src/exoplanets_research/experiments/artifacts.py`, `src/exoplanets_research/experiments/external_validation.py` | `write_paper_artifacts`, `run_external_validation`, `write_external_inventory` |
| Paper tables and figures | `src/exoplanets_research/paper/tables.py`, `src/exoplanets_research/paper/figures.py` | `write_top_candidate_table`, plot functions |
| Pipeline orchestration | `src/exoplanets_research/pipeline.py` | `run_pipeline`, CLI stages |
| Dashboard table | `frontend/src/components/HabitablePlanetsTable.jsx` | Ranked candidate rows |
| Evidence panel | `frontend/src/components/EvidenceBreakdown.jsx` | Top-candidate score decomposition |
| Literature panel | `frontend/src/components/LiteratureTracePanel.jsx` | Human-readable source-to-decision trace |

## Data Flow

1. `load_planetary_systems_csv` reads local NASA Exoplanet Archive CSVs, including files with leading metadata rows.
2. `select_best_planet_records` collapses duplicate `pl_name` records, preferring `default_flag == 1` and then the most complete critical fields.
3. `add_habitable_zone_columns` computes `hz_inner`, `hz_outer`, `hz_model`, and `habitable_zone_status`.
4. `add_habitability_features` adds radius class, stellar temperature class, HZ center offset, missing fields, data-quality features, and follow-up readiness.
5. `score_candidates` creates sub-scores, total score, confidence label, and a conservative caveat.
6. `generate_uncertainty_samples` and `summarize_rank_uncertainty` add score/rank stability summaries when requested.
7. `run_pipeline` orchestrates CSV outputs, provenance JSON, frontend JSON, and optional paper artifacts through dedicated writer modules.
8. The experiment runner generates paper-grade comparisons for HZ models, baseline rankers, score sensitivity, and external mission target overlap.
9. The React dashboard reads the generated JSON and displays the evidence breakdown.

## Paper and Platform Mapping

| Paper/Platform | Main idea | Architecture decision | Validation signal |
| --- | --- | --- | --- |
| Lovelock 1965 | Atmospheric disequilibrium can be a life-detection principle. | Disequilibrium is reserved as a future evidence class, not inferred from catalog-only data. | Caveat says no biosignature inference is made. |
| Sagan et al. 1993 | Remote life evidence needs multiple converging observations. | Score is decomposed into independent sub-scores. | Dashboard shows HZ, size, data, and context separately. |
| Schwieterman et al. 2018 | Biosignatures require environmental context and false-positive analysis. | Ranking stays at target-prioritization level. | Reports and frontend avoid detection claims. |
| Catling et al. 2018 | Biosignature assessment should be probabilistic. | Scores expose evidence components and penalties. | Tests check sub-score fields exist and are bounded. |
| Meadows et al. 2018 | Oxygen-like signals are contextual. | No single marker is treated as decisive. | No gas-based claim appears in outputs. |
| Walker et al. 2018 | Future biosignatures may be agnostic and statistical. | Pipeline is modular and future-ready. | Feature and scoring modules are separate. |
| Krissansen-Totton et al. 2018 | Disequilibrium is powerful but data-demanding. | Atmospheric evidence is not faked. | Interpretation caveat is present in every row. |
| Neveu et al. 2018 | Life detection should be staged by evidence maturity. | `evidence_confidence` labels are included. | Tests verify conservative labels and known candidates. |
| NASA Exoplanet Archive | Curated archive is the data source. | Ingestion and provenance are explicit. | Sidecar JSON records input and row count. |
| EMAC | Models and tools should be searchable and reusable. | Literature sources are machine-readable. | YAML schema test validates every source. |
| VPL | Exoplanet environments and spectra require modular models. | Climate/spectral integration can be added behind feature modules. | HZ model is labeled as a baseline, not final climate modeling. |
| AHED | Long-tail astrobiology data needs metadata and provenance. | Outputs use stable paths and sidecar metadata. | Pipeline writes provenance JSON. |
| LDKB | Life-detection arguments need structured true-positive and false-positive logic. | Caveats are explicit and can become structured evidence arguments later. | Overclaim search validates language. |
| NFoLD | Life-detection expertise should shape missions from inception to operations. | Validation report is mission-facing, not only software-facing. | Final validation includes scientific limitations. |
| HWO | Future observatory trades need target context. | Follow-up readiness is a score component. | Ranked outputs include `score_followup_readiness`. |

## Error Handling and Scientific Limits

The pipeline intentionally handles missing data as scientific evidence. Missing critical fields reduce `score_data_quality` and add `penalty_missing_data`. Missing luminosity or orbit fields produce `habitable_zone_status = "unknown"` instead of forcing a result.

The HZ formula is a reproducibility baseline matching the existing artifact. It is not a substitute for climate, atmospheric escape, stellar activity, or photochemical modeling. The architecture keeps that limitation visible through `hz_model`.

## Validation Strategy

The validation suite proves:

- Literature registry schema validity.
- HZ formula parity with existing generated artifacts.
- Duplicate handling policy.
- Scoring field bounds and conservative caveat.
- Known candidate survival after de-duplication.
- Pipeline output and provenance generation.
- Paper experiment summaries and artifact generation.
- Frontend build compatibility with generated JSON.

The final quality gate adds:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv
npm --prefix frontend run build
rg -n "life[ ]found|alien[ ]life|proof[ ]of[ ]life|confirmed[ ]life|biosignature[ ]detected" docs frontend/src src
```

## Extension Path

The next scientifically meaningful extensions are:

1. Add stellar activity and flare proxies for M-dwarf caveats.
2. Add atmospheric observation availability from archive spectroscopy fields.
3. Add VPL-compatible spectral model comparison hooks.
4. Add EMAC-style registry links for external models.
5. Add LDKB-style structured evidence and counter-evidence arguments.
6. Replace the simple HZ baseline with selectable HZ and climate-model families while preserving baseline parity.
