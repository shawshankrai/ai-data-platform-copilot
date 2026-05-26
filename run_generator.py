import yaml
import os
import sys
import glob

sys.path.append("pipeline-engine")

from validators.config_validator import validate_pipeline_config
from generators.ddl_generator import generate_bigquery_ddl
from generators.dag_generator import generate_airflow_dag
from generators.validation_report_generator import generate_validation_report
from generators.quality_sql_generator import generate_quality_sql


DEFAULT_CONFIG_PATH = "sample-configs/customer_ingestion.yaml"
CONFIG_DIR = "sample-configs"
OUTPUT_DIR = "generated"


def build_output_paths(pipeline_name: str) -> dict:
    pipeline_output_dir = f"{OUTPUT_DIR}/{pipeline_name}"

    return {
        "output_dir": pipeline_output_dir,
        "ddl": f"{pipeline_output_dir}/ddl.sql",
        "dag": f"{pipeline_output_dir}/dag.py",
        "quality_sql": f"{pipeline_output_dir}/quality_checks.sql",
        "validation_report": f"{pipeline_output_dir}/validation_report.md",
    }


def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)


def generate_for_config(config_path: str) -> None:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    pipeline_name = config.get("pipeline_name", "unknown_pipeline")
    output_paths = build_output_paths(pipeline_name)

    errors = validate_pipeline_config(config)

    os.makedirs(output_paths["output_dir"], exist_ok=True)

    report = generate_validation_report(config, errors)
    write_file(output_paths["validation_report"], report)

    if errors:
        print(f"Config validation failed for {config_path}. Report generated:")
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

    print(f"Generated artifacts for pipeline: {pipeline_name}")
    print(f"- {output_paths['ddl']}")
    print(f"- {output_paths['dag']}")
    print(f"- {output_paths['quality_sql']}")
    print(f"- {output_paths['validation_report']}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        config_paths = sorted(glob.glob(f"{CONFIG_DIR}/*.yaml"))

        if not config_paths:
            print(f"No config files found in {CONFIG_DIR}")
            return

        for config_path in config_paths:
            generate_for_config(config_path)

        print("Bulk generation completed.")
        return

    config_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG_PATH
    generate_for_config(config_path)

if __name__ == "__main__":
    main()