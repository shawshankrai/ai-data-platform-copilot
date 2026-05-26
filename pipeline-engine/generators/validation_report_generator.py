def generate_validation_report(config: dict, errors: list[str]) -> str:
    pipeline_name = config.get("pipeline_name", "unknown_pipeline")
    source = config.get("source", {})
    target = config.get("target", {})
    schema = config.get("schema", [])
    quality_rules = config.get("quality_rules", [])
    generation = config.get("generation", {})

    status = "PASSED" if not errors else "FAILED"

    report_lines = [
        f"# Validation Report: {pipeline_name}",
        "",
        f"## Status",
        "",
        f"**{status}**",
        "",
        "## Source",
        "",
        f"- Type: {source.get('type', 'N/A')}",
        f"- Path: {source.get('path', 'N/A')}",
        f"- Format: {source.get('format', 'N/A')}",
        "",
        "## Target",
        "",
        f"- Type: {target.get('type', 'N/A')}",
        f"- Project: {target.get('project', 'N/A')}",
        f"- Dataset: {target.get('dataset', 'N/A')}",
        f"- Table: {target.get('table', 'N/A')}",
        "",
        "## Schema",
        "",
    ]

    if schema:
        report_lines.append("| Column | Type | Mode |")
        report_lines.append("|---|---|---|")

        for column in schema:
            report_lines.append(
                f"| {column.get('name', 'N/A')} | {column.get('type', 'N/A')} | {column.get('mode', 'N/A')} |"
            )
    else:
        report_lines.append("No schema defined.")

    report_lines.extend([
        "",
        "## Quality Rules",
        "",
    ])

    if quality_rules:
        report_lines.append("| Column | Rule |")
        report_lines.append("|---|---|")

        for rule in quality_rules:
            report_lines.append(
                f"| {rule.get('column', 'N/A')} | {rule.get('rule', 'N/A')} |"
            )
    else:
        report_lines.append("No quality rules defined.")

    report_lines.extend([
        "",
        "## Generation Settings",
        "",
        f"- Airflow Mode: {generation.get('airflow_mode', 'python_dag')}",
        f"- BigQuery Mode: {generation.get('bigquery_mode', 'ddl_file')}",
        "",
        "## Validation Errors",
        "",
    ])

    if errors:
        for error in errors:
            report_lines.append(f"- {error}")
    else:
        report_lines.append("No validation errors found.")

    report_lines.extend([
        "",
        "## Copilot Explanation",
        "",
        "This pipeline reads customer data from GCS and loads it into a BigQuery bronze table.",
        "The schema defines the expected table structure, and the quality rules define basic checks that should be applied before or after ingestion.",
        "The generated Airflow DAG is responsible for orchestration, while the generated BigQuery DDL defines the target table.",
    ])

    return "\n".join(report_lines)