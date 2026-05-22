# External Data Inventory

Generated for experiment `paper_v1`.

| Dataset | Access | Source URL | Download date | Local path | Rows | SHA-256 | Processing command | Scientific role |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| HWO ExEP Precursor Science Stars | NASA Exoplanet Archive TAP table `DI_STARS_EXEP` via `https://exoplanetarchive.ipac.caltech.edu/TAP/sync` | https://exoplanetarchive.ipac.caltech.edu/docs/MissionStellar.html | 2026-05-22 | `data/external/hwo_exep_2023.csv` | 164 | `eb3228435eed444d566e65c560c5a9bed80477b51bf1a4da0da615e1049633b3` | `.venv/bin/python -m exoplanets_research.experiments.run_ablation --config configs/experiments/paper_v1.yml` | Mission-facing stellar target list used to test whether ECTP prioritizes known direct-imaging target hosts. |
| HWO Preliminary Input Catalog | NASA Exoplanet Archive `.tgz` package, DOI listed by NASA as `10.26133/NEA39` | https://exoplanetarchive.ipac.caltech.edu/docs/MissionStellar.html | Not downloaded | Not vendored | n/a | n/a | Planned HPIC ingestion step | Future large-scale expansion target; excluded from the default automated run until a stable tabular ingestion contract is added. |

The HWO ExEP crossmatch is host-name based and therefore conservative: it measures overlap with known stellar target hosts, not biological evidence.
