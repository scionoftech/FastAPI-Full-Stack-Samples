from app.conf.config import settings


def verify_api_key(api_key):
    return settings.APP_API_KEY == api_key
