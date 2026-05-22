import pandas as pd

from exoplanets_research.validation.external_targets import add_host_target_flags


def test_add_host_target_flags_marks_known_hosts():
    ranked = pd.DataFrame({"hostname": ["TRAPPIST-1", "Tau Ceti", "Kepler-442"]})
    targets = pd.DataFrame({"hostname": ["Tau Ceti"], "target_list": ["hwo_precursor"]})

    result = add_host_target_flags(ranked, targets)

    assert result.loc[result["hostname"] == "Tau Ceti", "external_target_match"].iloc[0] is True
    assert result.loc[result["hostname"] == "TRAPPIST-1", "external_target_match"].iloc[0] is False
