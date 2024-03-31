from fastapi import UploadFile
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from schema.shcema import Article_schema


async def db_create_img_url(
    cnx: AsyncConnectionPool, article_id: int, images: list[UploadFile]
):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            for index, _ in enumerate(images):
                img_url = f"art_{article_id}_img_{index+1}.jpeg"
                img_number = index + 1
                await cur.execute(
                    """--sql
                    INSERT INTO img_url 
                    (article_id,img_url, img_number) 
                    VALUES (%s,%s,%s);
                    """,
                    (article_id, img_url, img_number),
                )


async def db_create_article(cnx: AsyncConnectionPool, article: Article_schema):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                INSERT INTO article 
                (title,description,price,prev_price) 
                VALUES (%s,%s) 
                RETURNING id;
                """,
                (article.title, article.description, article.price, article.prev_price),
            )
            q = await query.fetchone()
            article_id = q[0]
            return article_id


async def db_get_all_article(
    cnx: AsyncConnectionPool, offset: int = 0, limit: int = 100
):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            q1 = await cur.execute(
                """--sql
                                SELECT a.id,a.title,a.price,i.image_url
                                FROM article a
                                JOIN image_url i
                                ON i.article_id=a.id
                                WHERE i.img_number=1
                                ;
                                """,
                (offset, limit),
            )
            data = await q1.fetchall()

            return data


async def db_get_article_by_id(cnx: AsyncConnectionPool, article_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            query1 = await cur.execute(
                """--sql
                SELECT article.id,title,brand,model,tissu,description,img_url
                FROM article 
                JOIN img_url ON article_id=article.id
                WHERE article.id=%s;
                                 
                 """,
                (article_id,),
            )
            data = await query1.fetchall()

            if cur.rowcount == 0:
                return False
            query2 = await cur.execute(
                """
                --sql
                SELECT size,size_qty,size_price,color 
                FROM article_stock 
                WHERE article_stock.article_id=%s;
                """,
                (article_id,),
            )
            stock = await query2.fetchall()

            article_data = {}
            img_list = []
            stock_list = []
            for item in data:
                img_list.append(item["img_url"])

            for item in stock:
                stock_list.append(
                    {
                        "size": item["size"],
                        "size_qty": item["size_qty"],
                        "size_price": item["size_price"],
                        "color": item["color"],
                    }
                )
            art = data[0]
            article_data.update(
                {
                    "id": art["id"],
                    "title": art["title"],
                    "brand": art["brand"],
                    "model": art["model"],
                    "tissu": art["tissu"],
                    "description": art["description"],
                }
            )
            article_data["img_url"] = img_list
            article_data["stock"] = stock_list
            return article_data


async def db_delete_article_by_id(cnx: AsyncConnectionPool, article_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                DELETE FROM article WHERE id=%s ;
                """,
                (article_id,),
            )


async def db_get_art_img_url(cnx: AsyncConnectionPool, article_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                SELECT img_url FROM img_url WHERE article_id=%s ;
                """,
                (article_id,),
            )
            return await cur.fetchall()


async def db_update_article_by_id(
    cnx: AsyncConnectionPool, article_id: int, data: Article_schema
):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                                UPDATE article SET title=%s,brand=%s,model=%s,description=%s  WHERE id=%s ;
                """,
                (data.title, data.brand, data.model, data.description, article_id),
            )
