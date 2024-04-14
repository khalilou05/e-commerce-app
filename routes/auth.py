from fastapi import APIRouter, HTTPException, Request, Response

from DB.db_auth import db_change_admin_passwd, db_get_login_info
from schema.shcema import login_data
from utils.jwtoken import make_token
from utils.pswdhash import hash_passwd, verify_passwd

route = APIRouter()


# ! -------- LOG IN AND GENERATE TOKEN -----------


@route.post("/admin")
async def admin_login(login_data: login_data, req: Request):
    exist, data = await db_get_login_info(req.app.pool, login_data.username)
    if not exist:
        raise HTTPException(status_code=400)
    id, _, passwd = data
    pascheck = verify_passwd(passwd, login_data.password)
    if not pascheck:
        return HTTPException(status_code=401, detail="Invalid email or password")
    token = await make_token(id)

    return {"token": token}


# ! -------- RESET ADMIN PASSWORD -------------------
@route.post("/resetpswd")
# todo check here boy
async def reset_passwd(raw_password, req: Request):
    hashed_password = hash_passwd(raw_password)
    pswd_changed = await db_change_admin_passwd(req.app.pool, hashed_password)
    return Response(content={}, status_code=201)
