import json
from datetime import date
from enum import Enum

from pydantic import BaseModel, EmailStr


class Price(str, Enum):
    one_day = "На 1 день"
    one_week = "На 7 дней"


class Status(str, Enum):
    on_check = "На проверке"
    approved = "Одобрено"
    refused = "Отказано"


class AdBaseSchema(BaseModel):
    user_id: int
    name: str
    city: str
    address: str
    tariff: Price
    email: EmailStr
    status: Status
    id_place: int
    date_to: date
    date_from: date
    photo: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AdSchema(AdBaseSchema):
    id: int

    class Config:
        orm_mode = True


class AdListSchema(BaseModel):
    name: str
    city: str
    address: str
    price: Price
    email: str
    user_name: str
