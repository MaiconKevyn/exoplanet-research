import pandas as pd

from exoplanets_research.paper.tables import write_markdown_table, write_top_candidate_table


def test_write_markdown_table(tmp_path):
    output = tmp_path / "summary.md"

    write_markdown_table(pd.DataFrame({"metric": ["overlap"], "value": [0.75]}), output)

    text = output.read_text(encoding="utf-8")
    assert "| metric  | value |" in text
    assert "| overlap | 0.75  |" in text


def test_write_top_candidate_table(tmp_path):
    ranked = pd.DataFrame(
        {
            "pl_name": ["A b", "B b"],
            "hostname": ["A", "B"],
            "score_total": [0.91234, 0.81234],
            "evidence_confidence": ["moderate_catalog_confidence", "limited_catalog_confidence"],
        }
    )
    output = tmp_path / "top_candidates.md"

    write_top_candidate_table(ranked, output, top_n=2)

    text = output.read_text(encoding="utf-8")
    assert "A b" in text
    assert "score_total" in text
    assert "0.912" in text
