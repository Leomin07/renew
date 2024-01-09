from fastapi import HTTPException, status

from sqlmodel import Session, select
from app.core import config
from sqlalchemy.orm import load_only
from app.core.security import (
    generate_access_token,
    generate_refresh_token,
    hash_password,
    verify_password,
    verify_refresh_access,
)
from app.db.models import member_model
from app.db.models.member_model import Member
from app.helpers.enum import CommonStatus, ErrorMessage, TokenType
from app.apis.auth.auth_schema import (
    login_schema,
    refresh_token_schema,
    register_schema,
)


def check_email_duplicate(email: str, db: Session):
    member = db.exec(
        select(Member)
        .options(load_only(Member.id, Member.email, Member.status))
        .where(Member.email == email)
    ).first()

    if member:
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
    member = db.exec(
        select(Member)
        .options(load_only(Member.id, Member.username, Member.status))
        .where(Member.username == username)
    ).first()
    if member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessage.USERNAME_ALREADY,
        )

    return


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

    # update refresh_token
    new_member.refresh_token = token["refresh_token"]
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return token


def login(db: Session, params: login_schema):
    member = db.exec(
        select(Member)
        .options(load_only(Member.id, Member.username, Member.status, Member.password))
        .where(
            Member.username == params.username,
        )
        .where(Member.status == CommonStatus.ACTIVE)
    ).first()

    if member is None:
        raise HTTPException(
            detail=ErrorMessage.Member_Not_Found,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if verify_password(params.password, member.password) != True:
        raise HTTPException(
            detail=ErrorMessage.Password_Not_Match,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    token = generate_token(int(member.id))

    member.refresh_token = token["refresh_token"]
    db.add(member)
    db.commit()
    db.refresh(member)

    return token


def refresh_token(params: refresh_token_schema, db: Session):
    payload = verify_refresh_access(params.refresh_token)

    member = db.exec(
        select(Member)
        .options(load_only(Member.id, Member.refresh_token))
        .where(Member.id == payload["member_id"])
    ).first()

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is expired",
        )

    if member.refresh_token != params.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token in valid"
        )

    token = generate_token(int(member.id))

    member.refresh_token = token["refresh_token"]
    db.add(member)
    db.commit()
    db.refresh(member)
    return token
