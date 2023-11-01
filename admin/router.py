
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import update as sqlalchemy_update

import jwt

import settings
from db_initializer import get_db
from models.models import *
from schemas.places import PlaceTwoBaseSchema

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post("/check_place")
def changed_status_place(token: Annotated[str, Depends(oauth2_scheme)],
                         payload: PlaceTwoBaseSchema = Body(),
                         session: Session = Depends(get_db), ):
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        stmt = session.query(User).get(data["id"])
        if stmt.role_id == 3:
                payload.user_id = data["id"]
                stmt = sqlalchemy_update(Place).where(
                    Place.id == payload.id).values(**payload.dict())
                session.execute(stmt)
                session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Не хватает прав на выполнение действий"
            )
        return {f'Status has changed: {payload.status}'}



