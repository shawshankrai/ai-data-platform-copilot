import yaml
import os
import sys

sys.path.append("pipeline-engine")

from validators.config_validator import validate_pipeline_config
from generators.ddl_generator import generate_bigquery_ddl
from generators.dag_generator import generate_airflow_dag
from generators.validation_report_generator import generate_validation_report
from generators.quality_sql_generator import generate_quality_sql


CONFIG_PATH = "sample-configs/customer_ingestion.yaml"
OUTPUT_DIR = "generated"


def build_output_paths(pipeline_name: str) -> dict:
    return {
        "ddl": f"{OUTPUT_DIR}/{pipeline_name}.sql",
        "dag": f"{OUTPUT_DIR}/{pipeline_name}_dag.py",
        "quality_sql": f"{OUTPUT_DIR}/{pipeline_name}_quality_checks.sql",
        "validation_report": f"{OUTPUT_DIR}/{pipeline_name}_validation_report.md",
    }


def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)


def main():
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    pipeline_name = config.get("pipeline_name", "unknown_pipeline")
    output_paths = build_output_paths(pipeline_name)

    errors = validate_pipeline_config(config)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    report = generate_validation_report(config, errors)
    write_file(output_paths["validation_report"], report)

    if errors:
        print("Config validation failed. Report generated:")
        print(f"- {output_paths['validation_report']}")

        for error in errors:
            print(f"- {error}")

        return

    ddl = generate_bigquery_ddl(config)
    dag = generate_airflow_dag(config)
    quality_sql = generate_quality_sql(config)

    write_file(output_paths["ddl"], ddl)
    write_file(output_paths["dag"], dag)
    write_file(output_paths["quality_sql"], quality_sql)

    print("Generated files:")
    print(f"- {output_paths['ddl']}")
    print(f"- {output_paths['dag']}")
    print(f"- {output_paths['quality_sql']}")
    print(f"- {output_paths['validation_report']}")
    print("Done.")


if __name__ == "__main__":
    main()