from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool


async def update_wilaya_shipping_cost(
    cnx: AsyncConnectionPool, desk_price, home_price, active, id
):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    UPDATE shipping_cost SET desk_price=%s , home_price=%s , active=%s WHERE id=%s;
                 """,
                (
                    desk_price,
                    home_price,
                    active,
                    id,
                ),
            )


async def get_all_wilaya_shipping_cost(cnx: AsyncConnectionPool):

    async with cnx.connection() as cnx:
        async with cnx.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """--sql
                    SELECT * FROM shipping_cost WHERE active=true ;
                 """,
            )
            data = await cur.fetchall()
            return data
