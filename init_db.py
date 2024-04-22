import json

import psycopg

from settings import db_name, db_pass, db_user
from utils.pswdhash import hash_passwd

cnx = psycopg.connect(f"dbname={db_name} user={db_user} password={db_pass}")


def create_DB_tables():
    with cnx as cur:
        cur.execute(
            """

            CREATE TABLE "user"(

                id SERIAL PRIMARY KEY,
                user_name VARCHAR(100) UNIQUE NOT NULL,
                password bytea NOT NULL
                
            );


            CREATE TABLE article(
            
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description text ,
                price INT NOT NULL,
                quantity INT NOT NULL,
                published timestamp DEFAULT CURRENT_TIMESTAMP

            );

            CREATE TABLE img_url(

                id SERIAL PRIMARY KEY,
                article_id int REFERENCES article(id) ON DELETE CASCADE NOT NULL,
                img_url VARCHAR(200) NOT NULL,
                img_number int NOT NULL

            );

            CREATE TABLE black_list(

                id SERIAL PRIMARY KEY,
                phone_number varchar(10) NOT NULL,
                banned_date timestamp DEFAULT CURRENT_TIMESTAMP


            );


            CREATE TABLE visitor(

                id SERIAL PRIMARY KEY,
                ip_address varchar(30) NOT NULL,
                article_viewed int REFERENCES article(id),
                visit_date timestamp DEFAULT CURRENT_TIMESTAMP

            );

            CREATE TABLE shipping_cost(

                id SERIAL PRIMARY KEY,
                fr_wilaya varchar(30) NOT NULL,
                ar_wilaya varchar(30) NOT NULL,
                desk_price int NOT NULL,
                home_price int NOT NULL
            );


            CREATE TABLE costumer_order(
            
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(30) NOT NULL,
                last_name VARCHAR(30) NOT NULL,
                wilaya VARCHAR(15) NOT NULL,
                baladiya VARCHAR(30) NOT NULL,
                phone_number VARCHAR(10),
                article_id int REFERENCES article(id) NOT NULL,
                quantity int NOT NULL,
                home_dilevery boolean,
                order_date timestamp DEFAULT CURRENT_TIMESTAMP,
                confirmed_date timestamp ,
                status VARCHAR(15) DEFAULT 'none'

            );

            """
        )

        hashed_psswd = hash_passwd("admin")

        cur.execute(
            """--sql
                    
                INSERT INTO "user" (user_name,password) VALUES (%s,%s)  ; 
            """,
            ("admin", hashed_psswd),
        )

        with open("./wilaya_dz.json", "r") as file:
            wilaya_list = json.load(file)

        for item in wilaya_list:

            cur.execute(
                """--sql
                        
                    INSERT INTO shipping_cost (fr_wilaya,ar_wilaya,desk_price,home_price) VALUES (%s,%s,%s,%s)  ; 
                """,
                (item["frenchName"], item["arabicName"], 0, 0),
            )


if __name__ == "__main__":
    create_DB_tables()
