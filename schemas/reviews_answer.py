import json

from pydantic import BaseModel
from pydantic.dataclasses import ConfigDict


class ReviewAnswerBaseSchema(BaseModel):
    user_id: int
    review_id: int
    user_name: str = None
    user_surname: str = None
    user_photo: str = None
    place_id: int
    body: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ReviewSchema(ReviewAnswerBaseSchema):
    id: int

    class Config:
        orm_mode = True
