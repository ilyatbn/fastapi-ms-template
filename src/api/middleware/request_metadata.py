

from starlette.middleware.base import BaseHTTPMiddleware


class RequestMetadataMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.requested_by = request.headers.get("x-request-user", request.client.host)
        response = await call_next(request)
        return response