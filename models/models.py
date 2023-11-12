from datetime import datetime
from typing import Dict, Any, Annotated

import bcrypt
import jwt
from fastapi import Depends
from sqlalchemy import (
    LargeBinary,
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    PrimaryKeyConstraint, ForeignKey, JSON, ARRAY, Enum, TIMESTAMP, Date
)
import enum
# This is a special import for ENUM strictly because I am using postgres DB
# from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import mapped_column, relationship

import settings
from db_initializer import Base


class FavoritePlace(Base):
    __tablename__ = "favoriteplace"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_id = Column(Integer, ForeignKey("place.id"))


class PlaceTags(Base):
    """Models a tags table"""
    __tablename__ = "placetags"
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    place_id = Column(Integer, ForeignKey("place.id"))


class Reviews(Base):
    """Models a reviews table"""
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_name = Column(String)
    user_surname = Column(String)
    user_photo = Column(String)
    place_id = Column(Integer, ForeignKey("place.id"))
    body = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    rank = Column(Integer)


class Tags(Base):
    """Models a tags table"""
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    place = relationship('Place', secondary="placetags", back_populates='tags')
    name = Column(String)


class Ad(Base):
    __tablename__ = "ad"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    address = Column(String)
    tariff = Column(String)
    email = Column(String)
    status = Column(String)
    id_place = Column(Integer)
    date_to = Column(Date)
    date_from = Column(Date)
    photo = Column(String)


class Place(Base):
    """Models a place table"""
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    district = Column(String, nullable=False)
    address = Column(String, nullable=False)
    description = Column(String, nullable=False)
    opening_hours = Column(String)
    cost = Column(String)
    type_cafe = Column(String)
    company_phone = Column(String)
    email = Column(String)
    site = Column(String)
    photo = Column(String)
    rating = Column(String)
    parking = Column(Boolean, default=False)
    recreation_area = Column(Boolean, default=False)
    conference_hall = Column(Boolean, default=False)
    tags = relationship('Tags', secondary="placetags", back_populates='place')
    reviews = relationship('User', secondary="reviews", back_populates='reviews_user')
    favorite = relationship('User', secondary="favoriteplace", back_populates="fav_user")
    status = Column(String)


class Role(Base):
    """Models a role table"""
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class User(Base):
    """Models a user table"""
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    phone = Column(String, nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    city = Column(String)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"))
    is_active = Column(Boolean, default=False)
    photo_user = Column(String)
    reviews_user = relationship('Place', secondary="reviews", back_populates='reviews', cascade='all, delete')
    fav_user = relationship('Place', secondary="favoriteplace", back_populates="favorite", cascade='all, delete')


    UniqueConstraint("phone", name="uq_user_phone")
    PrimaryKeyConstraint("id", name="pk_user_id")

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {phone!r}>".format(phone=self.phone)

    @staticmethod
    def hash_password(password) -> bytes:
        """Transforms password from it's raw textual form to
        cryptographic hashes
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool:
        """Confirms password validity"""
        return bcrypt.checkpw(password.encode(), self.hashed_password)

    def generate_token(self) -> dict:
        """Generate access token for user"""
        return {
            "access_token": str(jwt.encode(
                {"name": self.name, "phone": self.phone, "id": self.id},
                settings.SECRET_KEY, algorithm="HS256"
            ))
        }


