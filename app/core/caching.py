import redis

from app.core import config

redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


# ex = second, default 60 seconds
def set_cache(key, value, ttl: int | None = 60):
    redis_client.set(key, value, ex=ttl)


def get_cache(key):
    return redis_client.get(key)
