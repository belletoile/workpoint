from fastapi import APIRouter, UploadFile, File, Depends, Body
from sqlalchemy.orm import Session

from db_initializer import get_db
from models.models import Ad, Place
from schemas.ad import AdBaseSchema
from services.files import save_file_ad
from services.db import ad as ad_db_services

router = APIRouter(
    prefix="/ad",
    tags=["Ad"]
)


@router.get("/all_ad")
def get_all_advertisement(session: Session = Depends(get_db)):
    return session.query(Ad).all()


@router.post("/upload_ad", response_model=AdBaseSchema)
def upload_advertisement(payload: AdBaseSchema = Body(), file: UploadFile = File(...), session: Session = Depends(get_db)):
    payload.photo = save_file_ad(file)
    stmt = session.query(Place.id).filter_by(name=payload.name, address=payload.address).first()
    payload.id_place = stmt.id
    return ad_db_services.create_ad(session=session, ad=payload)


@router.post("/count_ad")
def check_count_advertisement(date_to: str, date_from: str, session: Session = Depends(get_db)):
    stmt = session.query(Ad).filter_by(date_to=date_to, date_from=date_from).count()
    if stmt < 5:
        return True
    else:
        return False
