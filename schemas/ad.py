from pydantic import BaseModel


class AdBaseSchema(BaseModel):
    photo: str


class AdSchema(AdBaseSchema):
    id: int

    class Config:
        orm_mode = True
