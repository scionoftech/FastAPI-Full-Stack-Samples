from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, insert, update, delete, func
from typing import Any, Union, List
from fastapi.encoders import jsonable_encoder
import uuid
from app.util.strawberry_utils import \
    convert_strawberry_to_dict_return_non_null
from db import models, pagination, get_session
from app.util import scalars
from app.util.fragments import GetArticles
import logging


async def create_article(article: scalars.ArticleInput) -> Union[
    scalars.Article, None]:
    """ Create New Article """
    try:
        uid = str(uuid.uuid4().hex)
        async with get_session() as session:
            stmt = insert(models.Article).values(
                id=uid,
                **convert_strawberry_to_dict_return_non_null(
                    article)
            )
            await session.execute(stmt)

            stmt = select(models.Article).filter(
                models.Article.id == uid)
            results = (await session.execute(stmt)).first()
            await session.commit()

        return scalars.Article(
            **jsonable_encoder(results)["Article"])
    except SQLAlchemyError as e:
        logging.info("create_article")
        return None


async def update_article(article_id: str,
                         article: scalars.ArticleInput) -> Union[
    scalars.Article, None]:
    """ Update Article """
    try:
        async with get_session() as session:
            stmt = update(models.Article).where(
                models.Article.id == article_id).values(
                **convert_strawberry_to_dict_return_non_null(
                    article)
            )
            await session.execute(stmt)

            stmt = select(models.Article).filter(
                models.Article.id == article_id)
            results = (await session.execute(stmt)).first()
            await session.commit()

        return scalars.Article(
            **jsonable_encoder(results)["Article"])
    except SQLAlchemyError as e:
        logging.info("update_article")
        return None


async def delete_article(article_id: str) -> Any:
    """ Delete Article """
    try:
        async with get_session() as session:
            stmt = delete(models.Article).where(
                models.User.id == article_id)
            await session.execute(stmt)
            await session.commit()
        return True
    except SQLAlchemyError as e:
        logging.info("delete_article")
        return None


async def get_article(article_id: str) -> Union[
    scalars.Article, None]:
    """ Get A Single article """
    try:
        async with get_session() as session:
            stmt = select(models.Article).filter(
                models.User.id == article_id)
            results = (await session.execute(stmt)).first()
        return scalars.Article(
            **jsonable_encoder(results)["Article"])
    except SQLAlchemyError as e:
        logging.info("get_article")
        return None


async def get_all_articles(tag: str, page_num: int,
                           sort_by: str = "latest") -> Union[
    scalars.GetArticles, None]:
    """ Get All Articles """
    try:
        async with get_session() as session:
            stmt = select(models.Article)
            if sort_by == "latest":
                stmt = stmt.order_by(
                    models.Article.modified_timestamp.desc())
            else:
                stmt = stmt.order_by(
                    models.Article.modified_timestamp.asc())

        query = select(func.count()).select_from(models.Article)

        if tag:
            looking_for = '%{0}%'.format(tag)
            stmt = stmt.filter(
                models.Article.tags.ilike(looking_for))
            query = query.filter(
                models.Article.tags.ilike(looking_for))

        sql_obj = await session.execute(query)
        total = sql_obj.scalar()

        data = await pagination.paginate(query=stmt, page=page_num,
                                         page_size=100, total=total,
                                         session=session)

        article_list = []
        for obj in data.items:
            article_list.append(
                scalars.Article(jsonable_encoder(obj)))

        return scalars.GetArticles(total_pages=data.pages,
                                   total_records=data.total_items,
                                   previous_page=data.previous_page,
                                   next_page=data.next_page,
                                   has_previous=data.has_previous,
                                   has_next=data.has_next,
                                   page_data=article_list)

    except SQLAlchemyError as e:
        logging.info("get_all_articles")
        return None


async def get_article_s(tag: str = None,
                        article_id: str = None,
                        page_num: int = 1) -> [scalars.GetArticles,
                                               scalars.Article, None]:
    if article_id:
        data = await get_article(article_id=article_id)
        return data
    else:
        data = await get_all_articles(tag=tag, page_num=page_num)
        return data
