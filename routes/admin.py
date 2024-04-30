from fastapi import APIRouter, Form, HTTPException, Request, UploadFile

from DB.db_blacklist import db_blacklist_add, db_blacklist_check, db_blacklist_remove
from DB.db_orders import (
    db_count_all_roder,
    db_get_all_order,
    db_remove_order,
    db_set_order_confirmed,
)
from DB.db_shipping_cost import (
    add_shipping_cost,
    arabic_wilaya,
    french_wilaya,
    get_all_wilaya_shipping_cost,
    remove_wilaya,
    update_wilaya_shipping_cost,
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


# SET ORDER CONFIRMED ( SINGLE AND BULK OPERATIONS )
@route.post("/order/confirm")
async def set_ordr_confirmed(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    idsList: int | list[int] = await req.json()
    if type(idsList) == list:
        for order_id in idsList:
            await db_set_order_confirmed(req.app.pool, order_id)
    await db_set_order_confirmed(req.app.pool, idsList)


# DELETE ORDER ( SINGLE AND BULK OPERATIONS )
@route.delete("/order/delete")
async def delete_order(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    idList: int | list[int] = await req.json()
    if type(idList) == list:
        for order_id in idList:
            await db_remove_order(req.app.pool, order_id)
    await db_remove_order(req.app.pool, idList)


# ! -------- BLACKLIST COSTUMER  ----------------
# add a phone number to blacklist
@route.post("/blacklist")
async def add_ban(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    phone_number_list: list[str] = await req.json()

    for phone in phone_number_list:
        in_blacklist = await db_blacklist_check(req.app.pool, phone)
        if in_blacklist:
            return {"error": "alredy in blacklist"}
        await db_blacklist_add(req.app.pool, phone)


# delete phone number from blacklist
@route.delete("/blacklist")
async def remove_ban(req: Request):
    if not req.auth:
        raise HTTPException(status_code=401)
    phone_number = await req.json()
    await db_blacklist_remove(req.app.pool, phone_number)


# ! -------- WILAYA SHIPPING COST   ----------------
@route.get("/shipping")
async def test(req: Request):
    try:
        shipping_cost = await get_all_wilaya_shipping_cost(req.app.pool)
        return shipping_cost
    except:
        raise HTTPException(status_code=400)


# add a wilaya shipping cost
@route.post("/shipping")
async def add_wilayaCost(
    req: Request,
    wilaya: str = Form(),
    desk_price: int = Form(),
    home_price: int = Form(),
):
    try:
        await add_shipping_cost(req.app.pool, wilaya, desk_price, home_price)
    except:
        raise HTTPException(status_code=400)


# update a wilaya shipping cost
@route.put("/shipping")
async def update_wilayaCost(
    req: Request,
):
    wilaya = await req.json()
    try:
        await remove_wilaya(req.app.pool, wilaya)
    except:
        raise HTTPException(status_code=400)


# delete a wilaya from shipping cost list
@route.delete("/shipping")
async def delete_wilayaCost(
    req: Request,
    desk_price: int = Form(),
    home_price: int = Form(),
    wilaya: str = Form(),
):
    try:
        await update_wilaya_shipping_cost(req.app.pool, desk_price, home_price, wilaya)
    except:
        raise HTTPException(status_code=400)


#! --------- DZ WILAYA FOR DROPDOWN IN FRONTEND ---------------
@route.get("/dzwilaya")
async def test(
    req: Request,
    lang: str | None = None,
):
    if lang == "fr":
        frwilaya = await french_wilaya(req.app.pool)
        return frwilaya
    arwilaya = await arabic_wilaya(req.app.pool)
    return arwilaya


# ! -------- test  ----------------
# todo remove this route
@route.post("/test")
async def test(req: Request, images: list[UploadFile]):

    # for img in images:
    #     imgFormat = img.content_type.split("/")
    #     print(imgFormat[1])
    valid_extension = ["jpg", "jpeg", "png", "webp", "avif"]
    for image in images:
        imgFormat = image.content_type.split("/")
        if imgFormat[1] not in valid_extension:
            raise HTTPException(status_code=400)
        print("valid images")
