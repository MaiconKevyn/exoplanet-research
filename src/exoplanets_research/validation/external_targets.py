from io import StringIO
from pathlib import Path

import pandas as pd
import requests


TAP_SYNC_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
HWO_EXEP_TABLE = "DI_STARS_EXEP"
HWO_EXEP_COLUMNS = [
    "hostname",
    "target_group",
    "sy_dist",
    "st_teff",
    "st_lum",
    "sy_planets_flag",
    "sy_pnum",
]


def normalize_host_name(value: str) -> str:
    return " ".join(str(value).strip().lower().split())


def build_mission_star_tap_query(
    *,
    table_name: str = HWO_EXEP_TABLE,
    columns: list[str] | None = None,
) -> str:
    selected = columns or HWO_EXEP_COLUMNS
    column_sql = ", ".join(selected)
    return f"SELECT {column_sql} FROM {table_name}"


def download_mission_star_table(
    output_path: Path,
    *,
    table_name: str = HWO_EXEP_TABLE,
    target_list: str = "hwo_exep_2023",
    timeout: int = 60,
) -> pd.DataFrame:
    output_path = Path(output_path)
    query = build_mission_star_tap_query(table_name=table_name)
    response = requests.get(TAP_SYNC_URL, params={"query": query, "format": "csv"}, timeout=timeout)
    response.raise_for_status()
    text = response.text.strip()
    if text.startswith("<?xml") or "QUERY_STATUS" in text[:500]:
        raise RuntimeError(f"NASA Exoplanet Archive TAP query failed for table {table_name}: {text[:500]}")

    targets = pd.read_csv(StringIO(text), low_memory=False)
    targets["target_list"] = target_list
    output_path.parent.mkdir(parents=True, exist_ok=True)
    targets.to_csv(output_path, index=False)
    return targets


def load_external_targets(path: Path, *, target_list: str = "hwo_exep_2023") -> pd.DataFrame:
    targets = pd.read_csv(path, low_memory=False)
    if "target_list" not in targets.columns:
        targets = targets.copy()
        targets["target_list"] = target_list
    return targets


def add_host_target_flags(ranked: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    result = ranked.copy()
    target_hosts = {normalize_host_name(value) for value in targets["hostname"].dropna()}
    normalized = result["hostname"].map(normalize_host_name)
    result["external_target_match"] = normalized.isin(target_hosts).astype(object)
    target_lists = targets.copy()
    target_lists["_host_key"] = target_lists["hostname"].map(normalize_host_name)
    grouped = target_lists.groupby("_host_key")["target_list"].apply(lambda values: ";".join(sorted(set(values)))).to_dict()
    result["external_target_lists"] = normalized.map(grouped).fillna("")
    return result
