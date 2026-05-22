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

## Output Field Definitions

| Field | Definition |
| --- | --- |
| `score_hz_position` | Central evidence score for whether the planet's orbit falls inside the selected HZ model and how close it is to the HZ center. |
| `score_planet_size` | Central evidence score for approximate terrestrial-size compatibility using catalog planet radius. |
| `score_stellar_context` | Central evidence score for stellar effective-temperature context, with G/K stars favored over hotter or poorly constrained hosts. |
| `score_data_quality` | Fraction of critical catalog fields present for the candidate. |
| `score_followup_readiness` | Simple observability/readiness score based on distance and availability of key catalog parameters. |
| `penalty_missing_data` | Bounded penalty for missing critical catalog fields. |
| `score_total` | Weighted, clipped ECTP central score from the versioned scoring profile. |
| `score_mean` | Mean `score_total` across Monte Carlo catalog-uncertainty samples. |
| `score_std` | Standard deviation of `score_total` across Monte Carlo samples. |
| `rank_median` | Median candidate rank across Monte Carlo samples. |
| `rank_p05` | Fifth-percentile candidate rank across Monte Carlo samples. |
| `rank_p95` | Ninety-fifth-percentile candidate rank across Monte Carlo samples. |
| `top10_probability` | Fraction of Monte Carlo samples in which the candidate appears in the top 10. |
| `evidence_confidence` | Conservative catalog-evidence maturity label; not a biosignature confidence score. |

## HZ Model Provenance

| Model | Method basis | Citation key | Interpretation |
| --- | --- | --- | --- |
| `simple_luminosity_baseline` | Luminosity-scaled inner/outer flux baseline retained for reproducibility against the original project artifact and used as the control model. | `BaselineInventory2026` | Baseline comparison model, not a full climate model. |
| `kopparapu_conservative_earth_mass` | Kopparapu et al. 2014 1 Earth-mass runaway-greenhouse and maximum-greenhouse limits. | `Kopparapu2014` | Conservative liquid-water HZ sensitivity model. |
| `kopparapu_optimistic_earth_mass` | Kopparapu et al. 2014 1 Earth-mass recent-Venus and early-Mars empirical limits. | `Kopparapu2014` | Optimistic HZ sensitivity model. |

## Uncertainty Sampling Rules

Monte Carlo rank-stability samples perturb `pl_orbsmax`, `pl_rade`, `pl_masse`, `st_teff`, `st_rad`, and `st_lum` when NASA Exoplanet Archive `err1`/`err2` columns are available. The sampler uses a normal draw centered on the catalog value with sigma equal to the larger absolute asymmetric uncertainty. Non-negative physical quantities are clipped at zero. Missing central values remain missing, and runs are summarized into score and rank statistics.

## Non-Claims

The system does not claim atmospheric composition, disequilibrium, biosignatures, biological activity, or habitability in the ecological sense.

## Paper Contribution

The contribution is a reproducible decision-support framework that makes target-prioritization assumptions explicit, measurable, and stress-tested.
