from fastapi import APIRouter
from api.models.api_models import UserModelData
from fastapi import status, Request, responses
from typing import List
from datetime import datetime
from uuid import uuid4


router = APIRouter(prefix="/users")

# placeholder. move to postgres.
sample_user_data = [{
    "item_id": '81c91f92-5f9c-42a2-9f69-5630570e441c',
    "username": "sample1",
    "password": "encrypted_data",
    "email": None,
    "description": "manually created user",
    "created_at": datetime.utcnow(),
    "created_by": "superuser"
}]


@router.get(path = "/")
async def list_users(request: Request, response_model=List[UserModelData]):
    response_model = [UserModelData(**user) for user in sample_user_data]
    return response_model


@router.get(path = "/{item_id}")
async def get(item_id: str, request: Request, response_model=UserModelData):
    user_query = [ response_model(**user) for user in sample_user_data if user.get("item_id", None) == item_id ]
    if not user_query:
        return responses.JSONResponse(content={"error": "not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return user_query[0]


@router.post("/")
async def create(request: Request, user=UserModelData):
    sample_user_data.append(user.model_dump_json())
    return 

# @router.put("/users/")
# @router.patch("/users/")
# async def update():
#     return [{"username": "Rick"}, {"username": "Morty"}]

@router.delete("/users/")
async def delete():
    return [{"username": "Rick"}, {"username": "Morty"}]
