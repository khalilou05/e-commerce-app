from fastapi import APIRouter, HTTPException, Request

from DB.db_auth import db_get_login_info
from schema.shcema import login_data
from utils.jwtoken import make_token
from utils.pswdhash import verify_passwd

route = APIRouter()


# ! -------- LOG IN AND GENERATE TOKEN -----------


@route.post("/admin")
async def admin_login(login_data: login_data, req: Request):
    id, _, passwd = await db_get_login_info(req.app.pool, login_data.username)
    pascheck = verify_passwd(passwd, login_data.password)
    if not pascheck:
        return HTTPException(status_code=401, detail="Invalid email or password")
    token = await make_token(id, 1)

    return {"token": token}
