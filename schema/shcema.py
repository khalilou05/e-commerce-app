from pydantic import BaseModel


class Article_schema(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class Order(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    wilaya: str
    baladiya: str
    quantity: int
    home_dilevery: bool = False


class phoneNumber(BaseModel):
    phone_number: list[str]


class login_data(BaseModel):
    username: str
    password: str
