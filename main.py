from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from db_utils import get_db
from decorators import inject_delay
from filters import HistoryFilter, FirstNameFilter, LastNameFilter

from models import History
from schemas import SubmitFormData, HistoryResponse, CustomCursorPage, CustomCursorParams

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def submit_validation_handler(request: Request, exc: RequestValidationError):
    try:
        errors_detail = {}
        for error in exc.errors():
            errors_detail[error['loc'][-1]] = str(error['ctx']['error'])
        return JSONResponse(
            status_code=400,
            content={
                'success': False,
                'error': errors_detail,
            },
        )
    except (KeyError, IndexError):
        return JSONResponse(
            status_code=422,
            content={'detail': jsonable_encoder(exc.errors())},
        )


@app.post('/submit')
async def submit(
    form_data: SubmitFormData,
    session: AsyncSession = Depends(get_db),
    _: None = Depends(inject_delay),
):
    item = History(**form_data.model_dump())
    session.add(item)
    await session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'success': True})


@app.get('/history', response_model=CustomCursorPage[HistoryResponse])
async def history(
    params: Annotated[CustomCursorParams, Depends()],
    history_filter: HistoryFilter = FilterDepends(HistoryFilter),
    session: AsyncSession = Depends(get_db),
):
    HistoryAlias = aliased(History)
    stmt = select(
        History.id,
        History.date,
        History.first_name,
        History.last_name,
        select(func.count())
        .where(
            and_(
                HistoryAlias.first_name == History.first_name,
                HistoryAlias.last_name == History.last_name,
                HistoryAlias.date < History.date,
            )
        )
        .scalar_subquery()
        .label('count'),
    ).order_by(History.id.desc())
    stmt = history_filter.filter(stmt)
    results = await apaginate(session, stmt, params)
    return results


@app.get('/first-names', response_model=CustomCursorPage[str])
async def first_names(
    params: Annotated[CustomCursorParams, Depends()],
    filter_params: FirstNameFilter = FilterDepends(FirstNameFilter),
    session: AsyncSession = Depends(get_db),
):
    stmt = select(History.first_name).order_by(History.first_name, History.id)
    stmt = filter_params.filter(stmt).distinct(History.first_name)
    results = await apaginate(session, stmt, params)
    results.items = [item[0] for item in results.items]
    return results


@app.get('/last-names', response_model=CustomCursorPage[str])
async def last_names(
    params: Annotated[CustomCursorParams, Depends()],
    filter_params: LastNameFilter = FilterDepends(LastNameFilter),
    session: AsyncSession = Depends(get_db),
):
    stmt = select(History.last_name).order_by(History.last_name, History.id)
    stmt = filter_params.filter(stmt).distinct(History.last_name)
    results = await apaginate(session, stmt, params)
    results.items = [item[0] for item in results.items]
    return results
