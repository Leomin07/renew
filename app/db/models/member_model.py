from sqlalchemy import Column, SmallInteger, String, null
from sqlmodel import Field
from app.db.models.init_model import InitModel

from app.helpers.enum import Gender, RoleMember


class Member(InitModel, table=True):
    email: str = Field(unique=True, index=True, nullable=True, max_length=255)
    password: str = Field(nullable=True, max_length=255)
    phone: str = Field(unique=True, index=True, nullable=True, max_length=10)
    birthday: str = Field(index=True, nullable=True, description="Birthday")
    name: str = Field(index=True, description="Full name or name", max_length=255)
    refresh_token: str = Field(nullable=True, max_length=255)
    role_id: int = Field(
        default=RoleMember.MEMBER, description="Role id member", index=True
    )
    gender: int = Field(index=True, default=Gender.ALL, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False, max_length=255)
