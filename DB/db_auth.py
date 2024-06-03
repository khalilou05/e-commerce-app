from psycopg_pool import AsyncConnectionPool

from schema.shcema import admin_data


async def db_get_login_info(cnx: AsyncConnectionPool, username: str):
    async with cnx.connection() as con, con.cursor() as cur:
        await cur.execute(
            """--sql
            SELECT id,user_name,password FROM "user" 
            WHERE user_name=%s;
            """,
            (username,),
        )
        exist = True
        data = await cur.fetchone()
        if data is None:
            exist = False
        return (exist, data)


async def db_change_admin_data(cnx: AsyncConnectionPool, data: admin_data):
    async with cnx.connection() as con, con.cursor() as cur:
        await cur.execute(
            """--sql
            UPDATE "user"
            SET user_name = %s,
            email = %s,
            password = %s
            WHERE id=1;
            """,
            (data.username, data.password, data.email),
        )
