REQUIRED_SOURCE_FIELDS = {
    "id",
    "title",
    "year",
    "url",
    "category",
    "evidence_type",
    "architecture_implication",
    "model_application",
}

ALLOWED_SOURCE_CATEGORIES = {
    "foundation",
    "nasa_strategy",
    "biosignature_review",
    "evidence_framework",
    "platform",
    "observatory_architecture",
    "data_infrastructure",
}


def validate_source(source: dict) -> None:
    missing = REQUIRED_SOURCE_FIELDS - set(source)
    if missing:
        source_id = source.get("id", "<missing id>")
        raise ValueError(f"{source_id} missing required fields: {sorted(missing)}")

    category = source["category"]
    if category not in ALLOWED_SOURCE_CATEGORIES:
        raise ValueError(f"{source['id']} has unsupported category: {category}")

    if not str(source["url"]).startswith("https://"):
        raise ValueError(f"{source['id']} must use an https URL")

    for field in ("architecture_implication", "model_application"):
        if not str(source[field]).strip():
            raise ValueError(f"{source['id']} has empty {field}")

