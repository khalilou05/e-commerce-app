from fastapi import Request, responses
from starlette.middleware.base import BaseHTTPMiddleware

from utils.jwtoken import isAuthanticated

banned_reqest = ["DLETE", "PATCH", "PUT"]


class Authmid(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cookie = request.headers.get("Cookie")
        request.scope["auth"] = await isAuthanticated(cookie)
        if request.method in banned_reqest and request.auth == False:
            return responses.JSONResponse(status_code=401, content="Unauthorized")
        resp = await call_next(request)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
