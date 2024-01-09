# from loguru import logger
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from app.core import config
# from app.helpers.enum import Environment

# engine = create_engine(config.PG_URL, echo=config.ENV == Environment.DEVELOPMENT)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# Base.metadata.create_all(engine)


# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from app.core import config
from app.helpers.enum import Environment

engine = create_engine(config.PG_URL, echo=config.ENV == Environment.DEVELOPMENT)

SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
