import asyncpg.exceptions as asyncpg_exc
from fastapi import responses, status
from sqlalchemy.exc import IntegrityError

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
