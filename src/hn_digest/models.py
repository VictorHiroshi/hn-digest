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
    pass