from urllib.parse import urlparse, urlunparse

import asyncpg.exceptions as asyncpg_exc
from asyncpg.exceptions import DuplicateDatabaseError
from fastapi import responses, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from core.app_config import config
from core.db_client import DatabaseSessionManager
from core.logger import logger


def database_exception_handler(ex):
    message = "an unknown database error has occured. check logs for further details."

    # sqlalchemy integrity errors should have an original exception
    if isinstance(ex, IntegrityError):
        original_exception = getattr(ex, "orig")
        if type(original_exception.__cause__) == asyncpg_exc.UniqueViolationError:
            logger.error(
                f"unique constrait violation: {original_exception.__cause__.message}: {original_exception.__cause__.detail}"
            )
            message = original_exception.__cause__.detail
        else:
            logger.error(
                f"an error occured while performing database operation. original exception: {original_exception}"
            )
    else:
        logger.error(f"{message}: {ex}")

    return responses.JSONResponse(
        content={"error": f"could not create object: {message}"},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


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
