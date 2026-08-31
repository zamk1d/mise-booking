from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.core.config import settings
from collections.abc import AsyncGenerator

class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session: # pragma: no cover
        try: # pragma: no cover
            yield session # pragma: no cover
            await session.commit() # pragma: no cover
        except Exception: # pragma: no cover
            await session.rollback() # pragma: no cover
            raise # pragma: no cover