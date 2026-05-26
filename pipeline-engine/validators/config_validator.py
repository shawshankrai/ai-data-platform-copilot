from pydantic import ValidationError

from models.pipeline_config import PipelineConfig


def validate_pipeline_config(config: dict) -> list[str]:
    try:
        PipelineConfig.model_validate(config)
        return []
    except ValidationError as error:
        errors = []

        for item in error.errors():
            field_path = ".".join(str(location) for location in item["loc"])
            message = item["msg"]
            errors.append(f"{field_path}: {message}")

        return errors