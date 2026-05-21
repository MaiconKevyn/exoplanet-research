import pandas as pd


CRITICAL_RECORD_FIELDS = ["pl_orbsmax", "pl_rade", "pl_masse", "st_teff", "st_rad", "st_lum"]


def select_best_planet_records(df: pd.DataFrame) -> pd.DataFrame:
    if "pl_name" not in df.columns:
        raise ValueError("Dataframe must include pl_name.")

    working = df.copy()
    if "default_flag" not in working.columns:
        working["default_flag"] = 0

    for column in CRITICAL_RECORD_FIELDS:
        if column not in working.columns:
            working[column] = pd.NA

    working["_critical_present_count"] = working[CRITICAL_RECORD_FIELDS].notna().sum(axis=1)
    working["_is_default"] = working["default_flag"].fillna(0).astype(float).eq(1)
    working["_original_order"] = range(len(working))
    working["duplicate_record_count"] = working.groupby("pl_name")["pl_name"].transform("size")

    sort_columns = ["pl_name", "_is_default", "_critical_present_count", "_original_order"]
    sorted_df = working.sort_values(
        sort_columns,
        ascending=[True, False, False, True],
        kind="mergesort",
    )
    selected = sorted_df.groupby("pl_name", as_index=False, sort=False).first()

    def reason(row: pd.Series) -> str:
        if row["duplicate_record_count"] == 1:
            return "single_record"
        if bool(row["_is_default"]):
            return "default_flag"
        return "most_complete_critical_fields"

    selected["selected_record_reason"] = selected.apply(reason, axis=1)
    return selected.drop(columns=["_critical_present_count", "_is_default", "_original_order"])

