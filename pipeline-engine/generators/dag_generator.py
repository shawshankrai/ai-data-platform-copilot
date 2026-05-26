def generate_airflow_dag(config: dict) -> str:
    pipeline_name = config["pipeline_name"]
    schedule = config["schedule"]

    source = config["source"]
    target = config["target"]

    dag_code = f'''from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime

with DAG(
    dag_id="{pipeline_name}",
    start_date=datetime(2024, 1, 1),
    schedule="{schedule}",
    catchup=False,
    tags=["generated", "data-platform-copilot"],
) as dag:

    start = EmptyOperator(task_id="start")

    load_to_bigquery = GCSToBigQueryOperator(
        task_id="load_to_bigquery",
        bucket="{source["path"].replace("gs://", "").split("/")[0]}",
        source_objects=["{"/".join(source["path"].replace("gs://", "").split("/")[1:])}*"],
        destination_project_dataset_table="{target["project"]}.{target["dataset"]}.{target["table"]}",
        source_format="{source["format"].upper()}",
        autodetect=False,
        write_disposition="WRITE_APPEND",
    )

    end = EmptyOperator(task_id="end")

    start >> load_to_bigquery >> end
'''

    return dag_code