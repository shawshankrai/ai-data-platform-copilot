def generate_bigquery_ddl(config: dict) -> str:
    target = config["target"]
    schema = config["schema"]

    full_table_name = (
        f"`{target['project']}.{target['dataset']}.{target['table']}`"
    )

    column_definitions = []

    for column in schema:
        column_name = column["name"]
        column_type = column["type"]
        column_mode = column["mode"]

        if column_mode == "REQUIRED":
            column_definitions.append(
                f"  {column_name} {column_type} NOT NULL"
            )
        else:
            column_definitions.append(
                f"  {column_name} {column_type}"
            )

    columns_sql = ",\n".join(column_definitions)

    ddl = f"""CREATE TABLE IF NOT EXISTS {full_table_name} (
{columns_sql}
);"""

    return ddl