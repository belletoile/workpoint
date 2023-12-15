from typing import Any, Sequence, Optional, List, Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi_filter import FilterDepends
import jwt
from sqlalchemy import select, Row, or_, join
from sqlalchemy.orm import Session
from sqlalchemy import update as sqlalchemy_update
from fastapi import APIRouter, Depends, Body, UploadFile, File, HTTPException, status
from sqlalchemy import update

import settings
from models.models import Place, Tags, Reviews, PlaceTags, ReviewsAnswer

from db_initializer import get_db
from schemas.places import Hours, Cafe, PlaceSchema, PlaceBaseSchema, PlaceTwoBaseSchema
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


# @router.get("/")
# def get_places_filter(
#         parking: Optional[bool] = False,
#         recreation_area: Optional[bool] = False,
#         conference_hall: Optional[bool] = False,
#         type_cafe: Optional[Cafe] = None,
#         district: Optional[str] = None,
#         hours: Optional[Hours] = None,
#         session: Session = Depends(get_db),
# ):
#     queryset = session.query(Place)
#     return queryset.filter(or_(Place.district == district, Place.type_cafe == type_cafe,
#                                Place.parking == parking, Place.conference_hall == conference_hall,
#                                Place.recreation_area == recreation_area, Place.opening_hours == hours)).all()


@router.post('/upload_place')
def upload(token: Annotated[str, Depends(oauth2_scheme)], payload: PlaceBaseSchema = Body(),
           session: Session = Depends(get_db),
           files: List[UploadFile] = File(...)
           ):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        payload.user_id = data["id"]
        payload.rating = 0
        print(type(payload))
        payload.photo = ""
        for file in files:
            payload.photo = payload.photo + save_file_place(file) + "#"
            # str1 = save_file_place(file)
            # payload.photo = "".join(str1 + ", ")
        # payload.photo = [save_file_place(file) for file in files]
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


@router.get('/get_tags')
def all_tags(session: Session = Depends(get_db)):
    return session.query(Tags).all()


@router.post('/get_place')
def get_place_by_id(id_place: int, session: Session = Depends(get_db)):
    # stmt = session.query(Reviews).filter(Reviews.place_id == id_place).all()
    stmt2 = session.query(Place).filter(Place.id == id_place).first()
    stmt2.tags
    # stmt3 = session.query(PlaceTags).filter(PlaceTags.place_id == id_place).all()
    # stmt + stmt2 + stmt3
    return stmt2


@router.post('/get_reviews')
def get_reviews_by_id_place(id_place: int, session: Session = Depends(get_db)):
    stmt = session.query(Reviews).filter(Reviews.place_id == id_place).all()
    return stmt


@router.post('/get_reviews_answer')
def get_reviews_answer_by_id_place(id_reviews: int, session: Session = Depends(get_db)):
    stmt = session.query(ReviewsAnswer).filter(Reviews.id == id_reviews).all()
    return stmt


@router.get('/all')
def all_places(session: Session = Depends(get_db)):
    return session.query(Place).all()


@router.post('/update')
def update_place(token: Annotated[str, Depends(oauth2_scheme)], payload: PlaceTwoBaseSchema = Body(),
                 session: Session = Depends(get_db)):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    payload.user_id = data["id"]
    stmt = sqlalchemy_update(Place).where(
        Place.id == payload.id).values(**payload.dict())
    session.execute(stmt)
    session.commit()
    return {'ok'}


@router.post('/update_photo')
def update_photo(id_place: int, token: Annotated[str, Depends(oauth2_scheme)], files: List[UploadFile] = File(...),
                 session: Session = Depends(get_db)):
    stmt = session.query(Place).get(id_place)
    test_list2 = stmt.photo.split('#')
    new_photo = ""
    for file in files:
        new_photo = new_photo + save_file_place(file) + "#"
    print(new_photo.split('#'))
    test_list1 = new_photo.split('#')

    temp1 = [ele for ele in test_list1 if ele not in test_list2]

    for i in range(len(temp1)):
        stmt.photo = stmt.photo + temp1[i] + '#'

    session.commit()
    return {'ok'}


@router.post('/update_tags')
def update_tags_place(id_place: int, tags: List[str], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    stmt = session.query(Place).filter_by(id=id_place).first()
    print(stmt.tags)
    stmt.tags = []
    for t in tags:
        tag = session.query(Tags).filter_by(id=t).first()
        stmt.tags.append(tag)
    session.commit()
    return stmt.tags


@router.delete('/delete')
def delete_place(id_place: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    place = session.query(Place).filter_by(id=id_place).first()
    session.delete(place)
    session.commit()
    return {'ok'}