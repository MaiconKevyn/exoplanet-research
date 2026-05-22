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
