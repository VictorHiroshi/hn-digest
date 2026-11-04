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
