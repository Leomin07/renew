from datetime import timedelta, datetime
from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager

# from app.modules.api_router import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from loguru import logger
import redis.asyncio as redis
from app.core import config
from app.apis.api_router import router


"""
Rate-limit read docs, please visit https://github.com/long2ice/fastapi-limiter
cron-job read docs, please visit https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/
"""


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url(config.REDIS_URL, encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(
    title=config.APP_NAME,
    openapi_url=f"{config.APP_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
