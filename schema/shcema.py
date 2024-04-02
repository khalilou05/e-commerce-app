from pydantic import BaseModel


class Article_schema(BaseModel):
    title: str
    description: str | None = None
    price: int


class Order(BaseModel):
    article_id: int
    first_name: str
    last_name: str
    phone_numer: int
    wilaya: str
    quantity: int
    home_dilevery: bool = False


class login_data(BaseModel):
    username: str
    password: str
