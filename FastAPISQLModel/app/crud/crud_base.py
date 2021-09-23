from sqlmodel import select
from sqlalchemy.sql import expression
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import defer
from typing import Any
from app.db import models, pagination, session_scope
from app.logs import fastapi_logger


def get_user(email: str) -> Any:
    """ Get User Data based on email"""
    try:
        with session_scope() as db:
            statement = select(models.User).where(
                models.User.email == email).options(defer('password'))
            results = db.exec(statement)
            data = results.one()
            return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_user")
        return None

def get_user_password(email: str) -> Any:
    """ Get User Password based on email"""
    try:
        with session_scope() as db:
            statement = select(models.User).where(
                models.User.email == email)
            results = db.exec(statement)
            data = results.one()
            return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_user")
        return None

def get_active_user(email: str) -> Any:
    """ Get User Data based on email and active status"""
    try:
        with session_scope() as db:
            statement = select(models.User).where(
                models.User.email == email).where(
                models.User.is_active == expression.true()).options(defer('password'))
            results = db.exec(statement)
            data = results.one()
            return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_user")
        return None
