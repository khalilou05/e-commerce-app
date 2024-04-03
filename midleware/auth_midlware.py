from fastapi import Request, responses
from starlette.middleware.base import BaseHTTPMiddleware

from utils.jwtoken import isAuthanticated

banned_reqest = ["DLETE", "PATCH", "PUT"]


class Authmid(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("token")
        request.scope["auth"] = await isAuthanticated(token)
        if not request.auth and request.method in banned_reqest:
            return responses.JSONResponse(status_code=401, content="Unauthorized")
        if request.base_url.path:
            pass
        resp = await call_next(request)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
