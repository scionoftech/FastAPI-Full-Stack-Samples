import os
from typing import Dict
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the .env file
load_dotenv(dotenv_path=f"{str(Path(__file__).parent.parent.parent.absolute())}{os.sep}.env")

def get_config() -> Dict:
    """ Get Config Json"""
    # Access the entire environment dictionary
    env_variables = os.environ
    env_data = {}
    # Loop through and print all environment variables and their values
    for key, value in env_variables.items():
        env_data[key] = value
    return env_data


class EmailSettings:
    """ Email Settings"""
    __DATA = get_config()
    EMAIL_RESET_TOKEN_EXPIRE_HOURS = __DATA[
        "EMAIL_RESET_TOKEN_EXPIRE_HOURS"]
    EMAIL_ID = __DATA["EMAIL_ID"]
    EMAIL_PASSWORD = __DATA["EMAIL_PASSWORD"]
    SMTP_SERVER = __DATA["SMTP_SERVER"]
    SMTP_PORT = __DATA["SMTP_PORT"]


class DBSettings:
    """ Database Configuration"""
    __DATA = get_config()
    # 'postgres+psycopg2://USER:PASSWORD@localhost:5432/DATABASE'
    SQLALCHEMY_DATABASE_URL = __DATA["DATABASE"] + '+' + __DATA[
        "DB_ADAPTER"] + '://' + \
                              __DATA["DB_USER"] + ':' + __DATA[
                                  "DB_PASSWORD"] + '@' + __DATA[
                                  "DB_SERVER"] + ':' + \
                              __DATA["DB_PORT"] + '/' + __DATA[
                                  "DB_DB"]

class DBSettingsMigration:
    """ Database Configuration"""
    __DATA = get_config()
    # 'postgres+psycopg2://USER:PASSWORD@localhost:5432/DATABASE'
    SQLALCHEMY_DATABASE_URL = __DATA["DATABASE"] + '+' + __DATA[
        "DB_MIGRATION_ADAPTER"] + '://' + \
                              __DATA["DB_USER"] + ':' + __DATA[
                                  "DB_PASSWORD"] + '@' + __DATA[
                                  "DB_SERVER"] + ':' + \
                              __DATA["DB_PORT"] + '/' + __DATA[
                                  "DB_DB"]
class ProjectSettings:
    """ Project Configuration"""
    __DATA = get_config()
    PROJECT_NAME = __DATA["PROJECT_NAME"]
    PROJECT_DESCRIPTION = __DATA["PROJECT_DESCRIPTION"]
    API_VERSION = __DATA["API_VERSION"]
    API_VERSION_PATH = __DATA["API_VERSION_PATH"]
    SERVER_NAME = __DATA["SERVER_NAME"]
    SERVER_HOST = __DATA["SERVER_HOST"]
    BACKEND_CORS_ORIGINS = __DATA["BACKEND_CORS_ORIGINS"]
    ACCESS_TOKEN_EXPIRE_MINUTES = __DATA[
        "ACCESS_TOKEN_EXPIRE_MINUTES"]
    SESSION_TOKEN_EXPIRE_SECONDS = __DATA[
        "SESSION_TOKEN_EXPIRE_SECONDS"]
