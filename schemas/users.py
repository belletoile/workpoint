from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBaseSchema(BaseModel):
    phone: str
    name: str
    surname: str
    role_id: str
    photo_user: str = None


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    is_active: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True


class UserOutSchema(BaseModel):
    id: int
    phone: str
    name: str
    surname: str
    role_id: int
    photo_user: str
    city: Optional[str] = None

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    phone: str = Field(alias="phone")
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    name: str = None
    phone: str = None


class SystemUser(UserBaseSchema):
    password: str
