from fastapi import APIRouter
from fastapi import status, Request, Response


router = APIRouter(prefix="")


@router.get(path = "/")
async def home(request: Request):
    return Response(content=f"Hello, {request.state.requested_by}", status_code=status.HTTP_418_IM_A_TEAPOT)