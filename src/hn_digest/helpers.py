import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

# P captures the parameters (names, types, defaults) of the original function
P = ParamSpec("P")
# R captures the exact return type of the original function
R = TypeVar("R")


def retry_on_timeout(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Decorator to retry an async function if it raises asyncio.TimeoutError,
    fully preserving all argument types and return values for static checkers.
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        # pyrefly: ignore[bad-return]
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            current_delay = delay
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except TimeoutError:
                    print(f"Timeout occurred. Retrying {attempt}/{retries}...")
                    if attempt == retries:
                        raise
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator
