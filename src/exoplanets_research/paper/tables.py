from pathlib import Path

import pandas as pd


def write_markdown_table(df: pd.DataFrame, output_path: Path) -> None:
    headers = list(df.columns)
    rows = df.values.tolist()
    widths = [
        max(len(str(header)), *(len(str(row[index])) for row in rows)) if rows else len(str(header))
        for index, header in enumerate(headers)
    ]
    header_line = "| " + " | ".join(str(header).ljust(widths[index]) for index, header in enumerate(headers)) + " |"
    divider_line = "| " + " | ".join("-" * widths[index] for index in range(len(headers))) + " |"
    row_lines = [
        "| " + " | ".join(str(row[index]).ljust(widths[index]) for index in range(len(headers))) + " |"
        for row in rows
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join([header_line, divider_line, *row_lines]) + "\n", encoding="utf-8")


def write_top_candidate_table(ranked: pd.DataFrame, output_path: Path, *, top_n: int = 25) -> None:
    columns = ["pl_name", "hostname", "score_total", "evidence_confidence"]
    optional_columns = ["score_mean", "score_std", "rank_median", "rank_p05", "rank_p95", "top10_probability"]
    columns.extend(column for column in optional_columns if column in ranked.columns)
    table = ranked.loc[:, columns].head(top_n).copy()
    for column in ["score_total", *optional_columns]:
        if column in table.columns:
            table[column] = table[column].round(3)
    write_markdown_table(table, output_path)
