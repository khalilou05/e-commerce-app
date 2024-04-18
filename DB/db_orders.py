from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from schema.shcema import Order


async def db_create_order(
    cnx: AsyncConnectionPool, costumer_order: Order, article_id: int
):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    INSERT INTO costumer_order 
                    (article_id,
                    first_name,last_name,
                    phone_number,
                    wilaya,
                    baladiya,
                    quantity,
                    home_dilevery)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
                 """,
                (
                    article_id,
                    costumer_order.first_name,
                    costumer_order.last_name,
                    costumer_order.phone_number,
                    costumer_order.wilaya,
                    costumer_order.baladiya,
                    costumer_order.quantity,
                    costumer_order.home_dilevery,
                ),
            )


async def db_get_all_order(
    cnx: AsyncConnectionPool,
    offset: int = 0,
    limit: int = 50,
    date: str | None = None,
    status: str | None = None,
):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            if date == None and status == None:
                #! get all orders standar filternig
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,
                o.home_dilevery,art.price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                WHERE o.status='NONE'
                OFFSET %s 
                LIMIT %s;"""
                data = (offset, limit)
                q1 = await cur.execute(sql, data)
                default = await q1.fetchall()
                return default

            #! get confirmed order
            if status == "confirmed":
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,o.wilaya,o.baladiya,o.article_id,o.quantity,o.home_dilevery,art.id,art.price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                WHERE status='confirmed'
                OFFSET %s 
                LIMIT %s;
                """
                data = (offset, limit)
                q1 = await cur.execute(sql, data)
                date_filter = await q1.fetchall()
                return date_filter

            if status == "delivred":
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,o.wilaya,o.baladiya,o.article_id,o.quantity,o.home_dilevery,o.order_proceded,art.id,art.price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                WHERE o.status='delivred'
                OFFSET %s 
                LIMIT %s;
                """
                data = (offset, limit)
                q1 = await cur.execute(sql, data)
                result = await q1.fetchall()
                return result

            # get all orders with purchase date filtering
            if date:
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,o.wilaya,o.baladiya,o.article_id,o.quantity,o.home_dilevery,o.order_proceded,art.id,art.price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                WHERE purchase_date=%s 
                OFFSET %s 
                LIMIT %s;"""

                data = (date, offset, limit)
                q1 = await cur.execute(sql, data)
                resp = await q1.fetchall()
                return resp


# note to think about it
async def db_get_order_by_id(cnx: AsyncConnectionPool, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            query = await cur.execute(
                """--sql
                SELECT *
                FROM order
                WHERE id=%s
                ;
                """,
                (order_id,),
            )
            data = await query.fetchone()

            return data


async def db_set_order_confirmed(cnx: AsyncConnectionPool, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                UPDATE order
                SET order_confirmed = true
                WHERE id=%s
                ;
                """,
                (order_id,),
            )


async def db_set_order_archived_and_shiped(cnx: AsyncConnectionPool, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                UPDATE order
                SET order_archived = true
                WHERE id=%s
                ;
                """,
                (order_id,),
            )


async def db_remove_order(cnx: AsyncConnectionPool, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                DELETE FROM costumer_order
                WHERE id=%s
                ;
                """,
                (order_id,),
            )
