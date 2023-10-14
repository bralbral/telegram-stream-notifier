from typing import Any
from typing import Collection
from typing import Dict
from typing import Union

from aiogram.filters.base import Filter
from aiogram.types import Message

from .model import UserRole


class RoleFilter(Filter):
    key = "role"

    def __init__(self, role: Union[None, UserRole, Collection[UserRole]] = None):
        if role is None:
            self.roles = None
        elif isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def __call__(self, message: Message, **data: Dict[str, Any]) -> bool:
        if self.roles is None:
            return True
        return data.get("role") in self.roles


__all__ = ["RoleFilter"]
