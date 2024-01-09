from datetime import datetime, timedelta
import time
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core import config
from app.helpers.enum import ErrorMessage, TokenType
import moment


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


def verify_refresh_access(token: str):
    try:
        payload: Any = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        token_type: TokenType = payload.get("token_type")
        if payload.get("exp") < time.time():
            raise HTTPException(
                detail=ErrorMessage.Token_Expire,
                status_code=status.HTTP_403_FORBIDDEN,
            )

        if token_type != TokenType.REFRESH_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh toke in valid",
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token expired"
        )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(non_hashed_pass, hashed_pass):
    return pwd_context.verify(non_hashed_pass, hashed_pass)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.APP_V1_STR}/auth/login")


async def get_current_member(token: Annotated[str, Depends(oauth2_scheme)]):
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
