from typing import Any
from collections.abc import Awaitable
from collections.abc import Callable

from aiocache import Cache
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from aiogram.types import TelegramObject

from src.db import DataAccessLayer
from src.db.models import UserModel
from src.db.models.user_role import UserRole


class RoleMiddleware(BaseMiddleware):
    """
    Set UserRole for events
    """

    def __init__(self):
        super().__init__()
        self.cache = Cache(cache_class=Cache.MEMORY, ttl=60)
        self.prefix = "role"

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        message = event
        if not isinstance(message, Message):
            return await handler(event, data)
        user = message.from_user
        dal: DataAccessLayer = data["dal"]
        data["role"] = UserRole.USER

        if user:
            verified = await self.cache.get(key=f"{self.prefix}_{user.id}")

            if verified:
                data["role"] = verified
            else:
                user_id = user.id

                _user: UserModel | None = await dal.get_user_by_attr(
                    **{"user_id": user_id}
                )
                if _user:
                    if _user.role.role == UserRole.ADMIN:
                        data["role"] = UserRole.ADMIN
                    else:
                        data["role"] = UserRole.USER

            result = await handler(event, data)
            return result


__all__ = ["RoleMiddleware"]
