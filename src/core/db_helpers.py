from urllib.parse import urlparse, urlunparse

from asyncpg.exceptions import DuplicateDatabaseError
from sqlalchemy.sql import text

from core.app_config import config
from core.db_client import DatabaseSessionManager

# TODO: Temporary, need to implement Alembic.


async def create_db():
    if not config.DB_ENGINE == "POSTGRES":
        return
    mgr = DatabaseSessionManager()
    conn_str = urlparse(config.DATABASE_URI)
    conn = urlunparse(conn_str._replace(path="/postgres"))
    mgr.init(conn, autocommit=True)

    database = conn_str.path[1:]

    async with mgr.session() as sess:
        try:
            result = await sess.execute(text(f"CREATE DATABASE {database}"))
            return result
        except DuplicateDatabaseError as ex:
            pass


async def create_schemas():
    sessionmanager = DatabaseSessionManager()
    # all models have to be imported before this can work.. sucks.
    from db.models import User

    sessionmanager.init(config.DATABASE_URI)
    await sessionmanager.create_all()


async def first_run():
    await create_db()
    await create_schemas()
