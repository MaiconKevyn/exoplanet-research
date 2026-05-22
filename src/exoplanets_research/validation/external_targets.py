import pandas as pd


def normalize_host_name(value: str) -> str:
    return " ".join(str(value).strip().lower().split())


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
