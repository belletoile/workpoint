from enum import Enum

from pydantic import BaseModel


class AdBaseSchema(BaseModel):
    photo: str


class AdSchema(AdBaseSchema):
    id: int

    class Config:
        orm_mode = True


class Price(str, Enum):
    one_day = "На 1 день"
    one_week = "На 7 дней"


class AdListSchema(BaseModel):
    name: str
    city: str
    address: str
    price: Price
    email: str
    user_name: str
