import asyncio
import random

from starlette.requests import Request


async def inject_delay(request: Request):
    delay = random.uniform(0, 3)
    await asyncio.sleep(delay)
