from gc import get_debug
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app.core.security import get_current_member
from app.db.init_db import get_db

from app.db.models.member_model import Member


CurrentMember = Annotated[Member, Depends(get_current_member)]

SessionDep = Annotated[Session, Depends(get_db)]
