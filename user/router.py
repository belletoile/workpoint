from typing import Optional, List, Dict, Annotated

from fastapi import APIRouter, UploadFile, File, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import update

import settings
from db_initializer import get_db
from models import models as user_model
from models.models import User, Place, FavoritePlace, Ad
from schemas.users import UserSchema, UserBaseSchema, UserOutSchema, TokenPayload, CreateUserSchema, UserTwoBaseSchema, \
    CreateFavoritePlaceSchema
from services.files import save_file_user
from services.db import users as user_db_services

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post('/signup', response_model=UserSchema)
def signup(
        payload: CreateUserSchema = Body(),
        session: Session = Depends(get_db)
):
    """Processes request to register user account."""
    payload.photo_user = "https://storage.yandexcloud.net/photo-user/840393.png#"
    payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
    return user_db_services.create_user(session, user=payload)


@router.post('/login', response_model=Dict)
def login(payload: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_db)
          ):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email,
                phone number, name

    - password:
    """
    try:
        user: user_model.User = user_db_services.get_user(
            session=session, phone=payload.username
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )
    return user.generate_token()


@router.post("/photo")
def upload_avatar(token: Annotated[str, Depends(oauth2_scheme)], file: UploadFile = File(...),
                  session: Session = Depends(get_db)):
    file_url = save_file_user(file)
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(User).get(data["id"])
    stmt.photo_user = file_url
    session.add(stmt)
    session.commit()
    return file_url


@router.post("/settings")
def edit_profile(token: Annotated[str, Depends(oauth2_scheme)],
                 payload: UserTwoBaseSchema = Body(),
                 session: Session = Depends(get_db)
                 ):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    payload.id = data["id"]
    stmt = sqlalchemy_update(User).where(
        User.id == payload.id).values(**payload.dict())
    session.execute(stmt)
    session.commit()
    return {'Status: 200 OK'}


@router.post("/role")
def edit_role(token: Annotated[str, Depends(oauth2_scheme)], role_id: int, session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(User).get(data["id"])
    stmt.role_id = role_id
    session.add(stmt)
    session.commit()
    return stmt


@router.get("/current", response_model=UserOutSchema)
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(User).get(data["id"])
    return stmt


@router.get("/place")
def get_place_by_user_id(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(Place).filter(Place.user_id == data["id"]).all()
    return stmt


@router.post("/favorite_place")
def add_favorite_place(token: Annotated[str, Depends(oauth2_scheme)],
                       payload: CreateFavoritePlaceSchema = Body(),
                       session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    payload.user_id = data["id"]
    return user_db_services.create_favorite_place(session, favorite_place=payload)


@router.get("/my_favorite_places")
def get_favorite_place_by_user_id(token: Annotated[str, Depends(oauth2_scheme)],
                                  session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(FavoritePlace).filter(FavoritePlace.user_id == data["id"]).all()
    return stmt


@router.delete('/delete_favorite_place')
def delete_favorite_place(id_fav_place: int,
                          token: Annotated[str, Depends(oauth2_scheme)],
                          session: Session = Depends(get_db)):
    place = session.query(FavoritePlace).filter_by(id=id_fav_place).first()
    session.delete(place)
    session.commit()
    return {'ok'}


@router.get("/add")
def get_advertisement_by_user_id(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(Ad).filter(Ad.user_id == data["id"]).all()
    return stmt