# Scientific Paper Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the current exoplanet target-prioritization prototype into a publishable scientific software contribution with a defensible method, uncertainty modeling, external validation, reproducible experiments, and a paper-ready artifact package.

**Architecture:** Keep the current modular pipeline, but promote the method from a fixed heuristic into an evidence-calibrated, uncertainty-aware research workflow. The pipeline will become: archive snapshot -> canonical records -> multiple HZ model families -> evidence features -> configurable scoring -> uncertainty/rank-stability -> external validation -> paper figures/tables -> reproducible manuscript package.

**Tech Stack:** Python 3.11+, pandas, numpy, PyYAML, pytest, matplotlib/seaborn, requests, NASA Exoplanet Archive TAP/PSCompPars, optional scipy for rank correlations, React/Vite dashboard as a communication artifact.

---

## 1. What We Want

We want a scientific contribution that is stronger than a dashboard or a ranked table. The target contribution is:

> An open, reproducible, literature-grounded framework for prioritizing exoplanet follow-up targets using decomposed evidence, multiple habitable-zone models, uncertainty propagation, rank-stability analysis, and validation against mission-relevant target catalogs.

The paper should not claim detection of life or biosignatures. The defensible claim is that we provide a transparent and reproducible decision-support layer for astrobiology target prioritization.

## 2. Scientific Originality

The original contribution should be the combination of these pieces in one reproducible platform:

1. **Evidence decomposition:** Every candidate is described by independent evidence dimensions instead of a single opaque habitability score.
2. **HZ model comparison:** The current simple luminosity baseline is compared against Kopparapu-style conservative and optimistic HZ boundaries.
3. **Uncertainty-aware ranking:** Catalog measurement errors are propagated into score distributions and rank-stability metrics.
4. **Mission-facing validation:** Results are crossmatched with HWO/HPIC and ExEP precursor science targets when host-star matches are available.
5. **Standards-of-evidence communication:** Outputs explicitly separate target prioritization from biosignature inference and map evidence maturity to conservative confidence labels.
6. **Reproducible scientific artifact:** The repo contains data lineage, code, tests, figures, manuscript sources, and exact commands for regeneration.

## 3. Literature and Source Base

Use these sources as the minimum scientific backbone. Add more only when they directly support a model, validation target, or limitation.

| Source | Why it matters for this project | Implementation use |
| --- | --- | --- |
| NASA Exoplanet Archive PS/PSCompPars documentation: https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html | Defines current archive columns, uncertainties, and PSCompPars semantics. | Data dictionary, TAP query builder, uncertainty column mapping. |
| NASA Exoplanet Archive TAP guide: https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html | Primary programmatic retrieval path. | Explicit `fetch-live` command with cached snapshots. |
| Akeson et al. 2013, NASA Exoplanet Archive: https://www.ipac.caltech.edu/publication/2013PASP..125..989A | Establishes the archive as a scientific data platform. | Data provenance and archive citation in Methods. |
| Kopparapu et al. 2013, new HZ estimates: https://arxiv.org/abs/1301.6674 | Standard modern 1D HZ boundaries. | Baseline comparative HZ model. |
| Kopparapu et al. 2014, planetary-mass-dependent HZ: https://arxiv.org/abs/1404.5292 | HZ depends on stellar effective temperature and planet mass assumptions. | Conservative/optimistic HZ model families and sensitivity analysis. |
| Schwieterman et al. 2018, remotely detectable signs of life: https://doi.org/10.1089/ast.2017.1729 | Biosignatures require environmental context and false-positive analysis. | Caveat and evidence-maturity schema. |
| Catling et al. 2018, biosignature assessment framework: https://www.giss.nasa.gov/pubs/abs/ca07620h.html | Argues for probabilistic assessment and abiotic alternatives. | Future evidence-argument fields; no single decisive marker. |
| Meadows et al. 2018, oxygen context: https://arxiv.org/abs/1705.07560 | Context matters for any atmospheric biosignature. | Explicit non-inference boundary for catalog-only data. |
| Neveu et al. 2018, Ladder of Life Detection: https://doi.org/10.1089/ast.2017.1773 | Confidence should be staged and evidence-based. | Evidence confidence labels and report language. |
| Community Biosignature Standards of Evidence Workshop 2022: https://arxiv.org/abs/2210.14293 | Community standards for communication and robustness. | Validation report and communication guardrails. |
| Green et al. 2024, confidence of life detection communication: https://www.nature.com/articles/s41550-023-02135-1 | Avoids sensational claims and motivates careful communication. | README, dashboard, and paper abstract language. |
| HPIC 2024: https://arxiv.org/abs/2402.08038 | HWO preliminary input catalog of about 13,000 nearby bright stars. | External host-star validation and mission relevance. |
| ExEP HWO precursor science stars: https://exoplanetarchive.ipac.caltech.edu/docs/MissionStellar.html | Mission-facing target list for HWO precursor science. | External validation labels for nearby target hosts. |
| Dynamical viability for HWO targets: https://arxiv.org/abs/2408.00263 | Adds dynamical viability as a mission-relevant HZ constraint. | Optional validation feature for systems with known dynamical metrics. |

## 4. Target Paper Shape

Working title:

**Evidence-Calibrated Target Prioritization for Astrobiology Follow-Up of Confirmed Exoplanets**

Paper sections:

1. Abstract.
2. Introduction: target prioritization gap; why not biosignature detection.
3. Data: NASA Exoplanet Archive snapshot, PSCompPars fields, provenance.
4. Methods: canonicalization, HZ models, evidence dimensions, score formulation, uncertainty propagation.
5. Validation: known candidates, baselines, HWO/HPIC crossmatch, ablations, rank stability.
6. Results: robust top candidates, disagreement cases, sensitivity to HZ model and weights.
7. Discussion: scientific interpretation, limitations, false-positive caution, mission relevance.
8. Reproducibility: code, data snapshot, DOI, tests, figures.

## 5. Success Criteria

The project is paper-ready when all criteria below are satisfied:

- [ ] The current fixed score is replaced by versioned scoring configurations.
- [ ] At least three HZ model outputs exist: current simple baseline, Kopparapu conservative, Kopparapu optimistic.
- [ ] Each ranked candidate has `score_mean`, `score_std`, `rank_median`, `rank_p05`, `rank_p95`, and `top10_probability`.
- [ ] The pipeline can reproduce all paper tables and figures with one command.
- [ ] The top-ranked candidates are compared against at least two baselines.
- [ ] External validation includes host-star overlap with HPIC or ExEP HWO precursor target lists.
- [ ] Results include rank-correlation metrics and top-k overlap metrics.
- [ ] The limitations section explicitly states why catalog-only ranking cannot infer biosignatures.
- [ ] CI runs tests, pipeline smoke checks, and conservative-language checks.
- [ ] The repo has `LICENSE`, `CITATION.cff`, `paper/`, and a reproducibility command.

## 6. File Structure To Create Or Modify

Create:

- `src/exoplanets_research/habitability/hz_models.py`  
  Multiple HZ model implementations and a stable public interface.

- `src/exoplanets_research/habitability/scoring_config.py`  
  Versioned score weights and named score profiles.

- `src/exoplanets_research/uncertainty/monte_carlo.py`  
  Uncertainty sampling from archive central values and asymmetric errors.

- `src/exoplanets_research/validation/baselines.py`  
  Baseline ranking methods and metrics.

- `src/exoplanets_research/validation/external_targets.py`  
  HPIC/ExEP/HWO external target loading and host-star crossmatch.

- `src/exoplanets_research/experiments/run_ablation.py`  
  CLI runner for score ablation, HZ model comparison, sensitivity, and top-k stability.

- `src/exoplanets_research/paper/figures.py`  
  Deterministic figure generation for paper-ready outputs.

- `configs/scoring/ectp_v1.yml`  
  First versioned score profile.

- `configs/experiments/paper_v1.yml`  
  Experiment manifest for paper results.

- `data/external/README.md`  
  Instructions for downloading external catalogs instead of committing large raw files.

- `data/external/.gitkeep`  
  Keeps directory structure without storing downloaded external data.

- `paper/manuscript.md`  
  Draft manuscript.

- `paper/references.bib`  
  Bibliography entries for the paper sources.

- `paper/figures/.gitkeep`  
  Output location for generated figures.

- `paper/tables/.gitkeep`  
  Output location for generated tables.

- `.github/workflows/ci.yml`  
  Reproducibility checks on push and pull request.

- `CITATION.cff`  
  Software citation metadata.

- `LICENSE`  
  Open-source license. Recommended: MIT for code unless a different license is required.

Modify:

- `src/exoplanets_research/habitability/habitable_zone.py`  
  Delegate to `hz_models.py` while preserving current behavior as `simple_luminosity_baseline`.

- `src/exoplanets_research/habitability/features.py`  
  Add model-aware HZ features, stellar context flags, and observation-quality features.

- `src/exoplanets_research/habitability/scoring.py`  
  Accept scoring configs, expose subscore formulas, and support profile metadata.

- `src/exoplanets_research/pipeline.py`  
  Add CLI options for HZ model, score profile, uncertainty runs, and paper artifact export.

- `docs/validation/validation_report.md`  
  Replace static validation with generated paper-validation summary.

- `README.md`  
  Add paper reproduction command and cite the method name.

- `.gitignore`  
  Ignore generated external data, paper build outputs, and large intermediate experiment files.

## 7. Implementation Tasks

### Task 1: Define The Scientific Method Contract

**Files:**
- Create: `docs/research/scientific_method_contract.md`
- Modify: `README.md`

- [ ] **Step 1: Write the method contract**

Create `docs/research/scientific_method_contract.md` with these sections:

```markdown
# Scientific Method Contract

## Method Name

Evidence-Calibrated Target Prioritization (ECTP)

## Scientific Claim

ECTP ranks confirmed exoplanets for astrobiology follow-up using catalog-level evidence, uncertainty propagation, and validation against mission-facing target lists. ECTP does not infer biosignatures or life.

## Evidence Dimensions

1. Habitable-zone position.
2. Planet radius and mass context.
3. Stellar effective temperature and host-star context.
4. Data completeness and measurement uncertainty.
5. Follow-up observability and mission relevance.
6. Evidence maturity and unsupported inference boundaries.

## Required Outputs

Every ranked row must include:

- central sub-scores;
- uncertainty-aware score summary;
- confidence label;
- HZ model used;
- score profile used;
- provenance pointer;
- interpretation caveat.

## Non-Claims

The system does not claim atmospheric composition, disequilibrium, biosignatures, biological activity, or habitability in the ecological sense.

## Paper Contribution

The contribution is a reproducible decision-support framework that makes target-prioritization assumptions explicit, measurable, and stress-tested.
```

- [ ] **Step 2: Link the method contract from README**

Add one sentence under `## Scientific Design`:

```markdown
The publishable method target is defined in [Scientific Method Contract](docs/research/scientific_method_contract.md).
```

- [ ] **Step 3: Validate docs**

Run:

```bash
rg -n "biosignature[ ]detected|confirmed[ ]life|proof[ ]of[ ]life|alien[ ]life|life[ ]found" README.md docs
```

Expected result: no matches.

- [ ] **Step 4: Commit**

```bash
git add README.md docs/research/scientific_method_contract.md
git commit -m "docs: define scientific method contract"
```

**Checkpoint:** The scientific claim is explicit, conservative, and traceable.

### Task 2: Implement Multiple Habitable-Zone Models

**Files:**
- Create: `src/exoplanets_research/habitability/hz_models.py`
- Modify: `src/exoplanets_research/habitability/habitable_zone.py`
- Test: `tests/test_hz_models.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_hz_models.py`:

```python
import math

import pandas as pd

from exoplanets_research.habitability.hz_models import (
    calculate_hz_bounds,
    supported_hz_models,
)


def test_supported_hz_models_include_baseline_and_kopparapu_profiles():
    assert {
        "simple_luminosity_baseline",
        "kopparapu_conservative_earth_mass",
        "kopparapu_optimistic_earth_mass",
    }.issubset(set(supported_hz_models()))


def test_simple_luminosity_baseline_preserves_current_solar_case():
    bounds = calculate_hz_bounds(st_lum=0.0, st_teff=5778, model="simple_luminosity_baseline")

    assert math.isclose(bounds.inner_au, math.sqrt(1 / 1.1), rel_tol=1e-12)
    assert math.isclose(bounds.outer_au, math.sqrt(1 / 0.53), rel_tol=1e-12)
    assert bounds.model == "simple_luminosity_baseline"


def test_kopparapu_conservative_returns_solar_like_bounds():
    bounds = calculate_hz_bounds(st_lum=0.0, st_teff=5780, model="kopparapu_conservative_earth_mass")

    assert 0.90 <= bounds.inner_au <= 1.05
    assert 1.55 <= bounds.outer_au <= 1.80
    assert bounds.inner_limit == "runaway_greenhouse"
    assert bounds.outer_limit == "maximum_greenhouse"


def test_invalid_or_missing_inputs_return_unknown_bounds():
    bounds = calculate_hz_bounds(st_lum=pd.NA, st_teff=5780, model="kopparapu_conservative_earth_mass")

    assert pd.isna(bounds.inner_au)
    assert pd.isna(bounds.outer_au)
    assert bounds.model == "kopparapu_conservative_earth_mass"
```

- [ ] **Step 2: Run tests and confirm failure**

Run:

```bash
.venv/bin/python -m pytest tests/test_hz_models.py -q
```

Expected: fails because `hz_models.py` does not exist.

- [ ] **Step 3: Implement model interface**

Create `src/exoplanets_research/habitability/hz_models.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Literal

import pandas as pd


HZModelName = Literal[
    "simple_luminosity_baseline",
    "kopparapu_conservative_earth_mass",
    "kopparapu_optimistic_earth_mass",
]


@dataclass(frozen=True)
class HZBounds:
    model: str
    inner_au: float
    outer_au: float
    inner_limit: str
    outer_limit: str


def supported_hz_models() -> list[str]:
    return [
        "simple_luminosity_baseline",
        "kopparapu_conservative_earth_mass",
        "kopparapu_optimistic_earth_mass",
    ]


def _is_missing(value: object) -> bool:
    return pd.isna(value)


def _luminosity_from_log10(st_lum: float) -> float:
    return 10 ** float(st_lum)


def _nan_bounds(model: str, inner_limit: str, outer_limit: str) -> HZBounds:
    return HZBounds(model=model, inner_au=float("nan"), outer_au=float("nan"), inner_limit=inner_limit, outer_limit=outer_limit)


def _simple_luminosity_baseline(st_lum: float) -> HZBounds:
    luminosity = _luminosity_from_log10(st_lum)
    return HZBounds(
        model="simple_luminosity_baseline",
        inner_au=sqrt(luminosity / 1.1),
        outer_au=sqrt(luminosity / 0.53),
        inner_limit="simple_inner_flux",
        outer_limit="simple_outer_flux",
    )


def _kopparapu_seff(st_teff: float, limit: str) -> float:
    # Coefficients from Kopparapu et al. 2014 for 1 Earth-mass HZ boundaries.
    coefficients = {
        "recent_venus": (1.776, -1.433e-4, -3.395e-9, -7.636e-12, -1.195e-15),
        "runaway_greenhouse": (1.107, -1.332e-4, -1.58e-8, 8.308e-12, -1.931e-15),
        "maximum_greenhouse": (0.356, 6.171e-5, 1.698e-9, -3.198e-12, -5.575e-16),
        "early_mars": (0.32, 2.137e-4, -2.533e-8, -1.332e-11, -3.097e-15),
    }
    seff_sun, a, b, c, d = coefficients[limit]
    t_star = float(st_teff) - 5780.0
    return seff_sun + (a * t_star) + (b * t_star**2) + (c * t_star**3) + (d * t_star**4)


def _kopparapu(st_lum: float, st_teff: float, *, model: str, inner_limit: str, outer_limit: str) -> HZBounds:
    luminosity = _luminosity_from_log10(st_lum)
    inner_flux = _kopparapu_seff(st_teff, inner_limit)
    outer_flux = _kopparapu_seff(st_teff, outer_limit)
    return HZBounds(
        model=model,
        inner_au=sqrt(luminosity / inner_flux),
        outer_au=sqrt(luminosity / outer_flux),
        inner_limit=inner_limit,
        outer_limit=outer_limit,
    )


def calculate_hz_bounds(st_lum: float, st_teff: float | None, model: HZModelName = "simple_luminosity_baseline") -> HZBounds:
    if model not in supported_hz_models():
        raise ValueError(f"Unsupported HZ model: {model}")
    if _is_missing(st_lum):
        if model == "kopparapu_optimistic_earth_mass":
            return _nan_bounds(model, "recent_venus", "early_mars")
        if model == "kopparapu_conservative_earth_mass":
            return _nan_bounds(model, "runaway_greenhouse", "maximum_greenhouse")
        return _nan_bounds(model, "simple_inner_flux", "simple_outer_flux")
    if model == "simple_luminosity_baseline":
        return _simple_luminosity_baseline(float(st_lum))
    if _is_missing(st_teff):
        if model == "kopparapu_optimistic_earth_mass":
            return _nan_bounds(model, "recent_venus", "early_mars")
        return _nan_bounds(model, "runaway_greenhouse", "maximum_greenhouse")
    if model == "kopparapu_conservative_earth_mass":
        return _kopparapu(
            float(st_lum),
            float(st_teff),
            model=model,
            inner_limit="runaway_greenhouse",
            outer_limit="maximum_greenhouse",
        )
    return _kopparapu(
        float(st_lum),
        float(st_teff),
        model=model,
        inner_limit="recent_venus",
        outer_limit="early_mars",
    )
```

- [ ] **Step 4: Update current HZ adapter**

Modify `src/exoplanets_research/habitability/habitable_zone.py` so `add_habitable_zone_columns` accepts `model`:

```python
from exoplanets_research.habitability.hz_models import calculate_hz_bounds

HZ_MODEL = "simple_luminosity_baseline"


def simple_habitable_zone_from_log_luminosity(st_lum: float) -> tuple[float, float]:
    bounds = calculate_hz_bounds(st_lum=st_lum, st_teff=None, model="simple_luminosity_baseline")
    return bounds.inner_au, bounds.outer_au


def add_habitable_zone_columns(df: pd.DataFrame, *, model: str = HZ_MODEL) -> pd.DataFrame:
    ...
    for index, row in result.loc[valid_luminosity].iterrows():
        bounds = calculate_hz_bounds(st_lum=row.get("st_lum"), st_teff=row.get("st_teff"), model=model)
        result.at[index, "hz_inner"] = bounds.inner_au
        result.at[index, "hz_outer"] = bounds.outer_au
        result.at[index, "hz_model"] = bounds.model
        result.at[index, "hz_inner_limit"] = bounds.inner_limit
        result.at[index, "hz_outer_limit"] = bounds.outer_limit
```

Keep the existing `habitable_zone_status` logic unchanged.

- [ ] **Step 5: Run tests**

Run:

```bash
.venv/bin/python -m pytest tests/test_hz_models.py tests/test_habitable_zone.py -q
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add src/exoplanets_research/habitability/hz_models.py src/exoplanets_research/habitability/habitable_zone.py tests/test_hz_models.py
git commit -m "feat: add publishable habitable-zone models"
```

**Checkpoint:** The current baseline is preserved and two literature-grounded HZ profiles are available.

### Task 3: Add Versioned Scoring Profiles

**Files:**
- Create: `configs/scoring/ectp_v1.yml`
- Create: `src/exoplanets_research/habitability/scoring_config.py`
- Modify: `src/exoplanets_research/habitability/scoring.py`
- Test: `tests/test_scoring_config.py`

- [ ] **Step 1: Create scoring config**

Create `configs/scoring/ectp_v1.yml`:

```yaml
id: ectp_v1
label: Evidence-Calibrated Target Prioritization v1
description: Catalog-level astrobiology follow-up prioritization with decomposed evidence.
weights:
  hz_position: 0.35
  planet_size: 0.20
  stellar_context: 0.15
  data_quality: 0.15
  followup_readiness: 0.15
penalties:
  missing_field: 0.05
  max_missing_data: 0.25
confidence:
  moderate_min_data_quality: 0.85
  limited_min_data_quality: 0.60
non_claim: No biosignature inference is made; this ranking prioritizes candidates for further observation and modeling.
```

- [ ] **Step 2: Write tests**

Create `tests/test_scoring_config.py`:

```python
from pathlib import Path

from exoplanets_research.habitability.scoring_config import load_scoring_config


def test_load_scoring_config_has_normalized_weights():
    config = load_scoring_config(Path("configs/scoring/ectp_v1.yml"))

    assert config.id == "ectp_v1"
    assert round(sum(config.weights.values()), 8) == 1.0
    assert config.penalties["max_missing_data"] == 0.25
    assert "No biosignature inference" in config.non_claim
```

- [ ] **Step 3: Implement config loader**

Create `src/exoplanets_research/habitability/scoring_config.py`:

```python
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class ScoringConfig:
    id: str
    label: str
    description: str
    weights: dict[str, float]
    penalties: dict[str, float]
    confidence: dict[str, float]
    non_claim: str


def load_scoring_config(path: Path) -> ScoringConfig:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    weights = {key: float(value) for key, value in payload["weights"].items()}
    total_weight = sum(weights.values())
    if round(total_weight, 8) != 1.0:
        raise ValueError(f"Scoring weights must sum to 1.0, got {total_weight}")
    return ScoringConfig(
        id=str(payload["id"]),
        label=str(payload["label"]),
        description=str(payload["description"]),
        weights=weights,
        penalties={key: float(value) for key, value in payload["penalties"].items()},
        confidence={key: float(value) for key, value in payload["confidence"].items()},
        non_claim=str(payload["non_claim"]),
    )
```

- [ ] **Step 4: Modify scoring function**

Modify `score_candidates` to accept `config: ScoringConfig | None = None`. When `None`, load `configs/scoring/ectp_v1.yml`. Add columns:

- `score_profile_id`
- `score_profile_label`
- `score_weight_hz_position`
- `score_weight_planet_size`
- `score_weight_stellar_context`
- `score_weight_data_quality`
- `score_weight_followup_readiness`

- [ ] **Step 5: Run tests**

```bash
.venv/bin/python -m pytest tests/test_scoring.py tests/test_scoring_config.py -q
```

Expected: all scoring tests pass.

- [ ] **Step 6: Commit**

```bash
git add configs/scoring/ectp_v1.yml src/exoplanets_research/habitability/scoring_config.py src/exoplanets_research/habitability/scoring.py tests/test_scoring_config.py tests/test_scoring.py
git commit -m "feat: add versioned scoring profiles"
```

**Checkpoint:** Reviewer can inspect exactly why a candidate received a score.

### Task 4: Add Uncertainty Propagation

**Files:**
- Create: `src/exoplanets_research/uncertainty/__init__.py`
- Create: `src/exoplanets_research/uncertainty/monte_carlo.py`
- Test: `tests/test_uncertainty.py`

- [ ] **Step 1: Write tests**

Create `tests/test_uncertainty.py`:

```python
import pandas as pd

from exoplanets_research.uncertainty.monte_carlo import summarize_rank_uncertainty


def test_rank_uncertainty_summary_has_required_columns():
    samples = pd.DataFrame(
        [
            {"run_id": 0, "pl_name": "A b", "score_total": 0.8},
            {"run_id": 0, "pl_name": "B b", "score_total": 0.6},
            {"run_id": 1, "pl_name": "A b", "score_total": 0.7},
            {"run_id": 1, "pl_name": "B b", "score_total": 0.9},
        ]
    )

    summary = summarize_rank_uncertainty(samples, top_k=1)

    assert {"score_mean", "score_std", "rank_median", "rank_p05", "rank_p95", "top1_probability"}.issubset(summary.columns)
    assert set(summary["pl_name"]) == {"A b", "B b"}
```

- [ ] **Step 2: Implement summary function**

Create `src/exoplanets_research/uncertainty/monte_carlo.py`:

```python
import pandas as pd


def summarize_rank_uncertainty(samples: pd.DataFrame, *, top_k: int = 10) -> pd.DataFrame:
    ranked = samples.copy()
    ranked["rank"] = ranked.groupby("run_id")["score_total"].rank(method="first", ascending=False)
    summary = (
        ranked.groupby("pl_name")
        .agg(
            score_mean=("score_total", "mean"),
            score_std=("score_total", "std"),
            rank_median=("rank", "median"),
            rank_p05=("rank", lambda values: values.quantile(0.05)),
            rank_p95=("rank", lambda values: values.quantile(0.95)),
            top_probability=("rank", lambda values: (values <= top_k).mean()),
        )
        .reset_index()
    )
    summary = summary.rename(columns={"top_probability": f"top{top_k}_probability"})
    return summary.sort_values(["rank_median", "score_mean"], ascending=[True, False]).reset_index(drop=True)
```

- [ ] **Step 3: Add sampling function**

Extend `monte_carlo.py` with:

```python
def sample_asymmetric_normal(
    value: float,
    err_plus: float | None,
    err_minus: float | None,
    *,
    rng,
) -> float:
    if pd.isna(value):
        return value
    sigma_plus = abs(float(err_plus)) if not pd.isna(err_plus) else 0.0
    sigma_minus = abs(float(err_minus)) if not pd.isna(err_minus) else sigma_plus
    sigma = max(sigma_plus, sigma_minus)
    if sigma == 0:
        return float(value)
    return float(rng.normal(float(value), sigma))
```

Use this for `pl_orbsmax`, `pl_rade`, `pl_masse`, `st_teff`, `st_rad`, and `st_lum` when corresponding `err1/err2` columns exist.

- [ ] **Step 4: Add pipeline integration**

Modify `src/exoplanets_research/pipeline.py` to accept:

```bash
--uncertainty-runs 0
--uncertainty-seed 42
```

When `--uncertainty-runs > 0`, write:

- `data/outputs/astrobiology_uncertainty_samples.csv`
- `data/outputs/astrobiology_rank_uncertainty.csv`

- [ ] **Step 5: Run tests**

```bash
.venv/bin/python -m pytest tests/test_uncertainty.py tests/test_pipeline_outputs.py -q
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add src/exoplanets_research/uncertainty tests/test_uncertainty.py src/exoplanets_research/pipeline.py tests/test_pipeline_outputs.py
git commit -m "feat: add rank uncertainty propagation"
```

**Checkpoint:** Every paper ranking can report stability, not just central values.

### Task 5: Add Baselines and Rank Metrics

**Files:**
- Create: `src/exoplanets_research/validation/baselines.py`
- Test: `tests/test_baselines.py`

- [ ] **Step 1: Write tests**

Create `tests/test_baselines.py`:

```python
import pandas as pd

from exoplanets_research.validation.baselines import top_k_jaccard, rank_correlation_summary


def test_top_k_jaccard_measures_overlap():
    left = ["A", "B", "C"]
    right = ["B", "C", "D"]

    assert top_k_jaccard(left, right, k=3) == 0.5


def test_rank_correlation_summary_handles_identical_rankings():
    df = pd.DataFrame(
        {
            "pl_name": ["A", "B", "C"],
            "rank_a": [1, 2, 3],
            "rank_b": [1, 2, 3],
        }
    )

    summary = rank_correlation_summary(df, "rank_a", "rank_b")

    assert summary["spearman_r"] == 1.0
```

- [ ] **Step 2: Add scipy dependency**

Modify `pyproject.toml`:

```toml
dependencies = [
  "pandas",
  "numpy",
  "pyyaml",
  "matplotlib",
  "seaborn",
  "requests",
  "scipy",
]
```

- [ ] **Step 3: Implement metrics**

Create `src/exoplanets_research/validation/baselines.py`:

```python
import pandas as pd
from scipy.stats import spearmanr, kendalltau


def top_k_jaccard(left: list[str], right: list[str], *, k: int) -> float:
    left_set = set(left[:k])
    right_set = set(right[:k])
    if not left_set and not right_set:
        return 1.0
    return len(left_set & right_set) / len(left_set | right_set)


def rank_correlation_summary(df: pd.DataFrame, left_rank: str, right_rank: str) -> dict[str, float]:
    clean = df[[left_rank, right_rank]].dropna()
    if len(clean) < 2:
        return {"spearman_r": float("nan"), "kendall_tau": float("nan"), "n": float(len(clean))}
    spearman = spearmanr(clean[left_rank], clean[right_rank]).statistic
    kendall = kendalltau(clean[left_rank], clean[right_rank]).statistic
    return {"spearman_r": float(spearman), "kendall_tau": float(kendall), "n": float(len(clean))}
```

- [ ] **Step 4: Add baseline ranking functions**

Add functions:

```python
def hz_radius_baseline(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["baseline_score"] = (
        (result["habitable_zone_status"].eq("inside").astype(float) * 0.7)
        + (result["pl_rade"].between(0.5, 1.5).fillna(False).astype(float) * 0.3)
    )
    return result.sort_values(["baseline_score", "pl_name"], ascending=[False, True]).reset_index(drop=True)
```

- [ ] **Step 5: Run tests**

```bash
.venv/bin/python -m pytest tests/test_baselines.py -q
```

Expected: tests pass.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/exoplanets_research/validation/baselines.py tests/test_baselines.py
git commit -m "feat: add baseline ranking metrics"
```

**Checkpoint:** We can quantify whether ECTP is meaningfully different from simple baselines.

### Task 6: Add External Mission-Facing Validation

**Files:**
- Create: `data/external/README.md`
- Create: `data/external/.gitkeep`
- Create: `src/exoplanets_research/validation/external_targets.py`
- Test: `tests/test_external_targets.py`

- [ ] **Step 1: Document external data policy**

Create `data/external/README.md`:

```markdown
# External Validation Data

This directory is for locally downloaded mission-facing validation catalogs.

Do not commit large external raw files. Record source URL, download date, checksum, and processing command in `docs/validation/external_data_inventory.md`.

Primary external sources:

- NASA Exoplanet Archive Mission Stellar Targets: https://exoplanetarchive.ipac.caltech.edu/docs/MissionStellar.html
- HPIC paper: https://arxiv.org/abs/2402.08038
- Dynamical viability HWO target paper: https://arxiv.org/abs/2408.00263
```

- [ ] **Step 2: Write crossmatch tests**

Create `tests/test_external_targets.py`:

```python
import pandas as pd

from exoplanets_research.validation.external_targets import add_host_target_flags


def test_add_host_target_flags_marks_known_hosts():
    ranked = pd.DataFrame({"hostname": ["TRAPPIST-1", "Tau Ceti", "Kepler-442"]})
    targets = pd.DataFrame({"hostname": ["Tau Ceti"], "target_list": ["hwo_precursor"]})

    result = add_host_target_flags(ranked, targets)

    assert result.loc[result["hostname"] == "Tau Ceti", "external_target_match"].iloc[0] is True
    assert result.loc[result["hostname"] == "TRAPPIST-1", "external_target_match"].iloc[0] is False
```

- [ ] **Step 3: Implement host crossmatch**

Create `src/exoplanets_research/validation/external_targets.py`:

```python
import pandas as pd


def normalize_host_name(value: str) -> str:
    return " ".join(str(value).strip().lower().split())


def add_host_target_flags(ranked: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    result = ranked.copy()
    target_hosts = {normalize_host_name(value) for value in targets["hostname"].dropna()}
    normalized = result["hostname"].map(normalize_host_name)
    result["external_target_match"] = normalized.isin(target_hosts)
    target_lists = targets.copy()
    target_lists["_host_key"] = target_lists["hostname"].map(normalize_host_name)
    grouped = target_lists.groupby("_host_key")["target_list"].apply(lambda values: ";".join(sorted(set(values)))).to_dict()
    result["external_target_lists"] = normalized.map(grouped).fillna("")
    return result
```

- [ ] **Step 4: Run tests**

```bash
.venv/bin/python -m pytest tests/test_external_targets.py -q
```

Expected: tests pass.

- [ ] **Step 5: Commit**

```bash
git add data/external src/exoplanets_research/validation/external_targets.py tests/test_external_targets.py
git commit -m "feat: add external target validation hooks"
```

**Checkpoint:** The method can be evaluated against mission-relevant target lists.

### Task 7: Build The Experiment Runner

**Files:**
- Create: `configs/experiments/paper_v1.yml`
- Create: `src/exoplanets_research/experiments/__init__.py`
- Create: `src/exoplanets_research/experiments/run_ablation.py`
- Test: `tests/test_experiment_config.py`

- [ ] **Step 1: Create experiment manifest**

Create `configs/experiments/paper_v1.yml`:

```yaml
id: paper_v1
input: data/PS_2025.06.22_09.41.26.csv
hz_models:
  - simple_luminosity_baseline
  - kopparapu_conservative_earth_mass
  - kopparapu_optimistic_earth_mass
score_profiles:
  - configs/scoring/ectp_v1.yml
uncertainty:
  runs: 500
  seed: 42
top_k:
  - 10
  - 25
  - 50
outputs:
  directory: data/outputs/experiments/paper_v1
```

- [ ] **Step 2: Write manifest test**

Create `tests/test_experiment_config.py`:

```python
from pathlib import Path

import yaml


def test_paper_v1_manifest_has_required_experiments():
    payload = yaml.safe_load(Path("configs/experiments/paper_v1.yml").read_text())

    assert payload["id"] == "paper_v1"
    assert "kopparapu_conservative_earth_mass" in payload["hz_models"]
    assert payload["uncertainty"]["runs"] >= 500
    assert 10 in payload["top_k"]
```

- [ ] **Step 3: Implement experiment CLI skeleton**

Create `src/exoplanets_research/experiments/run_ablation.py`:

```python
import argparse
from pathlib import Path

import yaml


def load_experiment_manifest(path: Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run paper-grade ECTP experiments.")
    parser.add_argument("--config", type=Path, default=Path("configs/experiments/paper_v1.yml"))
    args = parser.parse_args()
    manifest = load_experiment_manifest(args.config)
    output_dir = Path(manifest["outputs"]["directory"])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "manifest_resolved.yml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    print(f"experiment_id: {manifest['id']}")
    print(f"output_dir: {output_dir}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests and smoke command**

```bash
.venv/bin/python -m pytest tests/test_experiment_config.py -q
.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml
```

Expected:

```text
experiment_id: paper_v1
output_dir: data/outputs/experiments/paper_v1
```

- [ ] **Step 5: Commit**

```bash
git add configs/experiments/paper_v1.yml src/exoplanets_research/experiments tests/test_experiment_config.py
git commit -m "feat: add paper experiment manifest"
```

**Checkpoint:** The paper has one canonical experiment entry point.

### Task 8: Generate Paper Figures And Tables

**Files:**
- Create: `src/exoplanets_research/paper/__init__.py`
- Create: `src/exoplanets_research/paper/figures.py`
- Create: `paper/figures/.gitkeep`
- Create: `paper/tables/.gitkeep`
- Test: `tests/test_paper_figures.py`

- [ ] **Step 1: Write figure smoke test**

Create `tests/test_paper_figures.py`:

```python
from pathlib import Path

import pandas as pd

from exoplanets_research.paper.figures import write_top_candidate_table


def test_write_top_candidate_table(tmp_path):
    ranked = pd.DataFrame(
        {
            "pl_name": ["A b", "B b"],
            "hostname": ["A", "B"],
            "score_total": [0.9, 0.8],
            "evidence_confidence": ["moderate_catalog_confidence", "limited_catalog_confidence"],
        }
    )
    output = tmp_path / "top_candidates.md"

    write_top_candidate_table(ranked, output, top_n=2)

    text = output.read_text(encoding="utf-8")
    assert "A b" in text
    assert "score_total" in text
```

- [ ] **Step 2: Implement paper table writer**

Create `src/exoplanets_research/paper/figures.py`:

```python
from pathlib import Path

import pandas as pd


def write_top_candidate_table(ranked: pd.DataFrame, output_path: Path, *, top_n: int = 25) -> None:
    columns = ["pl_name", "hostname", "score_total", "evidence_confidence"]
    table = ranked.loc[:, columns].head(top_n).copy()
    table["score_total"] = table["score_total"].round(3)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(table.to_markdown(index=False) + "\n", encoding="utf-8")
```

- [ ] **Step 3: Add matplotlib figures**

Add functions:

- `plot_score_distribution(ranked, output_path)`
- `plot_subscore_heatmap(ranked, output_path, top_n=25)`
- `plot_rank_uncertainty(uncertainty, output_path, top_n=25)`
- `plot_hz_model_overlap(experiment_summary, output_path)`

Each function must create parent directories and write deterministic `.png` files.

- [ ] **Step 4: Run tests**

```bash
.venv/bin/python -m pytest tests/test_paper_figures.py -q
```

Expected: tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/exoplanets_research/paper paper tests/test_paper_figures.py
git commit -m "feat: add paper artifact generation"
```

**Checkpoint:** Figures and tables are generated from pipeline outputs, not manually assembled.

### Task 9: Add CI And Reproducibility Metadata

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `CITATION.cff`
- Create: `LICENSE`
- Modify: `.gitignore`

- [ ] **Step 1: Create GitHub Actions workflow**

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: actions/setup-node@v4
        with:
          node-version: "22.16.0"
      - name: Install Python package
        run: |
          python -m pip install --upgrade pip
          python -m pip install -e ".[dev]"
      - name: Run tests
        run: python -m pytest -q
      - name: Conservative language check
        run: |
          ! grep -R -n -E "life[ ]found|alien[ ]life|proof[ ]of[ ]life|confirmed[ ]life|biosignature[ ]detected" docs frontend/src src
      - name: Frontend install
        run: npm --prefix frontend ci
      - name: Frontend build
        run: npm --prefix frontend run build
```

- [ ] **Step 2: Add citation file**

Create `CITATION.cff`:

```yaml
cff-version: 1.2.0
title: Exoplanet Research Platform
message: If you use this software, please cite it using the metadata from this file.
type: software
authors:
  - family-names: Kevyn
    given-names: Maicon
repository-code: https://github.com/MaiconKevyn/exoplanet-research
abstract: Literature-grounded exoplanet habitability and astrobiology target-prioritization platform.
license: MIT
version: 0.1.0
```

- [ ] **Step 3: Add MIT license**

Create `LICENSE` with the MIT License text and copyright:

```text
MIT License

Copyright (c) 2026 Maicon Kevyn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Update `.gitignore`**

Add:

```gitignore
data/external/*
!data/external/README.md
!data/external/.gitkeep
data/outputs/experiments/*/intermediate/
paper/build/
paper/*.pdf
```

- [ ] **Step 5: Run local CI subset**

```bash
.venv/bin/python -m pytest -q
npm --prefix frontend run build
```

Expected: tests pass; frontend build succeeds with only known bundle-size warning.

- [ ] **Step 6: Commit**

```bash
git add .github/workflows/ci.yml CITATION.cff LICENSE .gitignore
git commit -m "chore: add reproducibility metadata and CI"
```

**Checkpoint:** The repo becomes citable, licensed, and automatically checked.

### Task 10: Draft The Paper Package

**Files:**
- Create: `paper/manuscript.md`
- Create: `paper/references.bib`
- Create: `paper/reproduce.sh`
- Modify: `README.md`

- [ ] **Step 1: Create manuscript skeleton**

Create `paper/manuscript.md`:

```markdown
# Evidence-Calibrated Target Prioritization for Astrobiology Follow-Up of Confirmed Exoplanets

## Abstract

We present Evidence-Calibrated Target Prioritization (ECTP), an open and reproducible framework for ranking confirmed exoplanets for astrobiology follow-up. ECTP combines NASA Exoplanet Archive catalog data, multiple habitable-zone model families, decomposed evidence scoring, uncertainty propagation, and validation against mission-facing target catalogs. The method prioritizes observation and modeling targets and does not infer biosignatures from catalog-only data.

## Introduction

Confirmed exoplanet catalogs are growing faster than follow-up resources. Target prioritization therefore requires transparent assumptions, reproducible data lineage, and conservative communication of evidence maturity.

## Data

The primary data source is the NASA Exoplanet Archive Planetary Systems Composite Parameters table. The pipeline records the archive snapshot, row counts, processing stage, and generator for every derived table.

## Methods

ECTP de-duplicates archive records, computes multiple HZ model families, derives evidence sub-scores, applies versioned scoring profiles, and estimates rank stability with Monte Carlo sampling over catalog uncertainties.

## Validation

We compare ECTP against simple HZ-radius baselines, known candidate sanity checks, HZ model ablations, score-weight sensitivity, and external mission-facing target lists including HWO/HPIC where crossmatches are available.

## Results

This section is generated from `paper/tables/` and `paper/figures/`.

## Discussion

ECTP should be interpreted as a decision-support layer for follow-up prioritization. It cannot infer atmospheric composition, disequilibrium, biological activity, or habitability in the ecological sense from catalog-only fields.

## Reproducibility

All tables and figures can be regenerated with `paper/reproduce.sh`.
```

- [ ] **Step 2: Create bibliography**

Create `paper/references.bib` with BibTeX entries for the sources in Section 3.

- [ ] **Step 3: Create reproduce script**

Create `paper/reproduce.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

.venv/bin/python -m pytest -q
.venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv
.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml
```

Make executable:

```bash
chmod +x paper/reproduce.sh
```

- [ ] **Step 4: Update README**

Add:

````markdown
## Paper Reproduction

The paper-grade experiment package can be regenerated with:

```bash
paper/reproduce.sh
```
````

- [ ] **Step 5: Run checks**

```bash
.venv/bin/python -m pytest -q
bash paper/reproduce.sh
```

Expected: all commands complete.

- [ ] **Step 6: Commit**

```bash
git add paper README.md
git commit -m "docs: add paper reproduction package"
```

**Checkpoint:** The project has a visible path from code to manuscript artifacts.

## 8. Iterative Scientific Review Loop

After every two implementation tasks, run this review loop:

1. **Scientific claim audit**
   - Check whether the current implementation still supports the paper claim.
   - Reject claims that require atmospheric spectra, disequilibrium chemistry, or biological interpretation.

2. **Originality audit**
   - Identify whether the latest task adds novelty or only engineering polish.
   - Keep engineering polish only when it improves reproducibility, validation, or communication.

3. **Method weakness audit**
   - Ask what a reviewer would attack first.
   - Convert the strongest criticism into a new validation test or ablation.

4. **Language audit**
   - Run:
     ```bash
     rg -n "life[ ]found|alien[ ]life|proof[ ]of[ ]life|confirmed[ ]life|biosignature[ ]detected" README.md docs paper frontend/src src
     ```
   - Expected: no matches.

5. **Evidence audit**
   - Check that every method choice maps to a source, a data field, or an explicit limitation.

## 9. Final Review, Tests, And Improvements

Before calling the implementation complete:

- [ ] Run the full test suite:
  ```bash
  .venv/bin/python -m pytest -q
  ```

- [ ] Run the full pipeline:
  ```bash
  .venv/bin/python -m exoplanets_research.pipeline --stage all --input data/PS_2025.06.22_09.41.26.csv
  ```

- [ ] Run the paper experiment:
  ```bash
  .venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml
  ```

- [ ] Run the frontend build:
  ```bash
  npm --prefix frontend run build
  ```

- [ ] Run conservative-language audit:
  ```bash
  rg -n "life[ ]found|alien[ ]life|proof[ ]of[ ]life|confirmed[ ]life|biosignature[ ]detected" README.md docs paper frontend/src src
  ```

- [ ] Run data-size review:
  ```bash
  du -h data/*.csv data/processed/*.csv data/outputs/*.csv frontend/src/data/*.json 2>/dev/null | sort -h
  ```

- [ ] Produce final paper artifacts:
  ```bash
  bash paper/reproduce.sh
  ```

- [ ] Update `docs/validation/validation_report.md` with:
  - exact commands;
  - date;
  - archive snapshot;
  - HZ model comparison;
  - uncertainty summary;
  - external validation summary;
  - known limitations.

- [ ] Commit final validation:
  ```bash
  git add docs/validation/validation_report.md data/outputs paper/figures paper/tables
  git commit -m "docs: publish paper validation results"
  ```

## 10. Paper-Readiness Checklist

The paper is not ready until every item is true:

- [ ] A reader can reproduce the main table without manual editing.
- [ ] A reader can reproduce every figure without manual plotting.
- [ ] Every score column has a definition.
- [ ] Every model name maps to a cited method.
- [ ] Every uncertainty column has a sampling rule.
- [ ] Every external validation table has source URL, download date, and checksum.
- [ ] Every major limitation is visible in README and manuscript.
- [ ] Every claim in the abstract is supported by a result table or validation command.
- [ ] The dashboard and README do not make biosignature or life-detection claims.
- [ ] CI passes on GitHub.

## 11. Recommended Execution Order

Execute in this exact order:

1. Task 1: method contract.
2. Task 2: HZ models.
3. Task 3: scoring profiles.
4. Task 4: uncertainty propagation.
5. Task 5: baselines and rank metrics.
6. Task 6: external validation hooks.
7. Task 7: experiment runner.
8. Task 8: paper figures and tables.
9. Task 9: CI and reproducibility metadata.
10. Task 10: paper package.

Each task should end with a commit. After Tasks 2, 4, 6, 8, and 10, run the iterative scientific review loop.
