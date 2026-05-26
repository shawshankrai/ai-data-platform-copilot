import yaml
import os
import sys

sys.path.append("pipeline-engine")

from validators.config_validator import validate_pipeline_config
from generators.ddl_generator import generate_bigquery_ddl
from generators.dag_generator import generate_airflow_dag
from generators.validation_report_generator import generate_validation_report


CONFIG_PATH = "sample-configs/customer_ingestion.yaml"
OUTPUT_DIR = "generated"


def main():
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    errors = validate_pipeline_config(config)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    report = generate_validation_report(config, errors)

    with open(f"{OUTPUT_DIR}/customer_ingestion_validation_report.md", "w") as file:
        file.write(report)

    if errors:
        print("Config validation failed. Report generated:")
        print("- generated/customer_ingestion_validation_report.md")

        for error in errors:
            print(f"- {error}")

        return

    ddl = generate_bigquery_ddl(config)
    dag = generate_airflow_dag(config)

    with open(f"{OUTPUT_DIR}/customer_ingestion.sql", "w") as file:
        file.write(ddl)

    with open(f"{OUTPUT_DIR}/customer_ingestion_dag.py", "w") as file:
        file.write(dag)

    print("Generated files:")
    print("- generated/customer_ingestion.sql")
    print("- generated/customer_ingestion_dag.py")
    print("- generated/customer_ingestion_validation_report.md")
    print("Done.")


if __name__ == "__main__":
    main()