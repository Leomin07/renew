from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.apis.deps import SessionDep
from app.db.init_db import get_db

from app.apis.auth import auth_service
from app.apis.auth.auth_schema import (
    refresh_token_schema,
    register_schema,
)


router = APIRouter()


# @router.post("/register", status_code=status.HTTP_201_CREATED)
# def register(params: register_schema, session: Session = Depends(get_db)):
#     return auth_service.register(session, params)


# @router.post("/login", status_code=status.HTTP_200_OK)
# def login(
#     session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     return auth_service.login(session, form_data)


# @router.post("/refresh-token", status_code=status.HTTP_200_OK)
# def refresh_token(
#     params: refresh_token_schema,
#     session: Session = Depends(get_db),
# ):
#     return auth_service.refresh_token(params, session)
