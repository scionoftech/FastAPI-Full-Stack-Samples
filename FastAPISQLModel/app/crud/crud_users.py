from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import defer
from sqlmodel import select
from datetime import datetime
from typing import Any
# import sys
#
# sys.path.append("..")
from app.db import models, pagination, session_scope
from app.util import passutil, schemas
from app.logs import fastapi_logger


class CRUDUsers:
    def create_user(self, user: schemas.UserCreate) -> Any:
        """ Add New User"""
        try:
            with session_scope() as db:
                hashed_password = passutil.get_password_hash(str(user.password))
                db_user = models.User(email=user.email,
                                      password=hashed_password,
                                      first_name=user.first_name,
                                      last_name=user.last_name,
                                      full_name=user.full_name,
                                      gender=user.gender,
                                      is_active=user.is_active,
                                      is_superuser=user.is_superuser,
                                      is_admin=user.is_admin,
                                      created_by_userid=user.created_by_userid,
                                      modified_by_userid=user.created_by_userid)
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("create_user")
            return None

    def update_user(self, user_id: int, user: schemas.UserUpdate) -> Any:
        """ Update User"""
        try:
            with session_scope() as db:
                statement = select(models.User).where(models.User.id == user_id)
                results = db.exec(statement)
                db_user = results.one()

                db_user.first_name = user.first_name
                db_user.last_name = user.last_name
                db_user.full_name = user.full_name
                db_user.city = user.city
                db_user.country = user.country
                db_user.is_active = user.is_active
                db_user.is_superuser = user.is_superuser
                db_user.is_admin = user.is_admin
                db_user.modified_by_userid = user.modified_by_userid
                db_user.modified_timestamp = datetime.utcnow()

                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("update_user")
            return None

    def check_password(self, user_id: int, password: str):
        """ get user Password"""
        try:
            with session_scope() as db:
                statement = select(models.User.password).where(
                    models.User.id == user_id)
                results = db.exec(statement)
                db_user = results.one()
                return passutil.verify_password(str(password),
                                                str(db_user.password))
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_password")
            return None

    def change_user_password(self, user_id: str, password: str) -> Any:
        """ Update User Password"""
        try:
            with session_scope() as db:
                hashed_password = passutil.get_password_hash(password)
                statement = select(models.User).where(
                    models.User.id == user_id)
                results = db.exec(statement)
                db_user = results.one()
                db_user.password = hashed_password
                db.commit()
                db.refresh(db_user)
                return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("change_user_password")
            return None

    def update_user_password(self, email: str, password: str) -> Any:
        """ Update User Password"""
        try:
            with session_scope() as db:
                hashed_password = passutil.get_password_hash(password)
                statement = select(models.User).where(
                    models.User.email == email)
                results = db.exec(statement)
                db_user = results.one()
                db_user.password = hashed_password
                db.commit()
                db.refresh(db_user)
                return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("update_user_password")
            return None

    def delete_user(self, user_id: int) -> Any:
        """ Delete User"""
        try:
            with session_scope() as db:
                statement = select(models.User).where(
                    models.User.id == user_id)
                results = db.exec(statement)
                db_user = results.one()
                db.delete(db_user)
                db.commit()
                return True
        except SQLAlchemyError as e:
            fastapi_logger.exception("delete_user")
            return None

    def user_status_update(self, user_id: int, status: str) -> Any:
        """ Disable User"""
        try:
            with session_scope() as db:
                statement = select(models.User).where(
                    models.User.id == user_id)
                results = db.exec(statement)
                db_user = results.one()
                if status == "enable":
                    db_user.is_active = True
                elif status == "disable":
                    db_user.is_active = False
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("user_status_update")
            return None

    def verify_user(self, email: str) -> Any:
        """ Verify User"""
        try:
            with session_scope() as db:
                statement = select(models.User.id, models.User.email).where(
                    models.User.email == email)
                results = db.exec(statement)
                data = results.one()
                return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("verify_user")
            return None

    def get_user_id(self, id: int) -> Any:
        """ Get User Data based on id"""
        try:
            with session_scope() as db:
                statement = select(models.User).where(
                    models.User.id == id).options(defer('password'))
                results = db.exec(statement)
                data = results.one()
                return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_user_id")
            return None

    # https://docs.sqlalchemy.org/en/13/orm/loading_columns.html#deferred
    def get_all_user(self, page_num: int) -> Any:
        """ Get All Users"""
        try:
            with session_scope() as db:
                # data = db.query(models.User).options(defer('password')).all()
                statement = select(models.User).options(
                    defer('password')).order_by(
                    models.User.modified_timestamp)
                data = pagination.paginate(query=statement,db=db,model=models.User, page=page_num,
                                           page_size=100)
                return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_all_user")
            return None


crud_users = CRUDUsers()
