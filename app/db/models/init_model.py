"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

# replace sqlalchemy.url file alembic.ini to postgresql://postgres:123@localhost/dbname


Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration"

# apply all migrations
alembic upgrade head

# downgrade migration 
alembic downgrade -1

# history migrations
alembic history
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, SmallInteger

from sqlmodel import Field, SQLModel, text

from app.helpers.enum import CommonStatus


class InitModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: int = Field(
        default=CommonStatus.ACTIVE,
        description="INACTIVE = 0, ACTIVE = 1, PENDING = 2",
        nullable=False,
        index=True,
    )
    created_at: datetime = Field(nullable=False, default=datetime.now())
    updated_at: datetime = Field(
        nullable=False,
        default=datetime.now(),
    )
