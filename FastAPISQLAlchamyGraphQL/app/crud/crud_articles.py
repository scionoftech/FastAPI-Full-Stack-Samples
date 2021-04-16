from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import cast
from sqlalchemy import String
from datetime import datetime
from typing import Any
import uuid
import sys

sys.path.append("..")
from db import models
from util import passutil, schemas
from logs import fastapi_logger


class CRUDArticles:
    def create_article(self, article: schemas.ArticleCreate,
                       db: Session) -> Any:
        """ Create New Article """
        try:
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

    def update_article(self, article_id: str, article: schemas.ArticleCreate,
                       db: Session) -> Any:
        """ Update Article """
        try:
            db_article = db.query(models.Article).filter(
                models.Article.article_id == article_id).first()

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

    def delete_article(self, article_id: str, db: Session) -> Any:
        """ Delete Article """
        try:
            db.query(models.Article).filter(
                models.Article.article_id == article_id).delete()
            db.commit()
            return True
        except SQLAlchemyError as e:
            fastapi_logger.exception("delete_article")
            return None

    def get_article(self, query: models.Article, article_id: str):
        """ Get A Single article """
        try:
            data = query.filter(
                models.Article.article_id == article_id).first()
            return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_article")
            return None

    def get_all_articles(self, query: models.Article, tag: str) -> Any:
        """ Get All Articles """
        try:
            data = query.order_by(
                models.Article.modified_timestamp.desc())

            if tag:
                looking_for = '%{0}%'.format(tag)
                data = query.filter(cast(
                    models.Article.tags, String).ilike(looking_for))

            return data
        except SQLAlchemyError as e:
            fastapi_logger.exception("get_all_articles")
            return None


crud_articles = CRUDArticles()
