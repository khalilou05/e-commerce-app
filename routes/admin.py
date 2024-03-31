import datetime
from fastapi import APIRouter, HTTPException, Request, Response

from DB.db_auth import db_get_login_info
from DB.db_orders import db_get_all_order, db_get_order_by_id
from utils.jwtoken import make_token
from utils.pswdhash import verify_passwd
from utils.pswdhash import hash_passwd
from DB.db_blacklist import db_blacklist_add, db_blacklist_remove, db_blacklist_check
from DB.db_auth import db_change_admin_passwd

route = APIRouter()


# ! -------- LOG IN AND GENERATE TOKEN -----------
@route.post("/admin")
async def admin_login(data, req: Request):
    id, _, passwd = await db_get_login_info(req.app.pool, data.email)
    pascheck = await verify_passwd(passwd, data.password)
    if not pascheck:
        return HTTPException(status_code=401, detail="Invalid email or password")
    token = await make_token(id, 1)

    return {"token": token}


# ! -------- COSTUMER ORDER ROUTES  ----------------
@route.get("/order")
async def get_all_order(
    req: Request,
    offset: int | None = None,
    limit: int | None = None,
    date: str | None = None,
):
    if not req.auth:
        return HTTPException(status_code=401)
    all_order = await db_get_all_order(req.app.pool, offset, limit, date)
    return all_order


@route.get("/order/{id}")
async def add_order(req: Request, id: int):
    try:
        single_order = await db_get_order_by_id(req.app.pool, id)
        return single_order
    except:
        return HTTPException(status_code=404)


# ! -------- BLACKLIST COSTUMER  ----------------
@route.post("/blacklist")
async def add_ban(phone_number: int, req: Request):
    in_blacklist = await db_blacklist_check(req.app.pool, phone_number)
    if in_blacklist:
        return {"info": "phone number alredy blacklisted"}
    await db_blacklist_add(req.app.pool, phone_number)


# --------   delete a costumer from blacklist  -----------
@route.delete("/blacklist")
async def remove_ban(phone_number: int, req: Request):
    in_blacklist = await db_blacklist_check(req.app.pool, phone_number)
    if in_blacklist:
        await db_blacklist_remove(req.app.pool, phone_number)
    return {"info": "not in blacklist"}


# ! -------- RESET ADMIN PASSWORD -------------------
@route.post("/resetpswd")
async def reset_passwd(raw_password, req: Request):
    hashed_password = hash_passwd(raw_password)
    pswd_changed = await db_change_admin_passwd(hashed_password)
    return Response(content={}, status_code=201)


# ! -------- test  ----------------
@route.get("/test")
async def get_all_order(
    req: Request,
    offset: int | None = None,
    limit: int | None = None,
    date: str | None = None,
):
    da = datetime.date.today()

    return [da]
