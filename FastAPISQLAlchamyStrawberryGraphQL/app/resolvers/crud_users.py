import uuid
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import defer
from sqlalchemy import select, insert, update, delete, func
from fastapi.encoders import jsonable_encoder
from app.util.strawberry_utils import \
    convert_strawberry_to_dict_return_non_null
from typing import Any, List, Union
from db import models, pagination, get_session
from app.util import passutil, scalars, schemas
import logging


async def create_user(user: scalars.UserInput) -> Union[
    scalars.User, None]:
    """ Add New User"""
    try:
        hashed_password = passutil.get_password_hash(
            str(user.password))
        user_id = uuid.uuid4().hex
        async with get_session() as session:
            stmt = insert(models.User).values(
                id=user_id,
                password=hashed_password,
                **convert_strawberry_to_dict_return_non_null(user)
            )
            await session.execute(stmt)

            stmt = select(models.User).filter(
                models.User.id == user_id)
            results = (await session.execute(stmt)).first()
            await session.commit()

        return scalars.User(**jsonable_encoder(results)["User"])
    except SQLAlchemyError as e:
        logging.info("create_user")
        return None


async def update_user(user_id: int, user: scalars.UserInput) -> Union[
    scalars.User, None]:
    """ Update User"""
    try:
        async with get_session() as session:
            stmt = update(models.User).where(
                models.User.id == user_id).values(
                **convert_strawberry_to_dict_return_non_null(user)
            )
            await session.execute(stmt)

            stmt = select(models.User).filter(
                models.User.id == user_id)
            results = (await session.execute(stmt)).first()
            await session.commit()

        return scalars.User(**jsonable_encoder(results)["User"])
    except SQLAlchemyError as e:
        logging.info("update_user")
        return None


async def check_password(user_id: int, password: str):
    """ get user Password"""
    try:
        async with get_session() as session:
            stmt = select(models.User.password).filter(
                models.User.id == user_id)
            results = (await session.execute(stmt)).first()
            db_user = jsonable_encoder(results)["User"]
        return passutil.verify_password(str(password),
                                        str(db_user.password))
    except SQLAlchemyError as e:
        logging.info("get_password")
        return None


async def change_user_password(user_id: str, password: str) -> Union[
    scalars.User, None]:
    """ Update User Password"""
    try:
        hashed_password = passutil.get_password_hash(password)
        async with get_session() as session:
            stmt = update(models.User).where(
                models.User.id == user_id).values(
                password=hashed_password)
            await session.execute(stmt)

            stmt = select(models.User).filter(
                models.User.id == user_id)
            results = (await session.execute(stmt)).first()
            await session.commit()

        return scalars.User(**jsonable_encoder(results)["User"])
    except SQLAlchemyError as e:
        logging.info("change_user_password")
        return None


async def delete_user(user_id: int) -> Any:
    """ Delete User"""
    try:
        async with get_session() as session:
            stmt = delete(models.User).where(
                models.User.id == user_id)
            await session.execute(stmt)
            await session.commit()
        return True
    except SQLAlchemyError as e:
        logging.info("delete_user")
        return None


async def verify_user(email: str) -> Union[schemas.UserVerify, None]:
    """ Verify User"""
    try:
        async with get_session() as session:
            stmt = select(models.User.id, models.User.email).filter(
                models.User.email == email)
            results = (await session.execute(stmt)).first()
            print(jsonable_encoder(results))
        return schemas.UserVerify(
            id=jsonable_encoder(results)["id"],email=jsonable_encoder(results)["email"])
    except SQLAlchemyError as e:
        logging.info("verify_user")
        return None


async def get_user_id(user_id: str) -> Union[scalars.User, None]:
    """ Get User Data based on id"""
    try:
        async with get_session() as session:
            stmt = select(models.User).filter(
                models.User.email == user_id)
            results = (await session.execute(stmt)).first()
        return scalars.User(**jsonable_encoder(results)["User"])
    except SQLAlchemyError as e:
        print(e)
        logging.info("get_user_id")
        return None


async def get_active_user(email: str) -> Union[scalars.User, None]:
    """ Get User Data based on email"""
    try:
        async with get_session() as session:
            stmt = select(models.User).filter(
                models.User.email == email)
            results = (await session.execute(stmt)).first()
        return scalars.User(**jsonable_encoder(results)["User"])
    except SQLAlchemyError as e:
        print(e)
        logging.info("get_user_id")
        return None


# https://docs.sqlalchemy.org/en/13/orm/loading_columns.html#deferred
async def get_all_user(page_num: int, sort_by="latest") -> Union[
    List[scalars.User], None]:
    """ Get All Users"""
    try:
        async with get_session() as session:
            stmt = select(models.User).options(defer('password'))
            if sort_by == "latest":
                stmt = stmt.order_by(
                    models.User.modified_timestamp.desc())
            else:
                stmt = stmt.order_by(
                    models.User.modified_timestamp.asc())

        query = select(func.count()).select_from(models.User)
        sql_obj = await session.execute(query)
        total = sql_obj.scalar()

        data = pagination.paginate(query=stmt, page=page_num,
                                   page_size=100, total=total,
                                   session=session)

        users_list = []
        for obj in data.items:
            users_list.append(scalars.User(**jsonable_encoder(obj)))

        return users_list
    except SQLAlchemyError as e:
        logging.info("get_all_user")
        return None
