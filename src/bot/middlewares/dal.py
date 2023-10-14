from typing import Any
from typing import Awaitable
from typing import Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.db.dal import DataAccessLayer


class DataAccessLayerMiddleware(BaseMiddleware):
    """
    Access to DAL from handlers
    """

    def __init__(self, dal: DataAccessLayer):
        super().__init__()
        self.dal = dal

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["dal"] = self.dal

        return await handler(event, data)


__all__ = ["DataAccessLayerMiddleware"]
