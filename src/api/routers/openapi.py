from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Request, responses, status

from api.schemas.api_schemas import UserModelData

router = APIRouter(prefix="/openapi")
