import os

from dotenv import load_dotenv

load_dotenv()

ENV = str(os.getenv("ENV"))
APP_NAME = str(os.getenv("APP_NAME"))
APP_V1_STR = str(os.getenv("APP_V1_STR"))
# e.g ["https://localhost:8000"]
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS")
PORT = os.getenv("PORT")
# openssl rand -hex 32
SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
REDIS_URL = str(os.getenv("REDIS_URL"))
REDIS_HOST = str(os.getenv("REDIS_HOST"))
REDIS_PORT = int(os.getenv("REDIS_PORT"))
PG_DATABASE_NAME = str(os.getenv("PG_DATABASE_NAME"))
PG_URL = str(os.getenv("PG_URL"))
CACHE_TTL = int(os.getenv("CACHE_TTL"))
