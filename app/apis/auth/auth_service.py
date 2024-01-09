from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.core import config

from app.core.security import (
    generate_access_token,
    generate_refresh_token,
    hash_password,
    verify_password,
)
from app.db.models import member_model
from app.helpers.enum import CommonStatus, ErrorMessage, TokenType
from app.apis.auth.auth_schema import (
    login_schema,
    refresh_token_schema,
    register_schema,
)


def check_email_duplicate(email: str, db: Session):
    obj = (
        db.query(member_model.Member.id, member_model.Member.email)
        .filter_by(email=email)
        .first()
    )

    if obj:
        raise HTTPException(
            detail=ErrorMessage.Email_Already_Exist,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return


def generate_token(member_id: int):
    # generate_access_token
    access_token = generate_access_token(data={"member_id": member_id})
    # generate_refresh_token
    new_refresh_token = generate_refresh_token(data={"member_id": member_id})

    return {"access_token": access_token, "refresh_token": new_refresh_token}


def check_username(username: str, db: Session):
    member = (
        db.query(member_model.Member.id, member_model.Member.username)
        .filter_by(username=username)
        .first()
    )
    if member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessage.USERNAME_ALREADY,
        )

    return member


def register(db: Session, params: register_schema):
    check_username(params.username, db)
    check_email_duplicate(params.email, db)
    # hashed password
    params.password = hash_password(params.password)
    # create new Member
    new_member = member_model.Member(**params.dict())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    token = generate_token(int(new_member.id))

    db.query(member_model.Member).filter_by(id=new_member.id).update(
        {"refresh_token": token["refresh_token"]}
    )
    db.commit()

    return token


def login(db: Session, params: login_schema):
    member = (
        db.query(
            member_model.Member.id,
            member_model.Member.username,
            member_model.Member.status,
            member_model.Member.password,
        )
        .filter(
            and_(
                member_model.Member.username == params.username,
                member_model.Member.status == CommonStatus.ACTIVE,
            )
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            detail=ErrorMessage.Member_Not_Found,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not verify_password(params.password, member.password) == True:
        raise HTTPException(
            detail=ErrorMessage.Password_Not_Match,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    token = generate_token(int(member.id))

    db.query(member_model.Member).filter_by(id=member.id).update(
        {"refresh_token": token["refresh_token"]}
    )
    db.commit()

    return token


def refresh_token(params: refresh_token_schema, db: Session):
    member = (
        db.query(member_model.Member.id, member_model.Member.refresh_token)
        .where(member_model.Member.refresh_token == params.refresh_token)
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is expired",
        )

    token = generate_token(int(member.id))

    db.query(member_model.Member).filter_by(id=member.id).update(
        {"refresh_token": token["refresh_token"]}
    )
    db.commit()

    return token
