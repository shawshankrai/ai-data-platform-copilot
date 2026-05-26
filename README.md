# ai-data-platform-copilot

## Dependency Separation

This project separates generator dependencies from generated runtime dependencies.

The generator engine uses:

- PyYAML
- Jinja2
- Pydantic

These are required to read pipeline configs, validate them, and generate artifacts.

Airflow is not required to run the generator. Airflow is only required when the generated DAG is deployed to an Airflow or Cloud Composer runtime.

Airflow runtime dependencies are tracked separately in:

```text
infra/airflow/requirements-airflow.txt