from mongoengine.queryset.visitor import Q
from typing import Any
import sys

sys.path.append("..")
from db import User
from logs import fastapi_logger


def get_password(email: str) -> Any:
    """ Get User Data based on email"""
    try:
        # this will extract user data by excluding password
        data = User.objects(email=email).only('password').first()
        return data
    except Exception as e:
        fastapi_logger.exception("get_user")
        return None


def get_user(email: str) -> Any:
    """ Get User Data based on email"""
    try:
        # this will extract user data by excluding password
        data = User.objects(email=email).exclude('password').first()
        return data
    except Exception as e:
        fastapi_logger.exception("get_user")
        return None


def get_active_user(email: str) -> Any:
    """ Get User Data based on email and active status"""
    try:
        # this will for check active user and returns data by excluding password
        # data = User.objects(Q(email=email) & Q(is_active=True)).exclude(
        #     'password').first()
        data = User.objects(Q(email=email) & Q(is_active=True)).fields(
            password=0).first()
        return data
    except Exception as e:
        fastapi_logger.exception("get_user")
        return None