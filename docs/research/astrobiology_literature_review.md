# Deep Astrobiology and Exobiology Literature Review

## Executive Synthesis

This project now treats exoplanet habitability as an evidence-accounting problem. The prior version ranked planets with a compact heuristic. The literature reviewed here argues for a more conservative scientific architecture: keep the ranking useful for target prioritization, expose all sub-scores, preserve provenance, and clearly state that catalog-level habitability is not a biosignature inference.

The strongest architectural lesson is shared by Lovelock, Sagan, the Exoplanet Biosignatures series, NASA strategy documents, and modern platforms such as EMAC, VPL, AHED, LDKB, and HWO planning resources: life-detection work must connect observations, environmental context, alternative abiotic explanations, measurement readiness, and communication standards. A platform that hides those components behind a single score is not scientifically durable.

The repository's scientific contribution is therefore:

> A transparent target-prioritization and evidence-accounting platform for known exoplanets, connecting NASA Exoplanet Archive data with modern astrobiology evidence frameworks while avoiding unsupported life-detection claims.

## Foundations of Life Detection

Lovelock's 1965 framing made atmospheric disequilibrium a central life-detection idea. The key architectural implication is that a system must distinguish between direct catalog habitability features and atmospheric evidence. The current repository cannot infer disequilibrium from NASA Exoplanet Archive population fields alone, so disequilibrium is represented as a future evidence class rather than a hidden assumption.

Sagan et al. used Earth as a remote-sensing control experiment. That paper is important for software architecture because it shows that useful astrobiology evidence is multi-modal and contextual: gases, surface reflectance, water, and artificial radio signals were interpreted together. This project mirrors that discipline by separating HZ position, planet size, stellar context, data quality, follow-up readiness, and caveats.

The Astrobiology Primer v2.0 and NASA strategy documents broaden the scope beyond "planet in the HZ." Habitability depends on planetary formation, stellar evolution, geochemistry, atmospheres, biology, preservation, and observation limits. The platform therefore uses modular feature engineering instead of treating the HZ formula as the whole scientific model.

## Modern Biosignature Frameworks

Schwieterman et al. review remotely detectable biosignatures and emphasize false positives, false negatives, detectability, and environmental context. This repository applies that idea by making the ranking explicitly observational: the output prioritizes candidates for follow-up, not candidates with detected life.

Catling et al. argue that biosignature assessment should be probabilistic. The current implementation does not attempt a full Bayesian model because the local dataset lacks the necessary atmospheric observations. Instead, it adopts the architectural pattern: evidence and anti-evidence must be explicit. The score is decomposed into HZ, size, stellar context, data quality, and follow-up readiness.

Meadows et al. show why even oxygen needs context. Walker et al. argue that future biosignatures may be agnostic and population-scale. Krissansen-Totton et al. highlight disequilibrium as a powerful but data-demanding signal. Together these papers require a conservative rule: do not invent biosignature confidence from catalog fields. The project encodes this through `interpretation_caveat` and `evidence_confidence` fields.

Neveu et al., Green et al., and the Biosignature Standards workshop shift attention from detection to communication and standards of evidence. This is now a software requirement: every row in the ranked output must include caveats, confidence labels, and provenance.

## Habitability and Host-Star Context

The current model preserves the existing simple luminosity-based HZ formula:

```text
hz_inner = sqrt(10 ** st_lum / 1.1)
hz_outer = sqrt(10 ** st_lum / 0.53)
```

This is deliberately labeled `simple_luminosity_kasting_like_baseline`. It is useful for reproducible parity with the previous project artifacts, but it is not a climate model. The new architecture makes this explicit through `hz_model`, `habitable_zone_status`, and `hz_center_offset`.

Planet radius and host-star temperature remain useful first-order filters. The scoring policy favors terrestrial-size planets, G/K stars, M-star candidates with caveats, complete critical fields, and nearby systems with follow-up readiness. This makes the top list more useful for scientific triage without claiming physical completeness.

## Platforms and Observatories

The NASA Exoplanet Archive and TAP documentation define the data foundation. This project keeps local CSV support but adds a query builder for PSCompPars fields so future runs can use live archive access without making tests network-dependent.

EMAC demonstrates that exoplanet science benefits from searchable registries of tools, models, and outputs. VPL demonstrates a model ecosystem for exoplanet environments and spectra. AHED and LDKB show how astrobiology platforms need metadata-rich, community-oriented, argument-aware data structures. NFoLD connects life-detection expertise to mission planning. HWO planning resources show why target prioritization and follow-up readiness must be explicit.

The platform pattern is therefore:

```text
literature registry -> provenance-aware data -> modular features -> explicit scoring -> validation report -> dashboard traceability
```

## Architecture Requirements Derived From the Literature

| Requirement | Literature basis | Implementation |
| --- | --- | --- |
| Preserve provenance for every generated table | NASA Exoplanet Archive, AHED, EMAC | Sidecar JSON files record source, input file, row count, stage, generator, and timestamp. |
| Avoid single unexplained scores | Catling et al., Neveu et al., Green et al. | `score_total` is decomposed into sub-scores and a missing-data penalty. |
| Keep biosignature claims separate from habitability ranking | Schwieterman et al., Meadows et al., Krissansen-Totton et al. | Every row carries a caveat stating that no biosignature inference is made. |
| Support future platform integration | EMAC, VPL, LDKB, HWO | Literature and scoring assumptions are machine-readable, and frontend JSON is generated from pipeline outputs. |
| Validate known candidates without overfitting | Sagan et al., NASA strategy, Exoplanet Science Strategy | Sanity checks ensure Kepler-442 b, Kepler-22 b, TRAPPIST-1 e, and TOI-700 d survive de-duplication and scoring. |

## Source Matrix

| Source ID | Central question | Evidence type | Architecture implication | Model application |
| --- | --- | --- | --- | --- |
| `lovelock_1965_life_detection` | Can planetary atmospheres reveal life-like processes? | Theoretical life-detection framework | Disequilibrium must be represented as a distinct evidence class. | Current data marks biosignature inference as unavailable. |
| `sagan_1993_galileo_life_on_earth` | What would Earth look like as a remote target? | Remote-sensing control experiment | Multiple evidence streams are stronger than one signal. | Dashboard shows multiple sub-scores. |
| `domagal_goldman_2016_astrobiology_primer` | What knowledge base defines astrobiology? | Interdisciplinary synthesis | Architecture must be modular across disciplines. | Features are separated from scoring. |
| `nasa_2015_astrobiology_strategy` | What are NASA's core astrobiology questions? | Agency strategy | The project must connect habitability to broader life-in-the-universe questions. | Research docs map features to strategy. |
| `nasem_2019_astrobiology_strategy` | How should NASA search for life? | Strategy report | False positives and false negatives must be explicit. | Validation report includes limitations. |
| `nasem_2018_exoplanet_science_strategy` | What exoplanet science is needed for future missions? | Strategy report | Target prioritization must support future observations. | Follow-up readiness is scored. |
| `nasem_2021_astro2020` | What observatories should shape the decade? | Decadal survey | Outputs should serve future biosignature-capable facilities. | Candidate tables expose follow-up fields. |
| `nasem_2022_origins_worlds_life` | How should planetary science and astrobiology coordinate? | Decadal survey | Cross-mission assumptions must be reusable. | Provenance and docs are first-class outputs. |
| `schwieterman_2018_biosignature_review` | What biosignatures are remotely detectable? | Review | Environmental context is required before interpretation. | Caveats prevent overclaiming. |
| `catling_2018_biosignature_framework` | How should biosignature confidence be assessed? | Probabilistic framework | Evidence and alternatives must be represented. | Sub-scores and confidence labels replace a single opaque score. |
| `meadows_2018_oxygen_context` | When is oxygen meaningful? | Context review | Even strong gases need environment context. | No hard-coded gas claim is made. |
| `walker_2018_future_directions` | How can biosignatures generalize beyond Earth analogs? | Future framework | The model should remain extensible. | Scoring is modular and conservative. |
| `krissansen_totton_2018_disequilibrium` | Can disequilibrium reveal life over Earth history? | Disequilibrium study | Atmospheric composition is required for that inference. | The platform does not infer disequilibrium from catalog metadata. |
| `neveu_2018_ladder_life_detection` | How should life-detection investigations be staged? | Evidence ladder | Evidence maturity should be graded. | `evidence_confidence` is included in outputs. |
| `green_2024_cold_scale_response` | How should confidence be communicated? | Communication framework | Public-facing language must be conservative. | Frontend text avoids detection language. |
| `community_2022_biosignature_standards` | What reporting standards does the community need? | Workshop report | Verification is part of the scientific product. | Validation report records commands and caveats. |
| `nasa_exoplanet_archive_docs` | What is the canonical archive source? | Data documentation | Source provenance must be preserved. | Pipeline sidecars record archive source and input file. |
| `nasa_exoplanet_archive_tap_docs` | How should archive data be accessed programmatically? | TAP documentation | Network access should be optional and testable. | Query builder is implemented without live API dependency. |
| `akeson_2013_exoplanet_archive` | What services support exoplanet research? | Archive platform paper | Data access and tooling should be connected. | Ingestion, cleaning, scoring, and export are separate modules. |
| `emac_platform` | How should exoplanet models be discoverable? | Platform | Registries should drive reuse. | Literature catalog is machine-readable. |
| `renaud_2022_emac` | How does EMAC structure model resources? | Platform paper | Hosted and external resources need clear boundaries. | Directory layout separates raw, processed, outputs, docs, and frontend. |
| `vpl_about` | How does VPL model exoplanet environments? | Modeling platform | Models must be modular. | Future climate and spectra modules can plug into scoring. |
| `vpl_spectral_explorer` | How are spectra explored and compared? | Spectral tool | Candidate ranking should support future spectral comparison. | Frontend shows evidence breakdowns. |
| `nasa_life_detection_resources` | What life-detection resources exist for missions? | Resource index | Platform outputs should connect to community tools. | Docs include future integration points. |
| `nasa_life_detection_knowledge_base` | How can life-detection arguments be structured? | Knowledge platform | Evidence and counter-evidence should become structured fields. | Future caveats can become argument records. |
| `nasa_ahed` | How should long-tail astrobiology data be managed? | Open-science data platform | Flexible metadata and provenance are required. | CSV/JSON outputs use sidecar provenance. |
| `nasa_nfold` | How should life-detection expertise feed missions? | Research coordination network | Mission planning and evidence interpretation must be connected. | Validation is mission-facing and conservative. |
| `hwo_program_page` | What observatory context motivates target ranking? | Program description | Ranking should expose direct-imaging relevance. | Follow-up readiness includes distance and context. |
| `hwo_2026_concept_maturation` | How is HWO trade-space maturing? | Architecture paper | Candidate assumptions must be inspectable. | Validation flags measurement limitations. |
| `hwo_2026_early_architecture_concepts` | How should HWO concepts evolve? | Architecture concepts | Outputs must remain stable as missions mature. | CSV/JSON interfaces decouple pipeline and dashboard. |

## Candidate Scientific Contributions of This Repository

1. A reproducible, provenance-aware pipeline that converts NASA Exoplanet Archive records into de-duplicated candidate rankings.
2. A transparent scoring model that exposes sub-scores, missing-data penalties, and caveats.
3. A machine-readable literature registry linking papers and platforms to architecture decisions.
4. A dashboard that communicates follow-up priority without implying life detection.
5. A validation framework that can expand toward atmospheric retrievals, VPL-like spectral models, EMAC-style tool registries, and LDKB-style evidence arguments.

## Bibliography

The canonical bibliography is maintained in `data/literature/astrobiology_sources.yml`. That file is validated by `tests/test_literature_catalog.py` and is intentionally machine-readable so the research review, architecture, and dashboard can remain synchronized.

