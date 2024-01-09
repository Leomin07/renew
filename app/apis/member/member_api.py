from typing import Annotated
from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from app.apis.deps import CurrentUser, SessionDep
from app.core import config
from app.core.security import get_current_user


from app.db.init_db import get_db
from app.apis.member import member_service
from app.db.models.member_model import Member

router = APIRouter()


@router.get("/me")
def get_profile(payload: Annotated[str, Header()], session: SessionDep):
    # return member_service.get_profile(session, payload["member_id"])
    return payload
