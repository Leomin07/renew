from fastapi import APIRouter
from app.apis.deps import CurrentMember, SessionDep


from app.db.init_db import get_db
from app.apis.member import member_service
from app.db.models.member_model import Member

router = APIRouter()


@router.get("/me")
def get_profile(payload: CurrentMember, session: SessionDep):
    return member_service.get_profile(session, payload["member_id"])
