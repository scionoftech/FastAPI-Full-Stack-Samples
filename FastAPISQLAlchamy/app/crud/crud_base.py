from sqlalchemy.orm import Session
from sqlalchemy.orm import defer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import expression
from typing import Any
import sys

sys.path.append("..")
from db import models, pagination, session_scope
from logs import fastapi_logger


def get_user(email: str, db: Session) -> Any:
    """ Get User Data based on email"""
    try:
        data = db.query(models.User).filter(
            models.User.email == email).options(defer('password')).first()
        return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_user")
        return None


def get_active_user(email: str, db: Session) -> Any:
    """ Get User Data based on email and active status"""
    try:
        data = db.query(models.User).filter(
            models.User.email == email,
            models.User.is_active == expression.true()).options(
            defer('password')).first()
        return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_user")
        return None
