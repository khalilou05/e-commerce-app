from pydantic import BaseModel


class Article_schema(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class Order(BaseModel):
    id: int | None = None
    full_name: str
    phone_number: str
    wilaya: str
    baladiya: str | None = None
    quantity: int | None = None
    home_dilevery: bool
    article_id: int


class phoneNumber(BaseModel):
    phone_number: list[str]


class login_data(BaseModel):
    username: str
    password: str
