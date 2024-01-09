from redis import Redis

from app.core import config

redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


def set_cache(key, value, ttl: int | None = 60):
    redis_client.set(key, value, ex=ttl)


def get_cache(key):
    return redis_client.get(key)
