from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Annotated, List, Optional, Union, Any

import fastapi
import uvicorn
from fastapi import Body, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# from db_initializer import get_async_session
import settings
from db_initializer import get_db
from models import models as user_model
# from models import users as link_model
from models.models import Place, User
# from models import places as place_model
from schemas.places import PlaceBaseSchema, PlaceSchema
from schemas.users import CreateUserSchema, UserSchema, UserLoginSchema, SystemUser, TokenPayload, \
    UserBaseSchema, UserOutSchema
from services.db import users as user_db_services
from services.db.users import get_user
from services.files import save_file_user

from places.router import router as router_places
from user.router import router as router_user
from ad.router import router as router_ad
from reviews.router import router as router_review

app = fastapi.FastAPI()

origins = [
    "*",
    "localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(router_places)
app.include_router(router_user)
app.include_router(router_ad)
app.include_router(router_review)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
