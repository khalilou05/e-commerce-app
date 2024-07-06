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
                    full_name,
                    phone_number,
                    wilaya,
                    baladiya,
                    quantity,
                    home_dilevery)
                    VALUES (%s,%s,%s,%s,%s,%s,%s);
                 """,
                (
                    article_id,
                    costumer_order.full_name,
                    costumer_order.phone_number,
                    costumer_order.wilaya,
                    costumer_order.baladiya,
                    costumer_order.quantity,
                    costumer_order.home_dilevery,
                ),
            )
            await cur.execute(
                """--sql
                UPDATE article SET quantity = quantity - %s WHERE id =%s;
                """,
                (
                    costumer_order.quantity,
                    article_id,
                ),
            )


async def db_get_all_order(
    cnx: AsyncConnectionPool,
    status: str,
    offset,
    limit,
    date: datetime.date | None = None,
):
    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            #! get all orders standar filternig

            if status == "confirmed" and date:
                sql = """--sql 
                SELECT o.id,o.full_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,o.order_date,o.confirmed_date,
                o.home_dilevery,
                art.price,art.free_shipping,art.reference,s.wilaya,s.desk_price,s.home_price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                JOIN shipping_cost s
                ON o.wilaya=s.wilaya
                WHERE o.status=%s AND  o.confirmed_date=%s
                ORDER BY o.id
                OFFSET %s 
                LIMIT %s;"""
                data = (status, date, offset, limit)
                q1 = await cur.execute(sql, data)
                data = await q1.fetchall()
                return data
            if status == "confirmed" and date == None:
                sql = """--sql 
                SELECT o.id,o.full_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,o.order_date,o.confirmed_date,
                o.home_dilevery,art.price,art.free_shipping,art.reference,s.wilaya,s.desk_price,s.home_price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                JOIN shipping_cost s
                ON o.wilaya=s.wilaya
                WHERE o.status=%s 
                ORDER BY o.id
                OFFSET %s 
                LIMIT %s;"""
                data = (status, offset, limit)
                q1 = await cur.execute(sql, data)
                data = await q1.fetchall()
                return data
            if (status == "shipped" or status == "canceled") and date == None:
                sql = """--sql
                SELECT o.id,o.full_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,o.order_date,o.confirmed_date,o.shipping_date,
                o.home_dilevery,art.price,art.reference,art.free_shipping,s.wilaya,s.desk_price,s.home_price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                JOIN shipping_cost s
                ON o.wilaya=s.wilaya
                WHERE o.status=%s
                ORDER BY o.id
                OFFSET %s
                LIMIT %s;"""
                data = (status, offset, limit)
                q1 = await cur.execute(sql, data)
                data = await q1.fetchall()
                return data
            if (status == "shipped" or status == "canceled") and date:
                sql = """--sql
                SELECT o.id,o.full_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,o.order_date,o.confirmed_date,o.shipping_date,
                o.home_dilevery,art.price,art.free_shipping,art.reference,s.wilaya,s.desk_price,s.home_price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                JOIN shipping_cost s
                ON o.wilaya=s.wilaya
                WHERE o.status=%s AND o.shipping_date=%s
                ORDER BY o.id
                OFFSET %s
                LIMIT %s;"""
                data = (status, date, offset, limit)
                q1 = await cur.execute(sql, data)
                data = await q1.fetchall()
                return data
            if date == None and status:
                sql = """--sql
                SELECT o.id,o.full_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,o.order_date,
                o.home_dilevery,art.price,art.free_shipping,art.reference,s.wilaya,s.desk_price,s.home_price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                JOIN shipping_cost s
                ON o.wilaya=s.wilaya
                WHERE o.status=%s
                ORDER BY o.id
                OFFSET %s
                LIMIT %s;"""
                data = (status, offset, limit)
                q1 = await cur.execute(sql, data)
                data = await q1.fetchall()
                return data

            if status and date:

                sql = """--sql 
                SELECT o.id,o.full_name,o.phone_number,
                o.wilaya,o.baladiya,o.article_id,o.quantity,o.order_date,
                o.home_dilevery,art.price,art.free_shipping,art.reference,s.wilaya,s.desk_price,s.home_price
                FROM costumer_order o
                JOIN article art
                ON article_id=art.id
                JOIN shipping_cost s
                ON o.wilaya=s.wilaya
                WHERE o.status=%s AND  o.order_date=%s
                ORDER BY o.id
                OFFSET %s 
                LIMIT %s;"""
                data = (status, date, offset, limit)
                q1 = await cur.execute(sql, data)
                data = await q1.fetchall()
                return data


async def db_update_and_confirm_order(cnx: AsyncConnectionPool, order: Order):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                UPDATE costumer_order
                SET full_name=%s,
                wilaya=%s,
                baladiya=%s,
                home_dilevery=%s,
                phone_number=%s,
                status='confirmed',
                quantity=%s,
                confirmed_date=CURRENT_TIMESTAMP
                WHERE id=%s
                ;
                """,
                (
                    order.full_name,
                    order.wilaya,
                    order.baladiya,
                    order.home_dilevery,
                    order.phone_number,
                    order.quantity,
                    order.id,
                ),
            )


async def db_count_roders(cnx: AsyncConnectionPool, status: str):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                SELECT count(*) FROM costumer_order WHERE status=%s
                ;
                """,
                (status,),
            )

            data = await query.fetchone()
            return data[0]


async def db_remove_order(
    cnx: AsyncConnectionPool, order_id: int, article_id: int, quantity: int
):
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
            await cur.execute(
                """--sql
                UPDATE article SET quantity = quantity + %s WHERE id =%s;
                """,
                (quantity, article_id),
            )


async def db_order_change_status(cnx: AsyncConnectionPool, status: str, order_id: int):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:

            sql = "UPDATE costumer_order SET status=%s WHERE id=%s"

            data = (status, order_id)
            if status == "shipped":
                sql = "UPDATE costumer_order SET status=%s, shipping_date=CURRENT_DATE WHERE id=%s"
            await cur.execute(sql, data)
