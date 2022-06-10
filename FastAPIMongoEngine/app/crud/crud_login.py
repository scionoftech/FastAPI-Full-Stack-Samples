from typing import Any

import sys

sys.path.append("..")
from db import User, UsersLoginAttempt
from util import passutil, schemas, get_json
from logs import fastapi_logger
from crud import get_password


class CRUDLogin:

    def check_username_password(self, email: str, password: str) -> Any:
        """ Verify Password"""
        db_user_info = get_password(email=email)

        return passutil.verify_password(str(password),
                                        str(db_user_info.password))

    def check_active_session(self, session_id: str):
        """ check for active session """
        try:
            db_session = UsersLoginAttempt.objects(
                session_id=session_id).first()
            return db_session
        except Exception as e:
            fastapi_logger.exception("logoff_user")
            return None

    def login_user(self, user: schemas.UserLogIn, session_id: str) -> Any:
        """ Login Attempt Record """
        try:
            db_session = UsersLoginAttempt(
                email=user.email,
                session_id=session_id,
                ip_address=user.ip_address,
                browser=user.browser,
                status="logged_in")
            db_session.save()
            return db_session
        except Exception as e:
            fastapi_logger.exception("login_user")
            return None

    def active_user(self, session_id: str) -> Any:
        """ check for active user"""
        try:
            db_session = UsersLoginAttempt.objects(
                session_id=session_id).first()
            db_session.status = "active"
            db_session.save()
            return db_session
        except Exception as e:
            fastapi_logger.exception("active_user")
            return None

    def logoff_user(self, session_id: str) -> Any:
        """ Logging off Record"""
        try:
            db_session = UsersLoginAttempt.objects(
                session_id=session_id).first()

            db_session.status = "logged_off"
            db_session.save()
            return db_session
        except Exception as e:
            fastapi_logger.exception("logoff_user")
            return None


crud_login = CRUDLogin()
