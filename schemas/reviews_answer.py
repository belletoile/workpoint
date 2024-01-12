from pydantic import BaseModel


class ReviewAnswerBaseSchema(BaseModel):
    user_id: int
    review_id: int
    user_name: str = None
    user_surname: str = None
    user_photo: str = None
    place_id: int
    body: str


class ReviewSchema(ReviewAnswerBaseSchema):
    id: int

    class Config:
        orm_mode = True
