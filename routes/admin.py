from fastapi import APIRouter, HTTPException, Request

from DB.db_blacklist import db_blacklist_add, db_blacklist_check, db_blacklist_remove
from DB.db_orders import (
    db_count_all_roder,
    db_get_all_order,
    db_remove_order,
    db_update_and_confirm_order,
)
from DB.db_shipping_cost import (
    get_all_wilaya_shipping_cost,
    update_wilaya_shipping_cost,
)
from schema.shcema import Order

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
    if not req.auth:
        raise HTTPException(status_code=401)
    try:
        all_order = await db_get_all_order(req.app.pool, offset, limit, date, status)
        return all_order

    except:
        raise HTTPException(status_code=404)


# GET THE NUMBER OF ALL ORDER
@route.get("/order/count")
async def db_ordr_count(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    order_count_number = await db_count_all_roder(req.app.pool)
    return order_count_number


# UPDATE & CONFIRME ORDER ( SINGLE AND BULK OPERATIONS )
@route.post("/order/confirm")
async def set_ordr_confirmed(req: Request, order_list: list[Order]):
    if not req.auth:
        raise HTTPException(status_code=401)
    for order in order_list:
        await db_update_and_confirm_order(req.app.pool, order)


# DELETE ORDER ( SINGLE AND BULK OPERATIONS )
@route.delete("/order/delete")
async def delete_order(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    idList: list[int] = await req.json()
    for order_id in idList:
        await db_remove_order(req.app.pool, order_id)


# ! -------- BLACKLIST COSTUMER  ----------------
# add a phone number to blacklist
@route.post("/blacklist/add")
async def add_ban(
    req: Request,
):
    if not req.auth:
        raise HTTPException(status_code=401)
    phone_number_list: list[str] = await req.json()

    for phone in phone_number_list:
        in_blacklist = await db_blacklist_check(req.app.pool, phone)
        if in_blacklist:
            return {"error": "alredy in blacklist"}
        await db_blacklist_add(req.app.pool, phone)


# delete phone number from blacklist
@route.delete("/blacklist/remove")
async def remove_ban(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    phone = await req.json()
    await db_blacklist_remove(req.app.pool, phone)


# ! -------- WILAYA SHIPPING COST   ----------------
@route.get("/shipping")
async def get_all_wilaya_shipping_cost(req: Request, wilayaID: int):
    try:
        # for the admin panel
        shipping_cost = await get_all_wilaya_shipping_cost(req.app.pool)
        return shipping_cost
    except:
        raise HTTPException(status_code=400)


# update wilaya shipping cost ( SINGLE AND BULK OPERATIONS )
@route.put("/shipping/update")
async def update_wilaya_cost(req: Request):

    wilaya_list: list[dict] = await req.json()
    try:
        for wilaya in wilaya_list:
            await update_wilaya_shipping_cost(
                req.app.pool,
                wilaya["desk_price"],
                wilaya["home_price"],
                wilaya["active"],
                wilaya["id"],
            )
    except:
        raise HTTPException(status_code=400)
