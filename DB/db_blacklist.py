from psycopg_pool import AsyncConnectionPool


async def db_blacklist_add(cnx: AsyncConnectionPool, phone_number: int):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    INSERT INTO black_list (phone_number) VALUES (%s);
                 """,
                (phone_number,),
            )


async def db_blacklist_check(cnx: AsyncConnectionPool, phone_number: int):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    SELECT * FROM  black_list WHERE phone_number=%s;
                 """,
                (phone_number,),
            )
            data = await cur.rowcount
            if data == 0:
                return False
            return True


async def db_blacklist_remove(cnx: AsyncConnectionPool, phone_number: int):

    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            await cur.execute(
                """--sql
                    DELETE FROM black_list WHERE phone_number=%s;
                 """,
                (phone_number,),
            )
