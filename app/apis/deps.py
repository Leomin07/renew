from gc import get_debug
from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import Depends, Header
from app.core.security import get_current_user
from app.db.init_db import get_db

from app.db.models.member_model import Member


CurrentUser = Annotated[str, Header(), Depends(get_current_user)]

SessionDep = Annotated[Session, Depends(get_db)]
