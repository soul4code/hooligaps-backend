import datetime

from fastapi_pagination.cursor import CursorParams, CursorPage
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from pydantic import BaseModel, field_validator, Field
from uuid import UUID


class CustomCursorParams(CursorParams):
    size: int = Field(default=10, ge=1, le=100)


class CustomCursorCustomizer(UseParamsFields):
    params = CustomCursorParams


CustomCursorPage = CustomizedPage[CursorPage, CustomCursorCustomizer()]


class SubmitFormData(BaseModel):
    date: datetime.date = Field(..., title='Date')
    first_name: str = Field(
        ..., title='First Name', description='First Name. Must be a string without whitespaces.'
    )
    last_name: str = Field(
        ..., title='Last Name', description='Last Name. Must be a string without whitespaces.'
    )

    @field_validator('first_name', 'last_name')
    @classmethod
    def check_whitespaces(cls, value, info):
        if ' ' in value:
            raise ValueError(f'No whitespace in {info.field_name} is allowed')
        return value


class HistoryResponse(BaseModel):
    id: UUID = Field(..., title='ID')
    date: datetime.date = Field(..., title='Date')
    first_name: str
    last_name: str
    count: int
