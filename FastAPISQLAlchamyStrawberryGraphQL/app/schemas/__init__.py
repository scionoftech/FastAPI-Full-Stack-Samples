import strawberry
from fastapi import Depends
from app.schemas.query_schema import Query
from app.schemas.mutation_schema import Mutation
from app.schemas.subscription import Subscription
from app.util.context import get_broadcaster, Broadcast
from strawberry.fastapi import GraphQLRouter

schema = strawberry.Schema(query=Query, mutation=Mutation,subscription=Subscription)


async def custom_context_dependency() -> Broadcast:
    return await get_broadcaster()


async def get_context(broadcast=Depends(custom_context_dependency)):
    return {
        "broadcast": broadcast
    }


graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)
