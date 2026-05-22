# Evidence-Calibrated Target Prioritization for Astrobiology Follow-Up of Confirmed Exoplanets

## Abstract

We present Evidence-Calibrated Target Prioritization (ECTP), an open and reproducible framework for ranking confirmed exoplanets for astrobiology follow-up. ECTP combines NASA Exoplanet Archive catalog data, multiple habitable-zone model families, decomposed evidence scoring, uncertainty propagation, and validation against mission-facing target catalogs. The method prioritizes observation and modeling targets and does not infer biosignatures from catalog-only data.

## Introduction

Confirmed exoplanet catalogs are growing faster than follow-up resources. Target prioritization therefore requires transparent assumptions, reproducible data lineage, and conservative communication of evidence maturity.

## Data

The primary data source is the NASA Exoplanet Archive Planetary Systems Composite Parameters table. The pipeline records the archive snapshot, row counts, processing stage, and generator for every derived table.

## Methods

ECTP de-duplicates archive records, computes multiple HZ model families, derives evidence sub-scores, applies versioned scoring profiles, and estimates rank stability with Monte Carlo sampling over catalog uncertainties. The paper experiment uses a default simple luminosity baseline plus Kopparapu 1 Earth-mass conservative and optimistic HZ boundaries, with out-of-domain temperatures treated as unknown rather than extrapolated.

## Validation

We compare ECTP against simple HZ-radius baselines, known candidate sanity checks, HZ model ablations, score-weight sensitivity, and external mission-facing target lists. The current automated external validation uses the NASA Exoplanet Archive HWO ExEP Precursor Science Stars TAP table. HPIC-scale ingestion is tracked as a planned expansion rather than treated as a completed validation source.

## Results

The current archive snapshot yields 4,236 ranked candidates with enough catalog information for HZ scoring. The top-ranked candidates under the default profile are listed in `paper/tables/top_candidates.md`, and score decomposition and rank-stability figures are written to `paper/figures/`.

HZ model sensitivity is substantial. Relative to the simple luminosity baseline, the Kopparapu conservative model has top-25 overlap of 0.429 and the Kopparapu optimistic model has top-25 overlap of 0.316. This shows that ECTP rankings are sensitive to the climate boundary assumption and that manuscript claims must report the HZ model family rather than presenting a single universal ranking.

The HZ-radius baseline has Spearman rank correlation of 0.304 and Kendall tau of 0.217 against ECTP, with top-25 overlap of 0.111. A follow-up-readiness baseline has higher global correlation (Spearman 0.641, Kendall tau 0.439) but no top-25 overlap. Together these comparisons support the contribution that ECTP is not simply reproducing a coarse HZ-and-radius filter or a nearby/easy-follow-up filter; the decomposed evidence score changes candidate ordering.

Score-weight sensitivity shows high global rank correlation across normalized perturbation profiles, but top-k candidate overlap changes. The HZ-emphasis and follow-up-emphasis profiles both have top-25 overlap of 0.613 against the default profile, while the data-quality-emphasis profile has top-25 overlap of 0.786. This means broad ordering is stable but headline top-candidate claims remain profile-dependent and must be reported with profile metadata.

The HWO ExEP crossmatch finds 16 ranked candidates whose host stars are present in the mission-facing target list, with one match in the top 50 and none in the top 25. This is not a failure of the model or a biosignature statement; it indicates that catalog-confirmed exoplanet follow-up ranking and direct-imaging stellar target selection optimize related but distinct scientific objectives.

## Discussion

ECTP should be interpreted as a decision-support layer for follow-up prioritization. It cannot infer atmospheric composition, disequilibrium, biological activity, or habitability in the ecological sense from catalog-only fields.

The main scientific contribution is a reproducible audit trail for astrobiology target prioritization: every ranked candidate carries model provenance, score decomposition, uncertainty summaries, confidence caveats, and sensitivity checks against alternative HZ assumptions, simple baselines, and score-weight perturbations. The next manuscript iteration should run the full 500-sample uncertainty experiment, decide the primary HZ family for the headline ranking, and add HPIC-scale validation if the paper frames ECTP as a mission-planning bridge rather than only a confirmed-exoplanet ranking platform.

## Reproducibility

All tables and figures can be regenerated with `paper/reproduce.sh`.
