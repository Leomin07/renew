from fastapi import APIRouter

from app.core import config
from app.apis.auth import auth_api
from app.apis.member import member_api

router = APIRouter()


router.include_router(
    auth_api.router, prefix=config.APP_V1_STR + "/auth", tags=["Auth"]
)

router.include_router(
    member_api.router, prefix=config.APP_V1_STR + "/member", tags=["Member"]
)
