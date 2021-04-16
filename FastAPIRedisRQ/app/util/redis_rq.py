import redis
import os
from rq import Queue
import sys

sys.path.append("..")
from conf import RedisSettings

# pool = redis.ConnectionPool(host=RedisSettings.HOST, port=RedisSettings.PORT,
#                             db=0)
pool = redis.ConnectionPool(host=os.getenv("REDIS_HOST", "127.0.0.1"),
                            port=os.getenv("REDIS_PORT", "6379"), db=0)
redis_conn = redis.Redis(connection_pool=pool)
redis_queue = Queue("test_job", connection=redis_conn, default_timeout=RedisSettings.REDIS_DEFAULT_TIMEOUT)
