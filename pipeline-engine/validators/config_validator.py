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

        supported_source_types = ["gcs"]
        if config["source"].get("type") not in supported_source_types:
            errors.append(
                f"Unsupported source type: {config['source'].get('type')}"
            )

        supported_formats = ["csv", "json", "parquet", "avro"]
        if config["source"].get("format") not in supported_formats:
            errors.append(
                f"Unsupported source format: {config['source'].get('format')}"
            )

    if "target" in config:
        for field in ["type", "project", "dataset", "table"]:
            if field not in config["target"]:
                errors.append(f"Missing target field: {field}")

        supported_target_types = ["bigquery"]
        if config["target"].get("type") not in supported_target_types:
            errors.append(
                f"Unsupported target type: {config['target'].get('type')}"
            )

    if "schema" in config:
        if not isinstance(config["schema"], list) or len(config["schema"]) == 0:
            errors.append("Schema must be a non-empty list")
        else:
            supported_bigquery_types = [
                "STRING",
                "INTEGER",
                "INT64",
                "FLOAT",
                "FLOAT64",
                "BOOLEAN",
                "BOOL",
                "DATE",
                "DATETIME",
                "TIMESTAMP",
                "NUMERIC",
                "BIGNUMERIC"
            ]

            supported_modes = ["NULLABLE", "REQUIRED", "REPEATED"]

            for column in config["schema"]:
                for field in ["name", "type", "mode"]:
                    if field not in column:
                        errors.append(f"Missing schema field: {field}")

                if column.get("type") not in supported_bigquery_types:
                    errors.append(
                        f"Unsupported BigQuery type for column {column.get('name')}: {column.get('type')}"
                    )

                if column.get("mode") not in supported_modes:
                    errors.append(
                        f"Unsupported BigQuery mode for column {column.get('name')}: {column.get('mode')}"
                    )

    if "generation" in config:
        supported_airflow_modes = ["python_dag"]
        supported_bigquery_modes = ["ddl_file"]

        airflow_mode = config["generation"].get("airflow_mode")
        bigquery_mode = config["generation"].get("bigquery_mode")

        if airflow_mode not in supported_airflow_modes:
            errors.append(f"Unsupported airflow generation mode: {airflow_mode}")

        if bigquery_mode not in supported_bigquery_modes:
            errors.append(f"Unsupported bigquery generation mode: {bigquery_mode}")

    return errors