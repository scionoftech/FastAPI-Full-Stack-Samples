import uuid

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, insert, update, delete
from typing import Any
from fastapi.encoders import jsonable_encoder
from db import models, pagination, get_session
from app.util import passutil, schemas
import logging
from app.resolvers.crud_users import get_active_user


async def check_username_password(email: str, password: str) -> Any:
    """ Verify Password"""
    db_user_info = await get_active_user(email=email)

    return passutil.verify_password(str(password),
                                    str(db_user_info.password))


async def check_active_session(session_id: str):
    """ check for active session """
    try:
        async with get_session() as session:
            stmt = select(models.UsersLoginAttempt).filter(
                models.UsersLoginAttempt.session_id == session_id)

            db_login = (await session.execute(stmt)).first()

        return jsonable_encoder(db_login)["UsersLoginAttempt"]
    except SQLAlchemyError as e:
        logging.info("logoff_user")
        return None


async def login_user(user: schemas.UserLogIn, session_id: str) -> Any:
    """ Login Attempt Record """
    try:
        record_id = uuid.uuid4().hex
        async with get_session() as session:
            stmt = insert(models.UsersLoginAttempt).values(
                id=record_id,
                email=user.email,
                session_id=session_id,
                ip_address=user.ip_address,
                browser=user.browser,
                status="logged_in")
            await session.execute(stmt)

            stmt = select(models.UsersLoginAttempt).filter(
                id == record_id)
            results = (await session.execute(stmt)).first()
            await session.commit()

        return jsonable_encoder(results)["UsersLoginAttempt"]
    except SQLAlchemyError as e:
        logging.info("login_user")
        return None


async def active_user(session_id: str) -> Any:
    """ check for active user"""
    try:
        async with get_session() as session:
            stmt = update(models.UsersLoginAttempt).where(
                models.UsersLoginAttempt.session_id == session_id).values(
                status="active")
            await session.execute(stmt)
            stmt = select(models.UsersLoginAttempt).filter(
                models.UsersLoginAttempt.session_id == session_id)
            results = (await session.execute(stmt)).first()
            await session.commit()

        return jsonable_encoder(results)["UsersLoginAttempt"]
    except SQLAlchemyError as e:
        logging.info("active_user")
        return None


async def logoff_user(session_id: str) -> Any:
    """ Logging off Record"""
    try:
        async with get_session() as session:
            stmt = update(models.UsersLoginAttempt).where(
                models.UsersLoginAttempt.session_id == session_id).values(
                status="logged_off")
            await session.execute(stmt)
            stmt = select(models.UsersLoginAttempt).filter(
                models.UsersLoginAttempt.session_id == session_id)
            results = (await session.execute(stmt)).first()
            await session.commit()

        return jsonable_encoder(results)["UsersLoginAttempt"]
    except SQLAlchemyError as e:
        logging.info("logoff_user")
        return None
