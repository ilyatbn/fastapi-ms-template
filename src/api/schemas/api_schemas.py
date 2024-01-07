from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel


class BaseModelMetadata(BaseModel):
    class Config:
        orm_mode = True


class BaseModelGet:
    id: Optional[int] = None


class UserModelDataCreate(BaseModelMetadata):
    username: str
    display_name: Optional[str] = None
    enabled: Optional[bool] = None


class UserModelDataUpdate(UserModelDataCreate):
    username: Optional[str] = None


class UserModelDataGet(BaseModelGet, UserModelDataCreate):
    pass
