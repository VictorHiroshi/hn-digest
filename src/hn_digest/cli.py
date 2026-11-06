import asyncio
from typing import Annotated, Literal

import typer

from hn_digest.client import HnClient
from hn_digest.digest import fetch_concurrent, fetch_sequential

app = typer.Typer()


@app.command()
def hn_digest(
    limit: int = 10,
    concurrency: int = 10,
    mode: Annotated[Literal["concurrent", "sequential"], typer.Option("--mode")] = "concurrent",
) -> None:
    """Fetches the top stories from Hacker News and displays them."""

    client = HnClient()

    async def list_stories() -> None:
        if mode == "concurrent":
            stories = await fetch_concurrent(client=client, limit=limit, concurrency=concurrency, timeout=5)
        else:
            stories = await fetch_sequential(client=client, limit=limit)
        for id, s in enumerate(stories):
            print(f"Story {id + 1}: {s}")

    asyncio.run(list_stories())


if __name__ == "__main__":
    typer.run(hn_digest)
