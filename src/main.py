from fastapi import FastAPI
from api.routers import ACTIVE_ROUTERS
from api.middleware import ACTIVE_MIDDLEWARE

app = FastAPI()

for router in ACTIVE_ROUTERS:
    app.include_router(router().router)
for middleware in ACTIVE_MIDDLEWARE:
    app.add_middleware(middleware)
