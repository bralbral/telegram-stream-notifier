from typing import Any
from typing import Awaitable
from typing import Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.logger import logger


class LoggerMiddleware(BaseMiddleware):
    """
    Logging events
    """

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        await logger.ainfo(event=event)
        return await handler(event, data)


__all__ = ["LoggerMiddleware"]
