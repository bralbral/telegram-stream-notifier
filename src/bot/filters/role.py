from typing import Any
from typing import Collection

from aiogram.filters.base import Filter
from aiogram.types import Message

from src.db.models.user_role import UserRole


class RoleFilter(Filter):
    key = "role"

    def __init__(self, role: None | UserRole | Collection[UserRole] = None):
        if role is None:
            self.roles = None
        elif isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def __call__(self, message: Message, **data: dict[str, Any]) -> bool:
        if self.roles is None:
            return True
        return data.get("role") in self.roles


__all__ = ["RoleFilter"]
