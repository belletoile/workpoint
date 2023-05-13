from typing import Any, Sequence, Optional, List, Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi_filter import FilterDepends
import jwt
from sqlalchemy import select, Row, or_, join
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body, UploadFile, File, HTTPException, status

import settings
from models.models import Place, Tags, Reviews, PlaceTags

from db_initializer import get_db
from schemas.places import Hours, Cafe, PlaceSchema, PlaceBaseSchema
from services.files import save_file_place
from services.db import users as user_db_services

from enum import Enum
from typing import List
from fastapi import Query

router = APIRouter(
    prefix="/places",
    tags=["Place"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/")
def get_places_filter(
        parking: Optional[bool] = False,
        recreation_area: Optional[bool] = False,
        conference_hall: Optional[bool] = False,
        type_cafe: Optional[Cafe] = None,
        district: Optional[str] = None,
        hours: Optional[Hours] = None,
        session: Session = Depends(get_db),
):
    queryset = session.query(Place)
    return queryset.filter(or_(Place.district == district, Place.type_cafe == type_cafe,
                               Place.parking == parking, Place.conference_hall == conference_hall,
                               Place.recreation_area == recreation_area, Place.opening_hours == hours)).all()


@router.post('/upload_place')
def upload(token: Annotated[str, Depends(oauth2_scheme)], payload: PlaceBaseSchema = Body(),
           session: Session = Depends(get_db),
           files: List[UploadFile] = File(...)
           ):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        payload.user_id = data["id"]
        payload.photo = [save_file_place(file) for file in files]
        tags = payload.tags
        payload.tags = []
        # for i in payload.tags:
        # tags = session.query(Tags).filter(Tags.id.in_(payload.tags)).all()
        # print(type(tags[0]))
        # print(session.query(Tags.name).filter(Tags.id.in_(payload.tags).all()))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="сорри"
        )
    return user_db_services.create_place(session, place=payload, tags=tags)


@router.post('/get_tags')
def add(session: Session = Depends(get_db)):
    return session.query(Tags).all()


@router.post('/get_place')
def get_place(id_place: int, session: Session = Depends(get_db)):
    stmt = session.query(Reviews).filter(Reviews.place_id == id_place).all()
    stmt2 = session.query(Place).filter(Place.id == id_place).all()
    stmt3 = session.query(Tags).filter(Tags.id == id_place).all()
    return stmt + stmt2 + stmt3


