from pydantic import BaseModel


class Article_schema(BaseModel):
    title: str
    description: str | None = None
    price: int
    prev_price: int | None = None


class Order(BaseModel):
    article_id: int
    first_name: str
    last_name: str
    phone_numer: int
    wilaya: str
    quantity: int
    home_dilevery: bool = False
