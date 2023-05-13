from sqlalchemy.orm import Session

from models.models import Reviews
from schemas.reviews import ReviewBaseSchema


def create_rw(session: Session, reviews: ReviewBaseSchema):
    db_rv = Reviews(**reviews.dict())
    session.add(db_rv)
    session.commit()
    session.refresh(db_rv)
    return db_rv