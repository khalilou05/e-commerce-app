from fastapi import APIRouter, HTTPException, Request

from DB.db_blacklist import db_blacklist_add, db_blacklist_check, db_blacklist_remove
from DB.db_orders import (
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
):

    try:
        all_order = await db_get_all_order(req.app.pool, offset, limit, date, status)
        return all_order
    except:
        raise HTTPException(status_code=404)


# SET ORDER CONFIRMED
@route.post("/order/confirm")
async def set_ordr_confirmed(req: Request):
    idsList = await req.json()
    for num in idsList:
        try:
            set_confirmed = await db_set_order_confirmed(req.app.pool, num)
        except:
            return HTTPException(status_code=404)


# SET ORDER ARCHIVED
@route.post("/order/archive")
async def set_ordr_archived(req: Request):
    idsList = await req.json()
    for num in idsList:
        try:
            set_archived = await db_set_order_archived_and_shiped(req.app.pool, num)
        except:
            return HTTPException(status_code=404)


# DELETE ORDER
@route.delete("/order/delete")
async def delete_order(req: Request):
    idList: list[int] = await req.json()
    for num in idList:
        try:
            delted = await db_remove_order(req.app.pool, num)
        except:
            return HTTPException(status_code=400)


# ! -------- BLACKLIST COSTUMER  ----------------
@route.post("/blacklist")
async def add_ban(phone_number: phoneNumber, req: Request):

    for phoneN in phone_number.phone_number:
        in_blacklist = await db_blacklist_check(req.app.pool, phoneN)
        if in_blacklist:
            return
        await db_blacklist_add(req.app.pool, phoneN)


# delete a costumer from blacklist
# @route.delete("/blacklist")
# async def remove_ban(phone_number: int, req: Request):
#     in_blacklist = await db_blacklist_check(req.app.pool, phone_number)
#     if in_blacklist:
#         await db_blacklist_remove(req.app.pool, phone_number)
#     return {"info": "not in blacklist"}
