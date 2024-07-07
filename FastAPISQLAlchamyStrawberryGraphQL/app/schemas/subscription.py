import asyncio

import strawberry
from strawberry.types import Info
from typing import AsyncGenerator


@strawberry.type
class Subscription:

    @strawberry.subscription
    async def on_event(self, info: Info) -> str:
        print(info.context["broadcast"])
        print(id(info.context["broadcast"]))
        async with info.context["broadcast"].subscribe(channel="notifications") as subscriber:
            print(f"{subscriber=}")
            async for event in subscriber:
                print(f"{event=}")
                yield event.message


    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield 1
            await asyncio.sleep(0.5)