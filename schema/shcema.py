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
    reference: str | None = None
    desk_price: int | None = None
    home_price: int | None = None
    article_id: int | None = None
    confirmed_date: str | None = None
    shipping_date: str | None = None


class phoneNumber(BaseModel):
    phone_number: list[str]


class login_data(BaseModel):
    username: str
    password: str


class admin_data(BaseModel):
    username: str
    password: str
    email: str


class UpdateOrder(BaseModel):
    status: str
    orders: list[Order]
