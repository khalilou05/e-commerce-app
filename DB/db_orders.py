import datetime

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
    date: datetime.date | None = None,
    status: str | None = None,
):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            #! get all orders standar filternig
            if date == None and status == None:
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,o.order_date,
                o.home_dilevery,art.price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                WHERE o.status='none'
                OFFSET %s 
                LIMIT %s;"""
                data = (offset, limit)
                q1 = await cur.execute(sql, data)
                default = await q1.fetchall()
                return default
            #! not confirmed order date filtering
            if date:
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,o.order_date,
                o.home_dilevery,art.price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                WHERE o.status='none'
                OFFSET %s 
                LIMIT %s;"""
                data = (offset, limit)
                q1 = await cur.execute(sql, data)
                default = await q1.fetchall()
                return default

            #! get confirmed order
            if status == "confirmed" and date == None:
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,o.wilaya,o.baladiya,o.article_id,o.quantity,o.home_dilevery,art.id,art.price,o.confirmed_date
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
            #! confirmed order + date
            if status == "confirmed" and date:
                sql = """--sql 
                SELECT o.id,o.first_name,o.last_name,o.phone_number,o.wilaya,o.baladiya,o.article_id,o.quantity,o.home_dilevery,art.id,art.price,o.confirmed_date
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                WHERE status='confirmed'
                AND confirmed_date=%s
                OFFSET %s 
                LIMIT %s;
                """
                data = (offset, limit, date)
                q1 = await cur.execute(sql, data)
                date_filter = await q1.fetchall()
                return date_filter


async def db_set_order_confirmed(cnx: AsyncConnectionPool, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                UPDATE article SET quantity = quantity - 1 WHERE id = (SELECT article_id FROM costumer_order WHERE id=%s);
                """,
                (order_id,),
            )
            await cur.execute(
                """--sql
                UPDATE costumer_order
                SET status = 'confirmed',confirmed_date=CURRENT_TIMESTAMP
                WHERE id=%s
                ;
                """,
                (order_id,),
            )


async def db_count_all_roder(cnx: AsyncConnectionPool):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query1 = await cur.execute(
                """--sql
                SELECT count(*) FROM costumer_order WHERE status='confirmed'
                ;
                """,
            )
            confirmedOrder = await query1.fetchone()
            query2 = await cur.execute(
                """--sql
                    SELECT count(*) FROM costumer_order WHERE status='none' ;
                    """,
            )
            notConfirmedOrder = await query2.fetchone()
            query3 = await cur.execute(
                """--sql
                    SELECT count(*) FROM costumer_order ;
                    """,
            )
            all = await query3.fetchone()
            return {
                "all": all[0],
                "confirmed": confirmedOrder[0],
                "not_confirmed": notConfirmedOrder[0],
            }


async def db_remove_order(cnx: AsyncConnectionPool, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                DELETE FROM costumer_order
                WHERE id=%s
                ;
                """,
                (order_id,),
            )
