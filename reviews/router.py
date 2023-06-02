from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends

import settings
from db_initializer import get_db
from models.models import User
from schemas.reviews import ReviewBaseSchema
from services.db import reviews as rw_db_services

router = APIRouter(
    prefix="/review",
    tags=["review"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post('/add_review')
def add_review(token: Annotated[str, Depends(oauth2_scheme)], payload: ReviewBaseSchema = Body(),
               session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    payload.user_id = data["id"]
    stmt = session.query(User).get(data["id"])
    payload.user_name = stmt.name
    payload.user_surname = stmt.surname
    payload.user_photo = stmt.photo_user
    return rw_db_services.create_rw(session=session, reviews=payload)
