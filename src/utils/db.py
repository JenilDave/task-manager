from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session, async_sessionmaker
from typing import AsyncGenerator
from asyncio import current_task

_engine = create_async_engine("sqlite+aiosqlite:///D:\\Storage\\sqlite\\task-manager\\manager.db")

async_session = async_sessionmaker(
    bind= _engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)

scoped_session = async_scoped_session(
    async_session,
    scopefunc=current_task
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async database session.

    The session is automatically closed when the request finishes.
    """
    session = scoped_session()
    try:
        yield session
    finally:
        await session.close()
