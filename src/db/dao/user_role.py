from typing import Optional
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from src.db.models import UserRoleModel


class UserRoleDAO(BaseDAO[UserRoleModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserRoleModel)

    async def get_first(self, *args, **kwargs) -> Optional[UserRoleModel]:
        return await super().get_first(*args, **kwargs)

    async def get_many(self, *args, **kwargs) -> Sequence[UserRoleModel]:
        return await super().get_many(*args, **kwargs)

    async def create(self, obj: UserRoleModel) -> Optional[UserRoleModel]:
        return await super().create(obj)

    async def update(self, obj: UserRoleModel) -> Optional[UserRoleModel]:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["UserRoleDAO"]
