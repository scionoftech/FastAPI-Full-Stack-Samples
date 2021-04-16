from datetime import datetime
from typing import Any
import sys

sys.path.append("..")
from db import User, pagination
from util import passutil, schemas
from logs import fastapi_logger


class CRUDUsers:
    def create_user(self, user: schemas.UserCreate) -> Any:
        """ Add New User"""
        try:
            hashed_password = passutil.get_password_hash(str(user.password))
            db_user = User(email=user.email,
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
            db_user.save()
            return db_user
        except Exception as e:
            print(e)
            fastapi_logger.exception("create_user")
            return None

    def update_user(self, user_id: int, user: schemas.UserUpdate) -> Any:
        """ Update User"""
        try:
            db_user = User.objects(id=user_id).first()

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

            db_user.save()
            return db_user
        except Exception as e:
            fastapi_logger.exception("update_user")
            return None

    def check_password(self, user_id: int, password: str):
        """ get user Password"""
        try:
            db_user = User.objects(id=user_id).first()
            return passutil.verify_password(str(password),
                                            str(db_user.password))
        except Exception as e:
            fastapi_logger.exception("get_password")
            return None

    def change_user_password(self, user_id: str, password: str) -> Any:
        """ Update User Password"""
        try:
            hashed_password = passutil.get_password_hash(password)
            db_user = User.objects(id=user_id).first()
            db_user.password = hashed_password
            db_user.save()
            return db_user
        except Exception as e:
            fastapi_logger.exception("change_user_password")
            return None

    def update_user_password(self, email: str, password: str) -> Any:
        """ Update User Password"""
        try:
            hashed_password = passutil.get_password_hash(password)
            db_user = User.objects(email=email).first()
            db_user.password = hashed_password
            db_user.save()
            return db_user
        except Exception as e:
            fastapi_logger.exception("update_user_password")
            return None

    def delete_user(self, user_id: int) -> Any:
        """ Delete User"""
        try:
            data = User.objects(id=user_id)
            data.delete()
            return True
        except Exception as e:
            fastapi_logger.exception("delete_user")
            return None

    def user_status_update(self, user_id: int, status: str) -> Any:
        """ Disable User"""
        try:
            db_user = User.objects(id=user_id).first()
            if status == "enable":
                db_user.is_active = True
            elif status == "disable":
                db_user.is_active = False
            db_user.save()
            return db_user
        except Exception as e:
            fastapi_logger.exception("user_status_update")
            return None

    def verify_user(self, email: str) -> Any:
        """ Verify User"""
        try:
            data = User.objects(email=email).only('id', 'email').first()
            return data
        except Exception as e:
            fastapi_logger.exception("verify_user")
            return None

    # https://www.tutorialspoint.com/mongoengine/mongoengine_queryset_methods.htm
    def get_user_id(self, idd: int) -> Any:
        """ Get User Data based on id"""
        try:
            data = User.objects(id=idd).exclude('password').first()
            return data
        except Exception as e:
            fastapi_logger.exception("get_user_id")
            return None

    # https://www.tutorialspoint.com/mongoengine/mongoengine_sorting.htm
    def get_all_user(self, page_num: int) -> Any:
        """ Get All Users"""
        try:
            query = User.objects.exclude('password').order_by(
                '-modified_timestamp')
            data = pagination.paginate(query=query, page=page_num,
                                       page_size=100)
            return data
        except Exception as e:
            fastapi_logger.exception("get_all_user")
            return None


crud_users = CRUDUsers()
