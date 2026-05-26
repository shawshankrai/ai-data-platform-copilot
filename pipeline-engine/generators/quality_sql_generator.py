import yaml
from jinja2 import Template


QUALITY_RULES_REGISTRY_PATH = "pipeline-engine/registries/quality_rules.yaml"


def load_quality_rule_registry() -> dict:
    with open(QUALITY_RULES_REGISTRY_PATH, "r") as file:
        return yaml.safe_load(file)


def clean_sql_block(sql: str) -> str:
    sql = sql.strip()

    if sql.endswith(";"):
        sql = sql[:-1]

    return sql


def generate_quality_sql(config: dict) -> str:
    target = config["target"]
    quality_rules = config.get("quality_rules", [])

    full_table_name = (
        f"`{target['project']}.{target['dataset']}.{target['table']}`"
    )

    registry = load_quality_rule_registry()
    registered_rules = registry.get("rules", {})

    sql_blocks = []

    for rule_config in quality_rules:
        column = rule_config["column"]
        rule_name = rule_config["rule"]

        rule_definition = registered_rules.get(rule_name)

        if not rule_definition:
            sql_blocks.append(
                f"SELECT\n"
                f"  '{column}' AS column_name,\n"
                f"  '{rule_name}' AS rule_name,\n"
                f"  -1 AS failed_count,\n"
                f"  'Unsupported quality rule' AS error_message"
            )
            continue

        template = Template(rule_definition["sql_template"])

        rendered_sql = template.render(
            column=column,
            table_name=full_table_name
        )

        sql_blocks.append(clean_sql_block(rendered_sql))

    if not sql_blocks:
        return "-- No quality rules defined."

    return "\n\nUNION ALL\n\n".join(sql_blocks) + ";"