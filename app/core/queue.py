"""
https://python-rq.org/docs/

rq worker --with-scheduler
"""

from redis import Redis
from rq import Queue

from app.core import config

redis_conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

queue = Queue(connection=redis_conn)
