import uuid
from .redis_rq import redis_queue, redis_conn
from .response_schemas import *


def get_process_id():
    pid = uuid.uuid1()
    return str(pid.hex)
