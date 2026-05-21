# Astrobiology Research Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the current exoplanet habitability scripts into a reproducible, literature-grounded astrobiology research platform that prioritizes scientifically defensible targets and communicates evidence without overstating life-detection claims.

**Architecture:** Build a layered research pipeline: literature corpus -> data provenance -> feature engineering -> habitability and biosignature-prior scoring -> validation -> report/dashboard. The main architectural shift is from a single heuristic ranking to an evidence-weighted platform where every score is traceable to a paper, dataset, assumption, and validation check.

**Tech Stack:** Python 3, pandas, numpy, PyYAML, pytest, matplotlib/seaborn, React/Vite/Recharts, NASA Exoplanet Archive TAP/CSV, Markdown research reports.

---

## Scientific Scope

This plan targets scientific impact through a defensible prioritization workflow, not through claims of life detection. The final system should answer: which known exoplanets are the strongest candidates for follow-up under modern astrobiology evidence standards, what assumptions produce that ranking, and how robust is each result to missing data, duplicate records, and false-positive risk?

Core scientific principles to apply:

- Habitability is contextual: planet, host star, orbit, stellar environment, measurement uncertainty, and detection bias must be modeled together.
- Biosignatures must be probabilistic and falsifiable: scores should encode evidence, uncertainty, and plausible abiotic alternatives.
- A platform should preserve provenance: every feature, paper-derived assumption, and output table must be reproducible.
- Communication must be conservative: use "candidate priority" and "evidence confidence", not detection-language claims.

## Seed Bibliography

Use these as the initial reading set before expanding with citation chasing through ADS, PubMed, NASA, and NAP references.

### Foundations and Strategy

- Lovelock, J. E. 1965. "A physical basis for life detection experiments." Nature. https://pubmed.ncbi.nlm.nih.gov/5883628/
- Sagan, C. et al. 1993. "A search for life on Earth from the Galileo spacecraft." Nature. https://www.nature.com/articles/365715a0
- Domagal-Goldman, S. D. et al. 2016. "The Astrobiology Primer v2.0." Astrobiology. https://pmc.ncbi.nlm.nih.gov/articles/PMC5008114/
- NASA. 2015. "NASA Astrobiology Strategy 2015." https://assets.science.nasa.gov/content/dam/science/psd/astrobiology/for-researchers/strategy/nasa_astrobiology_strategy_2015_final_041216.pdf
- National Academies. 2018/2019. "An Astrobiology Strategy for the Search for Life in the Universe." https://nap.nationalacademies.org/catalog/25252/an-astrobiology-strategy-for-the-search-for-life-in-the-universe
- National Academies. 2018. "Exoplanet Science Strategy." https://www.nationalacademies.org/read/25187
- National Academies. 2021. "Pathways to Discovery in Astronomy and Astrophysics for the 2020s." https://nap.nationalacademies.org/astro2020
- National Academies. 2022. "Origins, Worlds, and Life: A Decadal Strategy for Planetary Science and Astrobiology 2023-2032." Use the official NAP report page during implementation.

### Exobiology, Biosignatures, and Evidence Standards

- Schwieterman, E. W. et al. 2018. "Exoplanet Biosignatures: A Review of Remotely Detectable Signs of Life." Astrobiology. https://journals.sagepub.com/doi/10.1089/ast.2017.1729
- Catling, D. C. et al. 2018. "Exoplanet Biosignatures: A Framework for Their Assessment." Astrobiology. https://journals.sagepub.com/doi/abs/10.1089/ast.2017.1737
- Meadows, V. S. et al. 2018. "Exoplanet Biosignatures: Understanding Oxygen as a Biosignature in the Context of Its Environment." Astrobiology. https://arxiv.org/abs/1705.07560
- Walker, S. I. et al. 2018. "Exoplanet Biosignatures: Future Directions." Astrobiology. https://journals.sagepub.com/doi/10.1089/ast.2017.1738
- Krissansen-Totton, J., Olson, S., and Catling, D. C. 2018. "Disequilibrium biosignatures over Earth history and implications for detecting exoplanet life." Science Advances. https://arxiv.org/abs/1801.08211
- Neveu, M. et al. 2018. "The Ladder of Life Detection." Astrobiology. https://journals.sagepub.com/doi/abs/10.1089/ast.2017.1773
- Green, J. et al. 2024. "Moving toward a framework for communicating the confidence of life detection." Nature Astronomy. https://www.nature.com/articles/s41550-023-02135-1
- "Community Report from the Biosignatures Standards of Evidence Workshop." 2022. https://arxiv.org/abs/2210.14293

### Platforms, Observatories, and Data Infrastructure

- NASA Exoplanet Archive overview and TAP docs. https://exoplanetarchive.ipac.caltech.edu/docs/intro.html and https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html
- Akeson, R. L. et al. 2013. "The NASA Exoplanet Archive: Data and Tools for Exoplanet Research." PASP. https://www.ipac.caltech.edu/publication/2013PASP..125..989A
- NASA Exoplanet Modeling and Analysis Center (EMAC). https://emac.gsfc.nasa.gov/
- Renaud, J. P. et al. 2022. "The Exoplanet Modeling and Analysis Center at NASA Goddard." https://arxiv.org/abs/2209.04005
- Virtual Planetary Laboratory. https://vpl.uw.edu/about-us/
- VPL Spectral Explorer. https://vpl.uw.edu/models/vpl-spectral-explorer/
- NASA Astrobiology life-detection resources, including EMAC and AHED references. https://science.nasa.gov/astrobiology/researchers/life-detection-resources/
- NASA Habitable Worlds Observatory program page. https://science.nasa.gov/astrophysics/programs/habitable-worlds-observatory/
- HWO concept and technology maturation paper, 2026. https://ntrs.nasa.gov/citations/20260000389
- Early Architecture Concepts for HWO, 2026. https://arxiv.org/abs/2602.11046

## Target Architecture

Create these modules and artifacts:

```text
data/
  literature/astrobiology_sources.yml
  raw/
  processed/
  outputs/
docs/
  architecture/scientific_platform_architecture.md
  research/astrobiology_literature_review.md
  validation/validation_report.md
src/
  exoplanets_research/
    __init__.py
    config.py
    data/archive.py
    data/cleaning.py
    literature/catalog.py
    literature/schema.py
    habitability/habitable_zone.py
    habitability/features.py
    habitability/scoring.py
    validation/gold_standards.py
    pipeline.py
tests/
  test_literature_catalog.py
  test_habitable_zone.py
  test_scoring.py
  test_pipeline_outputs.py
```

Keep the existing scripts in `src/` until the new package reproduces their current outputs. After parity is proven, mark old scripts as legacy or replace them with thin wrappers.

## Task 1: Repository Safety and Baseline Inventory

**Files:**
- Create: `.gitignore`
- Create: `docs/validation/baseline_inventory.md`

- [ ] **Step 1: Confirm repository state**

Run:

```bash
pwd
git rev-parse --show-toplevel
git status --short
```

Expected if the current state is unchanged: `git rev-parse` fails because this directory is not yet a Git repository. Record that fact in `docs/validation/baseline_inventory.md`.

- [ ] **Step 2: Create `.gitignore` before any Git initialization**

Add:

```gitignore
venv/
.venv/
frontend/node_modules/
frontend/dist/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.mypy_cache/
.DS_Store
.idea/workspace.xml
data/raw/
data/outputs/*.tmp
```

- [ ] **Step 3: Inventory current files and generated artifacts**

Run:

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

Expected current baseline:

```text
data/processed_exoplanet_data.csv: rows=38500 cols=288
data/habitable_zone_calculated.csv: rows=1464 cols=290
data/potentially_habitable_exoplanets.csv: rows=20 cols=291
data/top_habitable_candidates.csv: rows=20 cols=292
```

- [ ] **Step 4: Write baseline inventory**

Document current data counts, known gaps, and validation commands in `docs/validation/baseline_inventory.md`.

## Task 2: Research Corpus Registry

**Files:**
- Create: `data/literature/astrobiology_sources.yml`
- Create: `src/exoplanets_research/literature/schema.py`
- Create: `src/exoplanets_research/literature/catalog.py`
- Create: `tests/test_literature_catalog.py`

- [ ] **Step 1: Write the source schema test**

Add a pytest that loads `data/literature/astrobiology_sources.yml` and asserts every entry has:

```python
required = {
    "id",
    "title",
    "year",
    "url",
    "category",
    "evidence_type",
    "architecture_implication",
    "model_application",
}
```

- [ ] **Step 2: Create the YAML registry**

Seed it with at least the sources listed in the bibliography above. Use categories:

```yaml
- foundation
- nasa_strategy
- biosignature_review
- evidence_framework
- platform
- observatory_architecture
- data_infrastructure
```

For each source, write a one-sentence `architecture_implication`, such as:

```yaml
architecture_implication: "Scoring must track both candidate evidence and plausible abiotic alternatives instead of producing a single unexplained score."
```

- [ ] **Step 3: Implement catalog loading**

Implement `load_sources(path: Path) -> list[dict]` and `group_sources_by_category(sources: list[dict]) -> dict[str, list[dict]]`.

- [ ] **Step 4: Run source validation**

Run:

```bash
pytest tests/test_literature_catalog.py -v
```

Expected: all registry entries pass schema validation.

## Task 3: Deep Literature Review Deliverable

**Files:**
- Create: `docs/research/astrobiology_literature_review.md`

- [ ] **Step 1: Build the review matrix**

For every source in `data/literature/astrobiology_sources.yml`, extract:

```text
Central question
Data/evidence type
Key scientific claim
False-positive or uncertainty concern
Architecture implication
Feature or validation rule added to this repo
```

- [ ] **Step 2: Organize the review**

Use these sections:

```markdown
# Deep Astrobiology and Exobiology Literature Review

## Executive Synthesis
## Foundations of Life Detection
## Modern Biosignature Frameworks
## Habitability and Host-Star Context
## Platforms and Observatories
## Architecture Requirements Derived From the Literature
## Candidate Scientific Contributions of This Repository
## Bibliography
```

- [ ] **Step 3: Define the scientific contribution**

State the contribution conservatively:

```text
This project contributes a transparent target-prioritization and evidence-accounting platform for known exoplanets, designed to connect NASA Exoplanet Archive data with modern astrobiology evidence frameworks.
```

- [ ] **Step 4: Validate citation coverage**

Run a script or manual checklist proving every source in the YAML appears in the review.

## Task 4: Scientific Platform Architecture Document

**Files:**
- Create: `docs/architecture/scientific_platform_architecture.md`

- [ ] **Step 1: Define architecture principles**

Write these non-negotiable rules:

```text
1. Every output row must be traceable to source data and scoring assumptions.
2. Every score must expose sub-scores and missing-data penalties.
3. Duplicate planet records must be handled before ranking.
4. Biosignature language must be probabilistic and evidence-based.
5. Validation must include known exoplanet sanity checks and pipeline reproducibility.
```

- [ ] **Step 2: Add C4-style architecture**

Document:

```text
Context: NASA Exoplanet Archive + literature corpus + user-facing dashboard.
Container: Python pipeline, data artifacts, validation suite, React dashboard.
Components: data ingestion, cleaning, feature engineering, scoring, reporting, frontend export.
```

- [ ] **Step 3: Map papers to architecture**

Add a table with columns:

```text
Paper/Platform | Main idea | Architecture decision | Validation signal
```

Examples:

```text
Catling et al. 2018 | probabilistic biosignature assessment | score stores evidence and anti-evidence | output includes uncertainty and caveats
EMAC | searchable platform of modeling tools | architecture separates registry from pipeline | source catalog is machine-readable
HWO | observatory trade-space and target prioritization | dashboard highlights follow-up readiness | candidates include observable/context fields
```

## Task 5: Python Package and Configuration

**Files:**
- Create: `pyproject.toml`
- Create: `src/exoplanets_research/__init__.py`
- Create: `src/exoplanets_research/config.py`

- [ ] **Step 1: Add project metadata**

Create `pyproject.toml` with package metadata and dependencies:

```toml
[project]
name = "exoplanets-research"
version = "0.1.0"
description = "Literature-grounded exoplanet habitability and astrobiology research platform."
requires-python = ">=3.11"
dependencies = [
  "pandas",
  "numpy",
  "pyyaml",
  "matplotlib",
  "seaborn",
  "requests",
]

[project.optional-dependencies]
dev = ["pytest"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

- [ ] **Step 2: Add typed paths**

Implement constants:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
LITERATURE_DIR = DATA_DIR / "literature"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports"
```

- [ ] **Step 3: Install and verify**

Run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest -q
```

Expected: tests either pass or fail only for not-yet-implemented modules from later tasks.

## Task 6: Data Ingestion and Provenance

**Files:**
- Create: `src/exoplanets_research/data/archive.py`
- Create: `tests/test_pipeline_outputs.py`
- Create: `data/raw/README.md`

- [ ] **Step 1: Preserve the local NASA CSV as a supported input**

Implement `load_planetary_systems_csv(path: Path) -> pd.DataFrame` that handles the current file format with 294 metadata rows.

- [ ] **Step 2: Add TAP query design without making live API mandatory**

Document and implement a query builder for the NASA Exoplanet Archive PSCompPars table. Keep live fetch behind an explicit CLI flag so tests do not depend on network availability.

Query target columns:

```text
pl_name, hostname, default_flag, discoverymethod, disc_year,
pl_orbper, pl_orbsmax, pl_rade, pl_masse, pl_dens, pl_insol, pl_eqt,
st_teff, st_rad, st_mass, st_lum, st_met, st_age, sy_dist
```

- [ ] **Step 3: Write provenance metadata**

Every processed output must include a sidecar JSON:

```json
{
  "source": "NASA Exoplanet Archive",
  "input_file": "data/PS_2025.06.22_09.41.26.csv",
  "row_count": 38500,
  "generated_by": "src/exoplanets_research/pipeline.py",
  "generated_at_utc": "ISO-8601 timestamp"
}
```

## Task 7: Cleaning, De-duplication, and Feature Base

**Files:**
- Create: `src/exoplanets_research/data/cleaning.py`
- Create: `tests/test_pipeline_outputs.py`

- [ ] **Step 1: Write tests for duplicate handling**

Expected rule:

```text
If multiple rows exist for the same pl_name, prefer default_flag == 1.
If no default row exists, keep the row with the highest count of non-null critical fields.
Critical fields are pl_orbsmax, pl_rade, pl_masse, st_teff, st_rad, st_lum.
```

- [ ] **Step 2: Implement `select_best_planet_records`**

Return one row per `pl_name` and add:

```text
duplicate_record_count
selected_record_reason
```

- [ ] **Step 3: Create canonical dataset**

Run:

```bash
.venv/bin/python -m exoplanets_research.pipeline --input data/PS_2025.06.22_09.41.26.csv --stage canonical
```

Expected output:

```text
data/processed/canonical_exoplanets.csv
data/processed/canonical_exoplanets.provenance.json
```

## Task 8: Habitable Zone Model

**Files:**
- Create: `src/exoplanets_research/habitability/habitable_zone.py`
- Create: `tests/test_habitable_zone.py`

- [ ] **Step 1: Preserve current baseline formula**

Implement:

```python
def luminosity_from_log_luminosity(st_lum: float) -> float:
    return 10 ** st_lum

def simple_habitable_zone_from_log_luminosity(st_lum: float) -> tuple[float, float]:
    luminosity = luminosity_from_log_luminosity(st_lum)
    inner = (luminosity / 1.1) ** 0.5
    outer = (luminosity / 0.53) ** 0.5
    return inner, outer
```

- [ ] **Step 2: Test parity with current artifact**

Use rows from `data/habitable_zone_calculated.csv` and assert computed `hz_inner` and `hz_outer` match within `1e-8`.

- [ ] **Step 3: Add model label**

Every HZ output must include:

```text
hz_model = "simple_luminosity_kasting_like_baseline"
```

Do not imply this is a final climate model.

## Task 9: Literature-Grounded Habitability Features

**Files:**
- Create: `src/exoplanets_research/habitability/features.py`
- Create: `tests/test_scoring.py`

- [ ] **Step 1: Define feature columns**

Add:

```text
radius_class
mass_radius_data_quality
stellar_temperature_class
habitable_zone_status
hz_center_offset
insolation_available
stellar_context_available
followup_readiness_score
missing_critical_fields
```

- [ ] **Step 2: Map literature to features**

Use this mapping:

```text
Schwieterman et al. 2018 -> biosignature plausibility requires environment context.
Catling et al. 2018 -> confidence must include alternatives and uncertainty.
Krissansen-Totton et al. 2018 -> disequilibrium requires atmosphere data, so this repo should expose "not observable in current data" rather than fake a biosignature score.
HWO reports -> prioritize candidates with observability and follow-up context.
```

- [ ] **Step 3: Validate known candidates**

Assert that known high-interest candidates present in the local artifact remain visible after de-duplication when data exists:

```text
Kepler-442 b
Kepler-22 b
TRAPPIST-1 e
TOI-700 d
```

## Task 10: Evidence-Weighted Scoring

**Files:**
- Create: `src/exoplanets_research/habitability/scoring.py`
- Create: `tests/test_scoring.py`

- [ ] **Step 1: Replace opaque score with sub-scores**

Implement output fields:

```text
score_total
score_hz_position
score_planet_size
score_stellar_context
score_data_quality
score_followup_readiness
penalty_missing_data
evidence_confidence
interpretation_label
interpretation_caveat
```

- [ ] **Step 2: Define scoring policy**

Use deterministic, transparent scoring:

```text
score_hz_position: 0 to 1 based on whether orbit is inside HZ and distance from HZ center.
score_planet_size: 1.0 for 0.5-1.5 Earth radii, 0.5 for 1.5-2.5, 0.0 otherwise.
score_stellar_context: 1.0 for G, 0.75 for K, 0.25 for M, 0.0 outside configured ranges.
score_data_quality: proportion of critical fields present.
score_followup_readiness: based on sy_dist, pl_rade, st_teff, pl_orbsmax availability.
penalty_missing_data: 0.05 per missing critical field, capped at 0.25.
```

- [ ] **Step 3: Avoid biosignature overclaiming**

Set:

```text
interpretation_label = "habitability_followup_candidate"
interpretation_caveat = "No biosignature inference is made; this ranking prioritizes candidates for further observation and modeling."
```

- [ ] **Step 4: Validate ranking stability**

Compare new top 20 against current `data/top_habitable_candidates.csv`. Expected: not identical, but known candidates must be explainable by sub-scores and caveats.

## Task 11: Pipeline CLI

**Files:**
- Create: `src/exoplanets_research/pipeline.py`
- Modify: `scripts/convert_data_to_json.py`

- [ ] **Step 1: Implement staged CLI**

Support:

```bash
.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv
.venv/bin/python -m exoplanets_research.pipeline --stage literature
.venv/bin/python -m exoplanets_research.pipeline --stage canonical
.venv/bin/python -m exoplanets_research.pipeline --stage score
.venv/bin/python -m exoplanets_research.pipeline --stage export-frontend
```

- [ ] **Step 2: Write outputs**

Expected generated files:

```text
data/processed/canonical_exoplanets.csv
data/processed/habitable_zone_exoplanets.csv
data/outputs/astrobiology_ranked_candidates.csv
data/outputs/astrobiology_ranked_candidates.provenance.json
frontend/src/data/astrobiology_ranked_candidates.json
```

- [ ] **Step 3: Keep legacy conversion working**

Modify `scripts/convert_data_to_json.py` so it can export both old files and the new ranked candidates file.

## Task 12: Validation Report

**Files:**
- Create: `docs/validation/validation_report.md`

- [ ] **Step 1: Run backend validation**

Run:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv
```

Record exact outputs, row counts, and any warnings.

- [ ] **Step 2: Run frontend validation**

Run:

```bash
npm --prefix frontend run build
```

Expected: production build succeeds. If Vite warns about large chunks, record it and add a follow-up issue; do not block scientific validation unless the dashboard fails to render.

- [ ] **Step 3: Validate current known warnings**

Fix or document:

```text
frontend/src/index.css has @import after @tailwind; move @import above Tailwind directives if build warning persists.
```

- [ ] **Step 4: Write scientific validation summary**

The report must include:

```text
Data provenance checks
Duplicate handling checks
Habitable-zone formula parity
Known candidate sanity checks
Ranking caveats
Frontend build result
Scientific limitations
```

## Task 13: Dashboard Scientific Upgrade

**Files:**
- Modify: `frontend/src/App.jsx`
- Modify: `frontend/src/components/HabitablePlanetsTable.jsx`
- Create: `frontend/src/components/EvidenceBreakdown.jsx`
- Create: `frontend/src/components/LiteratureTracePanel.jsx`

- [ ] **Step 1: Use new JSON output**

Load:

```javascript
import rankedCandidates from './data/astrobiology_ranked_candidates.json';
```

- [ ] **Step 2: Show evidence, not just score**

Add table columns:

```text
Planet
Host
Total score
HZ score
Planet-size score
Data confidence
Caveat
```

- [ ] **Step 3: Add literature trace panel**

Display the scoring assumptions and cite the relevant source IDs from `data/literature/astrobiology_sources.yml`.

- [ ] **Step 4: Build**

Run:

```bash
npm --prefix frontend run build
```

Expected: build succeeds.

## Task 14: Final Quality Gate

**Files:**
- Modify: `docs/validation/validation_report.md`

- [ ] **Step 1: Full clean run**

Run:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv
npm --prefix frontend run build
```

- [ ] **Step 2: Verify output freshness**

Run:

```bash
find data/processed data/outputs frontend/src/data -maxdepth 1 -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n' | sort
```

- [ ] **Step 3: Read reports for overclaiming**

Search:

```bash
rg -n "life[ ]found|alien[ ]life|proof[ ]of[ ]life|confirmed[ ]life|biosignature[ ]detected" docs frontend/src src
```

Expected: no unsupported claims. If any appear, rewrite them as candidate-prioritization or evidence-confidence language.

## Task 15: Commit and Push

**Files:**
- Modify as needed: `.gitignore`
- Commit all intended project files only.

- [ ] **Step 1: Confirm Git status**

Run:

```bash
git rev-parse --show-toplevel
git status --short
```

If `git rev-parse` fails, initialize only after `.gitignore` exists:

```bash
git init
git status --short
```

- [ ] **Step 2: Confirm remote before push**

Run:

```bash
git remote -v
```

If no remote exists, stop and ask for the target GitHub/Git remote URL. Do not push to an unverified remote.

- [ ] **Step 3: Stage intentionally**

Run:

```bash
git add .gitignore pyproject.toml src/exoplanets_research tests scripts frontend/src docs data/literature
git add data/processed/canonical_exoplanets.csv data/processed/habitable_zone_exoplanets.csv data/outputs/astrobiology_ranked_candidates.csv data/outputs/astrobiology_ranked_candidates.provenance.json frontend/src/data/astrobiology_ranked_candidates.json
git status --short
```

Do not stage:

```text
venv/
.venv/
frontend/node_modules/
frontend/dist/
.idea/workspace.xml
large temporary raw downloads not required for reproduction
```

- [ ] **Step 4: Commit**

Run:

```bash
git commit -m "feat: add literature-grounded astrobiology platform"
```

- [ ] **Step 5: Push**

Run only after the remote is verified:

```bash
git branch --show-current
git push -u origin "$(git branch --show-current)"
```

## Done Criteria

The work is complete only when:

- `docs/research/astrobiology_literature_review.md` exists and cites every source in `data/literature/astrobiology_sources.yml`.
- `docs/architecture/scientific_platform_architecture.md` maps literature ideas to concrete architecture decisions.
- The Python pipeline produces reproducible candidate rankings with provenance.
- Tests validate source schema, HZ formula parity, duplicate handling, scoring policy, and known candidate visibility.
- The frontend builds and displays score subcomponents plus caveats.
- `docs/validation/validation_report.md` records the exact commands and results.
- Git status is clean after a commit.
- Changes are pushed to a verified remote.

## Self-Review Checklist

- [ ] No unsupported life-detection claims remain.
- [ ] Every score has sub-scores and caveats.
- [ ] Every source has a URL and architecture implication.
- [ ] The current missing `processed_exoplanet_data.parquet` issue is eliminated by the new CSV-based package path.
- [ ] The missing checkpoint-2 script is replaced by tested HZ generation in `habitability/habitable_zone.py`.
- [ ] Commit/push steps are blocked on verified remote, not guessed.
