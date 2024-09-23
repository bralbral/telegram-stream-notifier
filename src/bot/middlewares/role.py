from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Optional

from aiocache import Cache
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message

from src.bot.filters.role import UserRole
from src.db import DataAccessLayer
from src.db.models import UserModel


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
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user = event.from_user
        dal: DataAccessLayer = data["dal"]
        data["role"] = UserRole.UNKNOWN

        if user:
            verified = await self.cache.get(key=f"{self.prefix}_{user.id}")

            if verified:
                data["role"] = verified
            else:
                user_id = user.id

                _user: Optional[UserModel] = await dal.get_user_by_attr(
                    **{"user_id": user_id}
                )
                if _user:
                    if _user.role.role == UserRole.SUPERUSER:
                        data["role"] = UserRole.SUPERUSER
                    else:
                        data["role"] = UserRole.USER

            result = await handler(event, data)
            return result


__all__ = ["RoleMiddleware"]
