from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import defer
from datetime import datetime
from typing import Any
import sys

sys.path.append("..")
from db import models, pagination
from util import passutil, schemas
from logs import fastapi_logger


class CRUDUsers:
    def create_user(self, user: schemas.UserCreate, db: Session) -> Any:
        """ Add New User"""
        try:
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

    def update_user(self, user_id: int, user: schemas.UserUpdate,
                    db: Session) -> Any:
        """ Update User"""
        try:
            db_user = db.query(models.User).filter(
                models.User.id == user_id).first()

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

            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("update_user")
            return None

    def check_password(self, user_id: int, password: str,
                       db: Session):
        """ get user Password"""
        try:
            db_user = db.query(models.User.password).filter(
                models.User.id == user_id).first()
            return passutil.verify_password(str(password),
                                            str(db_user.password))
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_password")
            return None

    def change_user_password(self, user_id: str, password: str,
                             db: Session) -> Any:
        """ Update User Password"""
        try:
            hashed_password = passutil.get_password_hash(password)
            db_user = db.query(models.User).filter(
                models.User.id == user_id).first()
            db_user.password = hashed_password
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("change_user_password")
            return None

    def update_user_password(self, email: str, password: str,
                             db: Session) -> Any:
        """ Update User Password"""
        try:
            hashed_password = passutil.get_password_hash(password)
            db_user = db.query(models.User).filter(
                models.User.email == email).first()
            db_user.password = hashed_password
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("update_user_password")
            return None

    def delete_user(self, user_id: int, db: Session) -> Any:
        """ Delete User"""
        try:
            db.query(models.User).filter(
                models.User.id == user_id).delete()
            db.commit()
            return True
        except SQLAlchemyError as e:
            fastapi_logger.exception("delete_user")
            return None

    def user_status_update(self, user_id: int, status: str,
                           db: Session) -> Any:
        """ Disable User"""
        try:
            db_user = db.query(models.User).filter(
                models.User.id == user_id).first()
            if status == "enable":
                db_user.is_active = True
            elif status == "disable":
                db_user.is_active = False
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("user_status_update")
            return None

    def verify_user(self, email: str, db: Session) -> Any:
        """ Verify User"""
        try:
            data = db.query(models.User.id, models.User.email).filter(
                models.User.email == email).first()
            return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("verify_user")
            return None

    def get_user_id(self, id: int, db: Session) -> Any:
        """ Get User Data based on id"""
        try:
            data = db.query(models.User).filter(
                models.User.id == id).options(defer('password')).first()
            return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_user_id")
            return None

    # https://docs.sqlalchemy.org/en/13/orm/loading_columns.html#deferred
    def get_all_user(self, page_num: int, db: Session) -> Any:
        """ Get All Users"""
        try:
            # data = db.query(models.User).options(defer('password')).all()
            query = db.query(models.User).options(
                defer('password')).order_by(
                models.User.modified_timestamp.desc())
            data = pagination.paginate(query=query, page=page_num,
                                       page_size=100)
            return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_all_user")
            return None


crud_users = CRUDUsers()
