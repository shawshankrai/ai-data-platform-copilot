def validate_pipeline_config(config: dict) -> list[str]:
    errors = []

    required_top_level_fields = [
        "pipeline_name",
        "source",
        "target",
        "schema",
        "schedule"
    ]

    for field in required_top_level_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")

    if "source" in config:
        for field in ["type", "path", "format"]:
            if field not in config["source"]:
                errors.append(f"Missing source field: {field}")

    if "target" in config:
        for field in ["type", "project", "dataset", "table"]:
            if field not in config["target"]:
                errors.append(f"Missing target field: {field}")

    if "schema" in config:
        if not isinstance(config["schema"], list) or len(config["schema"]) == 0:
            errors.append("Schema must be a non-empty list")
        else:
            for column in config["schema"]:
                for field in ["name", "type", "mode"]:
                    if field not in column:
                        errors.append(f"Missing schema field: {field}")

    return errors