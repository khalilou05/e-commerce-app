import os
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile

from DB.db_article import (
    db_create_article,
    db_create_img_url,
    db_delete_article_by_id,
    db_get_all_article,
    db_get_art_img_url,
    db_get_article_by_id,
    db_update_article_by_id,
)
from DB.db_orders import db_create_order
from DB.db_visitor import db_add_article_visitor, db_add_visitor_ip, db_check_visitor_ip
from schema.shcema import Article_schema, Order
from utils.img_upload import article_img_upload

route = APIRouter()


#! ------ GET ALL ARTICLE | WITH OFFSET AND LIMIT PARAMS -----------
@route.get("/")
async def all_article(
    req: Request, offset: int | None = None, limit: int | None = None
):
    visited = await db_check_visitor_ip(req.app.pool, req.client.host)
    if not visited:
        await db_add_visitor_ip(req.app.pool, req.client.host)
    data = await db_get_all_article(req.app.pool, offset, limit)
    return data


#! ------ GET ARTICLE BY ID -----------
@route.get("/article/{id}")
async def get_article_by_id(id: int, req: Request):
    # todo add the visitor ip to db
    visited = await db_check_visitor_ip(req.app.pool, req.client.host)
    if not visited:
        added = await db_add_article_visitor(req.app.pool, req.client.host, id)
        if not added:
            raise HTTPException(status_code=400)
    data = await db_get_article_by_id(req.app.pool, id)
    if not data:
        raise HTTPException(status_code=404)
    return data


#! ------ ORDER ARTICLE -----------
@route.post("/article/{article_id}")
async def order_article(req: Request, order_info: Order, article_id):
    order_created = await db_create_order(req.app.pool, order_info, article_id)


#! ------ DELETE ARTICLE BY ID -----------
@route.delete("/article/{id}")
async def delete_article_by_id(id: int, req: Request):

    try:
        img_list = await db_get_art_img_url(req.app.pool, id)
        deleted = await db_delete_article_by_id(req.app.pool, id)
        path = Path() / "static"

        for img in img_list:
            path_to_delete = f"{path}/{img[0]}"
            os.remove(path_to_delete)
    except:
        raise HTTPException(status_code=400)


#! ------ UPDATE ARTICLE BY ID -----------
@route.put("/article/{id}")
async def update_article(id: int, req: Request, article_data: Article_schema):

    try:
        data = await db_update_article_by_id(req.app.pool, id, article_data)
        return data
    except:
        raise HTTPException(status_code=404)


#! ------ CREATE ARTICLE -----------
@route.post("/article", status_code=201)
async def create_article(req: Request, article: Article_schema):

    try:
        article_id = await db_create_article(req.app.pool, article)
        return {"id": article_id}
    except:

        raise HTTPException(status_code=400, detail="not created")


#! ------ UPLAOD ARTICLE IMAGES -----------
@route.post("/upload")
async def test(
    images: list[UploadFile], req: Request, article_id: Annotated[int, Form()]
):

    try:
        create_db_url = await db_create_img_url(req.app.pool, article_id, images)
        upload_img = await article_img_upload(article_id, images)
        return Response(status_code=201)
    except:

        raise HTTPException(status_code=400, detail="not created")
