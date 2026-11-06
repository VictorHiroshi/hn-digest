import asyncio
import time

from hn_digest.client import HnClient
from hn_digest.helpers import retry_on_timeout
from hn_digest.models import Story


async def fetch_sequential(client: HnClient, limit: int) -> list[Story]:
    start = time.perf_counter()
    ids = await client.get_top_ids()
    stories = []
    for sid in ids[:limit]:
        s = await client.get_story(sid)
        if s:
            stories.append(s)
    print(f"sequencial: {time.perf_counter() - start:.2f}s")
    return stories


async def fetch_concurrent(client: HnClient, limit: int, concurrency: int = 10, timeout: int = 5) -> list[Story | None]:
    start = time.perf_counter()
    ids = (await client.get_top_ids())[:limit]
    sem = asyncio.Semaphore(concurrency)

    @retry_on_timeout(retries=3, delay=1.0, backoff=2.0)
    async def _fetch(sid: int) -> Story | None:
        async with sem:
            try:
                async with asyncio.timeout(timeout):
                    return await client.get_story(sid)
            except TimeoutError:
                print(f"Timeout occurred while fetching story with ID: {sid}")
                raise

    try:
        async with asyncio.TaskGroup() as tg:
            # pyrefly: ignore[bad-argument-type]
            tasks = [tg.create_task(_fetch(sid)) for sid in ids]
    except ExceptionGroup as eg:
        print(f"ExceptionGroup occurred: {eg}")
        return []

    stories = [t.result() for t in tasks if t.result() is not None]
    print(f"concorrente: {time.perf_counter() - start:.2f}s")
    return stories


if __name__ == "__main__":
    import asyncio

    async def main():
        client = HnClient()
        stories = await fetch_concurrent(client=client, limit=30, concurrency=10, timeout=5)
        for id, s in enumerate(stories):
            print(f"Story {id + 1}: {s}")

    asyncio.run(main())
