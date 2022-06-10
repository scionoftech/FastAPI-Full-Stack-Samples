import graphene
from graphene_mongo import MongoengineObjectType, \
    MongoengineConnectionField
from graphql import GraphQLError
from graphene import relay
import sys

sys.path.append("..")
from crud import crud_users, crud_articles, crud_base
from db import dbconf_models
from mutations import (CreateUser, AuthUser, UpdateUser, DeleteUser,
                       UpdatePassword,
                       CreateArticle, UpdateArticle, DeleteArticle)

"""
Pagination:
1. https://graphql.org/learn/pagination/
2. https://docs.graphene-python.org/projects/django/en/latest/queries/
3. https://relay.dev/graphql/connections.htm

"""


class CountableConnection(graphene.relay.Connection):
    """
    Relay Connection for pagination
    https://github.com/graphql-python/graphene-sqlalchemy/issues/58
    """

    class Meta:
        abstract = True

    # total_count = graphene.Int()
    edge_count = graphene.Int()

    # @staticmethod
    # def resolve_total_count(root, info):
    #     return root.length

    @staticmethod
    def resolve_edge_count(root, info):
        return len(root.edges)


class User(MongoengineObjectType):
    class Meta:
        model = dbconf_models.User
        # use `only_fields` to only expose specific fields ie "name"
        # only_fields = ("name",)
        # use `exclude_fields` to exclude specific fields ie "last_name"
        exclude_fields = ("password",)
        interfaces = (relay.Node,)
        connection_class = CountableConnection
        # fields = "__all__"


class Articles(MongoengineObjectType):
    class Meta:
        model = dbconf_models.Article
        # use `only_fields` to only expose specific fields ie "name"
        # only_fields = ("name",)
        # use `exclude_fields` to exclude specific fields ie "last_name"
        interfaces = (relay.Node,)
        connection_class = CountableConnection
        # fields = "__all__"


class Mutations(graphene.ObjectType):
    """
    GraphQL Mutations
    """
    create_user = CreateUser.Field()
    auth_user = AuthUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    update_password = UpdatePassword.Field()

    create_article = CreateArticle.Field()
    update_article = UpdateArticle.Field()
    delete_article = DeleteArticle.Field()


class Query(graphene.ObjectType):
    """
    GraphQL Query
    """
    get_single_user = graphene.Field(User,
                                     user_id=graphene.NonNull(
                                         graphene.String))
    get_users = MongoengineConnectionField(User)

    get_single_article = graphene.Field(Articles,
                                        article_id=graphene.NonNull(
                                            graphene.String))
    get_articles = MongoengineConnectionField(Articles,
                                              tag=graphene.String())

    def resolve_get_users(self, info, **kwargs):
        """
        Get All users with pagination
        """
        db_user = crud_users.get_all_user()
        if db_user is None:
            raise GraphQLError("No Users Found")
        return db_user

    def resolve_get_single_user(self, info, user_id):
        """
        Get single user
        """
        return crud_users.get_user_id(user_id=user_id)

    def resolve_get_articles(self, info, **kwargs):
        """
        Get All articles with pagination and filters
        """
        db_article = crud_articles.get_all_articles(
            tag=kwargs.get("tag"),
            article_title=kwargs.get("article_title"))
        if db_article is None:
            raise GraphQLError("No Users Found")
        return db_article

    def resolve_get_single_article(self, info, article_id):
        """
        Get Article
        """
        return crud_articles.get_article(article_id=article_id)

# schema = graphene.Schema()
# schema.execute(context_value={'session': SessionLocal()})
