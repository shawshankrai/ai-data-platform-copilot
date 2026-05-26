from jinja2 import Environment, FileSystemLoader


TEMPLATE_DIR = "pipeline-engine/templates"
DAG_TEMPLATE_NAME = "airflow_dag_template.py.j2"


def parse_gcs_path(gcs_path: str) -> tuple[str, str]:
    cleaned_path = gcs_path.replace("gs://", "")
    path_parts = cleaned_path.split("/", 1)

    bucket = path_parts[0]

    if len(path_parts) == 1:
        object_prefix = ""
    else:
        object_prefix = path_parts[1]

    source_object_pattern = f"{object_prefix}*"

    return bucket, source_object_pattern


def build_destination_table(target: dict) -> str:
    return f"{target['project']}.{target['dataset']}.{target['table']}"


def generate_airflow_dag(config: dict) -> str:
    source = config["source"]
    target = config["target"]

    bucket, source_object_pattern = parse_gcs_path(source["path"])

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template(DAG_TEMPLATE_NAME)

    dag_code = template.render(
        pipeline_name=config["pipeline_name"],
        schedule=config["schedule"],
        bucket=bucket,
        source_object_pattern=source_object_pattern,
        destination_table=build_destination_table(target),
        source_format=source["format"].upper()
    )

    return dag_code