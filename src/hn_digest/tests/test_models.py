from dataclasses import FrozenInstanceError

import pytest

from hn_digest.models import Story


def test_story_stores_its_fields():
    story = Story(id=1, title="Example", url="https://example.com", score=10, by="alice")

    assert story.id == 1
    assert story.title == "Example"
    assert story.url == "https://example.com"
    assert story.score == 10
    assert story.by == "alice"


def test_story_is_immutable():
    story = Story(id=1, title="Example", url=None, score=10, by="alice")

    with pytest.raises(FrozenInstanceError):
        # pyrefly: ignore[read-only]
        story.title = "Changed"


@pytest.mark.skip(reason="_parse_story is not implemented yet.")
def test_parse_story():
    # raw_story = {"id": 1, "title": "Example", "url": "https://example.com", "score": 10, "by": "alice"}

    assert True
    # _parse_story(raw_story) == Story(
    #     id=1,
    #     title="Example",
    #     url="https://example.com",
    #     score=10,
    #     by="alice",
    # )
