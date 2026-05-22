# Baseline Inventory

Generated on 2026-05-20 from `/home/maiconkevyn/PycharmProjects/exoplanets_research`.

## Repository State

The project directory is not currently initialized as a Git repository:

```text
fatal: not a git repository (or any of the parent directories): .git
```

This matches the implementation plan's safety gate: `.gitignore` must exist before any `git init`, and any push must wait until a remote is explicitly verified.

## Current Data Artifacts

| Artifact | Rows | Columns | Role |
| --- | ---: | ---: | --- |
| `data/processed_exoplanet_data.csv` | 38,500 | 288 | CSV extracted from the NASA Exoplanet Archive file after skipping metadata rows. |
| `data/habitable_zone_calculated.csv` | 1,464 | 290 | Existing habitable-zone candidate table with `hz_inner` and `hz_outer`. |
| `data/potentially_habitable_exoplanets.csv` | 20 | 291 | Existing filter of rows whose semi-major axis falls inside the simple HZ bounds. |
| `data/top_habitable_candidates.csv` | 20 | 292 | Existing heuristic ranking with `habitability_score`. |

## Current Top Candidates

| Planet | Host | Score | Radius Re | Stellar Temp K | Orbit AU | HZ Inner AU | HZ Outer AU |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Kepler-442 b | Kepler-442 | 1.75 | 1.340 | 4402 | 0.40900 | 0.326065 | 0.469745 |
| Kepler-22 b | Kepler-22 | 1.50 | 2.380 | 5518 | 0.84900 | 0.847820 | 1.221412 |
| Kepler-1410 b | Kepler-1410 | 1.25 | 2.150 | 3950 | 0.25430 | 0.251364 | 0.362128 |
| Kepler-1544 b | Kepler-1544 | 1.25 | 1.790 | 4820 | 0.54210 | 0.474574 | 0.683694 |
| TRAPPIST-1 e | TRAPPIST-1 | 1.25 | 0.918 | 2559 | 0.02817 | 0.021826 | 0.031443 |
| TRAPPIST-1 e | TRAPPIST-1 | 1.25 | 0.920 | 2566 | 0.02925 | 0.022422 | 0.032302 |
| Kepler-1653 b | Kepler-1653 | 1.25 | 2.170 | 4807 | 0.47060 | 0.458462 | 0.660484 |
| Kepler-443 b | Kepler-443 | 1.25 | 2.330 | 4723 | 0.49500 | 0.443919 | 0.639532 |
| TOI-700 d | TOI-700 | 1.25 | 1.190 | 3480 | 0.16300 | 0.145540 | 0.209673 |
| TOI-700 d | TOI-700 | 1.25 | 1.073 | 3459 | 0.16330 | 0.144286 | 0.207865 |

## Known Gaps

- `scripts/legacy/02_preprocessing.py` expects `data/processed_exoplanet_data.parquet`, but no such file exists in the current tree.
- The script that originally generated `data/habitable_zone_candidates.csv` and `data/habitable_zone_calculated.csv` is missing.
- `data/habitable_zone_candidates.csv` has duplicate `pl_name` rows. Current duplicate count by `pl_name` is 295 rows, with several planets appearing four times.
- Existing ranking is a single heuristic score and does not expose provenance, sub-scores, uncertainty, or false-positive caveats.
- The frontend builds from static JSON exports, but it does not yet show scientific evidence breakdowns or literature traceability.

## Baseline Verification Commands

```bash
find . -maxdepth 3 -type f \
  -not -path './venv/*' \
  -not -path './.venv/*' \
  -not -path './frontend/node_modules/*' \
  | sort > /tmp/exoplanets_research_files.txt

python3 - <<'PY'
import pandas as pd
for path in [
    "data/processed_exoplanet_data.csv",
    "data/habitable_zone_calculated.csv",
    "data/potentially_habitable_exoplanets.csv",
    "data/top_habitable_candidates.csv",
]:
    df = pd.read_csv(path, low_memory=False)
    print(f"{path}: rows={len(df)} cols={len(df.columns)}")
PY
```
