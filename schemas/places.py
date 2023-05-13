import enum
import json

from fastapi import Depends
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select, Row

from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from typing import Optional, Any, Sequence
from fastapi_filter import FilterDepends
from sqlalchemy.engine.result import _TP
from sqlalchemy.orm import Session

from db_initializer import get_db
from models.models import Place


class Hours(str, Enum):
    constantly = "Круглосуточно"
    on_weekdays = "По будням"


class Cost(str, Enum):
    free = "Бесплатно"
    paid = "Платно"


class Cafe(str, Enum):
    cafe = "Кафе"
    anti_cafe = "Антикафе"
    working_hall = "Рабочий зал"


class PlaceBaseSchema(BaseModel):
    user_id: int
    name: str
    city: str
    district: str
    address: str
    description: str
    opening_hours: Hours
    cost: Cost
    type_cafe: Cafe
    company_phone: str
    email: str
    site: str
    photo: str
    parking: bool
    recreation_area: bool
    conference_hall: bool
    tags: list

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class PlaceSchema(PlaceBaseSchema):
    id: int

    class Config:
        orm_mode = True


class LinkBaseSchema(BaseModel):
    pass


class LinkSchema(LinkBaseSchema):
    id: int

    class Config:
        orm_mode = True
