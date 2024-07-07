import strawberry
from strawberry.types import Info
from app.util.deps import jwt_and_error_handler
from app.util.scalars import ArticleInput, Article
from app.resolvers.crud_articles import create_article, update_article


@strawberry.type
class Mutation:

    @strawberry.mutation
    @jwt_and_error_handler
    async def add_edit_article(self, info: Info,
                               article_input: ArticleInput) -> Article:
        if article.article_id is not None:
            results = await update_article(article_id=article.article_id,
                                           article=article)
        else:
            results = await create_article(article=article)

        if results is None:
            raise ValueError("something went wrong please try again")

        return results

    @strawberry.mutation
    async def send_message(self, info: Info, message: str) -> bool:
        await info.context["broadcast"].publish(
            channel="notifications", message=message)
        return True
