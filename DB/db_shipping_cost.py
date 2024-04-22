from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool


async def add_shipping_cost(cnx: AsyncConnectionPool, wilaya, desk_price, home_price):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    INSERT INTO shipping_cost 
                    (wilaya,desk_price,home_price)
                    VALUES (%s,%s,%s);
                 """,
                (wilaya, desk_price, home_price),
            )


async def get_wilaya_shipping_cost(cnx: AsyncConnectionPool, wilaya):

    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """--sql
                    SELECT desk_price,home_price FROM shipping_cost WHERE wilaya=%s;
                 """,
                (wilaya),
            )


async def arabic_wilaya(cnx: AsyncConnectionPool):

    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """--sql
                    SELECT id,ar_wilaya FROM shipping_cost;
                 """,
            )
            data = await cur.fetchall()
            return data


async def french_wilaya(cnx: AsyncConnectionPool):

    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """--sql
                    SELECT id,fr_wilaya FROM shipping_cost;
                 """,
            )
            data = await cur.fetchall()
            return data


async def update_wilaya_shipping_cost(
    cnx: AsyncConnectionPool, desk_price, home_price, wilaya
):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    UPDATE shipping_cost SET desk_price=%s AND home_price=%s WHERE wilaya=%s;
                 """,
                (desk_price, home_price, wilaya),
            )
            data = await cur.fetchall()
            return data


async def get_all_wilaya_shipping_cost(cnx: AsyncConnectionPool, wilaya):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    SELECT * FROM shipping_cost ;
                 """,
                (wilaya),
            )


async def remove_wilaya(cnx: AsyncConnectionPool, wilaya):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    DELETE FROM shipping_cost WHERE wilaya=%s;
                 """,
                (wilaya),
            )
