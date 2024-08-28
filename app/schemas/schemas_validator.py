from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, model_validator


class CustomValidation(BaseModel):
    """ Валидация полей, должна наследоваться всеми моделями """

    @model_validator(mode="before")
    @classmethod
    def root_validator(cls, values: dict) -> dict:

        class_attrs = [
            field
            for field in cls.model_fields
            if cls.model_fields[field].is_required()
        ]

        missing_fields = set(class_attrs) - set(values)

        if missing_fields:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"Error fields required {missing_fields}",
            )

        return values
