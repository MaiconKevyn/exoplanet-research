# Legacy Exploratory Scripts

This directory stores the exploratory scripts that predate the packaged `exoplanets_research` pipeline.

They are retained for historical context only. The supported implementation path is:

```bash
.venv/bin/python -m exoplanets_research.pipeline --stage all
```

Do not add new production code here. New ingestion, feature, scoring, validation, paper, or frontend-export logic belongs under `src/exoplanets_research/` with tests under `tests/`.

## Files

| Script | Historical role |
| --- | --- |
| `01_initial_exploration.py` | Initial archive inspection. |
| `02_exploratory_analysis.py` | Exploratory statistics and figures. |
| `02_preprocessing.py` | Early preprocessing prototype. |
| `03_habitability_analysis.py` | Early habitable-zone analysis. |
| `04_habitable_planet_analysis.py` | Early candidate filtering. |
| `05_habitability_scoring.py` | Early heuristic scoring prototype. |
