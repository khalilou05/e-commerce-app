from psycopg_pool import AsyncConnectionPool


async def db_get_login_info(cnx: AsyncConnectionPool, username: str):
    async with cnx.connection() as con, con.cursor() as cur:
        await cur.execute(
            """--sql
            SELECT id,user_name,password FROM "user" 
            WHERE user_name=%s;
            """,
            (username,),
        )

        return await cur.fetchone()


async def db_change_admin_passwd(cnx: AsyncConnectionPool, password: str | bytes):
    async with cnx.connection() as con, con.cursor() as cur:
        await cur.execute(
            """--sql
            UPDATE "user"
            SET password = %s
            WHERE id=1;
            """,
            (password,),
        )

        return await cur.fetchone()
