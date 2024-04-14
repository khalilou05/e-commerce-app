from pydantic import BaseModel


class Article_schema(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class Order(BaseModel):
    first_name: str
    last_name: str
    phone_numer: str
    wilaya: str
    quantity: int
    home_dilevery: bool = False


class login_data(BaseModel):
    username: str
    password: str
