from pathlib import Path

import pandas as pd

from exoplanets_research.paper.figures import write_top_candidate_table


def test_write_top_candidate_table(tmp_path):
    ranked = pd.DataFrame(
        {
            "pl_name": ["A b", "B b"],
            "hostname": ["A", "B"],
            "score_total": [0.9, 0.8],
            "evidence_confidence": ["moderate_catalog_confidence", "limited_catalog_confidence"],
        }
    )
    output = tmp_path / "top_candidates.md"

    write_top_candidate_table(ranked, output, top_n=2)

    text = output.read_text(encoding="utf-8")
    assert "A b" in text
    assert "score_total" in text
