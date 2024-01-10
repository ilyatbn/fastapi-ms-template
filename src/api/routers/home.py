from fastapi import Request, Response, status

from api.routers.base_router import BaseRouter


class HomeRouter(BaseRouter):
    prefix = ""

    def __init__(self) -> None:
        super().__init__()
        self.router.add_api_route(
            "/", self.home, methods=["GET"], include_in_schema=False
        )

    async def home(self, request: Request):
        return Response(
            content=f"Hello, {request.state.requested_by}",
            status_code=status.HTTP_418_IM_A_TEAPOT,
        )
