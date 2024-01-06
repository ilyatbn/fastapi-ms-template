from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel


class BaseModelMetadata(BaseModel):
    item_id: Optional[str] = str(uuid4())
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None


class UserModelData(BaseModelMetadata):
    username: str
    email: Optional[str] = None
    description: Optional[str] = None
