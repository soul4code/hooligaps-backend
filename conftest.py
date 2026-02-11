import pytest
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, TEST_DB_NAME
from db_utils import get_db
from main import app as fastapi_app
from models import Base

TEST_DB_ASYNC_URL = (
    f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}'
)


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
    engine = create_async_engine(TEST_DB_ASYNC_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def engine():
    engine = create_async_engine(TEST_DB_ASYNC_URL, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        return db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db
    async_client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=fastapi_app), base_url='http://test'
    )
    yield async_client
    fastapi_app.dependency_overrides.clear()
    await async_client.aclose()


@pytest.fixture(autouse=True)
async def cleanup_db(db_session):
    yield
    for table in reversed(Base.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()
