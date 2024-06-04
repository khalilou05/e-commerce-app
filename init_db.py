import json
import time

import psycopg

from utils.pswdhash import hash_passwd

condata = "hostaddr=127.0.0.1 user=postgres password=khalil dbname=postgres"

cnx = psycopg.connect(conninfo=condata)


def create_DB_tables():
    time.sleep(20)
    with cnx.cursor() as cur:
        print("database table init ...")
        cur.execute(
            """

            CREATE TABLE "user"(

                id SERIAL PRIMARY KEY,
                user_name VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100) NOT NULL,
                password bytea NOT NULL
                
            );


            CREATE TABLE article(
            
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                reference VARCHAR(100) NOT NULL,
                description text ,
                price INT NOT NULL,
                quantity INT NOT NULL,
                published timestamp DEFAULT CURRENT_TIMESTAMP,
                free_shipping bool DEFAULT false

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
                wilaya varchar(15) NOT NULL,
                wilaya_code varchar(5) NOT NULL,
                desk_price int NOT NULL,
                home_price int NOT NULL,
                active boolean DEFAULT true
            );


            CREATE TABLE costumer_order(
            
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(30) NOT NULL,
                wilaya VARCHAR(15) NOT NULL,
                phone_number VARCHAR(10) NOT NULL,
                article_id int REFERENCES article(id) NOT NULL,
                home_dilevery boolean NOT NULL,
                quantity int DEFAULT 1,
                baladiya VARCHAR(20),
                order_date timestamp DEFAULT CURRENT_TIMESTAMP,
                confirmed_date timestamp ,
                status VARCHAR(15) DEFAULT 'none'

            );

            """
        )

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
