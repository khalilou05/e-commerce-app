from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from settings import DEV_MODE
from utils.jwtoken import isAuthanticated


class Authmid(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("token")
        isAuth = await isAuthanticated(token)
        request.scope["auth"] = isAuth
        # todo check dev mode
        if DEV_MODE:
            request.scope["auth"] = True
        resp = await call_next(request)

        return resp
