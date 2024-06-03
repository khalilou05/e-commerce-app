from fastapi import UploadFile
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from schema.shcema import Article_schema


async def db_create_img_url(
    cnx: AsyncConnectionPool, article_id: int, images: list[UploadFile]
):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            for index, image in enumerate(images):
                imgFormat = image.content_type.split("/")
                img_url = f"art_{article_id}_img_{index+1}.{imgFormat[1]}"
                img_number = index + 1
                await cur.execute(
                    """--sql
                    INSERT INTO img_url 
                    (article_id,img_url, img_number) 
                    VALUES (%s,%s,%s);
                    """,
                    (article_id, img_url, img_number),
                )


async def db_create_article(
    cnx: AsyncConnectionPool,
    title,
    description,
    price,
    quantity,
    reference,
    free_shipping,
):
    if free_shipping is None:
        free_shipping = False
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                INSERT INTO article 
                (title,description,price,quantity,reference, free_shipping) 
                VALUES (%s,%s,%s,%s,%s,%s) 
                RETURNING id;
                """,
                (title, description, price, quantity, reference, free_shipping),
            )
            article_id = await query.fetchone()
            return article_id[0]


# get article for the admin panel
async def db_get_all_article(
    cnx: AsyncConnectionPool, offset: int = 0, limit: int = 100
):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            q1 = await cur.execute(
                """--sql
                                SELECT a.id,a.title,a.price,a.quantity,a.free_shipping,a.published,i.img_url
                                FROM article a
                                JOIN img_url i
                                ON i.article_id=a.id
                                WHERE i.img_number=1
                                OFFSET %s
                                LIMIT %s
                                ;
                                """,
                (offset, limit),
            )
            data = await q1.fetchall()

            return data


async def db_check_article_quantity(cnx: AsyncConnectionPool, article_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            q1 = await cur.execute(
                """--sql
                                SELECT quantity FROM article WHERE id=%s
                                ;
                                """,
                (article_id,),
            )

            data = await q1.fetchone()
            if data is not None:
                return True
            return False


async def db_get_article_by_id(cnx: AsyncConnectionPool, article_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            query1 = await cur.execute(
                """--sql
                SELECT A.id,A.title,A.price,A.quantity,A.description,I.img_url
                FROM article A
                JOIN img_url I ON I.article_id=A.id
                WHERE A.id=%s;
                                 
                 """,
                (article_id,),
            )
            data = await query1.fetchall()

            if cur.rowcount == 0:
                return False

            query2 = await cur.execute(
                """--sql
                SELECT count(*) FROM visitor WHERE article_viewed=%s ;               
                 """,
                (article_id,),
            )
            resp = await query2.fetchone()
            number_of_visit = resp["count"]

            article_data = {}
            img_list = []
            for item in data:
                img_list.append(item["img_url"])

            art = data[0]
            article_data.update(
                {
                    "id": art["id"],
                    "title": art["title"],
                    "price": art["price"],
                    "quantity": art["quantity"],
                    "description": art["description"],
                    "viwed": number_of_visit,
                }
            )
            article_data["img_url"] = img_list
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


# function to get img url from db to disk delete
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
    cnx: AsyncConnectionPool, article_id: int, article: Article_schema
):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                                UPDATE article SET title=%s,brand=%s,model=%s,description=%s  WHERE id=%s ;
                """,
                (
                    article.title,
                    article.price,
                    article.quantity,
                    article.description,
                    article_id,
                ),
            )
