from collections.abc import Sequence

from .base import BaseDAO
from src.db.models import UserRoleModel


class UserRoleDAO(BaseDAO[UserRoleModel]):
    def __init__(self):
        super().__init__(UserRoleModel)

    async def get_first(self, *args, **kwargs) -> UserRoleModel | None:
        return await super().get_first(*args, **kwargs)

    async def get_many(self, *args, **kwargs) -> Sequence[UserRoleModel]:
        return await super().get_many(*args, **kwargs)

    async def create(self, obj: UserRoleModel) -> UserRoleModel | None:
        return await super().create(obj)

    async def get_or_create(self, **kwargs) -> tuple[UserRoleModel, bool]:
        return await super().get_or_create(**kwargs)

    async def update(self, obj: UserRoleModel) -> UserRoleModel | None:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["UserRoleDAO"]
