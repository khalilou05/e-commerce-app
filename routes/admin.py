from fastapi import APIRouter, HTTPException, Request

from DB.db_blacklist import db_blacklist_add, db_blacklist_check, db_blacklist_remove
from DB.db_orders import (
    db_count_all_roder,
    db_get_all_order,
    db_remove_order,
    db_set_order_archived_and_shiped,
    db_set_order_confirmed,
)
from schema.shcema import phoneNumber

route = APIRouter()


# ! -------- COSTUMER ORDER ROUTES  ----------------


# GET ALL ORDER
@route.get("/order")
async def get_all_order(
    req: Request,
    offset: int | None = None,
    limit: int | None = None,
    date: str | None = None,
    status: str | None = None,
    count: bool | None = None,
):
    if not req.auth:
        raise HTTPException(status_code=401)

    try:
        all_order = await db_get_all_order(
            req.app.pool, offset, limit, date, status, count
        )
        return all_order

    except:
        raise HTTPException(status_code=404)


# ORDER count
@route.get("/order/count")
async def db_ordr_count(req: Request, status: str | None = None):
    if not req.auth:
        raise HTTPException(status_code=401)
    order_count_number = await db_count_all_roder(req.app.pool, status)
    return order_count_number


# except:
# return HTTPException(status_code=404)


# SET ORDER CONFIRMED
@route.post("/order/confirm")
async def set_ordr_confirmed(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    idsList = await req.json()
    for num in idsList:
        try:
            set_confirmed = await db_set_order_confirmed(req.app.pool, num)
        except:
            return HTTPException(status_code=404)


# SET ORDER ARCHIVED
@route.post("/order/archive")
async def set_ordr_archived(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    idsList = await req.json()
    for num in idsList:
        try:
            set_archived = await db_set_order_archived_and_shiped(req.app.pool, num)
        except:
            return HTTPException(status_code=404)


# DELETE ORDER
@route.delete("/order/delete")
async def delete_order(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    idList: list[int] = await req.json()
    for num in idList:
        try:
            delted = await db_remove_order(req.app.pool, num)
        except:
            return HTTPException(status_code=400)


# ! -------- BLACKLIST COSTUMER  ----------------
@route.post("/blacklist")
async def add_ban(phone_number: phoneNumber, req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)

    for phoneN in phone_number.phone_number:
        in_blacklist = await db_blacklist_check(req.app.pool, phoneN)
        if in_blacklist:
            return
        await db_blacklist_add(req.app.pool, phoneN)
