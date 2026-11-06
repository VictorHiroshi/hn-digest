from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Story:
    id: int
    title: str
    url: str | None
    score: int
    by: str


class StoryRepository(Protocol):
    async def get_top_ids(self) -> list[int]: ...
    async def get_story(self, story_id: int) -> Story | None: ...


def _parse_story(raw: dict[str, object]) -> Story | None:
    if (
        not isinstance(raw.get("id"), (int, str))
        or not isinstance(raw.get("title"), str)
        or not isinstance(raw.get("url"), (str, type(None)))
        or not isinstance(raw.get("score"), (int, str))
        or not isinstance(raw.get("by"), str)
    ):
        return None

    try:
        return Story(
            id=int(raw["id"]),
            title=raw["title"],
            url=raw.get("url"),
            score=int(raw["score"]),
            by=raw["by"],
        )
    except (KeyError, TypeError, ValueError):
        return None
