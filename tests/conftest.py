import pytest
from datetime import date, time, timedelta
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from src.schemas.booking import BookingStatus
from src.core.config import settings
settings.DB_PATH = "./test.db"

from src.main import app
from src.database.db import Base, get_db, engine, AsyncSessionLocal


@pytest.fixture(autouse=True, scope="function")
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
def override_get_db():
    async def override():
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    app.dependency_overrides[get_db] = override
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client():
    async with LifespanManager(app) as manager:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session

