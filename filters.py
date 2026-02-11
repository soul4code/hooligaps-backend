import datetime
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field, ConfigDict

from models import History


class HistoryFilter(Filter):
    date__lte: Optional[datetime.date] = Field(
        None,
        alias='date',
        description='Date less than or equal to this date',
    )
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    def resolve(self):
        if self.date__lte is None:
            raise ValueError("Parameter 'date' is required")
        return super().resolve()

    model_config = ConfigDict(populate_by_name=True, extra='ignore')

    class Constants(Filter.Constants):
        model = History


class FirstNameFilter(Filter):
    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = History
        search_model_fields = [
            'first_name',
        ]


class LastNameFilter(Filter):
    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = History
        search_model_fields = [
            'last_name',
        ]
