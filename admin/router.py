from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import update as sqlalchemy_update, select

import jwt

import settings
from db_initializer import get_db
from models.models import *
from schemas.places import Status

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post("/check_place", response_model=None)
def changed_status_place(id_place: int,
                         status_place: Status,
                         token: Annotated[str, Depends(oauth2_scheme)],
                         session: Session = Depends(get_db), ):
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        stmt = session.query(User).get(data["id"])
        if stmt.role_id == 3:
            stmt = session.query(Place).filter_by(id=id_place).one()
            stmt.status = status_place
            session.add(stmt)
            session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Не хватает прав на выполнение действий"
            )
        return {f'The status has changed: {status_place}'}


@router.post("/check_ad", response_model=None)
def changed_status_advertisement(id_ad: int,
                         status_place: Status,
                         token: Annotated[str, Depends(oauth2_scheme)],
                         session: Session = Depends(get_db), ):
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        stmt = session.query(User).get(data["id"])
        if stmt.role_id == 3:
            stmt = session.query(Ad).filter_by(id=id_ad).one()
            stmt.status = status_place
            session.add(stmt)
            session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Не хватает прав на выполнение действий"
            )
        return {f'The status has changed: {status_place}'}


@router.delete("/delete_review")
def delete_reviews(id_review: int,
                   token: Annotated[str, Depends(oauth2_scheme)],
                   session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_stmt = session.query(User).get(data["id"])
    if user_stmt.role_id == 3:
        stmt = session.query(Reviews).filter_by(id=id_review).first()
        session.delete(stmt)
        session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не хватает прав на выполнение действий"
        )
    return {f'The review {id_review} has been deleted'}


@router.get("/users")
def get_all_users(token: Annotated[str, Depends(oauth2_scheme)],
                   session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_stmt = session.query(User).get(data["id"])
    if user_stmt.role_id == 3:
        stmt = session.query(User).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не хватает прав на выполнение действий"
        )
    return stmt


@router.put("/role")
def changed_role(user_id: int, role_id: int, token: Annotated[str, Depends(oauth2_scheme)],
                 session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_stmt = session.query(User).get(data["id"])
    if user_stmt.role_id == 3:
        stmt = session.query(User).get(user_id)
        stmt.role_id = role_id
        session.add(stmt)
        session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не хватает прав на выполнение действий"
        )
    return stmt