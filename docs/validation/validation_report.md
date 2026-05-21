# Validation Report

Generated on 2026-05-20 for the astrobiology research platform implementation.

## Summary

The implementation satisfies the current validation gate for a literature-grounded exoplanet target-prioritization platform. The pipeline runs end to end on the local NASA Exoplanet Archive CSV, produces provenance-aware outputs, preserves known candidate visibility, and builds the React dashboard.

The scientific interpretation remains deliberately conservative: outputs rank follow-up candidates for observation and modeling. They do not infer biosignatures from catalog-only data.

## Data Provenance Checks

Pipeline command:

```bash
.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv
```

Generated outputs:

| Artifact | Rows | Columns | Notes |
| --- | ---: | ---: | --- |
| `data/processed/canonical_exoplanets.csv` | 5,921 | 290 | One selected row per `pl_name`, with duplicate metadata. |
| `data/processed/habitable_zone_exoplanets.csv` | 4,236 | 294 | Canonical rows with orbit and luminosity sufficient for HZ calculation. |
| `data/outputs/astrobiology_ranked_candidates.csv` | 4,236 | 312 | Evidence-weighted ranked candidates with sub-scores and caveats. |
| `frontend/src/data/astrobiology_ranked_candidates.json` | 4,236 | n/a | Dashboard export. |

Provenance sidecars:

| Sidecar | Row count | Stage | Generator |
| --- | ---: | --- | --- |
| `data/processed/canonical_exoplanets.provenance.json` | 5,921 | `canonical` | `src/exoplanets_research/pipeline.py` |
| `data/outputs/astrobiology_ranked_candidates.provenance.json` | 4,236 | `score` | `src/exoplanets_research/pipeline.py` |

## Test Results

Command:

```bash
.venv/bin/python -m pytest -q
```

Result:

```text
11 passed in 2.80s
```

Covered behavior:

- Literature registry schema validation.
- HZ formula parity against the existing `data/habitable_zone_calculated.csv` artifact.
- HZ status labels for inside, outside, and unknown cases.
- Duplicate handling that prefers `default_flag == 1`.
- Scoring sub-scores, total score, confidence label, and conservative caveat.
- Known-candidate visibility after de-duplication and scoring.
- NASA metadata-row CSV loading.
- PSCompPars TAP query construction.
- Pipeline CSV, provenance, and frontend JSON output generation.

## Literature Coverage

Command:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
import yaml
sources = yaml.safe_load(Path('data/literature/astrobiology_sources.yml').read_text())
review = Path('docs/research/astrobiology_literature_review.md').read_text()
missing = [source['id'] for source in sources if source['id'] not in review]
print(f'sources={len(sources)} missing={len(missing)}')
PY
```

Result:

```text
sources=30 missing=0
```

## Known Candidate Sanity Check

The pipeline keeps the expected known candidates visible after de-duplication and scoring:

| Candidate | Current rank |
| --- | ---: |
| Kepler-442 b | 1 |
| TRAPPIST-1 e | 3 |
| TOI-700 d | 4 |
| Kepler-22 b | 466 |

Kepler-22 b ranks lower under the new scoring because the score is no longer only the older radius/stellar-temperature heuristic. The new policy includes HZ position, data quality, and follow-up readiness. It remains present and inspectable.

## Current Top Ranked Candidates

| Rank | Planet | Host | Total | HZ | Size | Stellar | Data | Follow-up | Confidence |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | Kepler-442 b | Kepler-442 | 0.815 | 0.923 | 1.00 | 0.75 | 0.83 | 0.70 | limited_catalog_confidence |
| 2 | LP 890-9 c | LP 890-9 | 0.793 | 0.729 | 1.00 | 0.25 | 1.00 | 1.00 | moderate_catalog_confidence |
| 3 | TRAPPIST-1 e | TRAPPIST-1 | 0.761 | 0.809 | 1.00 | 0.25 | 1.00 | 0.60 | moderate_catalog_confidence |
| 4 | TOI-700 d | TOI-700 | 0.742 | 0.799 | 1.00 | 0.25 | 0.83 | 1.00 | limited_catalog_confidence |
| 5 | Kepler-705 b | Kepler-705 | 0.725 | 0.951 | 0.50 | 0.75 | 0.83 | 0.70 | limited_catalog_confidence |

## Frontend Build

Command:

```bash
npm --prefix frontend run build
```

Result:

```text
vite v7.0.0 building for production...
617 modules transformed.
built in 5.66s
```

Warnings:

- Browserslist/caniuse-lite data is 11 months old.
- The JavaScript bundle is large because the dashboard imports large static JSON artifacts.

Resolved warning:

- The previous CSS warning caused by `@import` after Tailwind directives no longer appears.

## Conservative Language Check

Command:

```bash
rg -n "life[ ]found|alien[ ]life|proof[ ]of[ ]life|confirmed[ ]life|biosignature[ ]detected" docs frontend/src src
```

Result:

```text
No matches.
```

## Scientific Limitations

- The HZ model is a reproducibility baseline, not a climate model.
- The ranking uses catalog-level fields and cannot infer atmospheric biosignatures.
- Disequilibrium, oxygen context, atmospheric retrievals, surface spectra, stellar activity, and photochemical false positives remain future work.
- Follow-up readiness is a first-pass heuristic using available catalog fields, especially distance and measurement completeness.
- Static JSON makes the current dashboard easy to reproduce but creates a large bundle; a future version should lazy-load candidate data.

## Conclusion

The current implementation is validated as a reproducible, literature-grounded candidate-prioritization platform. It has scientific impact as a transparent evidence-accounting layer over the NASA Exoplanet Archive, with explicit links to modern astrobiology frameworks and platform patterns.
