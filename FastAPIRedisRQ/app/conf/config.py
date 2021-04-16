import json
import os
from pathlib import Path
from typing import Dict


def get_config() -> Dict:
    """ Get Config Json"""
    with open(str(Path(
            __file__).parent.parent) + os.sep + "conf" + os.sep + "conf.json",
              'r') as fp:
        return json.load(fp)


class ProjectSettings:
    """ Project Configuration"""
    __DATA = get_config()['PROJECT_CONF']
    PROJECT_NAME = __DATA["PROJECT_NAME"]
    PROJECT_DESCRIPTION = __DATA["PROJECT_DESCRIPTION"]
    API_VERSION = __DATA["API_VERSION"]
    API_VERSION_PATH = __DATA["API_VERSION_PATH"]
    SERVER_NAME = __DATA["SERVER_NAME"]
    SERVER_HOST = __DATA["SERVER_HOST"]
    BACKEND_CORS_ORIGINS = __DATA["BACKEND_CORS_ORIGINS"]


class RedisSettings:
    """ Redis Configuration"""
    __DATA = get_config()['REDIS_CONF']
    HOST = __DATA["HOST"]
    PORT = __DATA["PORT"]
    USER_NAME = __DATA["USER_NAME"]
    PASSWORD = __DATA["PASSWORD"]
    REDIS_DEFAULT_TIMEOUT = __DATA["REDIS_DEFAULT_TIMEOUT"]
    REDIS_JOB_TIMEOUT = __DATA["REDIS_JOB_TIMEOUT"]
