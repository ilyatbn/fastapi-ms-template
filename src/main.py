from fastapi import FastAPI

from api.middleware import ACTIVE_MIDDLEWARE
from api.middleware.cors import add_cors_middleware
from api.routers import ACTIVE_ROUTERS

app = FastAPI()

for router in ACTIVE_ROUTERS:
    app.include_router(router().router)
for middleware in ACTIVE_MIDDLEWARE:
    app.add_middleware(middleware)
    add_cors_middleware(app)
