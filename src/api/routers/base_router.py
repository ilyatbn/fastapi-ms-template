import inspect
from typing import List
from fastapi import APIRouter, Request, responses, status
from db.helpers import database_exception_handler

create_object_var = "create_object"
update_object_var = "update_object"
annotated_schemas = [create_object_var, update_object_var]

class BaseRouter:
    query_object_schema = None
    create_object_schema = None
    update_object_schema = None
    prefix = None
    model = None

    def __init__(self) -> None:
        if not self.prefix.startswith("/"):
            self.prefix = f"/{self.prefix}"
        self.router = APIRouter(prefix=f"{self.prefix}")
        # TODO: maybe move all this to a different method and add "allowed methods"
        # TODO: maybe split this and create like "mixins" in drf... idk.
        self.router.add_api_route(
            "/",
            self.list,
            methods=["GET"],
            tags=[self.prefix.capitalize()],
            response_model=List[self.query_object_schema],
        )
        self.router.add_api_route(
            "/{item_id}",
            self.get,
            methods=["GET"],
            tags=[self.prefix.capitalize()],
            response_model=self.query_object_schema,
        )
        self.router.add_api_route(
            "/",
            self.create,
            methods=["POST"],
            tags=[self.prefix.capitalize()],
            response_model=self.query_object_schema,
        )
        self.router.add_api_route(
            "/{item_id}",
            self.update,
            methods=["PUT", "PATCH"],
            tags=[self.prefix.capitalize()],
            response_model=self.query_object_schema,
        )
        self.router.add_api_route(
            "/{item_id}",
            self.delete,
            methods=["DELETE"],
            tags=[self.prefix.capitalize()],
        )
        self.model = self.model()

    async def list(self, request: Request):
        # TODO: pagination..
        # TODO: filters by queryparams..
        # TODO: base filter by access permissions..
        return await self.model.all()

    async def get(self, item_id: int, request: Request):
        user_query = await self.model.get_item_by_id(item_id)
        if not user_query:
            return responses.JSONResponse(
                content={"error": "not found"}, status_code=status.HTTP_404_NOT_FOUND
            )
        return user_query

    async def create(self, request: Request, create_object: create_object_schema):
        try:
            object = await self.model.create_item(
                **create_object.model_dump(exclude_unset=True)
            )
        except Exception as ex:
            return database_exception_handler(ex)
        return object

    async def update(
        self, item_id: int, request: Request, update_object: update_object_schema
    ):
        try:
            object = await self.model.update_item_by_id(
                item_id=item_id, **update_object.model_dump(exclude_unset=True)
            )
        except Exception as ex:
            return database_exception_handler(ex)
        return object

    async def delete(self, item_id: int, request: Request):
        deleted = await self.model.delete_item_by_id(item_id)
        if not deleted:
            return responses.JSONResponse(
                content={"error": "not found"}, status_code=status.HTTP_404_NOT_FOUND
            )
        return True

    # hacky but cool solution. this solves working with fastapi type annotations for POST request schemas.
    def reconfigure_annotations(self):
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            for var in annotated_schemas:
                method[1].__annotations__[var] = (
                    getattr(self, f"{var}_schema")
                    if var in method[1].__annotations__
                    else None
                )
