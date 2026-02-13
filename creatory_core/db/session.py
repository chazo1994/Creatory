from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from creatory_core.core.config import settings

engine = None
AsyncSessionLocal = None


def _ensure_session_factory() -> async_sessionmaker[AsyncSession]:
    global engine, AsyncSessionLocal

    if AsyncSessionLocal is not None:
        return AsyncSessionLocal

    engine = create_async_engine(
        settings.database_url,
        echo=settings.sql_echo,
        pool_pre_ping=True,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
    )
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return AsyncSessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = _ensure_session_factory()
    async with session_factory() as session:
        yield session
