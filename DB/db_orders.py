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
                    quantity,
                    home_dilevery)
                    VALUES (%s,%s,%s,%s,%s,%s,%s);
                 """,
                (
                    article_id,
                    costumer_order.first_name,
                    costumer_order.last_name,
                    costumer_order.phone_numer,
                    costumer_order.wilaya,
                    costumer_order.quantity,
                    costumer_order.home_dilevery,
                ),
            )


async def db_get_all_order(
    cnx: AsyncConnectionPool,
    offset: int = 0,
    limit: int = 50,
    date: str | None = None,
    dilvred: bool | None = None,
):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            if date == None and dilvred == None:
                # get all orders standar filternig
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,
                o.wilaya,o.article_ordered,o.quantity,
                o.home_dilevery,art.id,art.price 
                FROM costumer_order o
                JOIN article art
                ON article_ordered=art.id
                OFFSET %s 
                LIMIT %s;"""
                data = (offset, limit)
                q1 = await cur.execute(sql, data)
                date_filter = await q1.fetchall()
                return date_filter
            # get orders filtering -> delivred + date
            if date and dilvred:
                sql = """--sql 
                SELECT id,first_name,last_name,phone_number,wilaya,article_ordered,quantity,home_dilevery,art.id,atr.price
                FROM order 
                JOIN article art
                ON article_ordered=art.id
                WHERE purchase_date=%s 
                and order_proceded=%s
                OFFSET %s 
                LIMIT %s;
                """
                data = (date, dilvred, offset, limit)
                q1 = await cur.execute(sql, data)
                date_filter = await q1.fetchall()
                return date_filter

            # get all orders with date filtering
            sql = """--sql 
            SELECT id,first_name,last_name,phone_number,wilaya,article_ordered,quantity,home_dilevery,art.id,atr.price
            FROM order 
            JOIN article art
            ON article_ordered=art.id
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


async def db_set_order_delivred(cnx: AsyncConnectionPool, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                UPDATE order
                SET order_proceded = true, delivery_date= CURRENT_TIMESTAMP
                WHERE id=%s
                ;
                """,
                (order_id,),
            )
            row = await query.rowcount
            if row == 1:
                return True
            return False


async def db_remove_order(cnx: AsyncConnectionPool, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                DELETE FROM order
                WHERE id=%s
                ;
                """,
                (order_id,),
            )
            row = await query.rowcount
            if row == 1:
                return True
            return False
