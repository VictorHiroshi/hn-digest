from collections.abc import AsyncIterator

import httpx
import pytest
import pytest_asyncio

from hn_digest.client import BASE, HnClient
from hn_digest.models import Story


def _mock_hn_response(request: httpx.Request) -> httpx.Response:
    if request.url.path.endswith("/topstories.json"):
        return httpx.Response(200, json=[1])
    if request.url.path.endswith("/item/1.json"):
        return httpx.Response(
            200,
            json={
                "id": 1,
                "title": "Example",
                "url": "https://example.com",
                "score": 10,
                "by": "alice",
            },
        )
    return httpx.Response(404)


@pytest_asyncio.fixture
async def hn_client() -> AsyncIterator[HnClient]:
    async with httpx.AsyncClient(
        base_url=BASE,
        transport=httpx.MockTransport(_mock_hn_response),
    ) as client:
        yield HnClient(client)


@pytest.mark.asyncio
async def test_client_get_top_ids(hn_client: HnClient):
    assert await hn_client.get_top_ids() == [1]


@pytest.mark.asyncio
async def test_client_get_top_ids_on_error(hn_client: HnClient):
    with pytest.raises(httpx.HTTPStatusError):
        await hn_client.get_story(999)


@pytest.mark.asyncio
async def test_client_get_story(hn_client: HnClient):
    assert await hn_client.get_story(1) == Story(
        id=1,
        title="Example",
        url="https://example.com",
        score=10,
        by="alice",
    )


@pytest.mark.asyncio
async def test_client_get_story_on_error(hn_client: HnClient):
    with pytest.raises(httpx.HTTPStatusError):
        await hn_client.get_story(999)
