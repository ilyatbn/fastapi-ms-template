from fastapi import Request

from api.routers.base_router import BaseRouter
from api.schemas.api_schemas import (
    UserModelDataCreate,
    UserModelDataGet,
    UserModelDataUpdate,
)
from db.models import User


class UsersRouter(BaseRouter):
    query_object_schema = UserModelDataGet
    create_object_schema = UserModelDataCreate
    update_object_schema = UserModelDataUpdate
    prefix = "users"
    model = User

    def __init__(self) -> None:
        self.reconfigure_annotations()
        super().__init__()
