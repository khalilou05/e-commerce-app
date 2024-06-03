from fastapi import APIRouter, HTTPException, Request, Response

from DB.db_auth import db_change_admin_data, db_get_login_info
from schema.shcema import login_data
from utils.jwtoken import make_token
from utils.pswdhash import hash_passwd, verify_passwd

route = APIRouter()


# ! -------- LOG IN AND GENERATE TOKEN -----------


@route.post("/login")
async def admin_login(login_data: login_data, req: Request, res: Response):
    # todo some brut forse security
    exist, data = await db_get_login_info(req.app.pool, login_data.username)
    if not exist:
        raise HTTPException(status_code=400)
    id, _, passwd = data
    pascheck = verify_passwd(passwd, login_data.password)
    if not pascheck:
        return HTTPException(status_code=401, detail="Invalid email or password")
    token = await make_token(id)
    response = res.set_cookie(key="token", value=token, secure=True)

    # return response
    return {"res": "ok"}


# ! -------- RESET ADMIN PASSWORD ( MUST BE LOGED IN) -------------------
@route.post("/resetpassword")
# todo check here boy
async def reset_passwd(req: Request, admin_data: login_data):
    if not req.auth:
        raise HTTPException(status_code=401)
    hashed_password = hash_passwd(admin_data.password)
    await db_change_admin_data(req.app.pool, admin_data)
    return Response(content={}, status_code=201)


# ! -------- FORGOT PASSWORD -------------------
@route.post("/forgotpassword")
# todo add the logic
async def forgot_password(req: Request):

    pass


# ! -------- LOGOUT AND DELETE THE COOKIE -------------------
@route.post("/logout")
# todo add the logic
async def logout(res: Response):
    res.delete_cookie(key="token")
    return res
