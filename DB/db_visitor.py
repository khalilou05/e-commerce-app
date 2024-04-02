from psycopg_pool import AsyncConnectionPool


async def db_add_visitor_ip(cnx: AsyncConnectionPool, ip_addr: str):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                INSERT INTO visitor (ip_address)
                VALUES (%s)
                ;
                """,
                (ip_addr,),
            )


async def db_add_article_visitor(
    cnx: AsyncConnectionPool, ip_addr: str, article_viewed: int
):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                INSERT INTO visitor (ip_address, article_viewed)
                VALUES (%s,%s)
                ;
                """,
                (ip_addr, article_viewed),
            )


async def db_add_visitor_ip(cnx: AsyncConnectionPool, ip_addr: str):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                INSERT INTO visitor (ip_address)
                VALUES (%s)
                ;
                """,
                (ip_addr,),
            )


async def db_check_visitor_ip(cnx: AsyncConnectionPool, ip_addr: str):
    async with cnx.connection() as cnx:
        async with cnx.cursor() as cur:
            query = await cur.execute(
                """--sql
                SELECT * FROM visitor
                WHERE ip_address=%s
                ;
                """,
                (ip_addr,),
            )
            data = await query.rowcount
            if data == 1:
                return True
            return False
