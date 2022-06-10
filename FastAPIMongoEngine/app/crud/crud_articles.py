from datetime import datetime
from typing import Any
import sys

sys.path.append("..")
from db import Article, pagination
from util import passutil, schemas
from logs import fastapi_logger


class CRUDArticles:
    def create_article(self, article: schemas.ArticleCreate) -> Any:
        """ Create New Article """
        try:
            db_article = Article(user_id=article.user_id,
                                 article_title=article.article_title,
                                 article_text=article.article_text,
                                 tags=article.tags)
            db_article.save()
            return db_article
        except Exception as e:
            fastapi_logger.exception("create_article")
            return None

    def update_article(self, article_id: str,
                       article: schemas.ArticleCreate) -> Any:
        """ Update Article """
        try:
            db_article = Article.objects(id=article_id).first()

            db_article.article_title = article.article_title
            db_article.article_text = article.article_text
            db_article.tags.extend(article.tags)
            db_article.modified_timestamp = datetime.utcnow()

            db_article.save()
            return db_article
        except Exception as e:
            fastapi_logger.exception("update_article")
            return None

    def delete_article(self, article_id: str) -> Any:
        """ Delete Article """
        try:
            db_article = Article.objects(id=article_id)
            db_article.delete()
            return True
        except Exception as e:
            fastapi_logger.exception("delete_article")
            return None

    def get_article(self, article_id: str):
        """ Get A Single article """
        try:
            data = Article.objects(id=article_id).first()
            return data
        except Exception as e:
            fastapi_logger.exception("get_article")
            return None

    def get_all_articles(self, tag: str = None,
                         article_title: str = None,
                         page_num: int = 1, page_size=30) -> Any:
        """ Get All Articles """
        try:
            query = Article.objects

            if tag:
                query = query.filter(tags=tag)

            if article_title:
                query = query.filter(article_title=article_title)

            data = pagination.paginate(query=query.order_by(
                'modified_timestamp'), page=page_num,
                page_size=page_size)
            return data
        except Exception as e:
            fastapi_logger.exception("get_all_articles")
            return None


crud_articles = CRUDArticles()
