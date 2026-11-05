import time

from hn_digest.client import HnClient
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


async def fetch_concurrent(client: HnClient, limit: int, concurrency: int = 10) -> list[Story | None]:
    start = time.perf_counter()
    ids = (await client.get_top_ids())[:limit]
    sem = asyncio.Semaphore(concurrency)

    async def _fetch(sid: int) -> Story | None:
        async with sem:
            return await client.get_story(sid)

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(_fetch(sid)) for sid in ids]

    stories = [t.result() for t in tasks if t.result() is not None]
    print(f"concorrente: {time.perf_counter() - start:.2f}s")
    return stories


if __name__ == "__main__":
    import asyncio

    async def main():
        client = HnClient()
        stories = await fetch_concurrent(client=client, limit=20)
        for s in stories:
            print(s)

    asyncio.run(main())
