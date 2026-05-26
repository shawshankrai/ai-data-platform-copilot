from jinja2 import Environment, FileSystemLoader


TEMPLATE_DIR = "pipeline-engine/templates"
DDL_TEMPLATE_NAME = "bigquery_ddl_template.sql.j2"


def build_table_name(target: dict) -> str:
    return f"`{target['project']}.{target['dataset']}.{target['table']}`"


def build_partition_clause(target: dict) -> str | None:
    partition_config = target.get("partition_by")

    if not partition_config:
        return None

    column = partition_config.get("column")
    partition_type = partition_config.get("type", "DAY")

    if not column:
        return None

    if partition_type == "DAY":
        return f"DATE({column})"

    return column


def build_cluster_clause(target: dict) -> str | None:
    cluster_columns = target.get("cluster_by", [])

    if not cluster_columns:
        return None

    return ", ".join(cluster_columns)


def build_columns_sql(schema: list[dict]) -> str:
    column_lines = []

    for index, column in enumerate(schema):
        column_name = column["name"]
        column_type = column["type"]
        column_mode = column["mode"]

        not_null = " NOT NULL" if column_mode == "REQUIRED" else ""
        comma = "," if index < len(schema) - 1 else ""

        column_lines.append(
            f"  {column_name} {column_type}{not_null}{comma}"
        )

    return "\n".join(column_lines)


def generate_bigquery_ddl(config: dict) -> str:
    target = config["target"]
    schema = config["schema"]

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template(DDL_TEMPLATE_NAME)

    ddl = template.render(
        table_name=build_table_name(target),
        columns_sql=build_columns_sql(schema),
        partition_by=build_partition_clause(target),
        cluster_by=build_cluster_clause(target)
    )

    return ddl.replace("\n;", ";")