from fastapi import FastAPI
from api.middleware import ACTIVE_MIDDLEWARE
from api.middleware.cors import add_cors_middleware
from api.routers import ACTIVE_ROUTERS
from contextlib import asynccontextmanager
from core.logger import logger
from core.app_config import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler


SCHEDULED_JOBS = [
    # {"func": some_async_method, 'trigger': 'interval', 'minutes': 5, 'max_instances': 1}
]
running_scheduled_jobs = list()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if config.ENABLE_SCHEDULED_TASKS:
        logger.info("starting scheduled tasks.")
        scheduler = AsyncIOScheduler()
        scheduler.configure(job_defaults={"misfire_grace_time": 60})
        scheduler.start()
        for job in SCHEDULED_JOBS:
            running_scheduled_jobs.append(scheduler.add_job(**job))
    yield
    logger.info("shutting down")

app = FastAPI(lifespan=lifespan)

for router in ACTIVE_ROUTERS:
    app.include_router(router().router)

for middleware in ACTIVE_MIDDLEWARE:
    app.add_middleware(middleware)
    add_cors_middleware(app)  