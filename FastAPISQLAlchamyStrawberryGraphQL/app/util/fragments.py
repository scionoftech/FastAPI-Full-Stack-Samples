import strawberry
from typing import Union, Annotated

from app.util.scalars import GetArticles, Article

ArticleResponse = Annotated[
    Union[GetArticles, Article], strawberry.union("ArticleResponse")]
