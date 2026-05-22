# External Data Inventory

Generated for experiment `paper_v1`.

| Dataset | Access | Local path | Scientific role |
| --- | --- | --- | --- |
| HWO ExEP Precursor Science Stars | NASA Exoplanet Archive TAP table `DI_STARS_EXEP` | `data/external/hwo_exep_2023.csv` | Mission-facing stellar target list used to test whether ECTP prioritizes known direct-imaging target hosts. |
| HWO Preliminary Input Catalog | NASA Exoplanet Archive `.tgz` download, DOI listed by NASA as `10.26133/NEA39` | Not vendored | Future large-scale expansion target; excluded from the default automated run until a stable tabular ingestion contract is added. |

The HWO ExEP crossmatch is host-name based and therefore conservative: it measures overlap with known stellar target hosts, not biological evidence.
