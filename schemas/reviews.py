from pydantic import BaseModel


class ReviewBaseSchema(BaseModel):
    user_id: int
    user_name: str = None
    user_surname: str = None
    user_photo: str = None
    place_id: int
    body: str
    rank: int


class ReviewSchema(ReviewBaseSchema):
    id: int

    class Config:
        orm_mode = True