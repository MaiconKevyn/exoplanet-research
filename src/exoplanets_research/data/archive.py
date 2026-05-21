from pathlib import Path

import pandas as pd


PSCOMPPARS_COLUMNS = [
    "pl_name",
    "hostname",
    "default_flag",
    "discoverymethod",
    "disc_year",
    "pl_orbper",
    "pl_orbsmax",
    "pl_rade",
    "pl_masse",
    "pl_dens",
    "pl_insol",
    "pl_eqt",
    "st_teff",
    "st_rad",
    "st_mass",
    "st_lum",
    "st_met",
    "st_age",
    "sy_dist",
]


def _count_initial_metadata_rows(path: Path) -> int:
    count = 0
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("#"):
                count += 1
                continue
            break
    return count


def load_planetary_systems_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)

    skiprows = _count_initial_metadata_rows(path)
    return pd.read_csv(path, skiprows=skiprows, on_bad_lines="skip", low_memory=False)


def build_pscomppars_tap_query(columns: list[str] | None = None) -> str:
    selected = columns or PSCOMPPARS_COLUMNS
    column_sql = ", ".join(selected)
    return f"SELECT {column_sql} FROM pscomppars"

