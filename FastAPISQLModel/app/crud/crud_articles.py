from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Any
import uuid
# import sys
#
# sys.path.append("..")
from app.db import models, pagination, session_scope
from app.util import schemas
from app.logs import fastapi_logger


class CRUDArticles:
    def create_article(self, article: schemas.ArticleCreate) -> Any:
        """ Create New Article """
        try:
            with session_scope() as db:
                uid = str(uuid.uuid4().hex)
                db_user = models.Article(article_id=uid,
                                         user_id=article.user_id,
                                         article_title=article.article_title,
                                         article_text=article.article_text,
                                         tags=article.tags)
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                return db_user
        except SQLAlchemyError as e:
            fastapi_logger.exception("create_article")
            return None

    def update_article(self, article_id: str,
                       article: schemas.ArticleCreate) -> Any:
        """ Update Article """
        try:
            with session_scope() as db:
                statement = select(models.Article).where(
                    models.Article.article_id == article_id)
                results = db.exec(statement)
                db_article = results.one()

                db_article.article_title = article.article_title
                db_article.article_text = article.article_text
                db_article.tags = article.tags
                db_article.modified_timestamp = datetime.utcnow()

                db.commit()
                db.refresh(db_article)
                return db_article
        except SQLAlchemyError as e:
            fastapi_logger.exception("update_article")
            return None

    def delete_article(self, article_id: str) -> Any:
        """ Delete Article """
        try:
            with session_scope() as db:
                statement = select(models.Article).where(
                    models.Article.article_id == article_id)
                results = db.exec(statement)
                db_article = results.one()
                db.delete(db_article)
                db.commit()
                return True
        except SQLAlchemyError as e:
            fastapi_logger.exception("delete_article")
            return None

    def get_article(self, article_id: str):
        """ Get A Single article """
        try:
            with session_scope() as db:
                statement = select(models.Article).where(
                    models.Article.article_id == article_id)
                results = db.exec(statement)
                data = results.one()
                return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_article")
            return None

    def get_all_articles(self, page_num: int) -> Any:
        """ Get All Articles """
        try:
            with session_scope() as db:
                query = select(models.Article).order_by(
                    models.Article.modified_timestamp)

                data = pagination.paginate(query=query, db=db,
                                           model=models.Article, page=page_num,
                                           page_size=30)
                return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_all_articles")
            return None


crud_articles = CRUDArticles()
