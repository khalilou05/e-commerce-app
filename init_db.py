import psycopg

from utils.pswdhash import hash_passwd

cnx = psycopg.connect("dbname=djamel user=postgres password=khalil")


def init_db():
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
                phone_number INT NOT NULL,
                banned_date timestamp DEFAULT CURRENT_TIMESTAMP


            );


            CREATE TABLE visitor(

                id SERIAL PRIMARY KEY,
                ip_address varchar(100) NOT NULL,
                visit_date timestamp DEFAULT CURRENT_TIMESTAMP

            );


            CREATE TABLE costumer_order(
            
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                wilaya VARCHAR(100) NOT NULL,
                phone_number VARCHAR(50),
                article_order int REFERENCES article(id) NOT NULL,
                quantity int NOT NULL,
                purchase_date timestamp DEFAULT CURRENT_TIMESTAMP,
                delivery_date timestamp ,
                order_proceded boolean DEFAULT false

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


if __name__ == "__main__":
    init_db()
