from fastapi import Request, responses
from starlette.middleware.base import BaseHTTPMiddleware

from utils.jwtoken import isAuthanticated

banned_reqest = ["DLETE", "PATCH", "PUT"]


class Authmid(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # todo clean this shit
        # token = request.headers.get("token")
        # request.scope["auth"] = await isAuthanticated(token)
        # if not request.auth and request.method in banned_reqest:
        #     return responses.JSONResponse(status_code=401, content="Unauthorized")
        resp = await call_next(request)

        return resp
