import asyncio
from unittest.mock import AsyncMock, call

import pytest

from hn_digest import digest
from hn_digest.client import HnClient
from hn_digest.digest import fetch_concurrent, fetch_sequential
from hn_digest.models import Story


@pytest.mark.asyncio
async def test_fetch_sequential_respects_limit_and_skips_missing_stories():
    client = AsyncMock(spec=HnClient)
    story = Story(id=1, title="Example", url="https://example.com", score=10, by="alice")
    client.get_top_ids.return_value = [1, 2, 3]
    client.get_story.side_effect = [story, None]

    assert await fetch_sequential(client, 2) == [story]
    client.get_story.assert_has_awaits([call(1), call(2)])
    assert client.get_story.await_count == 2


@pytest.mark.asyncio
async def test_fetch_concurrent_respects_limit_and_skips_missing_stories(monkeypatch):
    monkeypatch.setattr(digest, "asyncio", asyncio, raising=False)
    client = AsyncMock(spec=HnClient)
    story = Story(id=1, title="Example", url="https://example.com", score=10, by="alice")
    client.get_top_ids.return_value = [1, 2, 3]
    client.get_story.side_effect = [story, None]

    assert await fetch_concurrent(client, 2) == [story]
    client.get_story.assert_has_awaits([call(1), call(2)])
    assert client.get_story.await_count == 2
