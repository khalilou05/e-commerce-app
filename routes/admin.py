from fastapi import APIRouter, HTTPException, Request

from DB.db_blacklist import db_blacklist_add, db_blacklist_check, db_blacklist_remove
from DB.db_orders import (
    db_count_roders,
    db_get_all_order,
    db_order_change_status,
    db_remove_order,
    db_update_and_confirm_order,
)
from DB.db_shipping_cost import (
    get_active_wilaya_for_frontend,
    get_all_wilaya_shipping_cost,
    get_wilaya_cost_by_id,
    update_wilaya_shipping_cost,
)
from schema.shcema import Order, UpdateOrder

route = APIRouter()


# ! -------- COSTUMER ORDER ROUTES  ----------------


# GET ALL ORDER
@route.get("/order")
async def get_all_order(
    req: Request,
    status: str,
    offset: int,
    limit: int,
    date: str | None = None,
):
    if not req.auth:
        raise HTTPException(status_code=401)
    try:
        all_order = await db_get_all_order(
            req.app.pool, date=date, status=status, offset=offset, limit=limit
        )
        return all_order
    except:
        raise HTTPException(status_code=400)


# GET THE NUMBER OF ALL ORDER
@route.get("/order/count")
async def db_ordr_count(req: Request, status: str):
    if not req.auth:
        raise HTTPException(status_code=401)
    order_count_number = await db_count_roders(req.app.pool, status)
    return order_count_number


# UPDATE & CONFIRME ORDER ( SINGLE AND BULK OPERATIONS )
@route.post("/order/confirm")
async def set_ordr_confirmed(req: Request, order_list: list[Order]):
    if not req.auth:
        raise HTTPException(status_code=401)
    for order in order_list:
        await db_update_and_confirm_order(req.app.pool, order)


# DELETE ORDER ( SINGLE AND BULK OPERATIONS )
@route.post("/order/delete")
async def delete_order(req: Request, order_list: list[Order]):
    if not req.auth:
        raise HTTPException(status_code=401)
    for order in order_list:
        await db_remove_order(req.app.pool, order.id, order.article_id, order.quantity)


# change orders status
@route.post("/order/update")
async def order_update_status(req: Request, data: UpdateOrder):
    if not req.auth:
        raise HTTPException(status_code=401)

    for order in data.orders:
        await db_order_change_status(req.app.pool, data.status, order.id)


# ! -------- BLACKLIST COSTUMER  ----------------
# add a phone number to blacklist
@route.post("/blacklist/add")
async def add_ban(req: Request, ordersList: list[Order]):
    if not req.auth:
        raise HTTPException(status_code=401)

    for order in ordersList:
        in_blacklist = await db_blacklist_check(req.app.pool, order.phone_number)
        if in_blacklist:
            return {"error": "alredy in blacklist"}
        await db_blacklist_add(
            req.app.pool, order.phone_number, order.quantity, order.article_id
        )


# delete phone number from blacklist
# @route.delete("/blacklist/remove")
# async def remove_ban(req: Request):
#     if not req.auth:
#         raise HTTPException(status_code=401)
#     phone = await req.json()
#     await db_blacklist_remove(req.app.pool, phone)


# ! -------- WILAYA SHIPPING COST   ----------------
@route.get("/shipping")
async def get_wilaya_shipping_cost(req: Request):

    # for the admin panel
    # try:
    shipping_cost = await get_all_wilaya_shipping_cost(req.app.pool)
    return shipping_cost


# except:
#     raise HTTPException(status_code=400)


@route.get("/shipping/available")
async def get_wilaya_shipping_cost_active(req: Request, wilayaId: int | None = None):

    # for the frontend dropdown
    try:
        if wilayaId:
            wilaya = await get_wilaya_cost_by_id(req.app.pool, wilayaId)
            return wilaya
        shipping_cost = await get_active_wilaya_for_frontend(req.app.pool)
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
