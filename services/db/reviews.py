from sqlalchemy.orm import Session

from models.models import Reviews, ReviewsAnswer
from schemas.reviews import ReviewBaseSchema
from schemas.reviews_answer import ReviewAnswerBaseSchema


def create_rw(session: Session, reviews: ReviewBaseSchema):
    db_rv = Reviews(**reviews.dict())
    session.add(db_rv)
    session.commit()
    session.refresh(db_rv)
    return db_rv


def create_rw_answer(session: Session, reviews: ReviewAnswerBaseSchema):
    db_rv_ans = ReviewsAnswer(**reviews.dict())
    session.add(db_rv_ans)
    session.commit()
    session.refresh(db_rv_ans)
    return db_rv_ans
