from fastapi import APIRouter, HTTPException, Request

from DB.db_blacklist import db_blacklist_add, db_blacklist_check, db_blacklist_remove
from DB.db_orders import (
    db_get_all_order,
    db_get_order_by_id,
    db_remove_order,
    db_set_order_delivred,
)

route = APIRouter()


# ! -------- COSTUMER ORDER ROUTES  ----------------


# GET ALL ORDER
@route.get("/order")
async def get_all_order(
    req: Request,
    offset: int | None = None,
    limit: int | None = None,
    date: str | None = None,
    dilivred: bool | None = None,
):

    all_order = await db_get_all_order(req.app.pool, offset, limit, date, dilivred)
    return all_order


# GET ORDER BY ID
@route.get("/order/{id}")
async def get_order_byId(req: Request, id: int):
    try:
        single_order = await db_get_order_by_id(req.app.pool, id)
        return single_order
    except:
        return HTTPException(status_code=404)


# SET ORDER DELEVIRED
@route.post("/order/{id}")
async def set_ordr_delivred(req: Request, id: int):
    try:
        set_delivred = await db_set_order_delivred(req.app.pool, id)
        return set_delivred
    except:
        return HTTPException(status_code=404)


# DELETE ORDER
@route.delete("/order/{id}")
async def delete_order(req: Request, id: int):
    try:
        delted = await db_remove_order(req.app.pool, id)
    except:
        return HTTPException(status_code=404)


# ! -------- BLACKLIST COSTUMER  ----------------
@route.post("/blacklist")
async def add_ban(phone_number: int, req: Request):
    in_blacklist = await db_blacklist_check(req.app.pool, phone_number)
    if in_blacklist:
        return {"info": "phone number alredy blacklisted"}
    await db_blacklist_add(req.app.pool, phone_number)


# delete a costumer from blacklist
@route.delete("/blacklist")
async def remove_ban(phone_number: int, req: Request):
    in_blacklist = await db_blacklist_check(req.app.pool, phone_number)
    if in_blacklist:
        await db_blacklist_remove(req.app.pool, phone_number)
    return {"info": "not in blacklist"}
