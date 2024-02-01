from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware

from application.utils.contexts import REQUEST_ID_CONTEXT_VAR


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        REQUEST_ID_CONTEXT_VAR.set(f"{request.client.host}-{uuid4()}")
        response = await call_next(request)
        return response
