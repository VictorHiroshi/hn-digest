import httpx

from hn_digest.models import Story, _parse_story

BASE = "https://hacker-news.firebaseio.com/v0"


class HnClient:
    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(base_url=BASE, timeout=10.0)

    async def get_top_ids(self) -> list[int]:
        response = await self._client.get("/topstories.json")
        response.raise_for_status()
        return response.json()

    async def get_story(self, story_id: int) -> Story | None:
        response = await self._client.get(f"/item/{story_id}.json")
        response.raise_for_status()
        return _parse_story(response.json())
