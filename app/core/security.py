from datetime import datetime, timedelta
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import and_

from app.core import config
from app.db.init_db import get_db
from app.db.models import member_model
from app.helpers.enum import CommonStatus, ErrorMessage, TokenType


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "exp": expire,
            "token_type": TokenType.ACCESS_TOKEN,
            "iat": datetime.utcnow(),
        }
    )
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, config.ALGORITHM)

    return encoded_jwt


def generate_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "exp": expire,
            "token_type": TokenType.REFRESH_TOKEN,
            "iat": datetime.utcnow(),
        }
    )

    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, config.ALGORITHM)

    return encoded_jwt


def verify_refresh_access(token: str, credentials_exception):
    try:
        payload: Any = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        token_type: TokenType = payload.get("token_type")
        # checking token expire
        if (
            datetime.strptime(payload.get("exp"), "%Y-%m-%d %H:%M:%S")
            < datetime.utcnow()
        ):
            raise HTTPException(
                detail=ErrorMessage.Token_Expire,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if token_type != TokenType.REFRESH_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.Unauthorized,
            )

    except JWTError as e:
        logger.error(e)
        raise credentials_exception

    return True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(non_hashed_pass, hashed_pass):
    return pwd_context.verify(non_hashed_pass, hashed_pass)


def verify_token_access(token: str, credentials_exception):
    try:
        payload: Any = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        token_type: TokenType = payload.get("token_type")
        # checking token expire
        if datetime.strptime(payload.get("exp")) < datetime.utcnow():
            raise HTTPException(
                detail=ErrorMessage.Token_Expire,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if token_type != TokenType.ACCESS_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorMessage.Unauthorized,
            )

    except JWTError as e:
        logger.error(e)
        raise credentials_exception

    return True


async def get_current_user(token: str):
    return token
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])

        if payload.get("token_type") != TokenType.ACCESS_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token not supported"
            )

        return payload
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired",
        )
