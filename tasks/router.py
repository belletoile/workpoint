from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Body
from fastapi.security import OAuth2PasswordBearer
import jwt

import settings
from schemas.ad import AdListSchema
from .tasks import send_email
from user.router import get_current_user

router = APIRouter(prefix="/report")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@router.post("/dashboard")
def get_report(token: Annotated[str, Depends(oauth2_scheme)],
               background_tasks: BackgroundTasks,
               payload: AdListSchema = Body()):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    payload.user_name = data['name']
    background_tasks.add_task(send_email, payload)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }
