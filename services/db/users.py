from sqlalchemy.orm import Session
from sqlalchemy import select, String

from models.models import User, Place, Tags
from schemas.places import PlaceBaseSchema
from schemas.users import CreateUserSchema


def create_user(session: Session, user: CreateUserSchema):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_place(session: Session, place: PlaceBaseSchema, tags):
    db_place = Place(**place.dict())
    for t in tags:
        tag = session.query(Tags).filter_by(id=t).first()
        db_place.tags.append(tag)
    session.add(db_place)
    session.commit()
    session.refresh(db_place)
    db_place.tags
    return db_place


def get_user(session: Session, phone: str):
    return session.query(User).filter(User.phone == phone).one()


def get_user_by_id(session: Session, id: int):
    return session.query(User).filter(User.id == id).one()


