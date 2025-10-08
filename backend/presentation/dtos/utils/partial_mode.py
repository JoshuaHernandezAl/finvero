
from pydantic import BaseModel, create_model

def partial_model(base_model: type[BaseModel]) -> type[BaseModel]:
    fields = {}
    for field_name, model_field in base_model.model_fields.items():
        annotation = model_field.annotation | None
        default = None
        fields[field_name] = (annotation, default)
    return create_model(
        f"Partial{base_model.__name__}",
        __base__=BaseModel,
        **fields
    )
