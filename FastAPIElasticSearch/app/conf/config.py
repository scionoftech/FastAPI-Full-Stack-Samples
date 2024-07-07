import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(
    dotenv_path=f"{str(Path(__file__).parent.parent.parent.absolute())}{os.sep}.env")


def get_config() -> Dict:
    """ Get Config Json"""
    # Access the entire environment dictionary
    env_variables = os.environ
    env_data = {}
    # Loop through and print all environment variables and their values
    for key, value in env_variables.items():
        env_data[key] = value
    return env_data


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
    EMAIL_RESET_TOKEN_EXPIRE_HOURS = __DATA[
        "EMAIL_RESET_TOKEN_EXPIRE_HOURS"]
    EMAIL_ID = __DATA["EMAIL_ID"]
    EMAIL_PASSWORD = __DATA["EMAIL_PASSWORD"]
    SMTP_SERVER = __DATA["SMTP_SERVER"]
    SMTP_PORT = __DATA["SMTP_PORT"]
    ELASTICSEARCH_URL = __DATA["ELASTICSEARCH_URL"]
    ELASTICSEARCH_API_KEY = __DATA["ELASTICSEARCH_API_KEY"]
    ELASTICSEARCH_USER_NAME = __DATA["ELASTICSEARCH_USER_NAME"]
    ELASTICSEARCH_PWD = __DATA["ELASTICSEARCH_PWD"]
    COHERE_API_KEY = __DATA["COHERE_API_KEY"]
    APP_API_KEY = __DATA["APP_API_KEY"]


settings = ProjectSettings()
