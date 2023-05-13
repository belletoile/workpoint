from pydantic import BaseModel


class ReviewBaseSchema(BaseModel):
    user_id: int
    place_id: int
    body: str
    rank: int


class ReviewSchema(ReviewBaseSchema):
    id: int

    class Config:
        orm_mode = True