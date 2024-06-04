import json
import time

import psycopg

from utils.pswdhash import hash_passwd

condata = "hostaddr=127.0.0.1 user=postgres password=khalil dbname=postgres"

cnx = psycopg.connect(conninfo=condata)


def create_DB_tables():

    with cnx.cursor() as cur:
        hashed_psswd = hash_passwd("admin")

        cur.execute(
            """--sql
                    
                INSERT INTO "user" (user_name,email,password) VALUES (%s,%s,%s)  ; 
            """,
            ("admin", "email@domain.com", hashed_psswd),
        )

        with open("./wilaya_dz3.json", "r") as file:
            wilaya_list = json.load(file)

        for item in wilaya_list:

            cur.execute(
                """--sql
                        
                    INSERT INTO shipping_cost (wilaya,wilaya_code,desk_price,home_price) VALUES (%s,%s,%s,%s)  ; 
                """,
                (item["arabicName"], item["wilaya_code"], 0, 0),
            )


if __name__ == "__main__":
    create_DB_tables()
