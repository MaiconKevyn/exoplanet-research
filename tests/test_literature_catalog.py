from pathlib import Path

import pytest

from exoplanets_research.literature.catalog import group_sources_by_category, load_sources


SOURCE_PATH = Path("data/literature/astrobiology_sources.yml")

REQUIRED_FIELDS = {
    "id",
    "title",
    "year",
    "url",
    "category",
    "evidence_type",
    "architecture_implication",
    "model_application",
}

REQUIRED_CATEGORIES = {
    "foundation",
    "nasa_strategy",
    "biosignature_review",
    "evidence_framework",
    "platform",
    "observatory_architecture",
    "data_infrastructure",
}


def test_literature_registry_entries_have_required_fields():
    sources = load_sources(SOURCE_PATH)

    assert len(sources) >= 20
    for source in sources:
        missing = REQUIRED_FIELDS - set(source)
        assert not missing, f"{source.get('id', '<missing id>')} missing {sorted(missing)}"
        assert source["category"] in REQUIRED_CATEGORIES
        assert source["url"].startswith("https://")
        assert source["architecture_implication"].strip()
        assert source["model_application"].strip()


def test_group_sources_by_category_indexes_all_sources():
    sources = load_sources(SOURCE_PATH)
    grouped = group_sources_by_category(sources)

    assert REQUIRED_CATEGORIES.issubset(grouped)
    assert sum(len(items) for items in grouped.values()) == len(sources)
    assert any(source["id"] == "catling_2018_biosignature_framework" for source in grouped["evidence_framework"])


def test_load_sources_rejects_missing_registry(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_sources(tmp_path / "missing.yml")
