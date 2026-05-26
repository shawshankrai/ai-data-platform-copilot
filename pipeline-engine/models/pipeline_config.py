from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class SourceConfig(BaseModel):
    type: Literal["gcs"]
    path: str
    format: Literal["csv", "json", "parquet", "avro"]


class PartitionConfig(BaseModel):
    column: str
    type: Literal["DAY"] = "DAY"


class TargetConfig(BaseModel):
    type: Literal["bigquery"]
    project: str
    dataset: str
    table: str
    partition_by: PartitionConfig | None = None
    cluster_by: list[str] = Field(default_factory=list)


class ColumnConfig(BaseModel):
    name: str
    type: Literal[
        "STRING",
        "INTEGER",
        "INT64",
        "FLOAT",
        "FLOAT64",
        "BOOLEAN",
        "BOOL",
        "DATE",
        "DATETIME",
        "TIMESTAMP",
        "NUMERIC",
        "BIGNUMERIC"
    ]
    mode: Literal["NULLABLE", "REQUIRED", "REPEATED"]


class QualityRuleConfig(BaseModel):
    column: str
    rule: str


class GenerationConfig(BaseModel):
    airflow_mode: Literal["python_dag"] = "python_dag"
    bigquery_mode: Literal["ddl_file"] = "ddl_file"


class PipelineConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pipeline_name: str
    source: SourceConfig
    target: TargetConfig
    pipeline_schema: list[ColumnConfig] = Field(alias="schema")
    schedule: str
    quality_rules: list[QualityRuleConfig] = Field(default_factory=list)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)