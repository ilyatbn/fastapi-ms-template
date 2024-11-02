# based on this awesome implementation.
# https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html

import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DatabaseSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str, autocommit: str = False):
        self.engine = create_async_engine(host)
        if autocommit:
            self.engine = self.engine.execution_options(isolation_level="AUTOCOMMIT")
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self.engine)

    async def close(self):
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()
        self.engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self):
        async with self.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
