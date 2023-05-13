from typing import Optional, List, Dict, Annotated

from fastapi import APIRouter, UploadFile, File, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from sqlalchemy import update

import settings
from db_initializer import get_db
from models import models as user_model
from models.models import User, Place
from schemas.users import UserSchema, UserBaseSchema, UserOutSchema, TokenPayload, CreateUserSchema
from services.files import save_file_user
from services.db import users as user_db_services

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# reuseable_oauth = OAuth2PasswordBearer(
#     tokenUrl="/login",
#     scheme_name="JWT"
# )
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post('/signup', response_model=UserSchema)
def signup(
        payload: CreateUserSchema = Body(),
        session: Session = Depends(get_db)
):
    """Processes request to register user account."""
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


# def get_current_user(token: str = Depends(reuseable_oauth), session: Session = Depends(get_db)) -> UserOutSchema:
#     payload = jwt.decode(
#         token, settings.SECRET_KEY, algorithms=[ALGORITHM]
#     )
#     token_data = TokenPayload(**payload)
#     stmt = session.query(User).filter(User.phone == token_data.phone).all()
#     if stmt is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Could not find user",
#         )
#     return stmt


@router.post("/photo")
def upload_avatar(id: int = None, file: UploadFile = File(...), session: Session = Depends(get_db)):
    file_url = save_file_user(file)
    stmt = session.query(User).get(id)
    stmt.photo_user = file_url
    session.add(stmt)
    session.commit()
    return file_url


@router.post("/settings")
def edit_profile(id: int, phone: Optional[str], name: Optional[str],
                 surname: Optional[str], city: Optional[str],
                 session: Session = Depends(get_db)):
    stmt = session.query(User).get(id)
    if name is None:
        pass
    else:
        stmt.name = name
    if surname is None:
        pass
    else:
        stmt.surname = surname
    if phone is None:
        pass
    else:
        stmt.phone = phone
    if city is None:
        pass
    else:
        stmt.city = city
    session.add(stmt)
    session.commit()
    return {'Status: 200 OK'}


@router.post("/role")
def edit_role(id: int, role_id: int, session: Session = Depends(get_db)):
    stmt = session.query(User).get(id)
    stmt.role_id = role_id
    session.add(stmt)
    session.commit()
    return stmt


@router.get("/{id}", response_model=UserOutSchema)
def get_me(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    stmt = session.query(User).get(data["id"])
    return stmt


# @router.get("/")
# def get_place_user_id(token: Annotated[str, Depends(oauth2_scheme)],session: Session = Depends(get_db)):
#     data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#     stmt = session.query(Place).filter()
