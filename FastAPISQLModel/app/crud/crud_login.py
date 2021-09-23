from sqlalchemy.orm import Session
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Any

# import sys
#
# sys.path.append("..")
from app.db import models, pagination,session_scope
from app.util import passutil, schemas
from app.logs import fastapi_logger
from app.crud import get_user,get_user_password


class CRUDLogin:

    def check_username_password(self, email: str, password: str) -> Any:
        """ Verify Password"""

        db_user_info = get_user_password(email=email)

        return passutil.verify_password(str(password),
                                        str(db_user_info.password))

    def check_active_session(self, session_id: str):
        """ check for active session """
        try:
            with session_scope() as db:
                statement = select(models.UsersLoginAttempt).where(
                    models.UsersLoginAttempt.session_id == session_id)
                results = db.exec(statement)
                data = results.one()
                return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("check_active_session")
            return None

    def login_user(self, user: schemas.UserLogIn, session_id: str) -> Any:
        """ Login Attempt Record """
        try:
            with session_scope() as db:
                db_session = models.UsersLoginAttempt(
                    email=user.email,
                    session_id=session_id,
                    ip_address=user.ip_address,
                    browser=user.browser,
                    status="logged_in")
                db.add(db_session)
                db.commit()
                db.refresh(db_session)
                return db_session
        except SQLAlchemyError as e:
            fastapi_logger.exception("login_user")
            return None

    def active_user(self, session_id: str) -> Any:
        """ check for active user"""
        try:
            with session_scope() as db:
                statement = select(models.UsersLoginAttempt).where(
                    models.UsersLoginAttempt.session_id == session_id)
                results = db.exec(statement)
                db_session = results.one()

                db_session.status = "active"
                db.add(db_session)
                db.commit()
                db.refresh(db_session)
                return db_session
        except SQLAlchemyError as e:
            fastapi_logger.exception("active_user")
            return None

    def logoff_user(self, session_id: str) -> Any:
        """ Logging off Record"""
        try:
            with session_scope() as db:
                statement = select(models.UsersLoginAttempt).where(
                    models.UsersLoginAttempt.session_id == session_id)
                results = db.exec(statement)
                db_session = results.one()

                db_session.status = "logged_off"
                db.add(db_session)
                db.commit()
                db.refresh(db_session)
                return db_session
        except SQLAlchemyError as e:
            fastapi_logger.exception("logoff_user")
            return None


crud_login = CRUDLogin()
