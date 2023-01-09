import asyncio

from loguru import logger

from brazzers import subscribe_brazzers


async def main():
    queue = asyncio.Queue()

    with open(input("Filename with emails: ")) as f:
        emails = f.read().splitlines()

    for email in emails:
        queue.put_nowait(email)

    tasks = [
        asyncio.create_task(subscribe_brazzers(f"Worker {i+1}", queue))
        for i in range(5)
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logger.error(err)
