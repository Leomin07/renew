from sqlalchemy import Column, SmallInteger, String, null
from app.db.models.init_model import InitModel

from app.helpers.enum import RoleMember


class Member(InitModel):
    __tablename__ = "member"

    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(
        String(255),
        nullable=True,
    )
    phone = Column(String(255), unique=True, index=True, nullable=True)
    birthday = Column(String(255), index=True, nullable=True, comment="Birthday")
    name = Column(String(255), index=True, comment="Full name or name")
    refresh_token = Column(String(255), nullable=True)
    role_id = Column(
        SmallInteger(), default=RoleMember.MEMBER, comment="Role id member", index=True
    )
    gender = Column(SmallInteger(), index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
