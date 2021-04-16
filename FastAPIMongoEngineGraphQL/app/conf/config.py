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


class EmailSettings:
    """ Email Settings"""
    __DATA = get_config()['EMAIL_CONF']
    EMAIL_RESET_TOKEN_EXPIRE_HOURS = __DATA["EMAIL_RESET_TOKEN_EXPIRE_HOURS"]
    EMAIL_ID = __DATA["EMAIL_ID"]
    EMAIL_PASSWORD = __DATA["EMAIL_PASSWORD"]
    SMTP_SERVER = __DATA["SMTP_SERVER"]
    SMTP_PORT = __DATA["SMTP_PORT"]


class DBSettings:
    """ Database Configuration"""
    __DATA = get_config()['DATABASE_CONF']
    # 'postgres+psycopg2://USER:PASSWORD@localhost:5432/DATABASE'
    MONGODB_DATABASE_URL = f"{__DATA['DATABASE']}://{__DATA['MONGODB_USER']}" \
                              f":{__DATA['MONGODB_PASSWORD']}@" \
                              f"{__DATA['MONGODB_HOST']}:{__DATA['MONGODB_PORT']}/" \
                              f"{__DATA['MONGODB_DB_NAME']}?authSource={__DATA['MONGODB_DB_NAME']}"


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
    ACCESS_TOKEN_EXPIRE_MINUTES = __DATA["ACCESS_TOKEN_EXPIRE_MINUTES"]
    SESSION_TOKEN_EXPIRE_SECONDS = __DATA["SESSION_TOKEN_EXPIRE_SECONDS"]

