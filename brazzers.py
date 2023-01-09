import asyncio

from aiohttp import ClientSession
from anti_useragent import UserAgent as ua
from loguru import logger

import config


def get_headers(): return config.HEADERS.copy()


async def subscribe_brazzers(worker: str, q: asyncio.Queue) -> None:
    while not q.empty():
        email = await q.get()

        headers = get_headers()
        headers["User-Agent"] = ua().random

        async with ClientSession(headers=headers) as session:
            resp = await session.post(
                "https://dev.joi.city/api/emailcollection/sendEmail",
                json={
                    "collectionId": "63ab5acf5a201c3dc9914228",
                    "email": email
                }
            )

        if (resp_json := await resp.json()).get("status") == "success":
            logger.success(f"({worker}) {email} successfully registered!")
        else:
            logger.error(f"({worker}) - {email} - {resp_json}")