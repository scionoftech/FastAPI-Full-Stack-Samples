import graphene
from graphql import GraphQLError
# from datetime import timedelta
# import uuid
import sys

sys.path.append("..")
from crud import crud_articles, crud_base
from db import SessionLocal as db
from util import schemas


class CreateArticle(graphene.Mutation):
    """
    Create Article Record
    """

    class Arguments:
        user_id = graphene.String(required=True)
        article_title = graphene.String(required=True)
        article_text = graphene.String(required=True)
        tags = graphene.List(required=False, of_type=graphene.String)

    message = graphene.String()

    # article = graphene.Field(lambda: schemas.ArticleCreate)

    @staticmethod
    def mutate(root, info, user_id, article_title, article_text, tags):
        article = schemas.ArticleCreate(user_id=user_id,
                                        article_title=article_title,
                                        article_text=article_text,
                                        tags=tags)
        message = "success"
        db_create = crud_articles.create_article(article=article, db=db)
        if db_create is None:
            raise GraphQLError("Internal Server Error")
        return CreateArticle(message=message)


class UpdateArticle(graphene.Mutation):
    """
    Update Article Record
    """

    class Arguments:
        user_id = graphene.String(required=True)
        article_id = graphene.String(required=True)
        article_title = graphene.String(required=True)
        article_text = graphene.String(required=True)
        tags = graphene.List(required=False, of_type=graphene.String)

    message = graphene.String()

    # user = graphene.Field(lambda: schemas.UserCreate)

    @staticmethod
    def mutate(root, info, user_id, article_id, article_title, article_text,
               tags):
        update_article = schemas.ArticleUpdate(user_id=user_id,
                                               article_id=article_id,
                                               article_title=article_title,
                                               article_text=article_text,
                                               tags=tags)
        message = "success"
        db_update = crud_articles.update_user(article_id=article_id,
                                              article=update_article,
                                              db=db)
        if db_update is None:
            raise GraphQLError("Internal Server Error")
        return UpdateArticle(message=message)


class DeleteArticle(graphene.Mutation):
    """
    Delete Article
    """

    class Arguments:
        article_id = graphene.Int(required=True)

    message = graphene.String()

    @staticmethod
    def mutate(root, info, article_id):
        delete_article = schemas.ArticleDelete(article_id=article_id)
        message = "success"
        db_update = crud_articles.delete_article(
            article_id=delete_article.article_id, db=db)
        if db_update is None:
            raise GraphQLError("Internal Server Error")
        return DeleteArticle(message=message)
