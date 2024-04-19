from fastapi import Request, responses
from starlette.middleware.base import BaseHTTPMiddleware

from utils.jwtoken import isAuthanticated


class Authmid(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # todo clean this shit
        token = request.cookies.get("token")
        isAuth = await isAuthanticated(token)
        request.scope["auth"] = isAuth
        resp = await call_next(request)

        return resp
